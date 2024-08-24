from json import load

class JsonLoader:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(JsonLoader, cls).__new__(cls, *args, **kwargs)
            cls._instance.init_json_loader()
        return cls._instance


    def init_json_loader(self):
        with open("./data/json/config.json", 'r', encoding='utf-8') as file:
            self.config = load(file)
            
        with open(self.config["paths"]["users_path"], 'r', encoding='utf-8') as file:
            self.data = load(file)

        with open(self.config["paths"]["bad_words_path"], 'r', encoding='utf-8') as file:
            self.bad_words = load(file)

        self.json_data = {"config": self.config, "data": self.data, "bad_words": self.bad_words}