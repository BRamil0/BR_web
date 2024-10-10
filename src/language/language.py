import json

async def open_language_file(language: str) -> dict[str:str | dict]:
    try:
        with open(file=f"repository/{language}_language.json") as f:
            return json.load(f)
    except FileNotFoundError:
        with open(file=f"repository/ukr_language.json") as f:
            return json.load(f)