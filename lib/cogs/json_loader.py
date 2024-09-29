from typing import Dict, List, Any
from json import load

class JsonLoader:
    _instance: 'JsonLoader' = None

    def __new__(cls, *args, **kwargs) -> 'JsonLoader':
        if not cls._instance:
            cls._instance = super(JsonLoader, cls).__new__(cls, *args, **kwargs)
            cls._instance.errors = []
            cls._instance.init_json_loader()
        return cls._instance


    def init_json_loader(self) -> Dict[str, Any]:
        self.config: Dict[str, Any] = self._load_json("./data/json/config.json")
        self.users: Dict[str, str] = self._load_json(self.config["paths"]["users_path"])
        self.bad_words: List[str] = self._load_json(self.config["paths"]["bad_words_path"])
        self.mods_ids: Dict[str, str] = self._load_json(self.config["paths"]["mods_ids"])

        self.json_data: Dict[str, Any] = {
            "config": self.config,
            "users": self.users,
            "bad_words": self.bad_words,
            "mods_ids": self.mods_ids
        }
        return self.json_data

    @staticmethod
    def _load_json(path: str) -> Dict[str, Any]:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return load(file)
        except FileNotFoundError:
            JsonLoader._instance.errors.append(f'Файл не найден: невозможно найти файл по пути "{path}"')
            return {}