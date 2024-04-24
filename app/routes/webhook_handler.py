import os
from typing import Optional

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks, Request, Header, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from app.db.orm import get_session
from app.internal.logger import logger
from app.llm.llm_core import LLMOllama
from app.models.task import Task
from app.models.webhook import MergeRequestEvent

load_dotenv()
GITLAB_ACCESS_TOKEN = os.getenv("GITLAB_ACCESS_TOKEN")
GITLAB_BASE_URL = os.getenv("GITLAB_BASE_URL")

llm = LLMOllama()

router = APIRouter()

# Setup the Jinja2 template environment
templates = Jinja2Templates(directory="templates")


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
        add_comment(project_id, merge_request_iid, llm.review(response.json()["changes"]))

    else:
        logger.warn("Cannot get diffs with response code {0}", response.status_code)


async def parse_gitlab_event(
        request: Request,
        x_gitlab_event: Optional[str] = Header(None),
):
    if x_gitlab_event != "Merge Request Hook":
        logger.warn(f"The webhook only handle Merge Request Hook, the request header is: {x_gitlab_event}")
        raise HTTPException(status_code=400, detail="Event type not supported")

    # If it's a merge request hook, parse the body using the appropriate model
    try:
        body = await request.json()
        return MergeRequestEvent(**body)
    except Exception as e:
        logger.error("Can't parse the request body", e)
        raise HTTPException(status_code=400, detail="Error parsing request body")


@router.post("/code-reviewer")
async def handle_merge_request(
        background_tasks: BackgroundTasks,
        event: MergeRequestEvent = Depends(parse_gitlab_event),
        db: Session = Depends(get_session)
):
    """
    receive webhook
    :param background_tasks: process background
    :param event: merge request event
    :param db: db to save
    :return: http response
    """

    logger.info(f"Receive Merge Request with Project {event.project.name}, Title {event.object_attributes.title}, "
                f"Merge Status {event.object_attributes.state}")
    if event.object_attributes.state == 'opened':
        task = Task()
        task.project_id = event.project.id
        task.merge_request_iid = event.object_attributes.iid
        task.status = "pending"
        task.source_url = event.object_attributes.url

        db.add(task)
        db.commit()
        db.refresh(task)

        background_tasks.add_task(process_merge_request, event.project.id, event.object_attributes.iid)
    else:
        logger.info(f"Merge Request State is {event.object_attributes.state}, won't be review")

    # Return a response
    return {"message": "Received", "merge_request_id": event.object_attributes.id}


@router.get("/models")
async def available_models():
    """
    list all available models
    :return: ["model1", "model2"]
    """
    query_ret = llm.list_models()
    ret = []
    for model in query_ret['models']:
        ret.append(model['name'])
    return ret


@router.post("/models/activate")
async def change_current_model(data: dict):
    logger.info(f"Change model from {llm.activate_model()} to {data}")
    llm.change_model(data['model'])


@router.get("/models/activate")
async def current_model():
    """
    display which llm model is use now
    :return:
    """
    return {"model": llm.activate_model(), "description": ""}


@router.get("/")
async def read_root(request: Request):
    """
    main page
    :param request: request
    :return: index.html
    """
    return templates.TemplateResponse("index.html", {"request": request})
