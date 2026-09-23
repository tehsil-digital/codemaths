import Mathlib

#eval 1 + 1


#check ℕ
#check Nat

example : ℕ = Nat := by rfl


def add1 (n : ℕ ) : ℤ    :=
  n - 1

#eval add1 0


def double (n : Nat) : Nat :=
  sorry

def isEven (n : Nat) : Bool :=
  sorry



def doubleIsEven (n : Nat) : Bool :=
  sorry
