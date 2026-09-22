<p align="center">
  <a href="https://oyren.ai">
    <img src="assets/oyren-button.svg" alt="Open this in Oyren" width="280" />
  </a>
</p>

# Lesson 001 — Hello, Lean!

**Time:** ~10–15 minutes · **Prerequisites:** none, not even prior programming experience.

You're on the `lesson-001` branch of [CodeMaths](https://github.com/tehsil-digital/codemaths).
Each lesson in this course lives on its own branch — this one has nothing on it but
Lesson 001, so there's nothing else to get lost in.

## What you'll learn

- What Lean is, and why we're learning it as a first programming language
- `#eval` — asking Lean to compute something and show you the answer
- `def` — defining your own functions
- `Nat` and `Bool`, and why Lean checks types *before* it runs your code

## Do this

1. Open [`Lesson001/Basic.lean`](Lesson001/Basic.lean).
2. Read it top to bottom — every new idea has a comment explaining it.
3. When you hit a `sorry`, replace it with your own definition. That's the exercise.
4. Uncomment the matching `#eval` line and check the answer, either:
   - by putting your cursor on that line and reading the **Lean Infoview** panel in your editor, or
   - from a terminal in this folder:
     ```bash
     lake env lean Lesson001/Basic.lean
     ```
     No output = no errors. A `declaration uses 'sorry'` warning means an exercise is still unfinished.

## Reference

This lesson follows the introduction to
*[Functional Programming in Lean](https://lean-lang.org/functional_programming_in_lean/Introduction/)*,
the book we're using to teach Lean 4 as a general-purpose programming language before
moving on to proofs.

## Next lesson

`lesson-002` (coming soon) — pattern matching and recursion.

---

<sub>Part of the CodeMaths Lean 4 course. Lessons live one-per-branch —
`git checkout lesson-001`, `lesson-002`, … — so switching branches always shows you
exactly one lesson's worth of code, never more.</sub>
