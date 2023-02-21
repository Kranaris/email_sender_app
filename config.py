from dataclasses import dataclass

from environs import Env


@dataclass
class Profile:
    FROM_E_MAIL: str
    PASS: str
    TO_E_MAIL: str
    SUBJECT: str


@dataclass
class Config:
    profile: Profile


def load_config(path: str | None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(profile=Profile(FROM_E_MAIL=env('FROM_E_MAIL'),
                                  PASS=env('PASS'),
                                  TO_E_MAIL=env('TO_E_MAIL'),
                                  SUBJECT=env('SUBJECT')))


def write_config(FROM_E_MAIL, PASS, TO_E_MAIL, SUBJECT):
    with open(".env", "w", encoding="utf-8") as env:
        env.write(f"FROM_E_MAIL = {FROM_E_MAIL}\n")
        env.write(f"PASS = {PASS}\n")
        env.write(f"TO_E_MAIL = {TO_E_MAIL}\n")
        env.write(f"SUBJECT = {SUBJECT}\n")
