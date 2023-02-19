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
