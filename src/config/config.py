from pathlib import Path


class Config(object):
    def __init__(self, config_dir: Path, configurations_file_name: str = "categories.json") -> None:
        splitted = configurations_file_name.split('.')
        assert len(splitted) == 2 and splitted[1] == "json", "Invalid categories file name. It must be <file-stem>.json"
        
        self.config_dir = config_dir
        self.config_dir.mkdir(mode=0o777, parents=True, exist_ok=True)

        self.configurations_file = self.config_dir / configurations_file_name
        self.configurations_file.touch(0o664, exist_ok=True)
