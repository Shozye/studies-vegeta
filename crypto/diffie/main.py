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

def diffie_helman_f2m(response: SubmissionChallengeResponse) -> tuple[F2mElement, F2mElement]:
    ctx = F2mContext(response.f2m_params.modulus)
    a: int = secrets.randbits(k=2048)
    g = F2mElement(ctx=ctx, val=response.f2m_params.generator)

    g_a = g.pow(a)
    g_b = F2mElement(ctx, response.f2m_challenge.public)

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
    g_a_f2m, g_ba_f2m = diffie_helman_f2m(response)
    g_a_fpk, g_ba_fpk = diffie_helman_fpk(response)

    solution_response = api.post_solution_challenge(
        response.session_id,
        g_a_modp.val, g_ba_modp.val, 
        g_a_f2m.val, g_ba_f2m.val,

        [elem.val for elem in g_a_fpk.coefficients], [elem.val for elem in g_ba_fpk.coefficients])
    print(solution_response.model_dump_json(indent=4))

def test_solution_wrong(api: Api):
    response: SubmissionChallengeResponse = api.get_solution_challenge()

    # g_a_modp, g_ba_modp = diffie_helman_modp(response)
    # g_a_f2m, g_ba_f2m = diffie_helman_f2m(response)
    # g_a_fpk, g_ba_fpk = diffie_helman_fpk(response)

    solution_response = api.post_solution_challenge(
        response.session_id,
        4334, 676776, 
        6776, 7667,
        [788], [88])
    print(solution_response.model_dump_json(indent=4))


def main():
    for student_id in [9997, 2561, 534666, 134988, 2348923]:
        print(f"{student_id=}")
        api = Api(student_id)
        # test_validate_modp(api)
        # test_validate_f2m(api)
        # test_validate_fpk(api)
        test_solution(api)
        # test_solution_wrong(api)

if __name__ == "__main__":
    main()