import Std

namespace DyadicEnvelope

-- Multiply through the denominators in the squared bounds for the
-- tail k = ℓ+d and head ℓ = k+d, respectively.
theorem tail_squared_power (ell d : Nat) :
    2^ell * 2^d = 2^(ell+d) := by
  rw [Nat.pow_add]

theorem head_squared_power (k d : Nat) :
    2^(k+d) * 2^(3*d) = 2^k * 2^(4*d) := by
  rw [← Nat.pow_add, ← Nat.pow_add]
  congr 1
  omega

theorem own_block_ratio {ell m : Nat} (upper : m < 2^(ell+1)) :
    m < 2 * 2^ell := by
  simpa [Nat.pow_succ, Nat.mul_comm] using upper

theorem disk_floor : (31/32 : Rat)^2 > 1/2 := by decide +kernel

#print axioms tail_squared_power
#print axioms head_squared_power
#print axioms own_block_ratio
#print axioms disk_floor

end DyadicEnvelope
