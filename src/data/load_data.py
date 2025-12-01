import os
from os import path
import logging
import requests

logging.basicConfig(level=logging.INFO)

def load_data(url: str, file_path: str) -> None:
    '''
    Download data from a URL and save it to a specified file path.
    Parameters:
    - url: str : The URL to download the data from.
    - file_path: str : The local file path to save the downloaded data.
    '''
    os.makedirs(path.dirname(file_path), exist_ok=True)

    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, 'wb') as f:
        f.write(response.content)
    logging.info(f"Data downloaded from {url} and saved to {file_path}")

def main() -> None:
    url = 'https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/bentoml/admission.csv'
    file_name = url.split('/')[-1]
    file_path = path.join(os.getcwd(), 'data', 'raw', file_name)
    load_data(url, file_path)

if __name__ == "__main__":
    main()