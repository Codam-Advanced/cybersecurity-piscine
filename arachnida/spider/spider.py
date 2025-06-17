import argparse
import os
from urllib.request import urlopen
from urllib.parse import urlparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="The URL that the program will use to start webcrawling")
    parser.add_argument("-r", "--recursive", action="store_true", help="recursively downloads the images in a URL received as a parameter.")
    parser.add_argument("-l", "--length", metavar="N",  type=int,  help="indicates the maximum depth level of the recursive download.If not indicated, it will be 5.",)
    parser.add_argument("-p", "--path", metavar="PATH", type=str, default="./data/", help="indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.")
    args = parser.parse_args()

    if (args.length != None and args.length < 0):
        parser.error("--length needs to be a positive interger")
    if (args.length != None and args.recursive == False):
        parser.error("The --length argument requires that the flag --recursive is set")
    if (args.length == None):
        args.length = 5; # Default length
    
    return args


def scrape_page(url: str):
   url = urlparse(url)
   page = urlopen(url.geturl())

   html_bytes = page.read()
   html = html_bytes.decode("utf-8")
   start_index = 0
   while (True):
    start_index = html.find("<img", start_index)
    if (start_index == -1):
       break
    start_index = html.find("src=\"", start_index)
    start_index = len("src=\"") + start_index
    end_index = html.find("\"", start_index)
    img_url = html[start_index:end_index]
    upload_file_path = args.path + img_url[img_url.rfind("/") + 1:]
    print(upload_file_path)
    if (os.path.isfile(upload_file_path)):
       continue
    with open(upload_file_path, "wb") as file:
        page = urlopen(url.scheme + "://" + url.hostname + img_url)
        file.write(page.read())

miep = set()

if __name__ == "__main__":
   args = parse_arguments()
   scrape_page(args.URL)
   


