from src.services.security.password.algorithms import (
    Argon2Algorithm,
    BCryptAlgorithm,
    SHA256Algorithm,
    SHA512Algorithm,
)

HashingAlgorithm = Argon2Algorithm | BCryptAlgorithm | SHA256Algorithm | SHA512Algorithm
