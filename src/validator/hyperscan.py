from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel, Field, RootModel, model_validator


class TokenHolders(BaseModel):
    token: str
    lastUpdate: str
    holders: Dict[str, float]

    @model_validator(mode="before")
    def time_to_str(cls, data):
        raw_date = data.get("lastUpdate")
        if isinstance(raw_date, int):
            dt = datetime.fromtimestamp(float(raw_date))
            format_time = dt.strftime("%y-%m-%d %H:%M")
            data["lastUpdate"] = format_time
        return data


class Spot(BaseModel):
    lastUpdate: int
    totalSpotUSDC: float
    holdersCount: int
    hip_2: float = Field(alias="HIP-2")


class Spots(RootModel[List[Spot]]):
    pass
