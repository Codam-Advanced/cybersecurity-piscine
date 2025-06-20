import argparse
import os
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.parse import ParseResult
from urllib.error import HTTPError


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

def find_tag_and_attribute(html: str, tag: str, attribute: str, start_index: int):
   start_index = html.find("<" + tag + " ", start_index)
   if (start_index == -1):
    return "", 0
   start_index = html.find(attribute + "=", start_index)
   start_index = len(attribute + "=") + start_index
   end_index = html.find(">", start_index)
   temp_index = html.find(" ", start_index, end_index)
   if (temp_index != -1):
      end_index = temp_index
   return html[start_index:end_index].strip("\""), start_index

def change_url(url: ParseResult, img_url: str):
   if (img_url.find("../") != -1):
      img_url = img_url.strip("../")
   if (img_url[0] != "/"):
      img_url = "/" + img_url
   img_url = url.scheme + "://" + url.hostname + img_url
   return img_url
   

def scrape_page(url: ParseResult, html: str):
   start_index = 0
   while (True):
    img_url, start_index = find_tag_and_attribute(html, "img", "src", start_index)
    if (img_url == ""):
        break
    if (img_url.find("http") == -1):
      img_url = change_url(url, img_url)
    upload_file_path = args.path + img_url[img_url.rfind("/") + 1:]
    if (upload_file_path.find("?") != -1):
       upload_file_path = upload_file_path[:upload_file_path.find("?")]
    if (os.path.isfile(upload_file_path) or img_url.endswith((".jpg", ".jpeg", ".png", ".gif" ".bmp")) == False):
       continue
    with open(upload_file_path, "wb") as file:
        page = urlopen(img_url)
        file.write(page.read())

miep = set()

def crawl_page(url: str, length: int):
   print("Length = " + str(length), url) 
   miep.add(url)
   print(miep)
   parsed_url = urlparse(url)
   try:
      page = urlopen(parsed_url.geturl())
      html_bytes = page.read()
      html = html_bytes.decode("utf-8")
      start_index = 0
      while (True):
         a_url, start_index = find_tag_and_attribute(html, "a", "href", start_index)
         if (a_url == ""):
            break
         if (a_url.find("http") == -1):   
            a_url = change_url(parsed_url, a_url)
         if (a_url in miep):
            continue
         if (length > 0 and a_url.endswith(".zip") == False): 
            crawl_page(a_url, length - 1)
      scrape_page(parsed_url, html)
   except HTTPError as e:
      if e.code == 308 or e.code == 302:
         redirected_url = e.headers["location"]
         print(f"Redirected to {redirected_url}")
         if (length > 0 and a_url not in miep): 
            crawl_page(redirected_url, length)
      if e.code == 404:
         print(f"Site Not Found! {url}")
      else:
         print(f"Error {e.code} found on site {url}")

if __name__ == "__main__":
   args = parse_arguments()
   crawl_page(args.URL, args.length)
   


