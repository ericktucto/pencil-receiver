import inspect
from typing import Callable

def route(name: str):
    def decorator(func: Callable):
        func._route_name = name
        firm = inspect.signature(func)
        params = list(firm.parameters.values())
        func._message_type = params[1].annotation
        return func
    return decorator
