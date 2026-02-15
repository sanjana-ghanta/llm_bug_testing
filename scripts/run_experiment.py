import json
import sys
from anthropic import Anthropic

def analyze_bug(bug, api_key):
    client = Anthropic(api_key=api_key)
    
    prompt = f'''I'm going to show you some code that contains a bug. Your task is to:

1. Identify the semantic issue in the code
2. Explain what the bug is and why it's problematic
3. Propose a fix for the bug

Project: {bug['project']}
Bug ID: {bug['bug_id']}

The buggy code:
```
{bug['buggy_code']}
```

Test failure: {bug.get('test_output', 'N/A')}

Please analyze this code and provide:
1. What is the bug?
2. What is the root cause?
3. Your proposed fix (show the corrected code)
'''
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_experiment.py <api_key>")
        sys.exit(1)
    
    api_key = sys.argv[1]
    
    # Load bugs
    with open('bugs_final.json', 'r') as f:
        data = json.load(f)
    
    results = []
    
    for i, bug in enumerate(data['bugs'], 1):
        print(f"\n{'='*60}")
        print(f"Analyzing Bug {i}/{len(data['bugs'])}: {bug['bug_id']}")
        print(f"{'='*60}\n")
        
        # Query LLM
        llm_response = analyze_bug(bug, api_key)
        
        print("LLM Response:")
        print("-" * 60)
        print(llm_response)
        print("-" * 60)
        
        print("\nGround Truth Fix:")
        print("-" * 60)
        print(bug['fixed_code'])
        print("-" * 60)
        
        # Save result
        result = {
            'bug_id': bug['bug_id'],
            'benchmark': bug['benchmark'],
            'project': bug['project'],
            'llm_response': llm_response,
            'ground_truth_fix': bug['fixed_code'],
            'bug_description': bug['bug_description']
        }
        results.append(result)
        
        input("\nPress Enter to continue to next bug...")
    
    # Save all results
    with open('llm_responses.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n✓ Results saved to llm_responses.json")
    print("\nNext: Manually evaluate each bug using the evaluation guide")

if __name__ == "__main__":
    main()