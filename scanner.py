from bs4 import BeautifulSoup
import urllib.request
import urllib.error


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

url ="https://packages.ubuntu.com/xenial/allpackages"
crawlSite(url)
#getCheckSum(url)



