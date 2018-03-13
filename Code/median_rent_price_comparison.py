"""
Here, we are trying to visually analyze the median rent prices per square feet 
of different types of residences from various San Diego County Zip Codes. The 
data includes historical data on one to three bedroom homes as well as all condos
from within the past few years.

Some basic conclusions we can find right away is that the most expensive two zip 
codes in this subset are 92037 and 92019. As seen in the map(zip.png in visualization
folder), they correspond to the La Jolla area and Pacific Beach, respectively. In 
addition, there seems to be a slight overall increase in the average price over the 
years, with a fair amount of variance.

Then, we are going to figure out the influence of two factors on the housing rent price 
in 92037: the type of apartment and the month when someone starts his rent. The data 
we obtained contains 4 types of apartment: 1 bedroom, 2 bedrooms, 3 bedrooms and 
condo. However, we can only find the data for all four types of apartment from 2017-01 
to 2017-12. So we decide to analyze only the rent prices for year 2017. We hope that 
the result can offer some guideline for UCSD students on when and which type of apartment
is the cheapest for leasing.

All the plots can be found in the "visualiztion" folder
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import subplots
from IPython.display import Image

def setup(fname):
    '''
    takes .csv file name and reads it as a dataframe
    then sorts columns by Zip Code and replaces NaN
    values with 0
    
    :param fname: file name
    :type fname: str ending with '.csv'
    '''
    
    assert isinstance(fname,basestring)
    assert fname[-4:]=='.csv'
    
    df=pd.read_csv(fname)
    df=df.sort_values('RegionName')
    df=df.drop(['City', 'State', 'Metro', 'SizeRank', 'CountyName'],axis=1)
    return df

def filter_data_by_date(fname, start):
    '''
    takes .csv file name and reads it as a dataframe
    then extract the info based on given data
    
    :param fname: file name
    :type fname: str ending with '.csv'
    '''
    assert isinstance(fname,basestring)
    assert fname[-4:]=='.csv'
    df = pd.read_csv(fname)
    df = df.set_index('RegionName')
    df = df.loc[:,start:]
    return df

def commonzips(dflist):
    '''
    finds the common zip codes with data specified in all 
    the dataframes contained in a list given as an input
    
    :param:  dflist
    :type: list of dataframes
    '''
    
    assert isinstance(dflist, list)
    assert len(dflist) > 1
    
    ziplist=list(set(dflist[0].RegionName))
    for i in range(len(dflist)):
        assert isinstance(dflist[i],pd.DataFrame)
        ziplist=list(set(ziplist) & set(dflist[i].RegionName))
    ziplist.sort()
    return ziplist

def moresetup(df, zips):
    '''
    reducing dataframe rows to only include the ones
    whose zip codes are found in zips and also getting
    rid of columns that contain only NaN values
    
    :param:  df
    :type: dataframe
    :param: zips
    :type: list of integer 5-digit zip codes
    '''
    
    assert isinstance(df, pd.DataFrame) and isinstance(zips, list)
    for i in zips:
        assert 10000<=i<=99999
        
    df=df[df.RegionName.isin(zips)]
    df=df.dropna(axis=1, how='all')
    return df


def plotdata(dflist):
    '''
    create subplot figure then plot the values for
    each column in each dataframe in a given list
    also, set x-axis tick marks, a y-axis label,
    and a legend for each subplot
    
    :param:  dflist
    :type: list of dataframes
    '''
    assert isinstance(dflist, list)
    assert len(dflist) > 1
    
    i=0

    for df in dflist:
        assert isinstance(dflist[i],pd.DataFrame)
        x0=df.iloc[0,1:].tolist()
        x1=df.iloc[1,1:].tolist()
        x2=df.iloc[2,1:].tolist()
        x3=df.iloc[3,1:].tolist()
        x4=df.iloc[4,1:].tolist()
        x5=df.iloc[5,1:].tolist()

        months=list(df)[1:]
        axes[i].plot(x0)
        axes[i].plot(x1)
        axes[i].plot(x2)
        axes[i].plot(x3)
        axes[i].plot(x4)
        axes[i].plot(x5)
        
        axes[i].set_xticks(range(len(months)))
        axes[i].set_xticklabels(i for i in months)
        axes[i].set_ylabel('price per sq ft($)')
        axes[i].grid(color='k', linestyle='-', linewidth=0.25)
        axes[i].legend(zips,loc='best')
        for tick in axes[i].get_xticklabels():
            tick.set_rotation(90) 
        i+=1

#file names
file1 = '../Data/Median Rent Price per sq ft 1 Bedrm.csv'
file2 = '../Data/Median Rent Price per sq ft 2 Bedrm.csv'
file3 = '../Data/Median Rent Price per sq ft 3 Bedrm.csv'
file4 = '../Data/Median Rent Price per sq ft Condo.csv'

#pass each file through function to produce four dataframes
df1=setup(file1)
df2=setup(file2)
df3=setup(file3)
df4=setup(file4)

#make list of four dataframes and pass it to function
dflist=[df1,df2,df3,df4]
zips=commonzips(dflist)
#update each dataframe using this most recent function
df1=moresetup(df1,zips)
df2=moresetup(df2,zips)
df3=moresetup(df3,zips)
df4=moresetup(df4,zips)

#create a large-enough matplotlib subplot
dflist=[df1,df2,df3,df4]
fig,axes=subplots(len(dflist),1)
fig.set_size_inches(len(dflist)*5, len(dflist)*9)
#have to manually set titles
axes[0].set_title('One Bedroom Median Rent Prices')
axes[1].set_title('Two Bedroom Median Rent Prices')
axes[2].set_title('Three Bedroom Median Rent Prices')
axes[3].set_title('Condo Median Rent Prices')

plotdata(dflist)
fig.savefig('./Visualization/median_price_comparsion_for_each_bedroom_in_various_zipcode')

#plot a vertical bar plot to show rental price different across zipcodes
df_date = filter_data_by_date('../Data/rent_all.csv', '2017-01')
zipcodes = [str(i) for i in list(df_date.index.values)]

# calculate the average
data = df_date.as_matrix()
avg = np.mean(data,1)
std = np.std(data,1)
avg_all = np.mean(avg)
avg,zipcodes = zip(*sorted(zip(avg, zipcodes)))
fig,ax = subplots(figsize=(5,10))

b=ax.barh(range(46),avg,align="center")
b[42].set_color('r')
b[34].set_color('r')
b[44].set_color('r')
ax.set_yticks(range(46))
ax.set_yticklabels(zipcodes)
ax.vlines(avg_all,-0.5,45.5,linewidth=2, linestyle='dashed',color = 'y',label='Mean=1.94$/sqrt')
ax.set_ylim(-0.5,45.5)
ax.set_xlim(0,4.0)
ax.legend()
# plt.show()
fig.savefig('./Visualization/median_price_comparsion_for_each_zipcode_barplot')


# Explore the price for La Jolla 92037 for different rooms
index = ['RegionName','2017-01','2017-02','2017-03','2017-04','2017-05','2017-06',
         '2017-07','2017-08','2017-09','2017-10','2017-11','2017-12']
br1 = df1.loc[:, index]
br2 = df2.loc[:, index]
br3 = df3.loc[:, index]
condo = df4.loc[:, index]

data1 = br1.iloc[0,1:].tolist()
data2 = br2.iloc[0,1:].tolist()
data3 = br3.iloc[0,1:].tolist()
data4 = condo.iloc[0,1:].tolist()
months=list(br1)[1:]

fig = plt.figure(figsize=(16,8)) 

line1, = plt.plot(months, data1,color = 'b',label = '1 Bedroom')
line2, = plt.plot(months, data2,color = 'g',label = '2 Bedroom')
line2, = plt.plot(months, data3,color = 'r',label = '3 Bedroom')
line2, = plt.plot(months, data4,color = 'm',label = 'Condo')
plt.legend(loc = 'upper left')

plt.grid(True)
plt.xticks(rotation=45)
plt.title('median price per square for different kinds of bedroom in 92037')
plt.ylabel(u'price per square feet')
fig.savefig('./Visualization/median_price_comparsion_for_each_bedroom_in_92037')


# Explore the price for La Jolla 92109 for different rooms
index = ['RegionName','2017-01','2017-02','2017-03','2017-04','2017-05','2017-06',
         '2017-07','2017-08','2017-09','2017-10','2017-11','2017-12']
br1 = df1.loc[:, index]
br2 = df2.loc[:, index]
br3 = df3.loc[:, index]
condo = df4.loc[:, index]

data1 = br1.iloc[1,1:].tolist()
data2 = br2.iloc[1,1:].tolist()
data3 = br3.iloc[1,1:].tolist()
data4 = condo.iloc[1,1:].tolist()
months=list(br1)[1:]

fig = plt.figure(figsize=(16,8)) 

line1, = plt.plot(months, data1,color = 'b',label = '1 Bedroom')
line2, = plt.plot(months, data2,color = 'g',label = '2 Bedroom')
line2, = plt.plot(months, data3,color = 'r',label = '3 Bedroom')
line2, = plt.plot(months, data4,color = 'm',label = 'Condo')
plt.legend(loc = 'upper left')
plt.title('median price per square for different kinds of bedroom in 92109')
plt.grid(True)
plt.xticks(rotation=45)
plt.ylabel(u'price per square feet')
fig.savefig('./Visualization/median_price_comparsion_for_each_bedroom_in_92109')
