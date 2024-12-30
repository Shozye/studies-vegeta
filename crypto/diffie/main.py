from api import *
import secrets

from api import SubmissionChallengeResponse
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
    print("Received Response from F2m")
    ctx = F2mContext(modulus=response.params.modulus)
    print("Created Context of F2m")
    g = F2mElement(ctx, response.params.generator)
    g_a = g.pow(a)
    print("Got g_a for F2m")

    response = api.f2m_challenge(g_a.val)
    print("Requested a challenge from F2m, and received it.")

    g_b = F2mElement(ctx, response.public)
    g_ab = response.shared

    assert g_b.pow(a).val == g_ab

def test_validate_fpk(api: Api):
    a = secrets.randbits(2048)
    response = api.fpk_param()

    ctx = FpkContext.from_ints(response.params.prime_base, response.params.modulus)

    g = FpkElement.from_ints(ctx, response.params.generator)
    g_a = g.pow(a)

    response = api.fpk_challenge([elem.val for elem in g_a.coefficients])

    g_b = FpkElement.from_ints(ctx, response.public)
    g_ab = FpkElement.from_ints(ctx, response.shared)

    assert g_b.pow(a) == g_ab

def diffie_helman_modp(response: SubmissionChallengeResponse):
    ctx = response.modp_params.modulus
    a = secrets.randbits(2048)
    g = FpElement(ctx, response.modp_params.generator)

    g_a = g.pow(a)

    g_b = FpElement(ctx, response.modp_challenge.public)
    g_ba = g_b.pow(a)
    return g_a, g_ba

def diffie_helman_fpk(response: SubmissionChallengeResponse) -> tuple[FpkElement, FpkElement]:
    ctx = FpkContext.from_ints(response.fpk_params.prime_base, response.fpk_params.modulus)
    a = secrets.randbits(2048)
    g = FpkElement.from_ints(ctx, response.fpk_params.generator)
    g_a = g.pow(a)

    g_b = FpkElement.from_ints(ctx, response.fpk_challenge.public)
    g_ba = g_b.pow(a)
    return g_a, g_ba


def test_solution(api: Api):
    response: SubmissionChallengeResponse = api.get_solution_challenge()

    g_a_modp, g_ba_modp = diffie_helman_modp(response)
    g_a_fpk, g_ba_fpk = diffie_helman_fpk(response)

    solution_response = api.post_solution_challenge(
        response.session_id,
          g_a_modp.val, g_ba_modp.val, 
          969868, 77, 
          [elem.val for elem in g_a_fpk.coefficients], [elem.val for elem in g_ba_fpk.coefficients])
    print(solution_response.model_dump_json(indent=4))


def main():
    api = Api(999997)
    # test_validate_modp(api)
    # test_validate_f2m(api)
    # test_validate_fpk(api)
    test_solution(api)

if __name__ == "__main__":
    main()