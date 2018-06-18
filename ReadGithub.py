import urllib.request
from bs4 import BeautifulSoup

source_page = 'https://github.com/search?l=Java&q=abhiap&type=Users'
#''https://docs.python.org/3.6/tutorial/index.html'

if __name__ == '__main__':
    #page = urllib.request.urlopen(source_page)
    with urllib.request.urlopen(source_page) as response:
        page = response.read()
        #print(page)
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.find_all('span', attrs={'class': 'f4 ml-1'})#.text.strip()
    for t in title:
        print(t.text)

    emails = soup.find_all('a', attrs={'class': 'muted-link'})  # .text.strip()
    for e in emails:
        print(e.text)
