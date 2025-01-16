import json
import base64
import binascii
import logging


def convert_array_to_dict(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    if isinstance(data, list):
        data = [{'data': item} for item in data]

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def decode_data(data):
    # Check if data is a valid string (already decoded)
    if isinstance(data, str):
        return data  # Return the string as is if it's already a valid UTF-8 string

    # Try Base64 decoding
    try:
        return base64.b64decode(data).decode('utf-8')
    except (binascii.Error, UnicodeDecodeError):
        pass  # If Base64 decoding fails, skip and move to the next step

    # Try hex decoding
    try:
        return bytes.fromhex(data).decode('utf-8')
    except (ValueError, UnicodeDecodeError):
        pass  # If hex decoding fails, skip and move to the next step

    # Try JSON decoding
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        pass  # If JSON decoding fails, skip and move to the next step

    # Try UTF-8 decoding (if data is raw bytes and needs decoding)
    try:
        return data.encode('utf-8').decode('utf-8')
    except UnicodeDecodeError:
        pass  # If UTF-8 decoding fails, return the data as is

    # If all decoding attempts fail, raise an error
    raise ValueError('Decoding failed')

def process_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    for item in data:
        if 'data' in item:
            try:
                item['data'] = decode_data(item['data'])
            except ValueError as e:
                logging.error(f"Error decoding data for item {item}: {e}")

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def get_captions_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    captions = []

    def extract_captions(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'caption':
                    captions.append(value)
                else:
                    extract_captions(value)
        elif isinstance(obj, list):
            for item in obj:
                extract_captions(item)

    extract_captions(data)
    return captions

def export_to_json(data, output_file_path):
    with open(output_file_path, 'w') as file:
        json.dump(data, file, indent=4)
