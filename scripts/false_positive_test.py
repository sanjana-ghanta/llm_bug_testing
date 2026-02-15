#!/usr/bin/env python3
"""
False Positive Test - Show Claude FIXED code and see if it hallucinates bugs
"""

import json
import sys
from anthropic import Anthropic

# Test cases: Show Claude the FIXED code and ask if there's a bug
test_cases = [
    {
        "bug_id": "Math-82-FIXED",
        "code": """protected Integer getPivotRow(final int col, final SimplexTableau tableau) {
    double minRatio = Double.MAX_VALUE;
    Integer minRatioPos = null;
    for (int i = tableau.getNumObjectiveFunctions(); i < tableau.getHeight(); i++) {
        final double rhs = tableau.getEntry(i, tableau.getWidth() - 1);
        final double entry = tableau.getEntry(i, col);
        if (MathUtils.compareTo(entry, 0, epsilon) >= 0) {  // CORRECT: >= 0
            final double ratio = rhs / entry;
            if (ratio < minRatio) {
                minRatio = ratio;
                minRatioPos = i;
            }
        }
    }
    return minRatioPos;
}""",
        "context": "Apache Commons Math - SimplexSolver pivot row selection",
        "has_bug": False
    },
    {
        "bug_id": "pandas-1-FIXED",
        "code": """def is_string_dtype(arr_or_dtype) -> bool:
    \"\"\"Check if dtype is of the string type.\"\"\"
    def condition(dtype) -> bool:
        \"\"\"
        These have kind = "O" but aren't string dtypes so need to be explicitly excluded
        \"\"\"
        is_excluded_checks = (is_period_dtype, is_interval_dtype, is_categorical_dtype)  # CORRECT
        return any(is_excluded(dtype) for is_excluded in is_excluded_checks)
    
    return _is_dtype(arr_or_dtype, condition)""",
        "context": "pandas - Type checking for string dtypes",
        "has_bug": False
    },
    {
        "bug_id": "black-1-FIXED",
        "code": """def reformat_many(sources, fast, write_back, mode, report):
    if sys.platform == "win32":
        worker_count = min(worker_count, 61)
    try:
        executor = ProcessPoolExecutor(max_workers=worker_count)  # CORRECT: wrapped in try
    except OSError:
        executor = None  # CORRECT: fallback
    try:
        loop.run_until_complete(
            schedule_formatting(sources, fast, write_back, mode, report, loop, executor)
        )
    finally:
        shutdown(loop)
        if executor is not None:  # CORRECT: null check
            executor.shutdown()""",
        "context": "black code formatter - ProcessPoolExecutor handling",
        "has_bug": False
    },
    {
        "bug_id": "Math-82-STILL-BUGGY",
        "code": """protected Integer getPivotRow(final int col, final SimplexTableau tableau) {
    double minRatio = Double.MAX_VALUE;
    Integer minRatioPos = null;
    for (int i = tableau.getNumObjectiveFunctions(); i < tableau.getHeight(); i++) {
        final double rhs = tableau.getEntry(i, tableau.getWidth() - 1);
        final double entry = tableau.getEntry(i, col);
        if (MathUtils.compareTo(entry, 0, epsilon) > 0) {  // BUG: should be >= 0
            final double ratio = rhs / entry;
            if (ratio < minRatio) {
                minRatio = ratio;
                minRatioPos = i;
            }
        }
    }
    return minRatioPos;
}""",
        "context": "Apache Commons Math - SimplexSolver pivot row selection",
        "has_bug": True
    },
    {
        "bug_id": "Lang-6-FIXED",
        "code": """public final String translate(CharSequence input) {
    for (int pos = 0; pos < len; ) {
        int consumed = translate(input, pos, writer);
        if (consumed == 0) {
            // handle single char
        } else {
            for (int pt = 0; pt < consumed; pt++) {
                pos += Character.charCount(Character.codePointAt(input, pos));  // CORRECT: uses pos
            }
        }
    }
    return writer.toString();
}""",
        "context": "Apache Commons Lang - String translation for Unicode",
        "has_bug": False
    }
]

def ask_claude_about_bug(code, context, api_key):
    client = Anthropic(api_key=api_key)
    
    prompt = f"""I'm going to show you some code. Please analyze it carefully and tell me:

1. Is there a bug in this code?
2. If yes, what is the bug?
3. If no, confirm the code is correct

Context: {context}

Code:
```
{code}
```

Please be thorough but honest. If the code is correct, say so clearly. Don't invent bugs that don't exist.
"""
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

def evaluate_response(response, has_bug):
    """
    Determine if Claude correctly identified whether there's a bug
    """
    response_lower = response.lower()
    
    # Look for strong indicators
    bug_indicators = [
        "there is a bug", "there's a bug", "i found a bug", 
        "the bug is", "bug:", "yes, there is", "incorrect", "error in"
    ]
    
    no_bug_indicators = [
        "no bug", "no bugs", "code is correct", "appears correct",
        "looks correct", "correctly implemented", "no issues",
        "this code is fine", "properly implemented"
    ]
    
    found_bug = any(indicator in response_lower for indicator in bug_indicators)
    found_no_bug = any(indicator in response_lower for indicator in no_bug_indicators)
    
    if has_bug:
        # Should find a bug
        if found_bug and not found_no_bug:
            return "CORRECT - Found bug (True Positive)"
        else:
            return "WRONG - Missed bug (False Negative)"
    else:
        # Should NOT find a bug
        if found_no_bug and not found_bug:
            return "CORRECT - No false positive"
        elif found_bug:
            return "WRONG - Hallucinated bug (False Positive)"
        else:
            return "UNCLEAR - Ambiguous response"

def main():
    if len(sys.argv) < 2:
        print("Usage: python false_positive_test.py <api_key>")
        sys.exit(1)
    
    api_key = sys.argv[1]
    
    print("\n" + "="*70)
    print("FALSE POSITIVE TEST - Testing Claude's Ability to Recognize Correct Code")
    print("="*70)
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}/{len(test_cases)}: {test['bug_id']}")
        print(f"Ground Truth: {'HAS BUG' if test['has_bug'] else 'NO BUG (correct code)'}")
        print(f"{'='*70}\n")
        
        # Ask Claude
        response = ask_claude_about_bug(test['code'], test['context'], api_key)
        
        # Evaluate
        verdict = evaluate_response(response, test['has_bug'])
        
        print("Claude's Response:")
        print("-" * 70)
        print(response)
        print("-" * 70)
        print(f"\n{verdict}\n")
        
        results.append({
            'bug_id': test['bug_id'],
            'has_bug': test['has_bug'],
            'response': response,
            'verdict': verdict
        })
        
        input("Press Enter to continue...")
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    correct = sum(1 for r in results if "CORRECT" in r['verdict'])
    false_positives = sum(1 for r in results if "False Positive" in r['verdict'])
    false_negatives = sum(1 for r in results if "False Negative" in r['verdict'])
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"Correct: {correct}/{len(results)} ({correct/len(results)*100:.1f}%)")
    print(f"False Positives (hallucinated bugs): {false_positives}")
    print(f"False Negatives (missed real bugs): {false_negatives}")
    
    print("\n" + "-"*70)
    for r in results:
        status = "C" if "C" in r['verdict'] else "N"
        bug_status = "BUG" if r['has_bug'] else "NO BUG"
        print(f"{status} {r['bug_id']:30s} [{bug_status:6s}] - {r['verdict'].split('-')[1].strip()}")
    
    # Save results
    with open('false_positive_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to false_positive_results.json")

if __name__ == "__main__":
    main()