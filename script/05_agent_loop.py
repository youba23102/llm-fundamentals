from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client=Anthropic()

tools=[{
    "name":"get_weather",
    "description":"Get the current weather in a given city. Use this whenever the user asks about weather, temperature, or conditions in any location.",
    "input_schema":{
        "type":"object",
        "propreties":{
            "city":{"type":"string",
                    "description":"The city name, e.g. 'Philadelphia' or 'Tokyo'"

            }
        },
        "required":["city"]

    }
}

]

# PART 2: THE ACTUAL FUNCTIONS (what runs)
# ═══════════════════════════════════════════════════════════
def get_weather(city):
    fake_data = {
        "Philadelphia": "58°F, cloudy",
        "Tokyo": "72°F, sunny",
        "London": "45°F, rainy",
        "Paris": "50°F, partly cloudy",
    }
    return fake_data.get(city, "unknown weather for " + city)


# ═══════════════════════════════════════════════════════════
# PART 3: DISPATCHER (maps tool name → actual function)
# ═══════════════════════════════════════════════════════════

def run_tool(name,args):

    if name=="get_weather" :

       return  get_weather(**args)
    else :
        return f"error,unkown '{name}' "
    

# ═══════════════════════════════════════════════════════════
# PART 4: THE AGENT LOOP
# ═══════════════════════════════════════════════════════════

def run_agent(user_question):
    """Run an agent that loops until Claude gives a final answer."""

    # Start the conversation

    massages=[{"role" :"user","content":user_question}]

    # Track iterations so we can see what's happening
    iteration =0

     # THE LOOP: keep going until Claude stops requesting tools

    while True:
        iteration+=1

        # Call Claude

        response=client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            tools=tools,
            messages=massages

        )

        print(f"stop reason :{response.stop_reason}")

        if response.stop_reason=="end_turn" :
             # Find the text block in the response and return it

             for block in response.content :
                 if block.type=="text":
                     print(f"the final answer is :{block.text}")
                     return block.text
       

    # ─── Case 2: Claude wants a tool ───

        if response.stop_reason=="tool_use" :

            massages.append({"role":"assistant","content":response.content})
            tool_result=[]
            for block in response.content :
                if block.type=="tool_use":
                    print(f"the claude wants {block.name} and {block.input}")
                    result=run_tool(block.name,block.input)
                    print(f"the result is {result}")

                    tool_result.append({
                        "type":"tool_result",
                        "tool_use_id":block.id,
                        "content":result
                    })

            massages.append({"role":"user","content":tool_result})

        if iteration==10 :
            print("⚠️ Hit max iterations, stopping")
            return None    
        



if __name__ == "__main__":
    question = "Compare weather in Philadelphia, Tokyo, London, and Paris."
    print(f"🧑 User: {question}")
    run_agent(question)        