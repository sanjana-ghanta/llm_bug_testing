# LLM Bug Detection - Evaluation Guide

## For Each Bug, Score Three Areas:

### 1. Bug Detection (0-10 points)
**Did the LLM correctly identify the bug?**

- **10 points:** Pinpoints exact line and explains issue 
- **8-9 points:** Identifies location and issue with minor gaps
- **6-7 points:** Identifies general area but vague on specifics
- **4-5 points:** Mentions problem exists but wrong location/cause
- **2-3 points:** Very vague or mostly wrong
- **0-1 points:** Completely missed the bug

**Questions to ask:**
- Did it identify the right line(s)?
- Did it explain what is wrong?
- Did it understand the impact?

---

### 2. Fix Quality (0-10 points)
**How does the LLM's fix compare to ground truth?**

- **10 points:** Matches ground truth exactly or is demonstrably better
- **8-9 points:** Different code but semantically equivalent
- **6-7 points:** Works but suboptimal
- **4-5 points:** Partially correct, may have edge case issues
- **2-3 points:** Wrong approach or introduces new bugs
- **0-1 points:** Completely broken or no fix provided

**Categories:**
- **Exact Match:** Same code as patch
- **Semantic Match:** Different code, same behavior
- **Different Approach:** Alternative that works
- **Incorrect:** Doesn't fix or breaks more

---

### 3. Semantic Understanding (0-10 points)
**Did the LLM understand WHY the bug exists?**

- **10 points:** Explains root cause at system/design level
- **8-9 points:** Explains immediate cause correctly
- **6-7 points:** Understands symptom but not underlying cause
- **4-5 points:** Surface-level understanding only
- **2-3 points:** Misunderstands the mechanism
- **0-1 points:** No understanding of semantics

**Questions to ask:**
- Did it explain WHY (not just WHAT)?
- Did it understand the broader context?
- Could it explain to someone else?

---

## Evaluation Template (Copy for Each Bug)
```
Bug ID: _______
Benchmark: _______

=== BUG DETECTION ===
Score: ___/10
Category: [ ] Exact [ ] Close [ ] Partial [ ] Wrong [ ] Missed

Evidence:
[Quote from LLM response showing what it identified]

Notes:


=== FIX QUALITY ===
Score: ___/10
Category: [ ] Exact Match [ ] Semantic Match [ ] Different [ ] Incorrect

LLM's Fix:
[Paste proposed fix]

Comparison to Ground Truth:
- Fixes the bug: [ ] Yes [ ] No [ ] Unknown
- Edge cases handled: [ ] Yes [ ] No
- Better/Worse than GT: [ ] Better [ ] Same [ ] Worse

Notes:


=== SEMANTIC UNDERSTANDING ===
Score: ___/10
Category: [ ] Full [ ] Good [ ] Partial [ ] Surface [ ] None

Evidence:
[Quote showing depth of understanding]

Notes:


=== OVERALL ===
Total Score: ___/30

Key Observations:
-
-
-

Surprising or Notable:
-
```

---

## Summary Analysis (After All 10 Bugs)

### Overall Statistics
- Bugs correctly identified: ___/10
- Average bug detection score: ___/10
- Average fix quality score: ___/10
- Average semantic understanding: ___/10
- **Overall average: ___/30**

### By Category
**Defects4J (Java):**
- Detection rate: ___/5
- Average score: ___/30

**BugsInPy (Python):**
- Detection rate: ___/5
- Average score: ___/30

### Patterns

**LLM handled well:**


**LLM struggled with:**

**Most surprising success:**

**Most surprising failure:**

---

## Tips for Consistent Evaluation

1. **Be consistent with scoring:** Use the same criteria for each bug
2. **Quote evidence:** Always cite what the LLM said
3. **Compare semantics, not syntax:** Different code can be equivalent
4. **Consider context:** Some bugs are genuinely harder
5. **Note patterns:** Track what types of bugs work well/poorly
6. **Be fair:** Don't penalize for different but valid approaches
