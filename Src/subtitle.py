from workflow import Workflow3
from bs4 import BeautifulSoup
import sys
import urllib2


def main(wf):
    url = sys.argv[1]
    base_url = 'http://www.zimuku.net'
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, features="html.parser")
    div = soup.find('div', 'subs box clearfix')
    tbody = div.find('tbody')
    trs = tbody.find_all('tr')

    for item in trs:
        td = item.find('td', 'first')
        a = td.a
        sub_url = base_url + a['href']
        produce = td.find('span', 'gray')
        
        download_url = get_download_url(sub_url)

        wf.add_item(a['title'], produce.text, arg=download_url, valid=True,
                    icon="favicon.jpeg")

    wf.send_feedback()


def get_download_url(url):
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, features="html.parser")
    a = soup.select('a#down1')[0]
    download_url = a['href']
    return download_url


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
