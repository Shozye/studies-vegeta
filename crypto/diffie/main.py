from api import *
import secrets

from f_p import FpElement
from f_pk import FpkElement, FpkContext
from f_2m import F2mContext, F2mElement

def test_validate_modp(api: Api):
    a = secrets.randbits(2048)
    response = api.modp_param()
    ctx = response.params.modulus

    g = FpElement(ctx, response.params.generator)
    g_a = g.pow(a)

    response = api.modp_challenge(g_a.val)

    g_b = FpElement(ctx, response.public)
    g_ab = response.shared

    assert g_b.pow(a).val == g_ab

def test_validate_f2m(api: Api):
    a = secrets.randbits(2048)
    response = api.f2m_param()
    ctx = F2mContext(response.params.modulus)

    g = F2mElement(ctx, response.params.generator)
    g_a = g.pow(a)

    response = api.f2m_challenge(g_a.val)

    g_b = F2mElement(ctx, response.public)
    g_ab = response.shared

    assert g_b.pow(a).val == g_ab

def test_validate_fpk(api: Api):
    a = secrets.randbits(2048)
    response = api.fpk_param()

    ctx = FpkContext.from_ints(response.params.prime_base, response.params.modulus + [1])

    g = FpkElement.from_ints(ctx, response.params.generator)
    g_a = g.pow(a)

    response = api.fpk_challenge([elem.val for elem in g_a.coefficients])

    g_b = FpkElement.from_ints(ctx, response.public)
    g_ab = FpkElement.from_ints(ctx, response.shared)

    assert g_b.pow(a) == g_ab

def main():
    api = Api(999997)
    # test_validate_modp(api)
    test_validate_f2m(api)
    # test_validate_fpk(api)

if __name__ == "__main__":
    main()