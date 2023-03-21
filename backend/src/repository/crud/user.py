from datetime import datetime

from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from pymongo.collection import ReturnDocument

from src.repository.crud.base import BaseCRUDRepository
from src.repository.serializers.user import serialize_user
from src.schema.user import UserBaseSchema
from src.services.security.password.manager import pwd_manager


class UserCRUDRepository(BaseCRUDRepository):
    def __init__(self, collection_name) -> None:
        super().__init__(collection_name)

    async def create(
        self, user_data: dict[str, str | EmailStr]
    ) -> dict[str, str | EmailStr | datetime | ObjectId | None]:
        hashed_salt, hashed_password = pwd_manager.generate_double_layered_password(password=user_data["password"])
        new_user = jsonable_encoder(
            obj=UserBaseSchema(
                username=user_data["username"],
                email=user_data["email"],  # type: ignore
                hashed_password=hashed_password,
                hashed_salt=hashed_salt,
                email_verification_code=user_data["emailVerificationCode"],
            )
        )
        registered_user = await self.collection.insert_one(new_user)  # type: ignore
        db_user = await self.collection.find_one({"_id": registered_user.inserted_id})  # type: ignore
        return serialize_user(user=db_user)

    async def read_all(self) -> list[dict[str, str | EmailStr | datetime | ObjectId | None]]:
        db_users = []
        async for db_user in await self.collection.find():  # type: ignore
            db_users.append(serialize_user(db_user))
        return db_users

    async def is_username_taken(self, username: str) -> bool:
        username = await self.collection.find_one({"username": username})  # type: ignore
        if not username:
            return False
        return True

    async def is_email_taken(self, email: str) -> bool:
        email = await self.collection.find_one({"email": email})  # type: ignore
        if not email:
            return False
        return True

    async def is_password_verified(self, hashed_salt: str, password: str, hashed_password: str) -> bool:
        return pwd_manager.is_hashed_password_verified(hashed_salt=hashed_salt, password=password, hashed_password=hashed_password)  # type: ignore

    async def is_password_matched(self, password: str, repeated_password: str) -> bool:
        if password != repeated_password:  # type: ignore
            return False
        return True

    async def read_user_by_id(self, id: str) -> dict[str, str | EmailStr | datetime | ObjectId | None]:
        db_user = await self.collection.find_one({"_id": id})  # type: ignore
        if not db_user:
            raise Exception(f"User with ID `{id}` doesn't exist!")
        return serialize_user(user=db_user)

    async def read_user_by_username(self, username: str) -> dict[str, str | EmailStr | datetime | ObjectId | None]:
        db_user = await self.collection.find_one({"username": username})  # type: ignore
        if not db_user:
            raise Exception(f"User with usesrname `{username}` doesn't exist!")
        return serialize_user(user=db_user)

    async def read_user_in_login(
        self, user_data: dict[str, str]
    ) -> dict[str, str | EmailStr | datetime | ObjectId | None]:
        db_user = await self.collection.find_one({"username": user_data["username"]})  # type: ignore
        if not db_user:
            raise Exception(f"User with username `{user_data['username']}` is not found!")
        is_correct_password = await self.is_password_verified(
            hashed_salt=db_user["hashedSalt"],  # type: ignore
            password=user_data["password"],  # type: ignore
            hashed_password=db_user["hashedPassword"],  # type: ignore
        )
        if not is_correct_password:
            raise Exception("Incorrect Password!")
        update_user = await self.collection.update_one(
            {"_id": db_user["_id"]},  # type: ignore
            {"$set": {"isLoggedIn": True, "updatedAt": datetime.utcnow()}},
        )  # type: ignore
        logged_in_user = await self.collection.find_one(update_user.upserted_id)  # type: ignore
        return serialize_user(user=logged_in_user)

    async def update_user_with_otp_details(
        self, otp_data: dict[str, str | bool]
    ) -> dict[str, str | EmailStr | datetime | ObjectId | None]:
        db_user = await self.collection.find_one({"_id": otp_data["userId"]})  # type: ignore
        if not db_user:
            raise Exception(f"User with id `{otp_data['userId']}` is not found!")
        otp_data.pop("userId")
        update_user = await self.collection.update_one(
            {"_id": db_user["_id"]}, {"$set": otp_data}  # type: ignore
        )  # type: ignore
        updated_user = await self.collection.find_one(update_user.upserted_id)  # type: ignore
        return serialize_user(user=updated_user)  # type: ignore

    async def read_user_in_email_verification(
        self, verification_code: str | None
    ) -> dict[str, str | EmailStr | datetime | ObjectId | None]:
        db_user = await self.collection.find_one({"emailVerificationCode": verification_code})  # type: ignore
        if not db_user:
            raise Exception(f"User with email verification code `{verification_code}` is not found!")
        update_user = await self.collection.update_one(
            {"_id": db_user["_id"]},  # type: ignore
            {"$set": {"isVerified": True, "updatedAt": datetime.utcnow()}},
        )  # type: ignore
        logged_in_user = await self.collection.find_one(update_user.upserted_id)  # type: ignore
        return serialize_user(user=logged_in_user)  # type: ignore

    async def update_user_before_logout(self, id: str) -> dict[str, str | EmailStr | datetime | ObjectId | None]:
        db_user = await self.collection.find_one({"_id": id})  # type: ignore
        if not db_user:
            raise Exception(f"User with id `{id}` is not found!")
        update_user = await self.collection.update_one(
            {"_id": db_user["_id"]}, {"$set": {"isLoggedIn": False, "isOtpVerified": False}}  # type: ignore
        )  # type: ignore
        updated_user = await self.collection.find_one(update_user.upserted_id)  # type: ignore
        return serialize_user(user=updated_user)  # type: ignore

    async def delete(self, id: str) -> bool:
        db_user = await self.collection.find_one({"_id": ObjectId(id)})  # type: ignore
        if not db_user:
            raise Exception(f"User with ID `{id}` is not found!")

        await self.collection.delete_one({"_id": ObjectId(id)})  # type: ignore
        return True
