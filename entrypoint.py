import yaml
from api_controller import ApiController

def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

if __name__ == '__main__':
    config = load_config('config.yml')

    # Initialize API
    api_controller = ApiController(
        config['cred_path'],
        config['pyrebase_config_path'],
        config['jwt_secret_key']
    )
    api_controller.start_server(port=config.get('port', 5000))
