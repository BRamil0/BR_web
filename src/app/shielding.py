async def shielding_markdown_v2(text: str) -> str:
    escape_chars = r'_ * [ ] ( ) ~ ` > # + - = | { } . !'.split()
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text