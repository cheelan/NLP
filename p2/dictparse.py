from lxml import etree
from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(open('Dictionary.xml'), 'xml')
top_dict = {}

synset_re = re.compile('synset="([^"]*)"')
gloss_re = re.compile('gloss="([^"]*)"')

count = 0
for tag in soup('lexelt'):
    split = tag['item'].split('.')
    inner_dict = {}
    for child in tag.findChildren():
        gloss = gloss_re.findall(str(child))
        synset = synset_re.findall(str(child))
        inner_dict[count] = (gloss, synset)
        count += 1
    top_dict[split[0]] = inner_dict
    print top_dict
    break
