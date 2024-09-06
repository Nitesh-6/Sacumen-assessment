import os
import yaml
import json
import configparser
from dotenv import load_dotenv, set_key


class ConfigHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config_data = {}

    def read_config(self):
        file_ext = os.path.splitext(self.file_path)[1]
        if file_ext == '.yaml':
            self._read_yaml()
        elif file_ext in ['.cfg', '.conf']:
            self._read_cfg_conf()
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
        return self.flatten_dict(self.config_data)

    def _read_yaml(self):
        with open(self.file_path, 'r') as file:
            self.config_data = yaml.safe_load(file)

    def _read_cfg_conf(self):
        config = configparser.ConfigParser()
        config.read(self.file_path)
        self.config_data = {section: dict(config.items(section)) for section in config.sections()}

    def flatten_dict(self, d, parent_key='', sep='.'):
        flat_dict = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                flat_dict.update(self.flatten_dict(v, new_key, sep=sep))
            else:
                flat_dict[new_key] = v
        return flat_dict

    def write_to_json(self, output_path):
        with open(output_path, 'w') as json_file:
            json.dump(self.config_data, json_file, indent=4)

    def write_to_env(self, output_path):
        with open(output_path, 'w') as env_file:
            for key, value in self.config_data.items():
                env_file.write(f"{key}={value}\n")

    def set_os_env(self):
        for key, value in self.config_data.items():
            os.environ[key] = str(value)


def main():
    import sys
    file_path = sys.argv[1]
    handler = ConfigHandler(file_path)

    config = handler.read_config()
    print("Flat configuration:", config)

    handler.write_to_json("output.json")

    handler.write_to_env(".env")

    handler.set_os_env()


if __name__ == "__main__":
    main()
