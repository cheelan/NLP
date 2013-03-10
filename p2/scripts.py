from nltk.corpus import wordnet
import re

#Returns a list of the definitions of all senses/synonyms of a word
def define_word(d, word):
    try:
        xmldef = xml_definition(d,word)
        if len(xmldef) > 0:
            return xmldef
    except:
        synsets = wordnet.synsets(word)
        definitions = list()
        for s in synsets:
            definitions.append(s.definition)
        return definitions

def genXmlDictionary(file):
    xml = open(file).read()
    dictionary = {}

    item_re = re.compile('item="([^"]*)"')
    #synset_re = re.compile('synset="([^"]*)"')
    gloss_re = re.compile('gloss="([^"]*)"')

    entries = xml.split("lexelt")
    for i in range(1, len(entries), 2):
        item = item_re.findall(entries[i])
        item = (item[0].split("."))[0]
        definitions = gloss_re.findall(entries[i])
        #syns = synset_re.findall(entries[i])
        #dictionary[item] = (definitions, syns)
        dictionary[item] = definitions
    return dictionary

#Returns the definitions of a word in the XML dictionary, or [] or something if it isn't defined
def xml_definition(d, word):
    return d[word]

def parse_target(string):
    split = string.split('@')
    targets = list()
    for i in range(0, len(split)):
        if i%2 == 1:
            targets.append(split[i])
    return targets

def parse_training(file):
    f = open(file)
    lines = f.readlines()
    parsed = list()
    
    for l in lines:
        space_split = l.split(' ')
        target = space_split[0][:-2]
        at_split = l.split('@')
        context = at_split[1:]
        temp = ""
        for c in context:
            temp += c
        parsed.append((target, temp))
    return parsed

print parse_training('debug_training.data')
"""dictionary = genXmlDictionary('Dictionary.xml')

for d in define_word(dictionary, "fish"):
    print "---"
    print(d)"""
