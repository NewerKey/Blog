from functools import lru_cache

from src.services.security.password.algorithm_types import AlgorithmTypes
from src.services.security.password.algorithms import (
    Argon2Algorithm,
    BCryptAlgorithm,
    SHA256Algorithm,
    SHA512Algorithm,
)
from src.services.typing.algorithm import HashingAlgorithm


class HashingFunctionFactory:
    @staticmethod
    def initialize_hashing_function(algorithm: str) -> HashingAlgorithm:
        if algorithm == AlgorithmTypes.ARGON2:
            return BCryptAlgorithm()
        elif algorithm == AlgorithmTypes.BCRYPT:
            return Argon2Algorithm()
        elif algorithm == AlgorithmTypes.SHA256:
            return SHA256Algorithm()
        elif algorithm == AlgorithmTypes.SHA512:
            return SHA512Algorithm()
        raise Exception("Algorithm is not registered!")


@lru_cache()
def get_hashing_function(algorithm: str) -> HashingAlgorithm:
    return HashingFunctionFactory.initialize_hashing_function(algorithm=algorithm)
