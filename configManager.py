import os
import platform

class ConfigManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if platform.system() == 'Windows':
            self.base_path = os.path.join(os.getenv('APPDATA'))

        elif platform.system() == 'Linux':
            self.base_path = os.path.join(os.getenv('HOME'), '.config')

        elif platform.system() == 'Darwin':
            self.base_path = os.path.join(os.getenv('HOME'), 'Library', 'Application Support')
        else:
            raise NotImplementedError("Unsupported operating system")

        self.config_path = os.path.join(self.base_path, 'KernelJames', 'services', 'SelfDevelopment', 'config.json')

        print(f"Config path set to: {self.config_path}")

        self.config = {
            "host": "localhost",
            "port": 8000,
            "environment": "production",
            "allowed_origins": ["*"],
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
            "https_redirect": True,
            "authentication": True
        }
        self.__load_config()

    def __load_config(self):
        import json
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as file:
                self.config = json.load(file)
                print("Configuration loaded successfully.")
        else:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as file:
                file.write(json.dumps(self.config, indent=4))
                print("Default configuration file created.")