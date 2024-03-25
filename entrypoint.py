import argparse
from api_controller import ApiController

def parse_arguments():
    parser = argparse.ArgumentParser(description='Start the API server.')
    parser.add_argument('--cred_path', type=str, required=True, help='Path to the Firebase admin credentials file')
    parser.add_argument('--pyrebase_config_path', type=str, required=True, help='Path to the Pyrebase configuration file')
    parser.add_argument('--port', type=int, default=5000, help='Port number to run Flask server on (default: 5000)')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    # Initialize API
    api_controller = ApiController(args.cred_path, args.pyrebase_config_path)
    api_controller.start_server(port=args.port)
