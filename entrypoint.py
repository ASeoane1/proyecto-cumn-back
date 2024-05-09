import argparse
import yaml
from api_controller import ApiController

def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the API server.')
    parser.add_argument('config_file', type=str, help='Path to the configuration file')
    args = parser.parse_args()

    config = load_config(args.config_file)

    # Initialize API
    api_controller = ApiController(
        config['cred_path'],
        config['pyrebase_config_path'],
        config['jwt_secret_key']
    )
    api_controller.start_server(port=config.get('port', 5000))
