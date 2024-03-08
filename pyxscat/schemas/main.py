import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError

with open('new_files.json') as f:
    document = json.load(f)

with open('inputfile-schema.json') as f:
    schema = json.load(f)


try:
    validate(instance=document, schema=schema)
    print('Validation succeded with jsonschema.')
except ValidationError as e:
    print('Validation failed!')
    print(f'Message error: {e.message}')
