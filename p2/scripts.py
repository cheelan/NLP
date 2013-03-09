from nltk.corpus import wordnet

#Returns a list of the definitions of all senses/synonyms of a word
def define_word(word):
    xmldef = xml_definition(word)
    if len(xmldef) > 0:
        return xmldef
    synsets = wordnet.synsets(word)
    definitions = list()
    for s in synsets:
        definitions.append(s.definition)
    return definitions

#To-do: Joe
#Returns the definitions of a word in the XML dictionary, or [] or something if it isn't defined
def xml_definition(word):
    return []

for d in define_word("bank"):
    print "---"
    print(d)