from datetime import datetime

from bson import ObjectId
from pydantic import EmailStr


def serialize_user(user: dict) -> dict[str, str | EmailStr | datetime | ObjectId | None]:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "hashed_password": user["hashedPassword"],
        "hashed_salt": user["hashedSalt"],
        "email_verification_code": user["emailVerificationCode"],
        "is_otp_enabled": user["isOtpEnabled"],
        "is_otp_verified": user["isOtpVerified"],
        "otp_base32": user["otpBase32"],
        "otp_auth_url": user["otpAuthUrl"],
        "is_verified": user["isVerified"],
        "is_logged_in": user["isLoggedIn"],
        "created_at": user["createdAt"],
        "updated_at": user["updatedAt"],
    }
