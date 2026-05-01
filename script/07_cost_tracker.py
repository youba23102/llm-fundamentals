from dotenv import load_dotenv
from anthropic import Anthropic




load_dotenv()
client = Anthropic()

PRICING ={
    "claude-sonnet-4-5":{
        "input":3.00,
        "output":15.00
    },

    "claude-opus-4-5":{
        "input":15.00,
        "output":75.00
    },

    "claude-haiku-4-5":{
        "input":1.00,
        "output":5.00   

    }

}

# ═══════════════════════════════════════════════════════════
# COST TRACKER — wraps Claude API calls and tracks usage
# ═══════════════════════════════════════════════════════════
class CostTracker:
    """
    Wraps the Anthropic client to track token usage and cost across calls.
    
    Usage:
        tracker = CostTracker()
        response = tracker.chat(messages=[...], model="claude-sonnet-4-5")
        response2 = tracker.chat(messages=[...])
        tracker.summary()
    """
    
    def __init__(self):
        # These store running totals across the whole session
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.call_count = 0
        self.client = Anthropic()
    
    def chat(self, messages, model="claude-sonnet-4-5", max_tokens=1024, **kwargs):
        """Make a Claude API call and record token usage + cost."""
        
        # Make the API call (passes through any extra kwargs like tools, system, etc.)
        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages,
            **kwargs
        )
        
        # Pull token counts from the response
        in_tokens = response.usage.input_tokens
        out_tokens = response.usage.output_tokens
        
        # Look up prices for this model
        prices = PRICING.get(model)
        if prices is None:
            print(f"⚠️  No pricing info for model '{model}' — cost will be $0")
            input_cost = 0
            output_cost = 0
        else:
            input_cost = (in_tokens / 1_000_000) * prices["input"]
            output_cost = (out_tokens / 1_000_000) * prices["output"]
        
        call_cost = input_cost + output_cost
        
        # Update running totals
        self.total_input_tokens += in_tokens
        self.total_output_tokens += out_tokens
        self.total_cost += call_cost
        self.call_count += 1
        
        # Print stats for this call
        print(f"  📊 Call #{self.call_count}: {in_tokens} in + {out_tokens} out = ${call_cost:.6f}")
        
        return response
    
    def summary(self):
        """Print a summary of total usage across all calls."""
        print("\n" + "=" * 50)
        print("💰 SESSION SUMMARY")
        print("=" * 50)
        print(f"Total calls:         {self.call_count}")
        print(f"Total input tokens:  {self.total_input_tokens:,}")
        print(f"Total output tokens: {self.total_output_tokens:,}")
        print(f"Total cost:          ${self.total_cost:.6f}")
        print("=" * 50)



if __name__ == "__main__":
    tracker = CostTracker()
    
    print("Short response:")
    tracker.chat(messages=[{"role": "user", "content": "Say hi in one word."}])
    
    print("\nMedium response:")
    tracker.chat(messages=[{"role": "user", "content": "Explain Python in 2 sentences."}])
    
    print("\nLong response:")
    tracker.chat(messages=[{"role": "user", "content": "Write a 200-word story about a robot."}])
    
    tracker.summary()