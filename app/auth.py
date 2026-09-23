import hmac
import os
from fastapi import Cookie, HTTPException
from itsdangerous import BadSignature, URLSafeTimedSerializer

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Cambiar-Esta-Clave-2026")
SESSION_SECRET = os.getenv("SESSION_SECRET", "dev-secret-change-me")
serializer = URLSafeTimedSerializer(SESSION_SECRET, salt="cotecmar-admin")

def verify_password(value: str) -> bool:
    return hmac.compare_digest(value or "", ADMIN_PASSWORD)

def create_session_token() -> str:
    return serializer.dumps({"role": "admin"})

def require_admin(cotecmar_session: str | None = Cookie(default=None)):
    if not cotecmar_session:
        raise HTTPException(status_code=401, detail="Sesión requerida")
    try:
        data = serializer.loads(cotecmar_session, max_age=60 * 60 * 12)
    except BadSignature:
        raise HTTPException(status_code=401, detail="Sesión inválida")
    if data.get("role") != "admin":
        raise HTTPException(status_code=403, detail="No autorizado")
    return True
