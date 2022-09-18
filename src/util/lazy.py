from typing import Any, Callable

class LazyEval(object):
    def __init__(self, method, *args) -> None:
        self._method = method
        self._cache = None
        self._args = args
        self.evaluated = False


    def get(self):
        if not self.evaluated and self._cache is None:
            self._cache = self._method(*self._args)
            self.evaluated = True
        return self._cache
