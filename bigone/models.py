from collections import namedtuple

Account = namedtuple('Account', ['asset_uuid', 'balance', 'locked_balance'])
Ticker = namedtuple('Ticker', ['market_uuid', 'bid', 'ask', 'open', 'close',
                    'high', 'low', 'volume', 'daily_change',
                    'daily_change_perc'])
Bid = namedtuple('Bid', ['price', 'amount'])
Ask = namedtuple('Ask', ['price', 'amount'])
Order = namedtuple('Order', ['id', 'market_uuid', 'price', 'amount',
                   'filled_amount', 'avg_deal_price', 'side', 'state'])
Trade = namedtuple('Trade', ['trade_id', 'market_uuid', 'price', 'amount',
                   'taker_side'])
Withdrawal = namedtuple('Withdrawal', ['id', 'customer_id', 'asset_uuid',
                        'amount', 'state', 'recipient_id', 'completed_at',
                        'inserted_at', 'is_internal', 'target_address',
                        'note'])
Deposit = namedtuple('Deposit', ['id', 'customer_id', 'asset_uuid', 'amount',
                     'state', 'note', 'txid', 'confirmed_at', 'inserted_at',
                     'confirms'])
PageInfo = namedtuple('PageInfo', ['start_cursor', 'end_cursor',
                      'has_next_page', 'has_previous_page'])
