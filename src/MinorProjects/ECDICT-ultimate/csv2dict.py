#!/usr/bin/env python3
import csv
from xml.sax.saxutils import escape, unescape, quoteattr

template = ''' <d:entry id="{id}" d:title={word_}><d:index d:value={word_}/>{index_list}<h1 class="word">{word}</h1>{contents}</d:entry>'''
phonetic_temp = '<span class="phonetic"><span d:pr="1">| {} |</span></span>'
definition_temp = '<div class="definition">{}</div>'
translation_temp = '<div class="translation">{}</div>'
tags_temp = '<div class="tags"><i>{}</i></div>'
index_temp = '<d:index d:value={}/>'
head = '''<?xml version="1.0" encoding="UTF-8"?>
<d:dictionary xmlns="http://www.w3.org/1999/xhtml"
xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">
'''
tail = '''</d:dictionary>'''
file_path = '/Users/charles/Downloads/ultimate.csv'
out_path = 'ECDICT.xml'
data = csv.reader(open(file_path, 'r').readlines()[1:])


def gen_entry(entry_id, word, phonetic, definition, translation, tags, exchange):
    contents = list()
    for data, temp in (
        (phonetic, phonetic_temp),
        (translation, translation_temp),
        (definition, definition_temp),
        (tags, tags_temp),
    ):
        if data:
            contents.append(temp.format(data))
    return template.format(id=entry_id, word_=quoteattr(word), word=word, contents=''.join(contents), index_list=exchange)


def name_escape(word, string):
    if string.startswith('n. ({})人名'.format(word.title())):
        return '<span class="trans_name"><i>{}</i></span>'.format(string), 1
    else:
        return string, 0


def format_trans(word, string):
    contents = string.strip().split(r'\n')
    contents = [name_escape(word, escape(unescape(i))) for i in contents]
    contents.sort(key=lambda x: x[1])
    return '<br />'.join(next(zip(*contents)))


def process_exchange(exchange):
    if not exchange:
        return ''
    exchange = set([i.split(':', 1)[1] for i in exchange.split('/') if not i.startswith('1')])
    return ''.join(index_temp.format(quoteattr(i)) for i in exchange)


f = open(out_path, 'w')
f.write(head)
for i, entry in enumerate(data):
    [
        word,
        phonetic,
        definition,
        translation,
        _,
        _,
        _,
        tag,
        _,
        _,
        exchange,
        _,
        _
    ] = entry
    entry_id = hex(i)[2:]
    print(
        gen_entry(
            entry_id,
            escape(unescape(word)),
            escape(unescape(phonetic)),
            format_trans(word, definition),
            format_trans(word, translation),
            escape(unescape(tag.replace(' ', ','))),
            process_exchange(exchange),
        ),
        file=f
    )

f.write(tail)
f.close()
