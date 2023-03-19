from enum import Enum


class AppEnvironment(str, Enum):
    PRODUCTION = "PROD"
    DEVELOPMENT = "DEV"
    TESTING = "Test"
