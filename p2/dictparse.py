from lxml import etree
from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(open('Dictionary.xml'), 'xml')
top_dict = {}

gloss_re = re.compile('gloss="(.*)"')
synset_re = re.compile('synset="(.*)"')
both_re = re.compile('gloss="(.*)" synset="(.*)"')

count = 0
for tag in soup('lexelt'):
    split = tag['item'].split('.')
    print split[0]
    for child in tag.findChildren():
        #print gloss_re.findall(str(child))
        print both_re.findall(str(child))
    break
    """for child in tag.findChildren():
        inner_dict = {}
        cid = child['id']
        gloss = child['gloss']
        synset = child['synset']
        inner_dict[int(cid) % 10] = (synset, gloss)
    top_dict[split[0]] = inner_dict"""
