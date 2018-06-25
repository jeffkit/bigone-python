from threading import Thread

class BaseLimiter(object):
    """
    """
    def check_ip_rate(self, ip='default'):
        pass
    
    def increase_ip_request(self, ip='default'):
        pass
    
    def check_account_rate(self, api):
        pass
    
    def increase_account_request(self, account):
        pass


class DefaultLimiter(BaseLimiter):
    """
    """
    
    pass


class RedisLimiter(BaseLimiter):
    """
    """
    pass
