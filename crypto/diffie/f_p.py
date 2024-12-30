
class FpElement:
    def __init__(self, p: int, val: int):
        self.p = p
        self.val = val % p
    
    def __eq__(self, other):
        return self.val == other.val

    def __repr__(self):
        return f"F_{self.p}({self.val})"

    def extended_gcd(self, a: int, b: int) -> tuple[int, int, int]:
        old_r, r = a, b
        old_s, s = 1, 0
        old_t, t = 0, 1

        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t

        return old_r, old_s, old_t

    def __add__(self, other: "FpElement") -> "FpElement":
        return FpElement(self.p, self.val + other.val)

    def __sub__(self, other: "FpElement") -> "FpElement":
        return self + (-other)

    def __neg__(self) -> "FpElement":
        return FpElement(self.p, (self.p - self.val) % self.p)

    def __mul__(self, other: "FpElement") -> "FpElement":
        return FpElement(self.p, (self.val * other.val) % self.p)

    def __truediv__(self, other: "FpElement") -> "FpElement":
        return self * other.inverse()

    def inverse(self) -> "FpElement":
        g, x, _ = self.extended_gcd(self.val, self.p)
        if g != 1:
            raise ValueError("No inverse exists!")
        return FpElement(self.p, x % self.p)

    def pow(self, exp: int) -> "FpElement":
        result = FpElement(p=self.p, val=1)
        base = self + FpElement(self.p, 0)

        while exp > 0:
            if exp % 2 == 1:
                result = result * base
            base = base * base
            exp //= 2

        return result

    def pow_secure(self, exp: int) -> "FpElement":
        # to jest odporne na sprawdzanie czasu. 
        result, dummy = FpElement(p=self.p, val=1), FpElement(p=self.p, val=1)
        base = self + FpElement(self.p, 0)

        while exp > 0:
            if exp % 2 == 1:
                result = result * base
            else:
                dummy = result * base
            base = base * base
            exp //= 2

        return result
    
    def is_zero(self) -> bool:
        return self.val == 0
    
    def is_one(self) -> bool:
        return self.val == 1


import unittest

class TestFpElement(unittest.TestCase):
    def setUp(self):
        self.p = 17

    def test_fp_addition(self):
        a = FpElement(self.p, 2)
        b = FpElement(self.p, 3)
        c = FpElement(self.p, 0)
        
        self.assertEqual((a + b).val, 5)
        self.assertEqual((a + c).val, a.val)  # a+0 = a
        
        x = FpElement(self.p, 16)
        y = FpElement(self.p, 5)
        self.assertEqual((x + y).val, 4)  

    def test_fp_subtraction(self):
        a = FpElement(self.p, 2)
        b = FpElement(self.p, 3)
        self.assertEqual((b - a).val, 1)
        
        x = FpElement(self.p, 1)
        y = FpElement(self.p, 0)
        self.assertEqual((y - x).val, 16) 

    def test_fp_multiplication(self):
        a = FpElement(self.p, 2)
        b = FpElement(self.p, 3)
        zero = FpElement(self.p, 0)
        
        self.assertEqual((a * b).val, 6)
        self.assertEqual((a * zero).val, 0)
        
        big = FpElement(self.p, 20)
        self.assertEqual((big * b).val, 9) 

    def test_fp_negation(self):
        a = FpElement(self.p, 2)
        zero = FpElement(self.p, 0)
        
        self.assertEqual((-a).val, 15)  # 17 - 2 = 15
        self.assertEqual((-zero).val, 0)

    def test_fp_inverse(self):
        a = FpElement(self.p, 3)
        inv_a = a.inverse()
        self.assertEqual((a * inv_a).val, 1)
        
        b = FpElement(self.p, 5)
        inv_b = b.inverse()
        self.assertEqual((b * inv_b).val, 1)

    def test_fp_division(self):
        a = FpElement(self.p, 2)
        b = FpElement(self.p, 3)
        div = a / b
        self.assertEqual(div.val, 12)  

    def test_fp_exponentiation(self):
        a = FpElement(self.p, 2)
        exp = 5
        res = a.pow(exp)
        self.assertEqual(res.val, 15)  # 2^5 % 17 = 32 % 17 = 15
        
        exp_big = 16
        res_big = a.pow(exp_big)
        self.assertEqual(res_big.val, 1)  # 2^16 % 17 = 1 // fermat

    def test_fp_exponentiation_secure(self):
        a = FpElement(self.p, 2)
        exp = 5
        res = a.pow_secure(exp)
        self.assertEqual(res.val, 15)  # 2^5 % 17 = 32 % 17 = 15
        
        exp_big = 16
        res_big = a.pow_secure(exp_big)
        self.assertEqual(res_big.val, 1)  # 2^16 % 17 = 1 // fermat

if __name__ == "__main__":
    unittest.main()
