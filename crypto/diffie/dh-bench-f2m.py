import json
import secrets
import sys
import time

from pydantic import BaseModel, ValidationInfo, field_validator

from src.f_p import FpElement
from src.f_2m import F2mElement, F2mContext
from src.f_pk import FpkElement, FpkContext
from src.api import F2mParams, ModPParams, base64_decode_bitstring, base64_encode_bitstring, base_64_encode

class InputFormat(BaseModel):
    public: int

    @field_validator("public", mode='before')
    @classmethod
    def decode_params(cls, value: str, info:ValidationInfo):
        try:
            return base64_decode_bitstring(value)
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value '{value}': {e}")

class ResponseFormat(BaseModel):
    public: str
    shared: str
    time_keygen: int # nanoseconds
    time_finalize: int # nanoseconds

    @field_validator("public", "shared", mode='before')
    @classmethod
    def encode_params(cls, value: str, info:ValidationInfo):
        try:
            return base64_encode_bitstring(int(value))
        except Exception as e:
            raise ValueError(f"Failed to decode base64 value '{value}': {e}")

def main(params: F2mParams):
    ctx = F2mContext(params.modulus)
    g = F2mElement(ctx, params.generator)

    t1 = time.time_ns() # THIS IS CLEARLY MARKED BENCHMARKED REGION IN MY CODE
    a = secrets.randbits(2048)
    g_a = g.pow_secure(a)
    t2 = time.time_ns() # THIS IS CLEARLY MARKED BENCHMARKED REGION IN MY CODE
    time_keygen = t2-t1

    for line in sys.stdin:
        # line is json format of ChallengeModPRequest yeah?
        request = InputFormat(**json.loads(line))
        # print(f"Received", request.model_dump_json())
        g_b = F2mElement(ctx, request.public)

        t1 = time.time_ns() # THIS IS CLEARLY MARKED BENCHMARKED REGION IN MY CODE
        g_ba = g_b.pow_secure(a)
        t2 = time.time_ns()# THIS IS CLEARLY MARKED BENCHMARKED REGION IN MY CODE
        time_finalize = t2 - t1

        response = ResponseFormat(
            public=str(g_a.val),
            shared=str(g_ba.val), 
            time_keygen=time_keygen, 
            time_finalize=time_finalize
        )
        print(response.model_dump_json())

if __name__ == "__main__":
    params_filepath_ = sys.argv[1]
    with open(params_filepath_, 'r') as file:
        params_ = json.loads(file.read())
        params_ = F2mParams(**params_)
    main(params_)