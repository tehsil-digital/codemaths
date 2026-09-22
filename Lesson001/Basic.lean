/- Lesson 001 -- Hello, Lean!

   Lean is a *functional* programming language: instead of giving the computer a
   list of steps to run, you write down definitions and Lean works out the answer.
   It also happens to be a proof assistant, but this lesson only cares about the
   programming-language half.

   Reference: "Functional Programming in Lean", Introduction
   https://lean-lang.org/functional_programming_in_lean/Introduction/
-/

-- `#eval` asks Lean to run an expression right now and print the result.
-- Put your cursor at the end of the line below and check the Lean Infoview
-- panel in your editor -- it shows the answer without you running anything.
#eval 1 + 1

-- `def` defines a new function. Every input and the output need a type.
-- `Nat` is the type of natural numbers: 0, 1, 2, 3, ...
def add1 (n : Nat) : Nat :=
  n + 1

#eval add1 7 -- 8

-- Lean checks types BEFORE running anything, not while running like Python.
-- Uncomment the line below and read the red squiggle: you can't add 1 to text.
-- #eval add1 "seven"

/- ============================================================
   YOUR TURN -- replace each `sorry` below with a real definition, then
   uncomment its `#eval` line to check your work in the Infoview.
   `sorry` is a placeholder that type-checks but computes nothing; Lean
   warns "declaration uses 'sorry'" until you replace it, and refuses to
   `#eval` anything built from it.
   ============================================================ -/

-- 1. Double a number.
def double (n : Nat) : Nat :=
  sorry

-- #eval double 5 -- should print 10

-- 2. Is this number even? `%` is remainder, `==` is boolean equality on Nat.
def isEven (n : Nat) : Bool :=
  sorry

-- #eval isEven 4 -- should print true
-- #eval isEven 7 -- should print false

-- 3. Combine what you just wrote.
def doubleIsEven (n : Nat) : Bool :=
  sorry

-- #eval doubleIsEven 3 -- should print true
