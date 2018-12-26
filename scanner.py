#!/bin/python
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import argparse
import sys

hardware=["amd64","armhf","i386"]
distros=["ubuntu-trusty","ubuntu-xenial","ubuntu-bionic","ubuntu-cosmic","debian-stable","debian-jessie","debian-stretch","debian-buster","debian-experimental"]
ubuntu="https://packages.ubuntu.com/xenial/allpackages"

def __main__(parser, args):
    if args.distro not in distros:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if args.type not in hardware:
        parser.print_help(sys.stderr)
        sys.exit(1)
    else:
        print("continue")


def parseUrl(resp):
    soup = BeautifulSoup(resp,"html5lib")
    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])
    return links


def getRequest(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print("URL-Error\n",e)
    except urllib.error.HTTPError as e:
        print("HTTP-Error\n",e)
    except urllib.error.ValueError as e:
        print("ValueError-Error\n",e)


def crawlSite(baseUrl):
    url ="https://packages.ubuntu.com/xenial/all/alsa-base-udeb/download"
    resp = getRequest(baseUrl)
    links = parseUrl(resp)
    print(len(links))
    for link in links:
        if link != "/":
            url="https://packages.ubuntu.com/xenial/amd64/"+link+"/download"
        print(link, getCheckSum(url))

def getCheckSum(url):
   resp = getRequest(url)
   soup = BeautifulSoup(resp,"html5lib")
   data = []
   try:
       table = soup.find('table')
       table_body = table.find('tbody')
       rows = table_body.find_all('tr')
       for row in rows:
           cols = row.find_all('td')
           cols = [ele.text.strip() for ele in cols]
           data.append((row.text.strip().split('\t')[0],[ele for ele in cols if ele]))
       return data
   except:
        print("Error")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pull Latest Hash for All Packages in Linux Distribution")
    parser.add_argument('-d','--distro', help=print("Distrbution: ", ', '.join(map(str,distros))),required=True)
    parser.add_argument('-t','--type', help="Hardware Type: amd64, armhf, i386",required=True)
    parser.add_argument('-o','--output', help="Filename of output file",required=True)
    parser.add_argument('-v','--verbose', help="Toggle Verbose on or off")
    args = parser.parse_args()
    __main__(parser,args)
