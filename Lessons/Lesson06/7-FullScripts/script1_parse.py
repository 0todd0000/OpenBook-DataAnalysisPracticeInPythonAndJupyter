'''
Script for parsing five HTML pages of kakaku.com book data.
'''


import os
import lxml.html
import pandas as pd


def parse_name_node(node):
    return node.text

def parse_price_node(node):
    s = node.text
    x = s[1:].replace(',', '')
    return int( x )

def parse_page_count_node(node):
    s = node.text
    if 'ページ' in s:
        x = s.split(':')[1].split(',')[0]
    else:
        x = -1  # assign a value of -1 if "ページ" is not in the text field
    return int( x )


def parse_page(fnameHTML):
    tree        = lxml.html.parse(fnameHTML)
    body        = tree.find('body') 
    box         = body.find_class('itemCatBox')[0]
    name_nodes  = box.find_class('name')
    page_nodes  = box.find_class('itemCatsetsumei')
    price_nodes = box.find_class('itemCatPrice')
    # parse the entries:
    title       = [parse_name_node( node )  for node in name_nodes]
    pages       = [parse_page_count_node( node )  for node in page_nodes]
    price       = [parse_price_node( node)  for node in price_nodes]
    return title, pages, price




# Specify data directory:
# dir0        = os.path.abspath('')            # (use this command only in notebooks)
dir0        = os.path.dirname( __file__ )      # directory in which this script is saved
dirLesson   = os.path.dirname( dir0 )          # Lesson directory
dirData     = os.path.join(dirLesson, 'Data')  # Data directory


# Parse all HTML pages:
title  = []
pages  = []
price  = []
for i in range(5):
    fnameHTML = os.path.join(dirData, f'page{i+1}.html')
    s,n,x     = parse_page(fnameHTML)
    title    += s
    pages    += n
    price    += x


# Write results:
fnameCSV = os.path.join( dir0, 'parsed_data.csv' )
df       = pd.DataFrame( dict(Title=title, Pages=pages, Price=price) )
df.to_csv(fnameCSV, index=False)
print('parsed_data.csv successfully written.')


