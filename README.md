# Welcome to BigOne-Python

An unofficial Python implementation of the latest Open API for big.one exchange.

## install

```bash
pip install bigone
```

## usage

for example:

```python
from bigone.client import Client
cli = Client(api, secret)
markets = cli.markets()
```
