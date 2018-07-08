from . base import Request


class BigOneClient(Request):
    #  public methods

    def get_all_tickers(self):
        return self.public_get('tickers', 'Ticker')
    
    def get_ticker(self, market):
        return self.public_get('markets/%s/ticker' % market, 'Ticker')
    
    def get_order_book(self, market):
        return self.public_get('markets/%s/depth' % market, 'OrderBook')
    
    def get_trades(self, market, **page_options):
        return self.public_get('markets/%s/trades' % market, 'Trade',
                               page_options)
    
    def get_markets(self):
        return self.public_get('markets', 'Market')

    # private methods

    def account_info(self):
        return self.private_get('viewer/accounts', 'Account')
    
    def get_orders(self, market_id=None, side=None, state=None, 
            **page_options):
        params = {
            'side': side,
            'state': state,
            'market_id': market_id
        }
        params.update(page_options)
        return self.private_get('viewer/orders', 'Order', params)
    
    def order_detail(self, order_id):
        return self.private_get('viewer/orders/%s' % order_id, 'Order')
    
    def create_order(self, market_id, side, price, amount):
        return self.private_post('viewer/orders', 'Order', {
            'market_id': market_id,
            'side': side,
            'price': price,
            'amount': amount
        })
    
    def cancel_order(self, order_id):
        return self.private_post('viewer/orders/%s/cancel' % order_id,
                                 'Order')
    
    def cancel_all_order(self):
        return self.private_post('viewer/orders/cancel_all', 'Order')
    
    def my_trades(self, market_id=None, **page_options):
        params = {
            'market_id': market_id
        }
        params.update(page_options)
        return self.private_get('viewer/trades', 'Trade', params)

    def withdrawals(self, **page_options):
        return self.private_get('viewer/withdrawals', 'Withdrawal',
                                page_options)
    
    def deposits(self, **page_options):
        return self.private_get('viewer/deposits', 'Deposit', page_options)
