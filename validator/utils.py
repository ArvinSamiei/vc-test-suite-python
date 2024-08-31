import json
from enum import Enum

VERIFIABLE_CREDENTIAL = 'VerifiableCredential'
VERIFIABLE_PRESENTATION = 'VerifiablePresentation'
VC_CONTEXT_2 = 'https://www.w3.org/ns/credentials/v2'
VC_CONTEXT_1 = 'https://www.w3.org/2018/credentials/v1'
DATE_TIME_TYPE1 = 'xsd:dateTime'
DATE_TIME_TYPE2 = 'http://www.w3.org/2001/XMLSchema#dateTime'
BIT_STRING_STATUS_URL = 'https://www.w3.org/ns/credentials/status#BitstringStatusListCredential'


def get_json_context(version):
    if version == 1:
        file_name = 'v1.json'
    else:
        file_name = 'v2.json'
    with open('v2.json', 'r') as file:
        context = file.read()
    return json.loads(context)


required_attributes = {
    VERIFIABLE_CREDENTIAL: ["credentialSubject", "issuer"],
    "JsonSchema": ["id", "type", "jsonSchema"],
    "BitstringStatusList": ["id", "type", "statusPurpose", "encodedList", "ttl", "statusReference", "statusSize"],
    "BitstringStatusListEntry": ["id", "type", "statusPurpose", "statusListIndex", "statusListCredential"],
    "DataIntegrityProof": ["id", "type", "challenge", "created", "domain", "expires", "nonce", "previousProof",
                           "proofPurpose", "cryptosuite", "proofValue", "verificationMethod"],
    "cnf": ["kid", "jwk"],
    "credentialSchema": ["type", "id"],
    "credentialStatus": ["type"],
    "evidence": ["type"],
    "termsOfUse": ["type"],
    "proof": ["type"],
    "refreshService": ["id", "type"]
}


class Restriction(Enum):
    MustBeUrl = 1


special_reqs = {
    "credentialStatus": {
        "type": [Restriction.MustBeUrl]
    }
}
