from . base import Request


class BigOneClient(Request):

    def __init__(self, api, secret, entry_point='https://big.one/api/v2/',
                 limit_rate=True, limiter=None):
        if not entry_point.endswith('/'):
            entry_point = entry_point + '/'
        super().__init__(api, secret, entry_point, limit_rate, limiter)
        self.ping()

    #  public methods
    def ping(self):
        return self.public_get('ping')

    def get_all_tickers(self):
        return self.public_get('tickers')
    
    def get_ticker(self, market):
        return self.public_get('markets/%s/ticker' % market)
    
    def get_order_book(self, market):
        return self.public_get('markets/%s/depth' % market)
    
    def get_trades(self, market):
        return self.public_get('markets/%s/trades ' % market)
    
    def get_markets(self):
        return self.public_get('markets')

    # private methods

    def account_info(self):
        return self.private_get('viewer/accounts')
    
    def get_orders(self):
        return self.private_get('viewer/orders')
    
    def order_detail(self, order_id):
        return self.private_get('viewer/orders/%s' % order_id)
    
    def create_order(self, market_id, side, price, amount):
        return self.private_post('viewer/orders', {
            'market_id': market_id,
            'side': side,
            'price': price,
            'amount': amount
        })
    
    def cancel_order(self, order_id):
        return self.private_post('viewer/orders/%s/cancel' % order_id)
    
    def cancel_all_order(self):
        return self.private_post('viewer/orders/cancel_all')
    
    def my_trades(self):
        return self.private_get('viewer/trades')

    def withdrawals(self):
        return self.private_get('viewer/withdrawals')
    
    def deposits(self):
        return self.private_get('viewer/deposits')
