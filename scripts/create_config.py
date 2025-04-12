import asyncio
import json
import os
try:
    import yaml
    import toml
    file_types = {
        'json': json,
        'yaml': yaml,
        'toml': toml,
    }
    json_only = False
except ImportError:
    yaml, toml = None, None
    json_only = True
    file_types = {'json': json}

def get_file_type() -> str:
    if json_only:
        return 'json'
    return input("Enter the file type (json, yaml, toml): ")

def get_config_data() -> dict:
    data = {
        'config': {
            'DEBUG': True,
            'is_log_record': True,
        },
        'BOT_TOKEN': input("Enter the BOT_TOKEN: "),
        'TELEGRAM_CHAT_ID': input("Enter the TELEGRAM_CHAT_ID: "),
        'MONGODB_URI': input("Enter the MONGODB_URI: "),
        'SECRET_KEY': input("Enter the SECRET_KEY: "),
    }
    return data

async def create_configs_files(file_type: str = get_file_type(), data: dict = get_config_data(), file_path: str = "./") -> bool:
    if file_type is file_types:
        raise ValueError(f"Unsupported file type: {file_type}")
    try:
        if os.path.exists(f'{file_path}config.{file_type}'):
            print(f"Config file already exists: {file_path}config.{file_type}")
        else:
            print(f"Config file created: {file_path}config.{file_type}")
            with open(f'{file_path}config.{file_type}', 'w') as file:
                file_types[file_type].dump(data['config'], file)

        if os.path.exists(f'{file_path}.config.env'):
            print(f"Env file already exists: {file_path}.env")
        else:
            print(f"Env file created: {file_path}.env")
            with open(f'{file_path}.env', 'w') as file:
                file.write(f"BOT_TOKEN={data['BOT_TOKEN']}\n")
                file.write(f"TELEGRAM_CHAT_ID={data['TELEGRAM_CHAT_ID']}\n")
                file.write(f"MONGODB_URI={data['MONGODB_URI']}\n")
                file.write(f"SECRET_KEY={data['SECRET_KEY']}\n")

        return True
    except Exception as e:
        print(f"Error creating config files: {e}")
        return False

if __name__ == '__main__':
    asyncio.run(create_configs_files(file_path='../'))