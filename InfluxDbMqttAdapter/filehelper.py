import json

class FileHelper:

    @staticmethod
    def load_config(filename):
        with open(filename) as f:
            config = json.load(f)
            return config
        return ""
