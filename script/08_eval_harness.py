import json
import time
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client=Anthropic()


class Evaluator:
    """
    Generic evaluation framework for LLM techniques.
    
    Usage:
        evaluator = Evaluator("tests/email_classification.json")
        results = evaluator.run(my_classifier_function)
    """
    
    def __init__(self, test_file_path):
        """Load test cases from a JSON file."""
        with open(test_file_path, "r", encoding="utf-8") as f:
            self.test_cases = json.load(f)
        
        self.test_file_path = test_file_path
        print(f"📁 Loaded {len(self.test_cases)} test cases from {test_file_path}")
    
    def run(self, technique_function, technique_name=None):
        """
        Run all test cases through a technique function.
        
        Args:
            technique_function: a function that takes one input string and returns a classification
            technique_name: optional label for printing (defaults to function name)
        
        Returns:
            a dict with summary stats
        """
        if technique_name is None:
            technique_name = technique_function.__name__
        
        print(f"\n{'━' * 50}")
        print(f"🧪 Running: {technique_name}")
        print(f"{'━' * 50}")
        
        correct = 0
        failures = []
        start_time = time.time()
        
        for i, case in enumerate(self.test_cases, start=1):
            input_text = case["input"]
            expected = case["expected"]
            
            # Run the technique
            actual = technique_function(input_text)
            
            # Compare
            is_correct = expected.upper() in actual.upper()
            if is_correct:
                correct += 1
                print(f"  ✅ Test {i}: {expected}")
            else:
                failures.append({
                    "input": input_text,
                    "expected": expected,
                    "actual": actual
                })
                print(f"  ❌ Test {i}: expected {expected}, got {actual}")
        
        elapsed = time.time() - start_time
        accuracy = correct / len(self.test_cases)
        
        # Build results summary
        results = {
            "technique": technique_name,
            "accuracy": accuracy,
            "correct": correct,
            "total": len(self.test_cases),
            "failures": failures,
            "elapsed_seconds": elapsed,
        }
        
        # Print summary
        print(f"\n📊 Results for {technique_name}:")
        print(f"   Accuracy: {accuracy:.1%} ({correct}/{len(self.test_cases)})")
        print(f"   Time:     {elapsed:.1f}s")
        
        return results
    

if __name__ == "__main__":
    # Import the techniques from your prompting script
    # We need to add the parent script folder to path so we can import it
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Now we can import the prompting techniques
    # Note: filename starts with a number, so we need a workaround
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "prompting", 
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "06_prompting_techniques.py")
    )
    prompting = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prompting)
    
    # Set up the evaluator
    evaluator = Evaluator("tests/email_classification.json")
    
    # Run each technique
    print("\n" + "=" * 50)
    print("COMPARING ALL 3 IMPLEMENTED TECHNIQUES")
    print("=" * 50)
    
    results_zero = evaluator.run(prompting.zero_shot, "Zero-shot")
    results_few = evaluator.run(prompting.few_shot, "Few-shot")
    
    
    # Print final comparison
    print("\n" + "=" * 50)
    print("📈 FINAL COMPARISON")
    print("=" * 50)
    for r in [results_zero, results_few]:
        print(f"  {r['technique']:20s}  {r['accuracy']:.1%}  ({r['correct']}/{r['total']})  {r['elapsed_seconds']:.1f}s")