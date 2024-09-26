from collections import OrderedDict
from typing import Any


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def cast_to_hashable(item: Any) -> Any:
    if isinstance(item, list):
        return tuple(i for i in item)
    elif isinstance(item, set):
        return frozenset(item)
    elif isinstance(item, dict):
        return tuple((k, cast_to_hashable(v)) for k, v in item.items())
    else:
        return item

def cache(func):
    def wrapper(*args, **kwargs):
        hashable_args = tuple(cast_to_hashable(arg) for arg in args)
        hashable_kwargs = tuple((k, cast_to_hashable(v)) for k, v in kwargs.items())
        
        key = (hashable_args, hashable_kwargs)
        value = cache_dir.get(key)
        
        if value is not None:
            print(f"[INFO]: Get value from cache with params: {key}")
            return value
        
        print("[INFO]: Calculate new value.")
        res = func(*args, **kwargs)
        
        if len(cache_dir) == 100:
            print("[WARNING]: Cache reached the limit... Pop first item.")
            cache_dir.popitem(last=False)
        
        print("[INFO]: Add new value to cache.")
        cache_dir[key] = res
        return res
    return wrapper


@cache
def foo(a, b):
    return {"result": [a, b]}


def main():
    """Tests"""
    print(f"[DEBUG]: Check cache limiter...")

    for i in range(101):
        foo(1, i)

    for _ in range(2):
        result = foo(1, 2)
        print(f"[INFO]: {result}")
        
        result = foo([1], [2])
        print(f"[INFO]: {result}")

        result = foo([1], b=[2])
        print(f"[INFO]: {result}")

        result = foo([1], b={2, 3})
        print(f"[INFO]: {result}")

        result = foo([1], b=p)
        print(f"[INFO]: {result}")


if __name__ == "__main__":
    cache_dir = OrderedDict()
    p = Point(1, 2)    
    main()
    print(len(cache_dir))
    print(cache_dir)
    