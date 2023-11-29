'''
A simple redis database to store how many times we have greeted the input name
'''

from redis import Redis

class RedisClient:
    '''
    Customize the original redis client
    '''
    def __init__(self) -> None:
        self._conn =Redis(host='localhost', port=6379, decode_responses=True)

    def set_val(self, key:str, value: int) -> None:
        self._conn.set(key, value)

    def get_val(self, key: str) -> int:
        result = self._conn.get(key)
        if result is None:
            self._conn.set(key, 0)
            return 0
        return int(result)

    def incr_get(self, key: str) -> int:
        '''
        Get value, increment it, and return the incremented value
        '''
        val = self.get_val(key)
        val += 1
        self.set_val(key, val)
        return val

    def decr_get(self, key: str) -> int:
        '''
        Get value, decrement it, and return the decremented value
        '''
        val = self.get_val(key)
        val = max(val - 1, 0)
        self.set_val(key, val)
        return val

