import json

def dirty_json_parser(content):
    if content.endswith('\n'):
        content = content[:-2]

    if content.startswith('\n'):
        content = content[2:]

    if content.endswith('```'):
        content = content[:-3]

    if content.startswith('```'):
        content = content[3:]

    if content.startswith('json') or content.startswith('JSON'):
        content = content[4:]

    return json.loads(content)
