
import os
import csv
import lxml.html
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt



def parse_page(fnameHTML):
    tree      = lxml.html.parse(fnameHTML)
    body      = tree.find('body')
    # nodes       = tree.xpath("//div[@class='itemCatWrap']")
    nodes     = body.find_class('itemCatWrap')
    title     = []
    price     = []
    page      = []
    for node in nodes:
        # parse title:
        s     = node.find_class('name')[0].text
        title.append( s )
        # parse price:
        s     = node.find_class('itemCatPrice')[0].text
        s     = s[1:].replace(',', '')
        price.append( int(s) )
        # parse number of pages:
        s     = node.find_class('itemCatsetsumei')[0].text
        if 'ページ' in s:
            s = s.split(':')[1].split(',')[0]
            page.append( int(s) )
        else:
            page.append( -1 )
    return title, price, page




# #(0) Parse one page:
# dir0             = os.path.dirname( __file__ )      # directory in which this PY file is saved
# dirLesson        = os.path.dirname( dir0 )          # Lesson directory
# dirData          = os.path.join(dirLesson, 'Data')  # Data directory
# fnameHTML        = os.path.join( dirData, 'page1.html' )
# title,price,page = parse_page(fnameHTML)




#(1) Parse all pages:
dir0             = os.path.dirname( __file__ )      # directory in which this PY file is saved
dirLesson        = os.path.dirname( dir0 )          # Lesson directory
dirData          = os.path.join(dirLesson, 'Data')  # Data directory
title,price,page = [], [], []
for i in [1, 2, 3, 4, 5]:
    fnameHTML    = os.path.join( dirData, f'page{i}.html' )
    t,pr,pa      = parse_page(fnameHTML)
    title       += t
    price       += pr
    page        += pa
title,price,page = np.asarray( title ), np.asarray( price ), np.asarray( page )
title_length     = np.array( [len(s) for s in title] )




# ### Save and read data (Option 1: CSV)
#
# #(2) Save data:
# fnameCSV = os.path.join(dir0, 'parsed_data.csv')
# header   = ['Title', 'Pages', 'Price']
# with open(fnameCSV, 'w') as f:
#     writer = csv.writer( f )
#     writer.writerow( header )
#     for t,pa,pr in zip(title, price, page):
#         writer.writerow( [t,pa,pr] )
#
#
# #(3) Read data:
# fnameCSV = os.path.join(dir0, 'parsed_data.csv')
# with open(fnameCSV, 'r') as f:
#     reader = csv.reader( f )
#     a      = np.array([row for row in reader])
#     a      = a[1:]
#     title  = a[:,0]
#     page   = np.asarray( a[:,1], dtype=int )
#     price  = np.asarray( a[:,2], dtype=int )




### Save and read data (Option 2: Pandas)

#(2) Save data:
fnameCSV = os.path.join(dir0, 'parsed_data.csv')
df       = pd.DataFrame( dict(title=title, price=price, page=page) )
df.to_csv(fnameCSV, index=False)

#(3) Read data:
fnameCSV = os.path.join(dir0, 'parsed_data.csv')
df       = pd.read_csv(fnameCSV)
title    = df['title']
page     = df['page']
price    = df['price']




#(3) Plot results:
plt.close('all')
# create figure:
fig    = plt.figure(figsize=(10,3))
# create axes:
axx    = np.linspace(0.06, 0.74, 3)
axy    = 0.18
axw    = 0.25
axh    = 0.8
ax0    = plt.axes([axx[0], axy, axw, axh])
ax1    = plt.axes([axx[1], axy, axw, axh])
ax2    = plt.axes([axx[2], axy, axw, axh])
# histogram:
ax0.hist( price )
ax0.set_xlabel(' Price (¥) ', size=12)
ax0.set_ylabel(' Count ', size=12)
# relation between number of pages and price:
i  = page > 0
ax1.scatter(page[i], price[i])
ax1.set_xlabel(' Number of pages ', size=12)
ax1.set_ylabel(' Price (¥) ', size=12)
# relation between title length and price:
ax2.scatter(title_length[i], price[i])
ax2.set_xlabel(' Title length ', size=12)
ax2.set_ylabel(' Price (¥) ', size=12)
plt.show()




