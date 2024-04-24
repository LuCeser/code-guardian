import os
from typing import List

from dotenv import load_dotenv
from ollama import Client

from app.internal.logger import logger


class LLMOllama:
    def __init__(self):
        load_dotenv()
        self.ollama_host = os.getenv("OLLAMA_HOST")
        self.ollama_code_model = os.getenv("OLLAMA_CODE_MODEL", "codellama:13b")
        self.ollama_client = Client(host=self.ollama_host)

    def list_models(self):
        """
        list all llm models
        :return:
        """
        return self.ollama_client.list()

    def activate_model(self):
        """
        get model use now
        :return: current model name
        """
        return self.ollama_code_model

    def change_model(self, new_model):
        self.ollama_code_model = new_model

    def review(self, changes: List):
        formatted_diffs = []
        for change in changes:
            file_path = change["new_path"]
            diff = change["diff"]
            # Append a formatted string for each change to the list
            formatted_diffs.append(f"File: {file_path}\nDiff:\n{diff}")
        prompt = "\n\n".join(formatted_diffs)
        logger.info(f"Format diffs. Try to talk to LLM with model {self.ollama_code_model}...")
        ollama_prompt = (f"Please review the following code changes:\n\n{prompt}\n\nProvide feedback on code quality, "
                         f"style, potential bugs, and performance optimizations.Please respond in chinese.")

        messages = [
            {
                'role': 'user',
                'content': ollama_prompt,
            },
        ]

        chat_prompt = self.ollama_client.chat(model=self.ollama_code_model, messages=messages)
        logger.info(f"get response {chat_prompt['message']['content']}")
        return chat_prompt['message']['content']
