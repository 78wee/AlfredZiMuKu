# encoding: utf-8

from workflow import Workflow3
from bs4 import BeautifulSoup
import sys
import urllib2


def main(wf):
    query = sys.argv[1]
    base_url = 'http://www.zimuku.net'
    url = "http://www.zimuku.cn/search?q=" + query

    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    div_item = soup.find_all('div', 'item prel clearfix')

    for item in div_item:
        img = item.find('img', 'lazy')
        img_url = 'http:' + img['data-original']

        div2 = item.find('div', 'title')
        a = div2.select("p a")[0]
        sub_url = base_url + a['href']

        sub_count = get_sub_count(sub_url)

        b = div2.select("p a b")[0]
        wf.add_item(b.text, '总共发现' + str(sub_count) + '个字幕', arg=sub_url, valid=True,
                    icon="favicon.jpeg", quicklookurl=img_url)

    wf.send_feedback()


def get_sub_count(url):
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, features="html.parser")
    div = soup.find('div', 'subs box clearfix')
    tbody = div.find('tbody')

    trs = tbody.find_all('tr')

    return len(trs)


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
