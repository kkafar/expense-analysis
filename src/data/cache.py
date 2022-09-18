from pathlib import Path


class Cache(object):
    def __init__(self, cache_dir: Path) -> None:
        self.invalidated = False
        self.cache_dir = cache_dir
        self.hashes_dir = cache_dir / "hash"
        self.hashes_dir.mkdir(mode=0o777, exist_ok=True, parents=True)


    def invalidate(self) -> None:
        self.invalidated = True

     
