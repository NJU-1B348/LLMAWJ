from openai import OpenAI

client = OpenAI(
    base_url='https://api.openai-proxy.org/v1',
    api_key='sk-rgM5v15Cjp1gEFPkn35QNXIiZTUXxfSbL3t9bxw6sAfwMd1G',
)

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")