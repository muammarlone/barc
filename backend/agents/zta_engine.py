import secrets
from pydantic import BaseModel
from datetime import datetime, timedelta

class SecurityToken(BaseModel):
    token_id: str
    identity: str
    scope: str
    expires_at: str

class ZTAEngine:
    def __init__(self):
        self.active_tokens = {}

    def issue_contextual_token(self, identity: str, scope: str) -> SecurityToken:
        # Least-privilege token generation
        token_id = f"ZTA-{secrets.token_hex(8).upper()}"
        expiry = (datetime.now() + timedelta(minutes=15)).isoformat()
        token = SecurityToken(
            token_id=token_id,
            identity=identity,
            scope=scope,
            expires_at=expiry
        )
        self.active_tokens[token_id] = token
        return token

    def verify_token(self, token_id: str, required_scope: str) -> bool:
        token = self.active_tokens.get(token_id)
        if not token:
            return False
        # Check expiry and scope
        if datetime.fromisoformat(token.expires_at) < datetime.now():
            return False
        return token.scope == required_scope
