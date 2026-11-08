from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Email(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    from_: str = Field(alias="from")
    display_name: str
    subject: str
    body: str = Field(max_length=1_000_000)


class ScanResult(BaseModel):
    verdict: Literal["safe", "suspicious"]
    links: list[str]
    reasons: list[str]
