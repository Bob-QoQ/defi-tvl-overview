# DeFi TVL Overview

Query Total Value Locked across DeFi protocols, chains, and the global ecosystem.

## Quick Start

```bash
pip install -r requirements.txt
python main.py --help
```

```
usage: main.py [-h] {protocols,protocol,chains,global} ...

Query DeFi TVL data via DefiLlama API.

positional arguments:
  {protocols,protocol,chains,global}
    protocols           List top protocols by TVL
    protocol            Get TVL details for a specific protocol
    chains              List chains by TVL
    global              Show global DeFi TVL chart
```

## Example Output

```
Rank  Protocol                     Category        Chain                      TVL
--------------------------------------------------------------------------------
1     Binance CEX                  CEX             Multi-Chain           $157.03B
2     Aave V3                      Lending         Multi-Chain            $26.21B
3     Lido                         Liquid Staking  Multi-Chain            $21.36B
4     OKX                          CEX             Multi-Chain            $18.82B
5     Bitfinex                     CEX             Multi-Chain            $17.48B
6     Bybit                        CEX             Multi-Chain            $16.29B
7     SSV Network                  Staking Pool    Ethereum               $15.99B
8     Robinhood                    CEX             Multi-Chain            $13.51B
9     EigenCloud                   Restaking       Ethereum               $10.15B
10    WBTC                         Bridge          Bitcoin                 $8.63B
```

**Data source:** [DefiLlama API](https://api.llama.fi) — free, no auth required.
