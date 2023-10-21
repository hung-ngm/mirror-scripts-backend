from langchain.document_loaders import PyMuPDFLoader
import os
"""Selenium web scraping module."""
import asyncio
from pathlib import Path
from fastapi import WebSocket

import processing.text as summary

from config import Config
from processing.html import extract_hyperlinks, format_hyperlinks

from concurrent.futures import ThreadPoolExecutor

from actions.tavily_search import tavily_client

executor = ThreadPoolExecutor()

def local_source_parse(folder: str = './resources'):
    """Parse the local resources and return the content of the pdf files

    Returns:
        None: If no file exits
        list: A list of dictionaries containing the file name and the content of the pdf files
    """
    
    # if no file exits, return None
    if not os.path.isdir(folder):
        return None
    
    else:
        output = []
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            # if the file is pdf
            if os.path.isfile(path) and path.endswith('.pdf'):
                # get file name
                file_name = file.split('.')[0]
                print(path)
                loader = PyMuPDFLoader(path)
                data = loader.load()
                # concatentate all the page_content into one string
                text = '\n'.join([page.page_content for page in data])
                output.append({'file_name': file_name, 'content': text})

        return output

async def async_gather_local(file_name: str, question: str, content: str, websocket: WebSocket) -> str:
    """Gather the information from a website url and return the answer to the user

    Args:
        file_name (str): The file name of the local resources
        question (str): The question asked by the user
        content: (str): The contnet of the website scraped
        websocket (WebSocketManager): The websocket manager

    Returns:
        str: The answer and links to the user
    """
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=8)

    print(f"Analysing file {file_name} with question {question}")
    await websocket.send_json(
        {"type": "logs", "output": f"🔎 Reading file {file_name} for relevant about: {question}..."})

    try:
        summary_text = await loop.run_in_executor(executor, summary.summarize_text, content, question)

        await websocket.send_json(
            {"type": "logs", "output": f"📝 Information gathered from file {file_name}: {summary_text}"})

        return f"Information gathered from file {file_name}: {summary_text}"

    except Exception as e:
        print(f"An error occurred while processing the file {file_name}: {e}")
        return f"Error processing the file {file_name}: {e}"
