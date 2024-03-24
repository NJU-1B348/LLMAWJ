#!/usr/bin/env python3
from openai import OpenAI
import prompts.prompt as prompt

PROMPT: list[str] = prompt.Prompt.gpt

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="sk-no-key-required"
)

stream = client.chat.completions.create(
    model="LLaMA_CPP",
    messages=[

        {"role": "user", "content": PROMPT[0]},
        {"role": "user", "content": PROMPT[1]},
        {"role": "user", "content": PROMPT[2]},

    ],
    stream=True
)

ans_str = ""
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        ans_str += chunk.choices[0].delta.content
print(ans_str)
