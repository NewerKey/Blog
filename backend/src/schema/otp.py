from src.schema.base import BaseSchema
from src.schema.user import UserResponseSchema


class OTPBaseSchema(BaseSchema):
    user_id: str


class OTPwithUserResponseSchema(BaseSchema):
    verified_2fa_user: UserResponseSchema


class OTPRequestSchema(OTPBaseSchema):
    code: str | None = None


class OTPDataGenerationSchema(OTPBaseSchema):
    otp_base32: str
    otp_auth_url: str


class OTPDataDisableFeatureSchema(OTPBaseSchema):
    is_otp_enabled: bool


class OTPDataVerificationSchema(OTPDataDisableFeatureSchema):
    is_otp_verified: bool


class OTPGenerationResponseSchema(OTPDataGenerationSchema):
    pass


class OTPDisableFeatureResponseSchema(OTPDataDisableFeatureSchema, OTPwithUserResponseSchema):
    pass


class OTPVerificationResponseSchema(OTPDataVerificationSchema, OTPwithUserResponseSchema):
    pass


class OTPValidationResponseSchema(OTPBaseSchema):
    is_otp_valid: bool
