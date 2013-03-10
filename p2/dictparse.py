from lxml import etree
from bs4 import BeautifulSoup
import re

#soup = BeautifulSoup(open('Dictionary.xml'), 'xml')


#items = item_re.findall(xml)
#gloss = gloss_re.findall(xml)
#synset = synset_re.findall(xml)
def genXmlDictionary(file):
    f = open(file)
    xml = f.read()
    dictionary = {}

    item_re = re.compile('item="([^"]*)"')
    synset_re = re.compile('synset="([^"]*)"')
    gloss_re = re.compile('gloss="([^"]*)"')

    entries = xml.split("lexelt")
    for i in range(1, len(entries), 2):
        item = item_re.findall(entries[i])
        item = (item[0].split("."))[0]
        definitions = gloss_re.findall(entries[i])
        dictionary[item] = definitions
    return dictionary

dict = genXmlDictionary('Dictionary.xml')
print(dict['appear'])

'''
for item in items:
    inner = list()
    split = item.split('.')
    #print split[0]
    for g in gloss:
        for s in synset:
            if split[0] in s:
                inner.append(g)
    dictionary[split[0]] = inner

print dictionary['activate']
#print dictionary
'''
"""for tag in soup('lexelt'):
    count = 0
    split = tag['item'].split('.')
    print split[0]
    inner = list()
    for child in tag.findChildren('sense'):
        gloss = gloss_re.findall(str(child))
        synset = synset_re.findall(str(child))
        inner.append((gloss, synset))
        count += 1
    dictionary[split[0]] = inner
#print top_dict"""
