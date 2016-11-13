# -*- coding:utf-8 -*-

import glob
import os
import sqlite3
import re
from lxml import etree


path = 'D:/PyQt4.docset'  # Enter you docset path here


db = sqlite3.connect(os.path.join(path, 'Contents/Resources/docSet.dsidx'))
cur = db.cursor()


re_list = [
    [r'<html>.*?<body>.*?<h3>Types</h3>(.*?)(?:<h3>|<h2>)', r'<a href=\"(.*?)\">(.*?)</a>', 'Type'],
    [r'<html>.*?<body>.*?<h3>Methods</h3>(.*?)(?:<h3>|<h2>)', r'<a href=\"(.*?)\">(.*?)</a>', 'Method'],
    [r'<html>.*?<body>.*?<h3>Qt Signals</h3>(.*?)(?:<h3>|<h2>)', r'<a href=\"(.*?)\">(.*?)</a>', 'Function']
]

class_exp = '/html/body/table[2]//td/a[@href]'


def get_class():
    for htmlfile in glob.glob(os.path.join(path, 'Contents/Resources/Documents/classes.html')):
        with open(os.path.join(path, 'Contents/Resources/Documents', htmlfile)) as html:
            sel = etree.HTML(html.read())
            result_sel = sel.xpath(class_exp)
            for rs in result_sel:
                newhtml = etree.tostring(rs)
                newsel = etree.HTML(newhtml)
                href = newsel.xpath('//a[@href]/@href')[0]
                nam = rs.text
                cur.execute("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES ('%s', 'Class', '%s')" % (nam, href))
            db.commit()


def get_doc(re0, re1, types):
    for htmlfile in glob.glob(os.path.join(path, 'Contents/Resources/Documents/*.html')):
        with open(os.path.join(path, 'Contents/Resources/Documents', htmlfile)) as html:
            print html
            first_result = re.search(re0, html.read(), re.S)
            if first_result:
                print first_result.group(1)
                result_sel = re.findall(re1, first_result.group(1), re.S)
                for rs in result_sel:
                    cur.execute(
                        "INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES ('%s', '%s', '%s')" % (
                        rs[1], types, rs[0]))
            db.commit()

get_class()
for rl in re_list:
    get_doc(rl[0], rl[1], rl[2])

db.close()
