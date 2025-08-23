from typing import List, Optional  # noqa: F401
from pydantic import BaseModel, EmailStr, RootModel


class TrackData(BaseModel):
    id: str
    email: EmailStr


# UserState Validator ####
class Summary(BaseModel):
    accountValue: float
    totalNtlPos: float


class Leverage(BaseModel):
    value: int


class CummulativeFunding(BaseModel):
    allTime: float


class Position(BaseModel):
    coin: str
    szi: float
    leverage: Leverage
    entryPx: float
    positionValue: float
    unrealizedPnl: float
    liquidityPx: float = None
    cumFunding: CummulativeFunding


class Asset(BaseModel):
    position: Position


class MarginSummary(BaseModel):
    marginSummary: Summary
    withdrawable: float
    assetPositions: List[Asset]

    class Config:
        str_to_float = True
        from_attributes = True


# Defi Validator ######
class Protocol(BaseModel):
    id: str
    name: str
    symbol: str
    chains: List[str] = []
    url: str
    description: str
    referralUrl: str = None
    logo: str


# Userspot Validator ###
class Coin(BaseModel):
    coin: str
    # token: int
    total: float
    hold: float
    entryNtl: float


class Balances(BaseModel):
    balances: List[Coin]

    class Config:
        str_to_float: True
        from_attributes: True


# Staking Summary Validator ####
class StakingSummary(BaseModel):
    delegated: float
    undelegated: float
    totalPendingWithdrawal: float
    nPendingWithdrawals: int

    class Config:
        str_to_float: True
        from_attributes: True


class Delegation(BaseModel):
    validator: str
    amount: float
    lockedUntilTimestamp: int


class Delegations(RootModel[List[Delegation]]):
    pass

    class Config:
        str_to_float: True
        from_attributes: True


class Reward(BaseModel):
    time: int
    source: str
    totalAmount: float


class Rewards(RootModel[List[Reward]]):
    pass

    class Config:
        str_to_float: True
        from_attributes: True


class FillByTime(BaseModel):
    coin: str
    px: float
    sz: float
    dir: str
    hash: str
    tid: int
    fee: float
    closedPnl: float


class FillsByTime(RootModel[List[FillByTime]]):
    pass

    class Config:
        str_to_float: True
        from_attributes: True
