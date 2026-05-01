from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client =Anthropic()

test_cases = [
    {"email": "My invoice was charged twice last month, can I get a refund?", "expected": "BILLING"},
    {"email": "The dashboard keeps crashing whenever I try to load reports.", "expected": "TECHNICAL"},
    {"email": "Do you offer enterprise pricing for teams over 50 people?", "expected": "SALES"},
    {"email": "I was charged $99 but my plan should be $49 — please fix this.", "expected": "BILLING"},
    {"email": "Login button is unresponsive on Chrome and Firefox.", "expected": "TECHNICAL"},
    {"email": "Interested in a demo for our 200-person company.", "expected": "SALES"},
    {"email": "Why was I billed for the annual plan when I signed up monthly?", "expected": "BILLING"},
    {"email": "API endpoint /users returns a 500 error every time.", "expected": "TECHNICAL"},
    {"email": "Looking for a custom contract — can we discuss pricing?", "expected": "SALES"},
    {"email": "The mobile app freezes when I open notifications.", "expected": "TECHNICAL"},
]

# HELPER — calls Claude and returns cleaned response
# ═══════════════════════════════════════════════════════════
def classify(prompt, system=None):
    """Send a prompt to Claude and return the cleaned uppercase response."""
    kwargs = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": prompt}]
    }
    if system:
        kwargs["system"] = system
    
    response = client.messages.create(**kwargs)
    return response.content[0].text.strip().upper()

# ═══════════════════════════════════════════════════════════
# TECHNIQUE 1 — ZERO-SHOT
# Just describe the task. No examples. No reasoning. No role.
# ═══════════════════════════════════════════════════════════
def zero_shot(email):
    prompt = f"Classify this email as BILLING, TECHNICAL, or SALES.\n\nEmail: {email}"
    return classify(prompt)


# ═══════════════════════════════════════════════════════════
# TECHNIQUE 2 — FEW-SHOT
# Same task, but show 3 examples of correct classifications first.
# The model learns the pattern from the examples.
# ═══════════════════════════════════════════════════════════
def few_shot(email):
    prompt = f"""Classify each email as BILLING, TECHNICAL, or SALES.

Example 1:
Email: "Your app keeps crashing when I try to log in."
Category: TECHNICAL

Example 2:
Email: "Can I get a refund for last month's charge?"
Category: BILLING

Example 3:
Email: "Do you offer volume discounts for large teams?"
Category: SALES

Now classify this email:
Email: "{email}"
Category:"""
    return classify(prompt)


if __name__ == "__main__":
    test_email = "I was charged $99 but my plan should be $49 — please fix this."
    result = zero_shot(test_email)
    result2=few_shot(test_email)
    print(f"Email: {test_email}")
    print(f"Classification: {result}")

    print("/n")

    print(f"Classification: {result2}")