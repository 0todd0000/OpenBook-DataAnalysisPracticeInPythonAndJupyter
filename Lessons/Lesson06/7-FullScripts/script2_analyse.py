
import os
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import pandas as pd


def add_regression_line(ax, x, y, xytext=None):
    a,b    = np.polyfit(x, y, deg=1)
    x0,x1  = min(x), max(x)
    y0,y1  = a*x0 + b, a*x1 + b
    ax.plot([x0,x1], [y0,y1], color='r', label='Regression line')
    if xytext is not None:
        xt,yt = xytext
        r     = np.corrcoef(x, y)[0,1]
        ax.text(xt, yt, 'r = %.3f' %r, color='r')



# Read data:
# dir0         = os.path.abspath('')            # (use this command only in notebooks)
dir0         = os.path.dirname( __file__ )      # directory in which this script is saved
fnameCSV     = os.path.join( dir0, 'parsed_data.csv' )
df           = pd.read_csv(fnameCSV)
title        = df['Title']
pages        = df['Pages']
price        = df['Price']
title_length = np.array( [len(s) for s in title] )


# Central tendency measures:
x0     = np.mean( price )
x1     = np.median( price )
x2     = stats.mode( price ).mode
print("Central tendency measures:")
print("    Mean        = ", x0)
print("    Median      = ", x1)
print("    Mode        = ", x2)
print()


# Dispersion measures:
x  = price
y0 = np.min( x )  # minimum
y1 = np.max( x )  # maximum
y2 = y1 - y0      # range
y3 = np.percentile( x, 25 ) # 25th percentile (i.e., lower quartile)
y4 = np.percentile( x, 75 ) # 75th percentile (i.e., upper quartile)
y5 = y4 - y3 # inter-quartile range
y6 = np.var( x ) # variance
y7 = np.std( x ) # standard deviation
print("Dispersion measures:")
print("    Minimum              = ", y0)
print("    Maximum              = ", y1)
print("    Range                = ", y2)
print("    25th percentile      = ", y3)
print("    75th percentile      = ", y4)
print("    Inter-quartile range = ", y5)
print("    Variance             = ", y6)
print("    Standard deviation   = ", y7)
print()


# Non normality:
z0 = stats.skew(x)
z1 = stats.kurtosis(x)
print("Non-normality measures:")
print( f"    Skewness     = {z0}")
print( f"    Kurtosis     = {z1}")
print()



# Correlation (in a figure)
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
i  = pages > 0
ax1.scatter(pages[i], price[i])
ax1.set_xlabel(' Page count ', size=12)
ax1.set_ylabel(' Price (¥) ', size=12)
add_regression_line(ax1, pages[i], price[i], xytext=(600,8000))
# relation between title length and price:
ax2.scatter(title_length[i], price[i])
ax2.set_xlabel(' Title length ', size=12)
ax2.set_ylabel(' Price (¥) ', size=12)
add_regression_line(ax2, title_length[i], price[i], xytext=(20,8000))
plt.show()




