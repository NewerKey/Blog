from enum import Enum


class AlgorithmTypes(str, Enum):
    ARGON2 = "a2"
    BCRYPT = "bc"
    SHA256 = "256"
    SHA512 = "512"
