import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def setup(fname, city):
    '''
    takes .csv file name and extract the data based on the city
    
    :param fname: file name
    :type fname: str ending with '.csv'
    '''
    
    assert isinstance(fname,basestring)
    assert fname[-4:]=='.csv'
    
    data=pd.read_csv(fname)
    data_city = data[data.City == city].dropna(axis=0)
    data_city = data_city.reset_index(drop=True) 
    return data_city

def plot_each_zipcode(group_size, data, plot_name, starting_date):
    '''
    plot the house price for each zipcode with certain group size
    
    :param fname: the size of each group
    :type fname: int
    :param fname: data
    :type fname: dataframe
    :param fname: plot_name
    :type fname: string
    :param fname: the starting date of the plot
    :type fname: string with format date-month
    '''
    assert isinstance(group_size,int)
    assert isinstance(plot_name,list)
    assert isinstance(starting_date, str)
    assert isinstance(data, pd.DataFrame)
    
    for i in range(group):
        data_clip = data.iloc[i*5:i*5+5,:]
        data_clip = data_clip.set_index(data_clip.RegionName.values)
        idx = data.columns.get_loc(starting_date)
        data_plt = data_clip.iloc[:,idx:]
        plt.figure(i+1)
        data_plt.T.plot()
        filename = './Visualization/%s since %s' %(plot_name[i],starting_date)
        plt.savefig(filename)
        plt.close()
    

def linear_regression_prediction(data, start_date, end_date):
    '''
    using the linear regression to fit the house price in recent years
    and predict the future tendency
    
    :param fname: data
    :type fname: dataframe
    :param fname: the starting date of the plot
    :type fname: string with format date-month
    :param fname: the ending date of the plot
    :type fname: string with format date-month
    '''
    assert isinstance(start_date, str)
    assert isinstance(end_date, str)
    assert isinstance(data, pd.DataFrame)
    idx1 = data.columns.get_loc(start_date)
    idx2 = data.columns.get_loc(end_date)
    length = idx2 - idx1 + 1
    f = [[1,k] for k in range(length)]
    thetaset1,resd1,rank,s=np.linalg.lstsq(f,data.loc[0][idx1:].values)
    data_test = data.iloc[0,idx1:].T
    data_test = data_test.to_frame(name = None)
    x = np.arange(length)
    y = thetaset1[0]+thetaset1[1]*x
    data_test[1] = y
    data_test[0].plot(label='price')
    data_test[1].plot(linestyle='--',label='linear regression')
    plt.legend()
    plt.title('slope for zip({}) is {}'.format(data.RegionName[0],thetaset1[1]))
    plt.xlabel(u'year-month')
    plt.ylabel(u'price')
    plt.savefig('./Visualization/Linear regression prediction from %s to %s' %(start_date, end_date))
    plt.close()
#     plt.show() 
    
    slope=[]
    for i in range(len(data)):
        theta,resd1,rank,s=np.linalg.lstsq(f,data_sd.loc[i][idx1:].values)
        slope.append(theta[1]/theta[0]*12)
    print 'The max slope is {}, and its zipcode is {}'.format(max(slope),data_sd.RegionName.values[slope.index(max(slope))])
    print thetaset1[0]+thetaset1[1]*0
    return slope

def plot_data(data,slope,starting_date):
    '''
    Plot the increasing rate of house price in different zipcode, based on calculated slope value
    
    :param fname: data
    :type fname: dataframe
    :param fname: slope
    :type fname: list of integer
    :param fname: starting_date
    :type fname: string
    '''
    assert isinstance(data, pd.DataFrame)
    assert isinstance(slope, list)
    assert isinstance(starting_date, str)
    ind=range(len(data))
    plt.figure(figsize=(20,10))
    barlist = plt.bar(ind,slope,0.5)
    idx = slope.index(max(slope))
    barlist[idx].set_color('r')
    plt.xticks(ind,data.RegionName.values,rotation=-60)
    plt.xlabel(u'Zip Code in San Diego City')
    plt.ylabel(u'Increasing rate from LR')
    name = './Visualization/zip code vs increasing Rate since %s'%(starting_date)
    plt.title(name)
    plt.savefig(name)
    plt.close()
    
data_sd = setup('../Data/Zip_Zhvi_AllHomes.csv', 'San Diego')
# gounp zipcode with size 5
group_size = 5
group = len(data_sd)/group_size + 1
print group
plot_name = ["real_estate_price_for_92109_92154", "real_estate_price_for_92105_92130", 
    "real_estate_price_for_92037_92116", "real_estate_price_for_92127_92108", 
    "real_estate_price_for_92131_92139", "real_estate_price_for_92119_92121"]

plot_each_zipcode(group_size, data_sd, plot_name, '2010-08')
plot_each_zipcode(group_size, data_sd, plot_name, '1996-07')

# calcualate the slope for the line in our linear regression model
slope1 = linear_regression_prediction(data_sd, '1996-04', '2018-01')
slope2 = linear_regression_prediction(data_sd, '2010-08', '2018-01')

# find one zipcode with largest investment value
plot_data(data_sd,slope1, '1996-04')
plot_data(data_sd,slope2, '2010-08')