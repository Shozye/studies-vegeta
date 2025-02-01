from dataclasses import dataclass


@dataclass
class F2mContext:
    modulus: int
    p: int = 2 # ?

class F2mElement:
    def __init__(self, ctx: F2mContext, val: int):
        self.ctx = ctx
        self.val =  self.poly_mod(val)

    def poly_mod(self, val: int) -> int:
        remainder = val
        divisor = self.ctx.modulus
        div_degree = self.get_binary_poly_degree(divisor)

        while self.get_binary_poly_degree(remainder) >= div_degree:
            remainder_degree = self.get_binary_poly_degree(remainder)
            shift = remainder_degree - div_degree
            remainder ^= divisor << shift
        return remainder
    
    
    def __eq__(self, other):
        return self.val == other.val

    def __add__(self, other: "F2mElement") -> "F2mElement":
        return F2mElement(self.ctx, self.val ^ other.val)

    def __sub__(self, other: "F2mElement") -> "F2mElement":
        return self + (-other)

    def __neg__(self) -> "F2mElement":
        return F2mElement(self.ctx, val=self.val)

    def __truediv__(self, other: "F2mElement") -> "F2mElement":
        return self * other.inverse()

    def poly_mul(self, a: int, b: int) -> int:
        result = 0
        while b:
            if b & 1:
                result ^= a  
            b >>= 1 
            a <<= 1  
        return result
    
    def get_binary_poly_degree(self, p: int) -> int:
        if p == 0:
            return -1  
        return p.bit_length() - 1

    
    def poly_div(self, a: int, b: int) -> tuple[int, int]:
        if b == 0:
            raise ValueError("Division by zero polynomial")

        quotient = 0
        remainder = a
        divisor_degree = self.get_binary_poly_degree(b)

        while self.get_binary_poly_degree(remainder) >= divisor_degree:
            remainder_degree = self.get_binary_poly_degree(remainder)
            shift = remainder_degree - divisor_degree

            quotient ^= 1 << shift

            remainder ^= b << shift

        return quotient, remainder
    
    def poly_extended_gcd(self, a: int, b: int) -> tuple[int, int, int]:
        """
        Extended GCD for binary polynomials.
        Returns (gcd, u, v) such that gcd = u*a + v*b.
        """
        if b == 0:
            return a, 1, 0

        r0, r1 = a, b
        u0, u1 = 1, 0
        v0, v1 = 0, 1

        while r1 != 0:
            q, r = self.poly_div(r0, r1)
            r0, r1 = r1, r
            u0, u1 = u1, u0 ^ self.poly_mul(q, u1)
            v0, v1 = v1, v0 ^ self.poly_mul(q, v1)

        return r0, u0, v0


    
    def __mul__(self, other: "F2mElement") -> "F2mElement":
        return F2mElement(self.ctx, val=self.poly_mul(self.val, other.val))

    def inverse(self) -> "F2mElement":
        """
        Compute the modular inverse of a polynomial modulo an irreducible polynomial.
        Returns the inverse if it exists, otherwise None.
        """
        gcd, u, _ = self.poly_extended_gcd(self.val, self.ctx.modulus)

        _, u = self.poly_div(u, self.ctx.modulus)
        return F2mElement(self.ctx, u)



    def pow(self, exp: int) -> "F2mElement":
        base = -self
 
        result = F2mElement(self.ctx, 1)

        while exp > 0:
            if exp % 2 == 1:
                result = result * base
            base = base*base
            exp //= 2
        return result

    
    def pow_secure(self, exp: int) -> "F2mElement":
        base = -self # those - selfs are just to copy tbh 
        dummy = -self

        result = F2mElement(self.ctx, val=1)
        while exp > 0:
            if exp % 2 == 1:
                result = result * base
            else:
                dummy = dummy * base
            base = base*base
            exp //= 2
        return result

import unittest

class TestF2mElement(unittest.TestCase):

    def setUp(self):
        # Initialize the F2mContext with a given modulus (irreducible polynomial)
        self.ctx = F2mContext(modulus=0b11111101111101001)

    def test_binary_polynomial_addition(self):
        poly_a = F2mElement(self.ctx, 0b1000101000011101)
        poly_b = F2mElement(self.ctx, 0b1010011011000101)
        
        result = poly_a + poly_b
        expected = F2mElement(self.ctx, 0b10110011011000)
        
        self.assertEqual(result, expected, f"Expected {expected.val}, got {result.val}")

    def test_binary_polynomial_subtraction(self):
        poly_a = F2mElement(self.ctx, 0b1000101000011101)
        poly_b = F2mElement(self.ctx, 0b1010011011000101)
        
        result_a_b = poly_a - poly_b
        result_b_a = poly_b - poly_a
        expected = F2mElement(self.ctx, 0b10110011011000)

        self.assertEqual(result_a_b, expected, f"Expected {expected.val}, got {result_a_b.val}")
        self.assertEqual(result_b_a, expected, f"Expected {expected.val}, got {result_b_a.val}")

    def test_binary_polynomial_multiplication(self):
        poly_a = F2mElement(self.ctx, 0b1000101000011101)
        poly_b = F2mElement(self.ctx, 0b1010011011000101)

        result = poly_a * poly_b
        expected = F2mElement(self.ctx, 0b1110001011001111)

        self.assertEqual(result, expected, f"Expected {expected.val}, got {result.val}")

    def test_binary_polynomial_negation(self):
        poly_a = F2mElement(self.ctx, 0b1000101000011101)
        poly_b = F2mElement(self.ctx, 0b1010011011000101)

        neg_a = -poly_a
        neg_b = -poly_b

        # Negation in GF(2^m) is the same value 
        self.assertEqual(neg_a, poly_a, f"Expected {poly_a.val}, got {neg_a.val}")
        self.assertEqual(neg_b, poly_b, f"Expected {poly_b.val}, got {neg_b.val}")


    def test_binary_polynomial_division(self):
        poly_a = F2mElement(self.ctx, 0b1000101000011101)
        poly_b = F2mElement(self.ctx, 0b1010011011000101)

        div_a_b = poly_a / poly_b
        div_b_a = poly_b / poly_a

        self.assertEqual(
            div_a_b, 
            F2mElement(self.ctx, 0b11001000101111),
            f"Expected {bin(0b11001000101111)}, got {bin(div_a_b.val)}"
        )
        self.assertEqual(
            div_b_a, 
            F2mElement(self.ctx, 0b1101101111011110),
            f"Expected {bin(0b1101101111011110)}, got {bin(div_b_a.val)}"
        )

    def test_binary_polynomial_inverse(self):
        poly_a = F2mElement(self.ctx, 0b1000101000011101)
        poly_b = F2mElement(self.ctx, 0b1010011011000101)

        inv_a = poly_a.inverse()
        inv_b = poly_b.inverse()

        self.assertEqual(
            inv_a * poly_a, 
            F2mElement(self.ctx, 1), 
        )
        self.assertEqual(
            inv_b * poly_b, 
            F2mElement(self.ctx, 1), 
        )

        self.assertEqual(
            inv_a, 
            F2mElement(self.ctx, 0b111001101011011),
        )
        self.assertEqual(
            inv_b, 
            F2mElement(self.ctx, 0b1100101110010000),
        )


    def test_binary_polynomial_exponentiation(self):
        poly_a = F2mElement(self.ctx, 0b1000101000011101)
        poly_b = F2mElement(self.ctx, 0b1010011011000101)

        order = 65535
        exp = 5
        exp_a = poly_a.pow(exp)
        exp_b = poly_b.pow(exp)

        assert exp_a == poly_a * poly_a * poly_a * poly_a * poly_a
        assert exp_b == poly_b * poly_b * poly_b * poly_b * poly_b
        assert exp_a == poly_a.pow_secure(exp)
        assert exp_b == poly_b.pow_secure(exp)


if __name__ == "__main__":
    unittest.main()