from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()


# Step 1: Define the tool schema (the "menu")
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


# Step 2: Define the ACTUAL function (fake data for now)
def get_weather(city, unit="fahrenheit"):
    fake_data = {
        "Philadelphia": {"temp": 58, "condition": "cloudy"},
        "Tokyo": {"temp": 72, "condition": "sunny"},
        "London": {"temp": 45, "condition": "rainy"},
    }
    data = fake_data.get(city, {"temp": 70, "condition": "unknown"})
    return f"{data['temp']} degrees {unit}, {data['condition']}"

# Step 3: Start the conversation
messages = [
    {"role": "user", "content": "What's the weather in Philadelphia right now?"}
]

# Step 4: First call — Claude will request the tool
print("=== Turn 1: Asking Claude ===")
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages
)
print(f"Stop reason: {response.stop_reason}")

# Step 5: Extract the tool request from Claude's response
tool_use_block = next(block for block in response.content if block.type == "tool_use")
tool_name = tool_use_block.name
tool_input = tool_use_block.input
tool_use_id = tool_use_block.id
print(f"Claude wants to call: {tool_name}({tool_input})")

# Step 6: Actually run the tool
tool_result = get_weather(**tool_input)
print(f"Tool returned: {tool_result}")

# Step 7: Append Claude's request AND our tool result to the conversation
messages.append({"role": "assistant", "content": response.content})
messages.append({
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": tool_use_id,
            "content": tool_result
        }
    ]
})

# Step 8: Second call — now Claude has the tool result, it can answer
print("\n=== Turn 2: Claude now has the data ===")
final_response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=messages
)
print(f"Stop reason: {final_response.stop_reason}")
print(f"Final answer: {final_response.content[0].text}")