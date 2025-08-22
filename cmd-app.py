#!/usr/bin/env python3
import argparse
import sys
import requests

# url = "https://hyper-dev-p1ob.onrender.com/api"
url = "http://ec2-3-92-225-105.compute-1.amazonaws.com:8000/api"


def getUserData(id: str, start: str, end: str = None):
    params = {"start_time": start}
    if end:
        params["end_time"] = end

    r = requests.get(f"{url}/user-info/{id}", params=params)

    if r.status_code != 200:
        print(r.status_code)
        print("error")
        return None
    return r.json()


def getTokenholders(token: str):
    r = requests.get(f"{url}/get-holder/{token}")
    if r.status_code != 200:
        print(r.status_code)
        print("error")
        return None
    return r.json()


def getDefi():
    r = requests.get(f"{url}/defi")
    if r.status_code != 200:
        print(r.status_code)
        print("error")
        return None
    return r.json()


def getSpot():
    r = requests.get(f"{url}/get-spot-info")
    if r.status_code != 200:
        print(r.status_code)
        print("error")
        return None
    return r.json()


# ---- CLI ----
def main():
    parser = argparse.ArgumentParser(
        prog="mycli",
        description=("CLI app that provide info about a user wallet and hyperliquid."),
        usage=("./cmd-app.py arguments e.g ./cmd-app.py get_tokenHolders HYPE"),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand 1: get user data
    parser_userdata = subparsers.add_parser(
        "get_userdata",
        help="Gets user wallet data with id, start-time and optional end-time",
    )
    parser_userdata.add_argument("id", type=str, help="User wallet id")
    parser_userdata.add_argument(
        "start_time", type=str, help="start-time for fillings format 'yyyy-mm-dd HH:MM'"
    )
    parser_userdata.add_argument(
        "--end_time",
        default=None,
        type=str,
        help="end-time for fillings format 'yyyy-mm-dd HH:MM'",
    )

    # Subcommand 2: token holders
    parser_tokenholders = subparsers.add_parser(
        "get_tokenholders", help="Returns holders of a token"
    )
    parser_tokenholders.add_argument("token", type=str, help="a token name")

    # Subcommand 3: defi
    subparsers.add_parser("defi", help="Show hyperliquid defi info")

    # Subcommand 4: spotUSDC
    subparsers.add_parser("spotUSDC", help="Show spotUSDC")

    args = parser.parse_args()

    # Route to functions
    if args.command == "get_userdata":
        value = getUserData(args.id, args.start_time, args.end_time)
        print(value)
    elif args.command == "get_tokenholders":
        value = getTokenholders(args.token)
        print(value)
    elif args.command == "defi":
        value = getDefi()
        print(value)
    elif args.command == "spotUSDC":
        value = getSpot()
        print(value)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
