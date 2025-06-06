import re

def validate_username(username: str) -> bool:
    pattern = r'^[a-zA-Zа-яА-Я0-9_.\-+~?,:{}=&|`[\]]{2,128}$'
    return bool(re.match(pattern, username))

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    pattern = r'^(?=.*[a-zA-Zа-яА-Я])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>+=]).{6,128}$'
    return bool(re.match(pattern, password))
