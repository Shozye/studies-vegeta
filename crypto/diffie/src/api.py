import base64
from typing import Literal
import requests
from pydantic import BaseModel, Field, ValidationInfo, field_validator, root_validator

def base_64_encode(value: int) -> str:
    """Encodes an integer into URL-safe base64, big-endian with no padding."""
    byte_array = value.to_bytes((value.bit_length() + 7) // 8, byteorder='big')
    return base64.urlsafe_b64encode(byte_array).decode().rstrip('=')

def base_64_decode(value: str) -> int:
    padding = '=' * (-len(value) % 4)
    decoded_bytes = base64.urlsafe_b64decode(value + padding)
    return int.from_bytes(decoded_bytes, "big")

def base64_encode_bitstring(value: int) -> str:
    """Encodes an integer as a bit string in little-endian order, then URL-safe base64."""
    byte_length = (value.bit_length() + 7) // 8
    little_endian_bytes = value.to_bytes(byte_length, byteorder='little')
    base64_encoded = base64.urlsafe_b64encode(little_endian_bytes).rstrip(b'=').decode('utf-8')

    return base64_encoded
        
def base64_decode_bitstring(value: str) -> int:
    padding = '=' * (-len(value) % 4)
    decoded_bytes = base64.urlsafe_b64decode(value + padding)
    return int.from_bytes(decoded_bytes, "little")

class BaseResponse(BaseModel):
    status: str

class ParamsBase(BaseModel):
    name: str  # Reference name of the parameter set

class ModPParams(ParamsBase):
    modulus: int  # Prime modulus p
    generator: int  # Subgroup generator g
    order: int  # Subgroup order q

    @field_validator("modulus", "generator", "order", mode='before')
    @classmethod
    def decode_params(cls, value: str, info:ValidationInfo):
        try:
            return base_64_decode(value)
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value '{value}': {e}")

class F2mParams(ParamsBase):
    extension: int  # Field extension factor m
    modulus: int  # Field-defining polynomial
    generator: int  # Subgroup generator g
    order: int  # Subgroup order q


    @field_validator("modulus", mode='before')
    @classmethod
    def decode_params1(cls, value: str, info:ValidationInfo):
        extension: int = info.data['extension']
        padding = '=' * (-len(value) % 4)
        decoded_bytes = base64.urlsafe_b64decode(value + padding)
        modulus = int.from_bytes(decoded_bytes, 'little')
        modulus_with_shit = modulus | (1 << extension)
        return modulus_with_shit

    @field_validator("generator", mode='before')
    @classmethod
    def decode_params2(cls, value: str, info:ValidationInfo):
        try:
            return base64_decode_bitstring(value)
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value generator '{value}': {e}")

    @field_validator("order", mode='before')
    @classmethod
    def decode_params3(cls, value: str, info:ValidationInfo):
        try:
            return base_64_decode(value)
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value order '{value}': {e}")



class FpkParams(ParamsBase):
    prime_base: int  # Base field prime modulus p
    extension: int  # Field extension factor k
    modulus: list[int]  # Field-defining polynomial as an array
    generator: list[int]  # Subgroup generator as a polynomial
    order: int  # Subgroup order q

    @field_validator("order", "prime_base", mode='before')
    @classmethod
    def decode_params1(cls, value: str, info:ValidationInfo):
        try:
            return base_64_decode(value)
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value '{value}': {e}")

    @field_validator("modulus", mode='before')
    @classmethod
    def decode_params2(cls, value: list[str], info:ValidationInfo):
        try:
            new_value = list(map(base_64_decode, value))
            return new_value + [1]
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value '{value}': {e}")

    @field_validator("generator", mode='before')
    @classmethod
    def decode_params3(cls, value: list[str], info:ValidationInfo):
        try:
            return list(map(base_64_decode, value))
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value '{value}': {e}")

class ModPParamsResponse(BaseResponse):
    type: str   
    params: ModPParams

class F2mParamsResponse(BaseResponse):
    type: str   
    params: F2mParams

class FpkParamsResponse(BaseResponse):
    type: str   
    params: FpkParams


class ChallengeF2mRequest(BaseModel):
    public: str # Client Diffie-Hellman public key. Encoded as bit string in little-endian order. Uses url-safe base64 encoding.

    @field_validator("public", mode="before")
    @classmethod
    def encode_public(cls, value: str, info: ValidationInfo):
        try:
            return base64_encode_bitstring(int(value))
        except Exception as e:
            raise # ValueError(f"Failed to encode public key: {e}")


class ChallengeFpkRequest(BaseModel):
    public: list[str] # Client Diffie-Hellman public key. Encoded as an array of coefficients in little endian order (element 0 corresponds to x^0). Each coefficient uses url-safe base64, big-endian encoding.

    @field_validator("public", mode="before")
    @classmethod
    def encode_public(cls, value: list[str], info: ValidationInfo):
        try:
            # Assume the input is a list of string representations of integers
            return [base_64_encode(int(coeff)) for coeff in value]  # Reverse for little-endian
        except Exception as e:
            raise ValueError(f"Failed to encode public key coefficients: {e}")


class ChallengeModPRequest(BaseModel):
    public: str # Client Diffie-Hellman public key. Uses url-safe base64, big-endian encoding.


    @field_validator("public", mode="before")
    @classmethod
    def encode_public(cls, value: str, info: ValidationInfo):
        try:
            return base_64_encode(int(value))  # Assume input is a string representation of an integer
        except Exception as e:
            raise ValueError(f"Failed to encode public key: {e}")
        

class ChallengeF2mResponse(BaseResponse):
    public: int  # Server Diffie-Hellman public key
    shared: int  # Client/Server Diffie-Hellman shared secret (result)

    @field_validator("public", "shared", mode="before")
    @classmethod
    def encode_fields(cls, value: str, info: ValidationInfo):
        try:
            return base64_decode_bitstring(value)
        except Exception as e:
            raise ValueError(f"Failed to encode field {info.field_name}: {e}")
        

class ChallengeModPResponse(BaseResponse):
    public: int  # Server Diffie-Hellman public key
    shared: int  # Client/Server Diffie-Hellman shared secret (result)

    @field_validator("public", "shared", mode="before")
    @classmethod
    def encode_fields(cls, value: str, info: ValidationInfo):
        """Encodes the input value using URL-safe base64 with big-endian encoding."""
        try:
            return base_64_decode(value)
        except Exception as e:
            raise ValueError(f"Failed to encode field {info.field_name}: {e}")


class ChallengeFpkResponse(BaseResponse):
    public: list[int]  # Server Diffie-Hellman public key coefficients
    shared: list[int]  # Client/Server Diffie-Hellman shared secret coefficients

    @field_validator("public", "shared", mode="before")
    @classmethod
    def encode_coefficients(cls, value: list[str], info: ValidationInfo):
        """Encodes a list of coefficients using URL-safe base64 with big-endian encoding."""
        try:
            return [base_64_decode(coeff) for coeff in value]
        except Exception as e:
            raise ValueError(f"Failed to encode field {info.field_name}: {e}")


class ModPParamsSubmissionRequest(BaseResponse):
    public: str
    shared: str

    @field_validator('public', 'shared', mode='after')
    @classmethod
    def decode_params(cls, value: str, info: ValidationInfo):
        try:
            return base_64_encode(int(value))
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value '{value}': {e}")

class F2mParamsSubmissionRequest(BaseResponse):
    public: str
    shared: str

    @field_validator('public', 'shared', mode='after')
    @classmethod
    def decode_params(cls, value: str, info: ValidationInfo):
        try:
            return base64_encode_bitstring(int(value))
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value '{value}': {e}")

class FpkParamsSubmissionRequest(BaseResponse):
    public: list[str]
    shared: list[str]

    @field_validator('public', 'shared', mode='after')
    @classmethod
    def decode_params(cls, value: list[str], info: ValidationInfo):
        try:
            # Decode each element of the list
            return [base_64_encode(int(item)) for item in value]
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value '{value}': {e}")

class SubmissionResponseRequest(BaseModel):
    session_id: str
    modp: ModPParamsSubmissionRequest
    f2m: F2mParamsSubmissionRequest
    fpk: FpkParamsSubmissionRequest
 
class SubmissionResponseResponse(BaseResponse):
    modp: BaseResponse
    f2m: BaseResponse
    fpk: BaseResponse


class ModPChallenge(BaseModel):
    public: int

    @field_validator('public', mode='before')
    @classmethod
    def decode_params(cls, value: str, info: ValidationInfo):
        try:
            return base_64_decode(value)
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value '{value}': {e}")
        
class FpkChallenge(BaseModel):
    public: list[int]

    @field_validator('public', mode='before')
    @classmethod
    def decode_params(cls, value: list[str], info: ValidationInfo):
        try:
            return [base_64_decode(val) for val in value]
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value '{value}': {e}")

class F2mChallenge(BaseModel):
    public: int

    @field_validator('public', mode='before')
    @classmethod
    def decode_params(cls, value: str, info: ValidationInfo):
        try:
            return base64_decode_bitstring(value)
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value '{value}': {e}")

class SubmissionChallengeResponse(BaseResponse):
    session_id: str
    timeout: str
    modp_params: ModPParams
    f2m_params: F2mParams
    fpk_params: FpkParams
    modp_challenge: ModPChallenge
    f2m_challenge: F2mChallenge
    fpk_challenge: FpkChallenge

class Api:
    def __init__(self, student_id: int):
        self.student_id = student_id
    
    def root(self) -> BaseResponse:
        url = "https://crypto24.random-oracle.xyz/"
        response = requests.get(url)
        return BaseResponse(**response.json())

    def modp_param(self) -> ModPParamsResponse:
        url = 'https://crypto24.random-oracle.xyz/validate/list2/modp/param'
        response = requests.get(url)
        return ModPParamsResponse(**response.json())

    def f2m_param(self) -> F2mParamsResponse:
        url = 'https://crypto24.random-oracle.xyz/validate/list2/f2m/param'
        response = requests.get(url)
        return F2mParamsResponse(**response.json())

    def fpk_param(self) -> FpkParamsResponse:
        url = 'https://crypto24.random-oracle.xyz/validate/list2/fpk/param'
        response = requests.get(url)
        return FpkParamsResponse(**response.json())
    
    def modp_challenge(self, public: int) -> ChallengeModPResponse:
        url = 'https://crypto24.random-oracle.xyz/validate/list2/modp/challenge'
        payload = ChallengeModPRequest(public=str(public))
        print(f"modp {payload.model_dump_json()=}")
        response = requests.post(url, json=payload.model_dump())
        if 'detail' in response.json():
            raise Exception(f"Error {response.json()} during modp challenge!")
        return ChallengeModPResponse(**response.json())
    
    def f2m_challenge(self, public: int) -> ChallengeF2mResponse:
        url = 'https://crypto24.random-oracle.xyz/validate/list2/f2m/challenge'
        payload = ChallengeF2mRequest(public=str(public))
        print(f"f2m {payload.model_dump_json()=}")
        response = requests.post(url, json=payload.model_dump())

        if 'detail' in response.json():
            raise Exception(f"Error {response.json()} during f2m challenge!")
        return ChallengeF2mResponse(**response.json())
    
    def fpk_challenge(self, public: list[int]) -> ChallengeFpkResponse:
        url = 'https://crypto24.random-oracle.xyz/validate/list2/fpk/challenge'
        payload = ChallengeFpkRequest(public=[str(x) for x in public])
        print(f"fpk {payload.model_dump_json()=}")
        response = requests.post(url, json=payload.model_dump())
        if 'detail' in response.json():
            raise Exception(f"Error {response.json()} during fpk challenge!")
        return ChallengeFpkResponse(**response.json())
    
    def get_solution_challenge(self) -> SubmissionChallengeResponse:
        url = f"https://crypto24.random-oracle.xyz/submit/list2/{self.student_id}/solution"
        response = requests.get(url)
        return SubmissionChallengeResponse(**response.json())
    
    def post_solution_challenge(self, session_id, modp_public: int, modp_shared: int, f2m_public: int, f2m_shared: int, fpk_public: list[int], fpk_shared: list[int]) -> SubmissionResponseResponse:
        url = f"https://crypto24.random-oracle.xyz/submit/list2/{self.student_id}/solution"
        payload = SubmissionResponseRequest(
            session_id=session_id,
            modp=ModPParamsSubmissionRequest(status="success", public=str(modp_public), shared=str(modp_shared)),
            f2m=F2mParamsSubmissionRequest(status="success", public=str(f2m_public), shared=str(f2m_shared)),
            fpk=FpkParamsSubmissionRequest(status="success", public=list(map(str,fpk_public)), shared=list(map(str,fpk_shared)))
        )
        response = requests.post(url=url, json=payload.model_dump())
        if 'detail' in response.json():
            raise Exception(f"Error {response.json()} during solution challenge!")
        return SubmissionResponseResponse(**response.json())
    

def test_challenges():
    api = Api(123456)
    SOLUTION_CHALLENGE_MODP_PUBLIC: int = 6689835855699192231345420327010098815447856515207931935365649445532496062420093311026603903556891753945810241912419680411285658066780064569504455391898015467565080272549212884728664915296813735313471791903411634988387765923121947704827367988819504008785863027000233092773394603605975060486101015463287949115764361929483660617360491095620340316851761258733054093891874189436444045084077858473352951300342577416628474912642640643715332511161937477097949500333112079260225405443804945941621977057351954402630110765417305993948136700925248768033320287900484925088446095984564968514600888688643935701598973058003193835920
    assert api.modp_challenge(SOLUTION_CHALLENGE_MODP_PUBLIC).status == "success"
    SOLUTION_CHALLENGE_F2M_PUBLIC: int = 7751035859167595319010573603930483260109412474948453100036817317501345150955705621570653179566530986372159256576641121685721317767248027166954617404395244388611300409544322503206192763217905106664136229757723992849047885286875841831016035618177739253704480758728329007318807536474521242969366568610798327786870682803096531735960978668865810533456209326510052175231568890078294606167550014324788482988838792199348056775354470300654847047432718762233974049687418242708066734177024985885171437747742481275138054147996023579840358144254717045500331205625372071511834298537657021877943170754066957729076664542196052998958
    assert api.f2m_challenge(SOLUTION_CHALLENGE_F2M_PUBLIC).status == "success"
    SOLUTION_CHALLENGE_FPK_PUBLIC: list[int] = [108551187513231552284180478915466260731738505337868716380944651662306442210992, 54261066806900338546825498572146661912046782693755854786725838669282886218724, 34829151539745835873577583470438339213514894288715655638145523183778482442075, 101619432569024292804499552547911958440681731570738548717028879810852731966321, 27830329610008654537634101980916785941938730354995361965885281577028634594335, 68741820566789445372724148373480526883432524359806804811176340839172358654941, 105055343970502763360047095980144320867220704271564195266738337887990100344151, 17307414726510811752309775369623853677127508947328870699072998482251720026967]
    assert api.fpk_challenge(SOLUTION_CHALLENGE_FPK_PUBLIC).status == "success"

def get_solution_challenge(student_id: int):
    api = Api(student_id)
    print(api.get_solution_challenge().model_dump_json(indent=4))

if __name__ == "__main__":
    get_solution_challenge(123456)

    # test_challenges()

