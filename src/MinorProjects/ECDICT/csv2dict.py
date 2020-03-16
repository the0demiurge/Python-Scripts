#!/usr/bin/env python3
import csv
from xml.sax.saxutils import escape, unescape, quoteattr

template = ''' <d:entry id="{id}" d:title={word_}> <d:index d:value={word_}/> <h1 class="word"> {word} </h1> {contents} </d:entry> '''
phonetic_temp = '<span class="phonetic"> <span d:pr="1"> | {} | </span> </span>'
definition_temp = '<div class="definition">{}</div>'
translation_temp = '<div class="translation">{}</div>'
tags_temp = '<div class="tags"> <i>{}</i> </div>'

head = '''<?xml version="1.0" encoding="UTF-8"?>
<d:dictionary xmlns="http://www.w3.org/1999/xhtml"
xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">
'''
tail = '''
</d:dictionary>
'''
file_path = '/Users/charles/Cloud/NextCloud/Disk/manga/ecdict.csv'
out_path = 'ECDICT.xml'
data = csv.reader(open(file_path, 'r').readlines()[1:])


def gen_entry(entry_id, word, phonetic, definition, translation, tags):
    contents = list()
    for data, temp in (
        (phonetic, phonetic_temp),
        (definition, definition_temp),
        (translation, translation_temp),
        (tags, tags_temp),
    ):
        if data:
            contents.append(temp.format(data))
    return template.format(id=entry_id, word_=quoteattr(word), word=word, contents=''.join(contents))


def format_trans(string):
    contents = string.strip().split(r'\n')

    return '<br />'.join([escape(unescape(i)) for i in contents])


f = open(out_path, 'w')
f.write(head)
for i, entry in enumerate(data):
    [word,
     phonetic,
     definition,
     translation,
     _,
     _,
     _,
     tag,
     _,
     _,
     _,
     _,
     _] = entry
    entry_id = hex(i)[2:]
    print(gen_entry(entry_id, escape(unescape(word)), escape(unescape(phonetic)), format_trans(definition), format_trans(translation), escape(unescape(tag.replace(' ', ',')))), file=f)

f.write(tail)
f.close()
