# proyecto-cumn-back
## Python version required:  3.12

## Features

- API integration for Google Firebase sign up via email & passsword
- API integration for Google Firebase login via email & passsword
- API integration with Google Firebase Firestore for logged in users


## Installation
### Dependencies

```sh
pip install -r requirements.txt
```
### Config file

Needs a config.yml file with this paremeters:
```sh
cred_path: "path_to_firebase_admin_credentials_file"
pyrebase_config_path: "path_to_pyrebase_configuration_file"
port: 5000
jwt_secret_key: "your_jwt_secret_key"
```


#### Building 

```sh
python entrypoint.py "config.yml path"
```
Default port is 5000