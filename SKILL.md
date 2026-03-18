---
title: DeFi TVL Overview
description: |
  Query Total Value Locked (TVL) data across DeFi protocols and blockchains using the DefiLlama API.
  Supports protocol listings, TVL history, global DeFi charts, and per-chain TVL breakdowns.
metadata:
  author: Bob-QoQ
  version: "1.0"
license: MIT
---

# DeFi TVL Overview

Query Total Value Locked (TVL) data across DeFi protocols and blockchains using the DefiLlama API. This skill enables AI agents to retrieve real-time and historical TVL metrics for protocols, chains, and the global DeFi ecosystem.

## API Base URL

```
https://api.llama.fi
```

No authentication required. All endpoints are public and free.

---

## Endpoints

### 1. List All Protocols

Returns all tracked DeFi protocols with their current TVL and metadata.

```
GET https://api.llama.fi/protocols
```

**Parameters:** None

**Response fields (per protocol):**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Protocol ID |
| `name` | string | Protocol display name |
| `slug` | string | URL-safe protocol identifier (use for `/protocol/{name}`) |
| `symbol` | string | Native token symbol |
| `chain` | string | Primary chain or "Multi-Chain" |
| `chains` | array | All chains the protocol is deployed on |
| `category` | string | Protocol category (e.g., "Lending", "DEX", "CEX") |
| `tvl` | number | Current TVL in USD |
| `chainTvls` | object | TVL breakdown by chain |
| `description` | string | Protocol description |
| `url` | string | Protocol website |
| `logo` | string | Logo image URL |
| `twitter` | string | Twitter handle |
| `gecko_id` | string | CoinGecko token ID |
| `cmcId` | string | CoinMarketCap token ID |
| `listedAt` | number | Unix timestamp when listed |

**Example request:**

```http
GET https://api.llama.fi/protocols
```

**Example response (truncated):**

```json
[
  {
    "id": "2269",
    "name": "Binance CEX",
    "symbol": "BNB",
    "chain": "Multi-Chain",
    "category": "CEX",
    "slug": "binance-cex",
    "tvl": 157216522942.88,
    "chains": ["Ethereum", "Bitcoin", "Binance", "Solana"],
    "chainTvls": {
      "Ethereum": 68440975139.58,
      "Bitcoin": 41918417530.54,
      "Binance": 25745790262.02
    },
    "description": "Binance is a cryptocurrency exchange...",
    "url": "https://www.binance.com",
    "twitter": "binance",
    "gecko_id": null,
    "cmcId": null,
    "listedAt": 1668170565
  }
]
```

---

### 2. Get Protocol TVL History

Returns detailed TVL history and current chain breakdown for a specific protocol.

```
GET https://api.llama.fi/protocol/{name}
```

**Path parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Protocol slug (e.g., `aave`, `uniswap`, `curve`). Use the `slug` field from `/protocols`. |

**Response fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Protocol ID |
| `name` | string | Protocol display name |
| `description` | string | Protocol description |
| `chains` | array | All chains deployed on |
| `symbol` | string | Token symbol |
| `currentChainTvls` | object | Current TVL per chain (including borrowed, staking, pool2 breakdowns) |
| `chainTvls` | object | Historical daily TVL per chain — each key maps to `{ tvl: [{ date, totalLiquidityUSD }] }` |
| `tvl` | array | Global daily TVL — array of `{ date: unixTimestamp, totalLiquidityUSD: number }` |
| `gecko_id` | string | CoinGecko ID |
| `twitter` | string | Twitter handle |
| `url` | string | Protocol website |

**Example request:**

```http
GET https://api.llama.fi/protocol/aave
```

**Example response (truncated):**

```json
{
  "id": "parent#aave",
  "name": "Aave",
  "description": "Aave is an Open Source and Non-Custodial protocol to earn interest on deposits and borrow assets",
  "chains": [],
  "symbol": "AAVE",
  "currentChainTvls": {
    "Ethereum": 22587066894,
    "Ethereum-borrowed": 14084974273,
    "Ethereum-staking": 361285746,
    "Polygon": 178859020,
    "Avalanche": 446708508,
    "Arbitrum": 807687616,
    "Base": 788661679,
    "borrowed": 17984456297,
    "staking": 361285746
  },
  "chainTvls": {
    "Ethereum": {
      "tvl": [
        { "date": 1606953600, "totalLiquidityUSD": 244094753 },
        { "date": 1607040000, "totalLiquidityUSD": 243189473 }
      ]
    }
  },
  "tvl": [
    { "date": 1606953600, "totalLiquidityUSD": 244094753 }
  ],
  "gecko_id": "aave",
  "twitter": "aave",
  "url": "https://aave.com"
}
```

**Common protocol slugs:**

| Protocol | Slug |
|----------|------|
| Aave | `aave` |
| Uniswap | `uniswap` |
| Curve | `curve` |
| MakerDAO | `makerdao` |
| Lido | `lido` |
| Compound | `compound` |

---

### 3. Global DeFi TVL Chart

Returns the daily total TVL across all DeFi protocols over time.

```
GET https://api.llama.fi/charts
```

**Parameters:** None

**Response:** Array of daily data points.

| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Unix timestamp (as string) |
| `totalLiquidityUSD` | number | Total DeFi TVL in USD for that day |

**Example request:**

```http
GET https://api.llama.fi/charts
```

**Example response (truncated):**

```json
[
  { "date": "1614643200", "totalLiquidityUSD": 38500000000 },
  { "date": "1614729600", "totalLiquidityUSD": 40200000000 },
  { "date": "1614816000", "totalLiquidityUSD": 41800000000 }
]
```

---

### 4. TVL by Blockchain

Returns current TVL for each blockchain tracked by DefiLlama.

```
GET https://api.llama.fi/chains
```

**Parameters:** None

**Response fields (per chain):**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Chain display name |
| `tvl` | number | Current TVL in USD |
| `tokenSymbol` | string | Native token symbol |
| `gecko_id` | string | CoinGecko ID for the native token |
| `cmcId` | string | CoinMarketCap ID |
| `chainId` | number | EVM chain ID (if applicable) |

**Example request:**

```http
GET https://api.llama.fi/chains
```

**Example response (truncated):**

```json
[
  {
    "name": "Binance",
    "tvl": 7509293141.26,
    "tokenSymbol": "BNB",
    "gecko_id": "binancecoin",
    "cmcId": "1839",
    "chainId": 56
  },
  {
    "name": "Mantle",
    "tvl": 1006835525.01,
    "tokenSymbol": "MNT",
    "gecko_id": "mantle",
    "cmcId": "27075",
    "chainId": 5000
  }
]
```

---

## Usage Notes

### TVL Breakdowns

The `currentChainTvls` and `chainTvls` fields in protocol responses include special suffixed keys:

| Suffix | Meaning |
|--------|---------|
| *(none)* | Core collateral / deposited TVL |
| `-borrowed` | Borrowed assets (counted separately from deposited) |
| `-staking` | Tokens staked in protocol governance |
| `-pool2` | Liquidity in LP pools containing the protocol's own token |

### Sorting Protocols by TVL

The `/protocols` endpoint returns all protocols unsorted. Sort client-side by the `tvl` field to find the largest protocols.

### Data Freshness

- TVL data updates approximately every 24 hours for daily chart points
- Current TVL values (`tvl` field on protocol objects) refresh more frequently (typically every few hours)

### Rate Limits

DefiLlama does not publish explicit rate limits for these free public endpoints. Best practices:
- Avoid polling more than once per minute for the same endpoint
- The `/protocols` response is large (~2–5 MB); cache it client-side when possible
- For high-frequency use, consider caching responses for at least 5 minutes

### Error Handling

| HTTP Status | Meaning |
|-------------|---------|
| `200` | Success |
| `404` | Protocol not found (check slug spelling) |
| `429` | Rate limited — back off and retry |
| `500` | Upstream error — retry with exponential backoff |

---

## Example Agent Workflows

### Find the top 5 DeFi protocols by TVL

```
1. GET https://api.llama.fi/protocols
2. Sort results by `tvl` descending
3. Return top 5 with name, category, chain, and tvl
```

### Get Aave's TVL on Ethereum today

```
1. GET https://api.llama.fi/protocol/aave
2. Read currentChainTvls["Ethereum"]
```

### Compare TVL across L2 chains

```
1. GET https://api.llama.fi/chains
2. Filter for Arbitrum, Optimism, Base, zkSync Era, Scroll
3. Sort by tvl descending
```

### Check if DeFi TVL is at an all-time high

```
1. GET https://api.llama.fi/charts
2. Find the max totalLiquidityUSD across all dates
3. Compare to the most recent date's value
```
