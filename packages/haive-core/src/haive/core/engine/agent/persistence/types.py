from enum import Enum


class CheckpointerType(str, Enum):
    memory = "memory"
    postgres = "postgres"
    mongodb = "mongodb"
