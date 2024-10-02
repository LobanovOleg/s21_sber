import os
import sys
from bs4 import BeautifulSoup
import requests

url_server = 'http://localhost:8888'

def download(filepath):
    if os.path.isfile(filepath):
        with open(filepath, 'r') as file:
            requests.post(f"{url_server}/downloads", files={'file': file})
    else:
        print(f"{filepath} does not exist")
        return


def list_of_files():
    folder_path = 'downloads'
    response = requests.get(f"{url_server}/{folder_path}")
    files = response.text
    soup = BeautifulSoup(files, 'html.parser')
    a_tags = soup.find_all('a')

    for i  in a_tags:
        file_name = i.text.strip()
        print(file_name)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 screwdriver.py [download|list] [filepath]")
        sys.exit()

    if sys.argv[1] == 'download':
        if len(sys.argv) < 3:
            print("Usage: python3 screwdriver.py download [filepath]")
            sys.exit()
        download(sys.argv[2])
    elif sys.argv[1] == 'list':
        list_of_files()
    else:
        print("Invalid command")
    

if __name__ == '__main__':
    main()