from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

# We're telling Claude: "here's a tool you can request to use"
tools = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given city",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city name"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["city"]
        }
    }
]

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather in Philadelphia right now?"}
    ]
)

print("Stop reason:", response.stop_reason)
print("\nFull response content:")
for block in response.content:
    print(f"  Type: {block.type}")
    if block.type == "text":
        print(f"  Text: {block.text}")
    elif block.type == "tool_use":
        print(f"  Tool: {block.name}")
        print(f"  Input: {block.input}")



        