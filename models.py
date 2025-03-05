import logging
import sys
from datetime import datetime
from openai import OpenAI
from pydantic import BaseModel
import tiktoken
from typing import List
import os
import dotenv

dotenv.load_dotenv(override=True)

text_model = "gpt-4o"

client = OpenAI()

def llm_call(prompt: str, system_prompt: str = None, response_format: BaseModel = None, model: str = text_model):
    '''
    Make a LLM call

    ### Args:
        `prompt` (`str`): The user prompt to send to the LLM.
        `system_prompt` (`str`, optional): System-level instructions for the LLM. Defaults to None.
        `response_format` (`BaseModel`, optional): Format for structured responses. Defaults to None.
        `model` (`str`, optional): Model identifier to use. Defaults to "gpt-4o-mini".

    ### Returns:
        The LLM's response, either as raw text or as a parsed object according to `response_format`.
    '''
    kwargs = {}

    kwargs['model'] = model
    
    if system_prompt:
        kwargs["messages"] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
    else:
        kwargs["messages"] = [
            {"role": "user", "content": prompt},
        ]
    
    if response_format is not None:

        kwargs["response_format"] = response_format
        return client.beta.chat.completions.parse(
            **kwargs
        ).choices[0].message.parsed
    
    return client.chat.completions.create(
        **kwargs
    ).choices[0].message.content

def llm_call_messages(messages: List[dict], response_format: BaseModel = None, model: str = text_model):
    '''
    Make a LLM call with a list of messages instead of a prompt + system prompt

    ### Args:
        `messages` (`list[dict]`): The list of messages to send to the LLM.
        `response_format` (`BaseModel`, optional): Format for structured responses. Defaults to None.
        `model` (`str`, optional): Model identifier to use. Defaults to "gpt-4o-mini".
    '''
    kwargs = {}
    kwargs["messages"] = messages
    kwargs["model"] = model


    if response_format is not None:

        kwargs["response_format"] = response_format
        return client.beta.chat.completions.parse(
            **kwargs
        ).choices[0].message.parsed
    
    return client.chat.completions.create(
        **kwargs
    ).choices[0].message.content


def num_tokens_from_messages(messages: List[dict], model: str = text_model) -> int:
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("o200k_base")

    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

if __name__ == "__main__":
    prompt = "What is the capital of the moon?"
    response = llm_call(prompt)
    print(response)

    messages = [
        {"role": "user", "content": prompt}
    ]
    response = llm_call_messages(messages)
    print(response)
    