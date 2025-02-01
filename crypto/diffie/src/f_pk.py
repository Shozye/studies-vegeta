from dataclasses import dataclass
import logging
import sys
from .f_p import FpElement
import unittest

@dataclass
class FpkContext:
    p: int
    modulus: list[FpElement]

    @staticmethod
    def from_ints(p: int, modulus: list[int]) -> "FpkContext":
        return FpkContext(p, modulus=[FpElement(p, c) for c in modulus])

    def get_poly_degree(self,):
      return len(self.modulus) - 1 # that is because if 8 elements in the list, the last one is x^7

class FpkElement:
    ctx: FpkContext
    coefficients: list[FpElement]

    @staticmethod
    def from_ints(ctx: FpkContext, coefficients: list[int]) -> 'FpkElement':
        return FpkElement(ctx, [FpElement(ctx.p, c) for c in coefficients])

    def __init__(self, ctx: FpkContext, coefficients: list[FpElement]):
        self.coefficients = [c for c in coefficients]
        self.ctx = ctx
        self.normalize()
    
    def normalize(self):
        # but if length of coefficients was actually bigger or of the same size, 
        # we need to do coefficients modulo ctx.modulus to normalize it.
        self.coefficients = self.modulus(self.coefficients)

        # we want to make two fpk elements the same if they are the same logically
        # for example polynomial [1] is equal to [1, 0] and we need to take one of these and always go with this one
        # i do amount of coefficients equal to polynomial degree
        while len(self.coefficients) < self.ctx.get_poly_degree():
            self.coefficients.append(FpElement(self.ctx.p, 0))
    
    def modulus(self, coeffs: list[FpElement]) -> list[FpElement]:
        # This function wants to do coeffs % ctx.coeffs
        coeffs = [a for a in coeffs] # just copying the list
        some_i = 0

        while len(coeffs) > self.ctx.get_poly_degree():
            leading = coeffs[-1]
            if leading.is_zero():
                coeffs.pop()
                continue

            diff1 = len(coeffs) - len(self.ctx.modulus)
            temp: list[FpElement] = [FpElement(self.ctx.p, 0) for _ in range(diff1)]
            for c in self.ctx.modulus:
                temp.append(leading*c)
            
            coeffs = [c - t for c, t in zip(coeffs, temp)] # subtraction between coeffs and temp
            while coeffs[-1].is_zero():
                coeffs.pop()
            some_i += 1
        return coeffs
    

    def poly_div(self, a: list[FpElement], b: list[FpElement]) -> tuple[list[FpElement], list[FpElement]]:
        """
        Perform polynomial division and return the quotient.
        """
        if len(b) == 0 or all(c.is_zero() for c in b):
            raise ValueError("Cannot divide by zero polynomial.")

        remainder: list[FpElement] = a[:]
        quotient: list[FpElement] = []

        while len(remainder) >= len(b):
            # Compute the leading coefficient for the quotient
            lead_coeff = remainder[-1] / b[-1]
            degree_diff = len(remainder) - len(b)

            # Create the scaled divisor for subtraction
            scaled_divisor = [FpElement(self.ctx.p, 0)] * degree_diff + [c * lead_coeff for c in b]

            while len(quotient) < degree_diff + 1:
                quotient.append(FpElement(self.ctx.p, 0))
            
            quotient[degree_diff] += lead_coeff

            # Update the remainder
            remainder = self.poly_sub(remainder, scaled_divisor)

            while len(remainder) != 0 and remainder[-1].is_zero():
                remainder.pop()

        return quotient, remainder 

    def poly_sub(self, poly1: list[FpElement], poly2: list[FpElement]) -> list[FpElement]:
        """
        Subtract two polynomials and return the result.
        """
        result: list[FpElement] = []
        for i in range(max(len(poly1), len(poly2))):
            elem1 = poly1[i] if i < len(poly1) else FpElement(self.ctx.p, 0)
            elem2 = poly2[i] if i < len(poly2) else FpElement(self.ctx.p, 0)
            result.append(elem1 - elem2)
        
        return result

    def poly_mul(self, poly1: list[FpElement], poly2: list[FpElement]) -> list[FpElement]:
        """
        Multiply two polynomials and return the result.
        """
        result = [FpElement(self.ctx.p, 0)] * (len(poly1) + len(poly2) - 1)
        for i, a in enumerate(poly1):
            for j, b in enumerate(poly2):
                result[i + j] += a * b
        return result
    
    def inverse(self):
        """
        Compute the inverse of the polynomial using the Extended Euclidean Algorithm.
        """
        # Get the modulus polynomial and ensure the context is set up correctly
        modulus_poly = self.ctx.modulus

        # Initializing the algorithm variables
        r0 = modulus_poly[:]
        r1 = self.coefficients[:]

        s0 = [FpElement(self.ctx.p, 1)]  # Identity for multiplication
        s1 = [FpElement(self.ctx.p, 0)]  # Zero polynomial

        t0 = [FpElement(self.ctx.p, 0)]  # Zero polynomial
        t1 = [FpElement(self.ctx.p, 1)]  # Identity for multiplication

        while r1 != [] and any(not coeff.is_zero() for coeff in r1):
            # Polynomial division: quotient and remainder
            q, r = self.poly_div(r0, r1)

            r2 = r[:]
            
            s2 = self.poly_sub(s0, self.poly_mul(q, s1))
            t2 = self.poly_sub(t0, self.poly_mul(q, t1))

            # Update variables for next iteration
            r0, r1 = r1, r2
            s0, s1 = s1, s2
            t0, t1 = t1, t2
            # logging.info(r1)

        # At the end, r0 is the gcd, and t0 is the inverse polynomial up to a scaling factor
        inv_lead = r0[-1].inverse()
        inv = self.poly_mul(t0, [inv_lead])
        return FpkElement(self.ctx, self.modulus(inv))

    def check(self, other: "FpkElement"):
        if self.ctx != other.ctx:
           raise ValueError(f"{self.ctx=} != {other.ctx=}")
    
    def __add__(self, other: "FpkElement") -> "FpkElement":
        self.check(other)
        result = [a + b for a, b in zip(self.coefficients, other.coefficients)]
        return FpkElement(self.ctx, result)

    def __eq__(self, other) -> bool:
        self.check(other)
        return all(a == b for a, b in zip(self.coefficients, other.coefficients))
    
    def __neg__(self) -> "FpkElement":
        return FpkElement(ctx=self.ctx, coefficients=[-b for b in self.coefficients])

    def __sub__(self, other: "FpkElement") -> "FpkElement":
        self.check(other)
        return self + (-other)

    def __mul__(self, other: "FpkElement") -> "FpkElement":
        self.check(other)
        result = self.poly_mul(self.coefficients, other.coefficients)
        return FpkElement(self.ctx, result)

    def __truediv__(self, other: "FpkElement") -> "FpkElement":
        return self * other.inverse()
    
    def pow(self, exp: int) -> "FpkElement":
        base = self + FpkElement(self.ctx, [FpElement(self.ctx.p, 0)])
 
        result = FpkElement(self.ctx, [FpElement(self.ctx.p, 1)])
        while exp > 0:
            if exp % 2 == 1:
                result = result * base
            base = base*base
            exp //= 2
        return result

    
    def pow_secure(self, exp: int) -> "FpkElement":
        base = self + FpkElement(self.ctx, [FpElement(self.ctx.p, 0)])
        dummy = self + FpkElement(self.ctx, [FpElement(self.ctx.p, 0)])

        result = FpkElement(self.ctx, [FpElement(self.ctx.p, 1)])
        while exp > 0:
            if exp % 2 == 1:
                result = result * base
            else:
                dummy = dummy * base
            base = base*base
            exp //= 2
        return result


    def __repr__(self):
        return " + ".join(f"{c}x^{i}" for i, c in enumerate(self.coefficients))



class FpkElementTests(unittest.TestCase):

    def setUp(self):
        self.ctx1 = FpkContext(p=11, modulus=[FpElement(11, coef) for coef in [1, 0, 5, 3, 1, 4, 4, 1]])

        self.p1 = FpkElement.from_ints(self.ctx1, [8, 6, 7, 7, 3, 9, 1])
        self.p2 = FpkElement.from_ints(self.ctx1, [3, 7, 0, 3, 4, 2, 4])

    def test_mizoz_addition(self):
        result = self.p1 + self.p2
        expected = FpkElement.from_ints(self.ctx1, [0, 2, 7, 10, 7, 0, 5])
        self.assertEqual(result, expected)

    def test_mizoz_negation1(self):
        result = -self.p1
        expected = FpkElement.from_ints(self.ctx1, [3, 5, 4, 4, 8, 2, 10])
        self.assertEqual(result, expected)

    def test_mizoz_negation2(self):
        result = -self.p2
        expected = FpkElement.from_ints(self.ctx1, [8, 4, 0, 8, 7, 9, 7])
        self.assertEqual(result, expected)

    def test_mizoz_subtraction1(self):
        result = self.p1 - self.p2
        expected = FpkElement.from_ints(self.ctx1, [5, 10, 7, 4, 10, 7, 8])
        self.assertEqual(result, expected)

    def test_mizoz_subtraction2(self):
        result = self.p2 - self.p1
        expected = FpkElement.from_ints(self.ctx1, [6, 1, 4, 7, 1, 4, 3])
        self.assertEqual(result, expected)
    
    def test_mizoz_multiplication(self):
        result = self.p1 * self.p2
        expected = FpkElement.from_ints(self.ctx1, [4, 10, 10, 4, 10, 1, 3])
        self.assertEqual(result, expected)

    def test_mizoz_inverse1(self):
        result = self.p1.inverse()
        expected = FpkElement.from_ints(self.ctx1, [0, 5, 8, 4, 1, 5, 2])
        self.assertEqual(result, expected)

    def test_mizoz_inverse2(self):
        result = self.p2.inverse()
        expected = FpkElement.from_ints(self.ctx1, [10, 2, 2, 6, 2, 2, 10])
        self.assertEqual(result, expected)

    def test_mizoz_division1(self):
        result = self.p1 / self.p2
        expected = FpkElement.from_ints(self.ctx1, [6, 2, 0, 3, 0, 0, 9])
        self.assertEqual(result, expected)

    def test_mizoz_division2(self):
        result = self.p2 / self.p1
        expected = FpkElement.from_ints(self.ctx1, [7, 2, 4, 2, 1, 1, 10])
        self.assertEqual(result, expected)

if __name__ == "__main__":
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger( "SomeTest.testSomething" ).setLevel( logging.DEBUG )
    
    unittest.util._MAX_LENGTH = 2000 # type: ignore
    unittest.main()