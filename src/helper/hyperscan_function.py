import requests
from src.validator.hyperscan import Spots, TokenHolders
from src.config import hypurrsca_url


async def get_token_holders(token: str):
    limit = 2000
    r = requests.get(f"{hypurrsca_url}/holdersWithLimit/{token}/{limit}")
    holders = TokenHolders.model_validate(r.json())
    return holders


async def get_spot_in_usdc():
    r = requests.get(f"{hypurrsca_url}/spotUSDC")
    spots = Spots.model_validate(r.json())
    return spots.root
