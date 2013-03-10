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

dictionary = genXmlDictionary('Dictionary.xml')

for d in define_word(dictionary, "fish"):
    print "---"
    print(d)
