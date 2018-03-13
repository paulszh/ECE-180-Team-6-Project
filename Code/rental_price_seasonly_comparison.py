'''
In this file, we are looking at the median prices for each season, 
where winter is (December, Januaray, February), spring is (March, 
April, May), summer is (June, July, August), and fall is (September, October, 
November).

We will plot each type of room(one bedroom, two bedroom, three bedroom) 
seperately. At the end, we will display the statitical value we calculated for 
each season and room type 

At the end, we will focus on the data in two nearest zipcode close to the campus, 
92037 and 92122. We will use the data in the recent 7 years(from 2011 to 2018) and 
see the change of monthly rental price change within the same year. 

We will also plot how many times the rental price in a month exceeds the average 
rental price of the year. For example, we found that, there are 6 times in seven years, 
the rental price in June and August exceeds the year average. This indicates the price
for those two months tends to be higher. Thus, we suggest people to avoid those two
months

All the plots can be found in the "visualiztion" folder
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import subplots
import calendar

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
def zipsetup(df, zips):
    '''
    reducing dataframe rows to only include the ones
    whose RegionNames are found 'zips'
    once again, drop any remaining columns with all NaN values
    
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

def plotseasons(df):
    '''
    separate the columns in df by its season
    and then plot the mean square feet price
    of each month
    
    :param:  df
    :type: dataframe
    '''
    
    assert isinstance(df,pd.DataFrame)
    winter=[]
    spring=[]
    summer=[]
    fall=[]
    
    for col in df:
        #2-digit month
        month=col[-2:]
        if month in ['12','01','02']:
            winter.append(col)
        elif month in ['03','04','05']:
            spring.append(col)
        elif month in ['06','07','08']:
            summer.append(col)
        elif month in ['09','10','11']:
            fall.append(col)
            
    dflist=[df[winter],df[spring],df[summer],df[fall]]
    i=j=0
    
    for season in dflist:
        assert isinstance(dflist[i],pd.DataFrame)
        for row in range(len(season.mean())):
            axes[i,j].bar(row,season.mean()[row])

        months=list(season)        
        axes[i,j].set_xticks(range(len(months)))
        axes[i,j].set_xticklabels(i for i in months)
        axes[i,j].set_ylabel('price per sq ft($)')
        axes[i,j].grid(color='k', linestyle='-', linewidth=0.25)

        for tick in axes[i,j].get_xticklabels():
            tick.set_rotation(90)
            
        j+=1
        if j==2:
            j=0
            i=1
def getstats(dflist, zips):
    '''
    get all statistical data for all previously
    plotted series lists
    
    :param:  dflist
    :type: list of dataframes
    :param:  zips
    :type: list of integer 5-digt zip codes
    '''

    for df in dflist:
        assert isinstance(df,pd.DataFrame)
        winter=[]
        spring=[]
        summer=[]
        fall=[]
        for col in df:
            #2-digit month
            month=col[-2:]
            if month in ['12','01','02']:
                winter.append(col)
            elif month in ['03','04','05']:
                spring.append(col)
            elif month in ['06','07','08']:
                summer.append(col)
            elif month in ['09','10','11']:
                fall.append(col)

        print 'winter data:'
        print df[winter].mean().describe()
        print '\n'
        print 'spring data:'
        print df[spring].mean().describe()
        print '\n'
        print 'summer data:'
        print df[summer].mean().describe()
        print '\n'
        print 'fall data:'
        print df[fall].mean().describe()
        print '\n'
        df=zipsetup(df,zips)
        
#create a large 2x2 matplotlib subplot
fig1,axes = subplots(2,2)
fig1.set_size_inches(20, 20)
#see seasonal mean prices for all One Bedroom Homes
file1 = '../Data/Median Rent Price per sq ft 1 Bedrm.csv'
file2 = '../Data/Median Rent Price per sq ft 2 Bedrm.csv'
file3 = '../Data/Median Rent Price per sq ft 3 Bedrm.csv'
df1=setup(file1)
plotseasons(df1)
axes[0,0].set_title('One Bedroom Mean Winter Prices')
axes[0,1].set_title('One Bedroom Mean Spring Prices')
axes[1,0].set_title('One Bedroom Mean Summer Prices')
axes[1,1].set_title('One Bedroom Mean Fall Prices')
# plt.show()
# plt.gcf().clear()
fig1.savefig('./Visualization/median_price_comparsion_for_1_bedroom_in_different_seasons')
plt.gcf().clear()

#do the same for two bedroom 
fig2,axes = subplots(2,2)
fig2.set_size_inches(20, 20)

df2=setup(file2)
plotseasons(df2)
axes[0,0].set_title('Two Bedroom Mean Winter Prices')
axes[0,1].set_title('Two Bedroom Mean Spring Prices')
axes[1,0].set_title('Two Bedroom Mean Summer Prices')
axes[1,1].set_title('Two Bedroom Mean Fall Prices')
fig2.savefig('./Visualization/median_price_comparsion_for_2_bedroom_in_different_seasons')
plt.gcf().clear()
#do the same for three bedroom 
fig3,axes = subplots(2,2)
fig3.set_size_inches(20, 20)

df3=setup(file3)
plotseasons(df3)
axes[0,0].set_title('Three Bedroom Mean Winter Prices')
axes[0,1].set_title('Three Bedroom Mean Spring Prices')
axes[1,0].set_title('Three Bedroom Mean Summer Prices')
axes[1,1].set_title('Three Bedroom Mean Fall Prices')
fig3.savefig('./Visualization/median_price_comparsion_for_3_bedroom_in_different_seasons')
# plt.show()
plt.gcf().clear()

# get statical result using the getstats method
dflist=[df1,df2,df3]
zips=commonzips(dflist)
dflist=[df1, df2, df3]
getstats(dflist, zips)


r=pd.read_csv('../Data/rent_all.csv')
r=r.set_index('RegionName')
r=r.loc[[92037,92122],'2011-01':'2017-12']
print r.loc[92122,'2011-01']
data=np.zeros([7,12])
for i in range(7):
    for j in range(12):
        mon=str(2011+i)+'-'+'%02d'%(j+1)
        data[i,j]=r.loc[92122,mon]
        
avg=np.sum(data,1)/12

lar_num=np.zeros(12)
for i in range(7):
    for j in range(12):
        if data[i,j]>=avg[i]:
            lar_num[j]=lar_num[j]+1
            
# Montly price comparison in past 7 years
df = pd.DataFrame(data, index=range(2011,2018), columns=calendar.month_name[1:])
fig = plt.figure(figsize=(20,10)) 
df.T.plot()
plt.legend(bbox_to_anchor=(1.0, 0.4))
plt.legend(loc = 'upper left')
plt.xticks(range(12),calendar.month_name[1:],rotation=45, fontsize = 8)
plt.title('montly price among 12 months in recent 7 years')
plt.xlabel('months')
plt.ylabel('median rent price($/sqft)')
plt.savefig('./Visualization/monthly_price_comparsion')
plt.close()
# plot how many times the rental price in a month exceeds the average 
# rental price of the year
plt.bar(range(12),lar_num)
plt.xticks(range(12),calendar.month_name[1:],rotation=45)
plt.xlabel('months')
plt.ylabel('number of years over average')
plt.title('How many times in 7 years does the month rental price exceeds yearly average')
plt.ylim(0,7)
plt.savefig('./Visualization/couting_number_of_times_montly_price_exceeds_average_rental_price')



