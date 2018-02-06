#!/venv/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html
import csv

# Write start page and xpath to parse links of inner items for subsequent parsing.
link = 'http://karo.spb.ru/shop/catalog/'
xpath = '//*[@id="page"]/aside/ul/li/a'

# To set item's xpath for inner pages.
xpathitems = ['//*[@id="product-list"]/section/div/a[2]/div[1]', '//*[@id="product-list"]/section/div/div[2]']

cat = [] # Item's links for parsing.
items = [] # Items, for example, names, url, description.

def findlinks(link, xpath):
    page = requests.get(link)
    root = html.fromstring(page.text)
    tree = root.getroottree()
    result = root.xpath(xpath)
    for i in result:
        cat.append('http://karo.spb.ru' + i.attrib['href']) # Correct the link here!
    return result

def findItems(cat, xpathcat):
    for link in cat:
        page = requests.get(link)
        root = html.fromstring(page.text)
        checkpages(root) # Check pagination pages and push them to cat.
        for i in range(0, len(root.xpath(xpathcat[0]))):
            if not root.xpath(xpathcat[0])[i].text is None: # Check if item is not None.
            items.append([
                root.xpath(xpathcat[0])[i].text, # Push first xpath item.
                root.xpath(xpathcat[1])[i].text, # Push second xpath item.
                link # Push item's link.
            ])

def checkpages(root):
    if root.xpath('//*[@id="product-list"]/div[3]/ul/li/a'): # Check if pagination exists.
        for item in root.xpath('//*[@id="product-list"]/div[3]/ul/li/a'):
            if ('http://karo.spb.ru' + item.attrib['href']) not in cat: # Check is there the same link in cat.
                cat.append('http://karo.spb.ru' + item.attrib['href'])

# Execute functions.
findlinks(link, xpath)
findItems(cat, xpathitems)


# Create out.csv before!
with open('out.csv', 'wb') as f:
    w = csv.writer(f)
    w.writerows([[j.encode('utf-8', 'ignore') for j in i if j is not None] for i in items])g


