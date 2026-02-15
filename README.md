# How to Run

### 5 Java Bugs (Defects4J):
1. Math-82: Off-by-one error (> vs >=)
2. Math-5: Wrong return value (INF vs NaN)
3. Lang-6: Index calculation bug
4. Time-4: Partial date handling
5. Chart-1: Null pointer exception

### 5 Python Bugs (BugsInPy):
6. pandas-1: Missing type in exclusion list
7. keras-1: TensorFlow control dependencies
8. black-1: Missing exception handling
9. scrapy-1: Domain filtering logic
10. youtube-dl-1: Boolean value handling

---

### Step 1: Save the files
Create these files in a folder:
- `bugs_final.json` (the bug data)
- `run_experiment.py` (the experiment script)

### Step 2: Install Anthropic SDK
```bash
pip install anthropic
```

### Step 3: Run the experiment
```bash
python run_experiment.py YOUR_ANTHROPIC_API_KEY
```

---

## What Happens

For each of the 10 bugs:

1. Shows Claude the buggy code + test failure
2. Asks Claude to identify the bug and propose a fix
3. Shows you Claude's response vs ground truth
4. Saves everything to `llm_responses.json`

**Time:** ~10-15 minutes

---

## After Running

1. Open `llm_responses.json` to see all results
2. Use `EVALUATION_GUIDE.md` to score each bug
3. For each bug, answer:
   - Did Claude identify the bug correctly?
   - How does Claude's fix compare to the real fix?
   - Did Claude understand WHY the bug exists?

---

## Scoring

Each bug gets scored on 3 dimensions (0-10 each):
- **Bug Detection:** Did it find the right issue?
- **Fix Quality:** Is the fix correct?
- **Semantic Understanding:** Does it know WHY?

**Total: 30 points per bug × 10 bugs = 300 points max**

---

## Expected Timeline

| Task | Time |
|------|------|
| Run experiment | 10-15 min |
| Review responses | 30 min |
| Evaluate all bugs | 1-2 hours |
| Analyze patterns | 30 min |
| **Total** | **~3 hours** |
