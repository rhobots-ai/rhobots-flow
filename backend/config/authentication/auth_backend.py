import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import requests
from requests.exceptions import RequestException
from urllib.parse import urlparse
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from jwt.utils import base64url_decode

from config import settings

# Better Auth configuration
RHOBOTS_AUTH_EP = settings.RHOBOTS_AUTH_EP
RHOBOTS_AUTH_ISSUER = 'http://localhost:10000'
RHOBOTS_AUTH_JWKS_URL = f"{RHOBOTS_AUTH_EP}/api/auth/jwks"
RHOBOTS_AUTH_SIGNUP_URL = f"{RHOBOTS_AUTH_EP}/api/auth/sign-up/email"
RHOBOTS_AUTH_SIGNIN_URL = f"{RHOBOTS_AUTH_EP}/api/auth/sign-in/email"
RHOBOTS_AUTH_AUDIENCE = 'http://localhost:10000'

def get_jwks():
    """
    Fetch JWKS with a resilient fallback for Docker environments.
    Primary URL is built from RHOBOTS_AUTH_EP. If it points to localhost (unreachable from containers),
    we fallback to the docker-compose service name 'auth'.
    """
    urls = [RHOBOTS_AUTH_JWKS_URL]

    try:
        parsed = urlparse(RHOBOTS_AUTH_EP)
        if parsed.hostname in {"localhost", "127.0.0.1", "0.0.0.0", None}:
            # Fallback to docker service name
            urls.append("http://auth:10000/api/auth/jwks")
    except Exception:
        # Best-effort; ignore parse issues
        urls.append("http://auth:10000/api/auth/jwks")

    last_exc = None
    for u in urls:
        try:
            resp = requests.get(u, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except RequestException as e:
            last_exc = e
            continue

    # If all attempts failed, raise a consolidated error
    raise Exception(f"Unable to fetch JWKS from any endpoint. Last error: {last_exc}")

def get_signing_key(jwks, token):
    unverified_header = jwt.get_unverified_header(token)
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            if key["kty"] == "OKP" and key["crv"] == "Ed25519":  # EdDSA key
                x = base64url_decode(key["x"])
                return Ed25519PublicKey.from_public_bytes(x)
            else:
                raise InvalidTokenError(f"Unsupported key type: {key['kty']}/{key.get('crv')}")
    raise InvalidTokenError("No matching key found in JWKS")


def verify_better_auth_token(token):
    try:
        # 1. Get JWKS
        jwks = get_jwks()

        # 2. Get the appropriate signing key
        signing_key = get_signing_key(jwks, token)

        # 3. Verify the token
        payload = jwt.decode(
            token,
            key=signing_key,
            algorithms=["EdDSA"],  # Better Auth uses RS256
            audience=RHOBOTS_AUTH_AUDIENCE,
            issuer=RHOBOTS_AUTH_ISSUER,
            options={
                "require": ["exp", "iat", "aud", "iss"],
                "verify_signature": True,
                "verify_aud": True,
                "verify_iss": True,
                "verify_exp": True,
            }
        )

        return payload

    except ExpiredSignatureError:
        return {"error": "Token expired"}
    except InvalidTokenError as e:
        return {"error": f"Invalid token: {str(e)}"}
    except Exception as e:
        return {"error": f"Verification failed: {str(e)}"}
