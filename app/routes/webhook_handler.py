import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks
from ollama import Client

from app.internal.logger import logger
from app.models.webhook import MergeRequestEvent

load_dotenv()
GITLAB_ACCESS_TOKEN = os.getenv("GITLAB_ACCESS_TOKEN")
GITLAB_BASE_URL = os.getenv("GITLAB_BASE_URL")

OLLAMA_HOST = os.getenv("OLLAMA_HOST")
if OLLAMA_HOST:
    ollama_client = Client(host=OLLAMA_HOST)

router = APIRouter()


def add_comment(project_id: int, merge_request_iid: int, comment: str):
    """
    add comment
    :param project_id: the project should add comment
    :param merge_request_iid: the merge request iid
    :param comment: the comment
    :return: None
    """
    logger.info("Trying to add comment to")
    url = f"http://{GITLAB_BASE_URL}/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}/notes"
    headers = {
        "Private-Token": GITLAB_ACCESS_TOKEN,
        "Content-Type": "application/json",
    }

    data = {
        "body": comment
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        logger.info("Comment added successfully.")
    else:
        logger.warn(f"Failed to add comment. Status code: {response.status_code}, Response: {response.text}")


def process_merge_request(project_id: int, merge_request_iid: int):
    url = f"http://{GITLAB_BASE_URL}/api/v4/projects/{project_id}/merge_requests/{merge_request_iid}/changes"
    headers = {"Authorization": f"Bearer {GITLAB_ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        logger.info("Get Diffs Success.")

        formatted_diffs = []
        changes = response.json()["changes"]
        for change in changes:
            file_path = change["new_path"]
            diff = change["diff"]
            # Append a formatted string for each change to the list
            formatted_diffs.append(f"File: {file_path}\nDiff:\n{diff}")

        prompt = "\n\n".join(formatted_diffs)
        logger.info("Format diffs. Try to talk to LLM...")
        ollama_prompt = (f"Please review the following code changes:\n\n{prompt}\n\nProvide feedback on code quality, "
                         f"style, potential bugs, and performance optimizations. please output with chinese")

        messages = [
            {
                'role': 'user',
                'content': ollama_prompt,
            },
        ]

        chat_prompt = ollama_client.chat(model="codellama:13b", messages=messages)
        logger.info(f"get response {chat_prompt['message']['content']}")

        add_comment(project_id, merge_request_iid, chat_prompt['message']['content'])

    else:
        logger.warn("Cannot get diffs with response code {0}", response.status_code)


@router.post("/code-reviewer")
async def handle_merge_request(background_tasks: BackgroundTasks, event: MergeRequestEvent):
    """
    receive webhook
    :param background_tasks: process background
    :param event: merge request event
    :return: http response
    """
    logger.info(f"Receive Merge Request with Project {event.project.name}, Title {event.object_attributes.title}")
    background_tasks.add_task(process_merge_request, event.project.id, event.object_attributes.iid)

    # Return a response
    return {"message": "Received", "merge_request_id": event.object_attributes.id}
