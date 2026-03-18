"""
DeFi TVL Overview — CLI
Fetches TVL data from the DefiLlama API (free, no auth).
"""

import argparse
import sys
import requests


BASE_URL = "https://api.llama.fi"


def fmt_usd(value):
    if value is None:
        return "N/A"
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"${value / 1_000:.2f}K"
    return f"${value:.2f}"


def cmd_protocols(args):
    resp = requests.get(f"{BASE_URL}/protocols", timeout=30)
    resp.raise_for_status()
    protocols = resp.json()

    # Filter by category if specified
    if args.category:
        protocols = [p for p in protocols if (p.get("category") or "").lower() == args.category.lower()]

    protocols.sort(key=lambda p: p.get("tvl") or 0, reverse=True)
    protocols = protocols[: args.limit]

    print(f"{'Rank':<5} {'Protocol':<28} {'Category':<15} {'Chain':<15} {'TVL':>14}")
    print("-" * 80)
    for i, p in enumerate(protocols, 1):
        print(
            f"{i:<5} {p.get('name', '?'):<28}"
            f" {(p.get('category') or '?'):<15}"
            f" {(p.get('chain') or '?'):<15}"
            f" {fmt_usd(p.get('tvl')):>14}"
        )


def cmd_protocol(args):
    resp = requests.get(f"{BASE_URL}/protocol/{args.slug}", timeout=15)
    resp.raise_for_status()
    data = resp.json()

    print(f"Protocol:    {data.get('name')}")
    print(f"Symbol:      {data.get('symbol')}")
    print(f"Description: {data.get('description', '')[:120]}")
    print(f"URL:         {data.get('url')}")
    print(f"Twitter:     @{data.get('twitter')}" if data.get("twitter") else "")

    print("\nCurrent TVL by chain:")
    chain_tvls = data.get("currentChainTvls", {})
    for chain, tvl in sorted(chain_tvls.items(), key=lambda x: x[1], reverse=True):
        if "-" not in chain:  # skip borrowed/staking sub-keys
            print(f"  {chain:<20} {fmt_usd(tvl)}")

    tvl_series = data.get("tvl", [])
    if tvl_series:
        latest = tvl_series[-1]
        print(f"\nLatest global TVL: {fmt_usd(latest.get('totalLiquidityUSD'))}")


def cmd_chains(args):
    resp = requests.get(f"{BASE_URL}/chains", timeout=15)
    resp.raise_for_status()
    chains = resp.json()

    chains.sort(key=lambda c: c.get("tvl") or 0, reverse=True)
    chains = chains[: args.limit]

    print(f"{'Rank':<5} {'Chain':<20} {'Token':<8} {'TVL':>14}")
    print("-" * 52)
    for i, c in enumerate(chains, 1):
        print(
            f"{i:<5} {c.get('name', '?'):<20}"
            f" {(c.get('tokenSymbol') or '?'):<8}"
            f" {fmt_usd(c.get('tvl')):>14}"
        )


def cmd_global(args):
    resp = requests.get(f"{BASE_URL}/charts", timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if not data:
        print("No data.")
        return

    recent = data[-args.days :]
    max_tvl = max(d["totalLiquidityUSD"] for d in data)
    latest = data[-1]

    print(f"Global DeFi TVL — last {args.days} days")
    print(f"Current: {fmt_usd(latest['totalLiquidityUSD'])}")
    print(f"All-time high: {fmt_usd(max_tvl)}")
    print(f"\n{'Date':<12} {'TVL':>14}")
    print("-" * 28)
    import datetime
    for d in recent:
        date_str = datetime.datetime.utcfromtimestamp(int(d["date"])).strftime("%Y-%m-%d")
        print(f"{date_str:<12} {fmt_usd(d['totalLiquidityUSD']):>14}")


def main():
    parser = argparse.ArgumentParser(description="Query DeFi TVL data via DefiLlama API.")
    sub = parser.add_subparsers(dest="command")

    p_protocols = sub.add_parser("protocols", help="List top protocols by TVL")
    p_protocols.add_argument("--limit", type=int, default=20, help="Number of results (default: 20)")
    p_protocols.add_argument("--category", help="Filter by category (e.g. Lending, DEX, CEX)")
    p_protocols.set_defaults(func=cmd_protocols)

    p_protocol = sub.add_parser("protocol", help="Get TVL details for a specific protocol")
    p_protocol.add_argument("slug", help="Protocol slug (e.g. aave, uniswap, curve)")
    p_protocol.set_defaults(func=cmd_protocol)

    p_chains = sub.add_parser("chains", help="List chains by TVL")
    p_chains.add_argument("--limit", type=int, default=20, help="Number of results (default: 20)")
    p_chains.set_defaults(func=cmd_chains)

    p_global = sub.add_parser("global", help="Show global DeFi TVL chart")
    p_global.add_argument("--days", type=int, default=30, help="Number of recent days to show (default: 30)")
    p_global.set_defaults(func=cmd_global)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        # Default: list top protocols
        args.func = cmd_protocols
        args.limit = 10
        args.category = None

    try:
        args.func(args)
    except requests.HTTPError as e:
        print(f"HTTP error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
