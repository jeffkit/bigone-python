# Welcome to BigOne-Python

An unofficial Python implementation of the [latest Open API](https://big.one/api/v2/) for [big.one](https://big.one) exchange.

## install

```bash
pip install bigone
```

## usage

for example:

```python
>>> api = 'your-api'
>>> secret = 'your-secret'
>>> from bigone.client import BigOneClient
>>> cli = BigOneClient(api, secret)
>>> markets = cli.get_markets()
>>> market = markets[0]
>>> market
<Market (uuid=d2185614-50c3-4588-b146-b8afe7534da6,quoteScale=8,quoteAsset=<Quoteasset (uuid=0df9c3c3-255a-46d7-ab82-dedae169fba9,symbol=BTC,name=Bitcoin)>,name=BTG-BTC,baseScale=4,baseAsset=<Baseasset (uuid=5df3b155-80f5-4f5a-87f6-a92950f0d0ff,symbol=BTG,name=Bitcoin Gold)>)>
>>> market.name
'BTG-BTC'
>>> len(markets)
112
```
if you don't like the python object-like style data accessing, you can simply use the raw response, they are just dict and list objects:

```python
>>> cli = BigOneClient(api, secret, raw_response=True)
>>> markets = cli.get_markets()
>>> market = markets[0]
>>> market
{'uuid': 'd2185614-50c3-4588-b146-b8afe7534da6', 'quoteScale': 8, 'quoteAsset': {'uuid': '0df9c3c3-255a-46d7-ab82-dedae169fba9', 'symbol': 'BTC', 'name': 'Bitcoin'}, 'name': 'BTG-BTC', 'baseScale': 4, 'baseAsset': {'uuid': '5df3b155-80f5-4f5a-87f6-a92950f0d0ff', 'symbol': 'BTG', 'name': 'Bitcoin Gold'}}
```

## API List

### Public API

#### ping

```python
>>> cli.ping()
<Bigobject (timestamp: 1529986424481114000)>
```

#### get_all_tickers

```python
cli.get_all_tickers()
```

#### get_ticker

```python
cli.get_ticker('ETH-BTC')
```

#### get_order_book

```python
cli.get_order_book('ETH-BTC')
```

#### get_trades

```python
cli.get_trades('ETH-BTC')
```

#### get_markets

```python
cli.get_markets()
```

### private API

#### account_info

```python
cli.account_info()
```

#### get_orders

```python
cli.get_orders('ETH-BTC', side='BID', state='CANCELLED')
```

#### order_detail

```python
cli.order_detail(12232)
```

#### create_order

```python
cli.create_order(market_id='ETH-BTC', side='BID', price='0.12', amount='2')
```

#### cancel_order

```python
cli.cancel_order(11232)
```

#### cancel_all_order

```python
cli.cancel_all_order()
```

#### my_trades

```python
cli.my_trades('ETH-BTC')
```

#### withdrawals

```python
cli.withdrawals(first=10)
```

#### deposits

```python
cli.deposit(first=20)
```
