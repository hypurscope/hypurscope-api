# Defi Validator ######
from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel, model_validator


class TVLEntry(BaseModel):
    date: str
    totalLiquidityUSD: float  # Ensure positive numbers

    @model_validator(mode="before")
    def time_to_str(cls, data):
        raw_date = data.get("date")
        if isinstance(raw_date, int):
            dt = datetime.fromtimestamp(float(raw_date))
            format_time = dt.strftime("%y-%m-%d %H:%M")
            data["date"] = format_time
        return data


class TokenInUsd(BaseModel):
    date: str
    tokens: Dict[str, float]

    @model_validator(mode="before")
    def time_to_str(cls, data):
        raw_date = data.get("date")
        if isinstance(raw_date, int):
            dt = datetime.fromtimestamp(float(raw_date))
            format_time = dt.strftime("%y:%m:%d %H:%M")
            data["date"] = format_time
        return data


class ChainData(BaseModel):
    tvl: List[TVLEntry]
    tokensInUsd: List[TokenInUsd]


class Protocol(BaseModel):
    name: str
    currentChainTvls: Dict[str, float]
    chainTvls: Dict[str, ChainData]

    @model_validator(mode="after")
    def filter_chainTvls(self):
        keys_allowed = set(self.currentChainTvls)
        self.chainTvls = {k: v for k, v in self.chainTvls.items() if k in keys_allowed}
        return self

    class Config:
        str_to_float: True
        from_attributes: True


# Example
# example_data = {
#     "currentChainTvls": {"Hyperliquid L1": 607555974.80751},
#     "chainTvls": {
#         "Hyperliquid L1": {
#             "tvl": [
#                 {"date": 1733011200, "totalLiquidityUSD": 158295217.03339},
#                 {"date": 1733097600, "totalLiquidityUSD": 158514283.61405},
#             ],
#             "tokensInUsd": [
#                 {"date": 1733011200, "tokens": {"USDT": 158295217.03339}},
#                 {"date": 1733097600, "tokens": {"USDT": 158514283.61405}},
#                 {"date": 1733184000, "tokens": {"USDT": 164132183.22056}},
#             ],
#         },
#         "Ethereum": {
#             "tvl": [
#                 {"date": 1733011200, "totalLiquidityUSD": 158295217.03339},
#                 {"date": 1733097600, "totalLiquidityUSD": 158514283.61405},
#             ],
#             "tokensInUsd": [
#                 {"date": 1733011200, "tokens": {"USDT": 158295217.03339}},
#                 {"date": 1733097600, "tokens": {"USDT": 158514283.61405}},
#                 {"date": 1733184000, "tokens": {"USDT": 164132183.22056}},
#             ],
#         },
#         "Boronze": {
#             "tvl": [
#                 {"date": 1733011200, "totalLiquidityUSD": 158295217.03339},
#                 {"date": 1733097600, "totalLiquidityUSD": 158514283.61405},
#             ],
#             "tokensInUsd": [
#                 {"date": 1733011200, "tokens": {"USDT": 158295217.03339}},
#                 {"date": 1733097600, "tokens": {"USDT": 158514283.61405}},
#                 {"date": 1733184000, "tokens": {"USDT": 164132183.22056}},
#             ],
#         },
#     },
# }

# validated = DataModel.model_validate(example_data)
# print(validated)
