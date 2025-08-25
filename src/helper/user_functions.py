#!/usr/bin/env python

from fastapi import HTTPException
from hyperliquid.info import Info
from hyperliquid.utils import constants  # noqa: F401
from hyperliquid.utils.types import Meta, SpotMeta  # noqa: F401
import json  # noqa: F401
import time
from src.validator.user import (
    Balances,
    Delegations,
    FillsByTime,
    MarginSummary,
    # Rewards,
    StakingSummary,
)
from src.helper.time import to_epoch_millis
# start_time = int(time.time() * 1000) - (7 * 24 * 60 * 60 * 1000)  # 7 days ago


TEST_META: Meta = {"universe": []}
TEST_SPOT_META: SpotMeta = {"universe": [], "tokens": []}
info = Info(skip_ws=True, meta=TEST_META, spot_meta=TEST_SPOT_META)


# id = "0x03b9a189e2480d1e4c3007080b29f362282130fa"


def process_user_state(id: str):
    user_state = info.user_state(id)

    d = MarginSummary.model_validate(user_state)
    processed = {
        "Portfolio": {
            "Account Value": d.marginSummary.accountValue,
            "Net Volume of Trade": d.marginSummary.totalNtlPos,
            "Withdrawable Balance": d.withdrawable,
        },
        "Open Positions": [
            {
                "coin": p.position.coin,
                "size": p.position.szi,
                "leverage": f"{p.position.leverage.value}X",
                "entry_price": p.position.entryPx,
                "position_value": p.position.positionValue,
                "unrealized_pnl": p.position.unrealizedPnl,
                "cum_funding_all_time": p.position.cumFunding.allTime,
            }
            for p in d.assetPositions
        ],
    }
    return processed
    # print(processed)
    # json_string = user_state.model_dump_json(indent=4)
    # with open("process_user_state.json", "w") as f:
    #     f.write(json_string)


def spot_user_state(id: str):
    spot_user_state = info.spot_user_state(id)
    balances = Balances.model_validate(spot_user_state)
    modified_balances = [
        {
            "coin": b.coin,
            # "token": b.token,
            "total": b.total,
            "hold": b.hold,
            "entry": b.entryNtl,
        }
        for b in balances.balances
    ]
    return {"Holdings": modified_balances}
    # print(modified_balances)

    # with open("spot_user_state.json", "w") as f:
    #     json.dump(spot_user_state, f, indent=4)


def user_staking_summary(id: str):
    staking_summary = info.user_staking_summary(id)
    summary = StakingSummary.model_validate(staking_summary)
    modified_summary = {
        "delegated": summary.delegated,
        "undelegated": summary.undelegated,
        "total pending withdrawal": summary.totalPendingWithdrawal,
        "number of pending withdrawals": summary.nPendingWithdrawals,
    }
    return {"Staking summary": modified_summary}

    # print(modified_summary)
    # with open("summary.json", "w") as f:
    #     json.dump(staking_summary, f, indent=3)


# user_staking_summary()
def user_staking_delegations(id: str):
    staking_delegations = info.user_staking_delegations(id)
    delegations = Delegations.model_validate(staking_delegations).root

    modified_delegations = [
        {
            "validator": b.validator,
            "locked Until Time": b.lockedUntilTimestamp,
            "amount": b.amount,
        }
        for b in delegations
    ]
    return {"Delegations": modified_delegations}
    # print(modified_delegations)

    # with open("delegation.json", "w") as f:
    #     json.dump(staking_delegations, f, indent=4)


def user_fills_by_time(id: str, start_time: int, end_time: int = None):
    user_fills_by_time = info.user_fills_by_time(
        id, start_time=start_time, end_time=end_time
    )
    value = FillsByTime.model_validate(user_fills_by_time).root
    processed_data = [
        {
            "token name": v.coin,
            "entry price": v.px,
            "dir": v.dir,
            "transaction id": v.tid,
            "transaction hash": v.hash,
            "fee paid": v.fee,
            "closed PnL": v.closedPnl,
            "trade size": v.sz,
        }
        for v in value
    ]

    return {"Trading History": processed_data}
    # print(processed_data)
    # with open("user_fill.json", "w") as f:
    #     json.dump(user_fills_by_time, f, indent=4)


def get_mids():
    return info.all_mids()


def all_user_data(id: str, start_time: str, end_time: str = None):
    try:
        start_time = to_epoch_millis(start_time)
        # print(start_time)
        if end_time:
            end_time = to_epoch_millis(end_time)
            # print(end_time)
        user_state = process_user_state(id)
        user_spot_state = spot_user_state(id)
        staking_summary = user_staking_summary(id)
        delegation = user_staking_delegations(id)
        user_history = user_fills_by_time(id, start_time, end_time)
        mids = get_mids()

        user_data = {
            "user_state": user_state,
            "user_spot_state": user_spot_state,
            "staking_summary": staking_summary,
            "staking_delegation": delegation,
            "trading_history": user_history,
        }

        for h in user_data["user_spot_state"]["Holdings"]:
            price = mids.get(h["coin"])
            if price:
                price = float(price)
                h["value_in_usd"] = h["total"] * price
        return user_data
    except Exception as e:
        print(str(e))
        print(str(e))
        raise HTTPException(detail=str(e), status_code=400)


async def all_user_data_without_fills(id: str):
    try:
        user_state = process_user_state(id)
        user_spot_state = spot_user_state(id)
        staking_summary = user_staking_summary(id)
        delegation = user_staking_delegations(id)

        user_data = {
            "user_state": user_state,
            "user_spot_state": user_spot_state,
            "staking_summary": staking_summary,
            "staking_delegation": delegation,
        }
        return user_data
    except Exception as e:
        print(str(e))
        return None