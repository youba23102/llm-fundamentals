import os

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    temperature=0.5,
    messages=[
        {"role": "user", "content": "Write a one-sentence story about a robot who discovers music"}
    ]
)

print(response.content[0].text)
print("\n--- Stats ---")
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
print(f"Stop reason: {response.stop_reason}")