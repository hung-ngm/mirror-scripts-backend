from __future__ import annotations

import json

from fastapi import WebSocket
import time

import openai
from langchain.adapters import openai as lc_openai
from colorama import Fore, Style
from openai.error import APIError, RateLimitError
from llama_index.llms import ChatMessage
from agent.prompts import auto_agent_instructions
from config import Config

CFG = Config()

openai.api_key = CFG.openai_api_key

from typing import Optional
import logging

async def create_chat_completion(
    messages: list[ChatMessage],  # type: ignore
    model: Optional[str] = None,
    temperature: float = CFG.temperature,
    max_tokens: Optional[int] = None,
    stream: Optional[bool] = False,
    websocket: WebSocket | None = None,
) -> str:
    """Create a chat completion using the OpenAI API
    Args:
        messages (list[dict[str, str]]): The messages to send to the chat completion
        model (str, optional): The model to use. Defaults to None.
        temperature (float, optional): The temperature to use. Defaults to 0.9.
        max_tokens (int, optional): The max tokens to use. Defaults to None.
        stream (bool, optional): Whether to stream the response. Defaults to False.
    Returns:
        str: The response from the chat completion
    """

    # validate input
    if model is None:
        raise ValueError("Model cannot be None")
    if max_tokens is not None and max_tokens > 8001:
        raise ValueError(f"Max tokens cannot be more than 8001, but got {max_tokens}")
    if stream and websocket is None:
        raise ValueError("Websocket cannot be None when stream is True")

    # create response
    for attempt in range(10):  # maximum of 10 attempts
        response = await send_chat_completion_request(
            messages, model, temperature, max_tokens, stream, websocket
        )
        return response

    logging.error("Failed to get response from OpenAI API")
    raise RuntimeError("Failed to get response from OpenAI API")

def init_llm(model, temperature, max_tokens):
    if CFG.llm_provider == "ChatOpenAI":
        from llama_index.llms import OpenAI
        llm = OpenAI(model=model, temperature=temperature, max_tokens=max_tokens)
        return llm


async def send_chat_completion_request(
    messages, model, temperature, max_tokens, stream, websocket
) -> str:
    llm = init_llm(model, temperature, max_tokens)

    if not stream:
        response = await llm.achat(messages=messages) # type: ignore
        response = str(response).replace("assistant: ", "")
        return response
    else:
        return await stream_response(llm, messages, websocket) 


async def stream_response(llm, messages, websocket) -> str:
    response = ""
    print(f"streaming response...")

    async for chunk in await llm.astream_chat(messages): 
        content = chunk.delta
        if content is not None:
            response += content
            await websocket.send_json({"type": "report", "output": content})
    print(f"streaming response complete")
    return response.replace("assistant: ", "")


async def choose_agent(task: str) -> dict:
    """Determines what agent should be used
    Args:
        task (str): The research question the user asked
    Returns:
        agent - The agent that will be used
        agent_role_prompt (str): The prompt for the agent
    """
    try:
        response = await create_chat_completion(
            model=CFG.smart_llm_model,
            messages=[
                ChatMessage(role="system", content=f"{auto_agent_instructions()}"), # type: ignore
                ChatMessage(role="user", content=f"task: {task}\nresponse:") # type: ignore
            ],
            temperature=0,
        )

        print("Agent selection prompt:", response)

        return json.loads(response)
    except Exception as e:
        print(f"{Fore.RED}Error in choose_agent: {e}{Style.RESET_ALL}")
        return {"agent": "Default Agent",
                "agent_role_prompt": "You are an AI critical thinker research assistant. Your sole purpose is to write well written, critically acclaimed, objective and structured reports on given text."}

