
# coding: utf-8

import matplotlib.pyplot as plt
import csv
import numpy as np
import collections as c

#####open file#####
def openfile(filename):
    content = []
    with open(filename, 'r') as csvfile:
        r = csv.reader(csvfile)
        for row in r:
            content.append(row)
    return content

sources = ['../Data/City_Zri_AllHomes.csv', 
           '../Data/Zip_Zri_AllHomes.csv',
           '../Data/Zip_Zhvi_AllHomes.csv',
           '../Data/City_Zhvi_AllHomes.csv']

##clean up the data
datafiles = c.defaultdict(list)
for source in sources:
    datafiles[source] = openfile(source)

def get_month_keys(keys):
    return keys[-70:]

def get_attr(keys):
    return keys[:6]

months = get_month_keys(datafiles['../Data/City_Zri_AllHomes.csv'][0])
attr = get_attr(datafiles['../Data/Zip_Zhvi_AllHomes.csv'][0])
##construct new key list
keys= attr + months

def form_list(keys, content, index = 6):
    ls = []
    for line in content:
        temp= {}
        for key, val in zip(keys[:index], (line[:index])):
            temp[key] = val
        for key, val in zip(keys[index:], (line[-70:])):
            temp[key] = val
        ls.append(temp)
    return ls

# form dictioanries of necessary attributes
def preprocess_data(keys, datafiles):
    dataset = {}
    for i in datafiles:
        print(i)
        dataset[i] = form_list(keys, datafiles[i][1:])
    return dataset

########reconstruct the dataset
dataset = preprocess_data(keys, datafiles)

######## convert string to floats for the rent,
def astype_float(dataset, months):
    for i in dataset:
        ls = dataset[i]
        for d in ls:
            for m in months:
                if d[m]=='':
                    d[m] = float(d[months[months.index(m)-1]])
                else:
                    d[m] = float(d[m])
    return dataset
dataset = astype_float(dataset, months)

##acquire different data
def get_data(category, dataset, s = sources):
    if category == 'zip_rent':
        return dataset[s[1]]
    elif category == 'zip_home':
        return dataset[s[2]]
    elif category == 'city_home':
        return dataset[s[3]]
    else:
        return dataset[s[0]]

## plot rent/price change over years
#############check the rent change over months for other cities ############
def calc_average(name, dataset, m = months, excludes = 'San Diego'):
    month_average = []
    for month in m:
        month_average.append(np.mean([i[month] for i in get_data(name, dataset) if i['City'] != excludes]))
    return month_average

home_month_average = calc_average('zip_home', dataset)
rent_month_average = calc_average('zip_rent', dataset)

# record areas to show on the graph
sd =[92101,92037, 92109, 92122]

def get_plotdata(name, county, dataset, s = source, selection_zip = sd):
    data = get_data(name, dataset)
    target_areas = [d for d in data if d['City'] == county and int(d['RegionName']) in selection_zip]
    target_index = [data.index(d) for d in target_areas]
    target_months = [[d[month] for month in months] for d in target_areas]
    return target_areas, target_months, target_index

##### form data of san diego areas from the dataset
sd_areas, sd_months, sd_indices = get_plotdata('zip_home', 'San Diego', dataset)
sd_areas_rent, sd_months_rent, sd_indices_rent = get_plotdata('zip_rent', 'San Diego', dataset)

def plot_month_price(name, target_areas, target_months, target_index, month_average, m = months):
    plt.title('average %s with months in cities in USA vs. San Diego'%name)
    r = month_average
    x = range(len(m))
    plt.plot(x,r,'bo')
    legend = []
    for i in target_months:
        pid = target_areas[target_months.index(i)]['RegionName']
        plt.plot(x,i,label=pid)
    plt.legend(bbox_to_anchor=(0.9, 1), loc=2, borderaxespad=0.)
    i_min = r.index(min(r))
    i_max = r.index(max(r))
    plt.plot(i_min, min(r), marker = 's')
    plt.plot(i_max, max(r), marker = 's')
    frame = plt.gca()
    ### hide the x values
    frame.axes.get_xaxis().set_ticks([])
    plt.xlabel("months from 2012 to 2018")
    plt.ylabel("average %s of other cities vs san diego"%name)
    plt.show()

### plot for both rent and home values
plot_month_price('home val', sd_areas, sd_months, sd_indices, home_month_average)
plot_month_price('rent', sd_areas_rent, sd_months_rent, sd_indices_rent, rent_month_average)

################ plot counties
def getCounties(dataset, file):
    data = get_data(file, dataset)
    return list(set([d['CountyName'] for d in data]))

counties = getCounties(dataset, 'zip_rent')
len(counties)

def formNewData(file, dataset, m = months, c = counties):
    data = get_data(file, dataset)
    new_data=[]
    for i in c:
        temp = [d for d in data if d['CountyName'] == i]
        rent = sum([d[months[-1]] for d in temp])/len(temp)
        new_data.append({'CountyName': i, 'Rent': rent})
    return new_data

new_data = formNewData('zip_rent', dataset)
targets = ['San Diego', 'New York', 'Santa Clara', 'San Francisco']

def plot_counties(category, new_data, c_list, m = months):
    selected_month1 = m[-1]
    rent = [d['Rent'] for d in new_data]   
    plt.plot(rent, 'yo')
    ls  = []
    for i in c_list:
        ls.append([d for d in new_data if d['CountyName'] == i])

    markers_on = [i[0] for i in ls]
    legend=[]
    for i,name in zip(markers_on, c_list):
        plt.plot(new_data.index(i),rent[new_data.index(i)],  marker = '^', label = name)
        legend.append(name)
    plt.legend(bbox_to_anchor=(0.9, 1), loc=2, borderaxespad=0.)
    plt.title('%s comparison among all recorded cities in USA for %s'%(category,selected_month1))
    frame = plt.gca()
    ### hide the x values
    frame.axes.get_xaxis().set_ticks([])
    plt.xlabel("all counties")
    plt.ylabel("average %s"%category)
    plt.show()

plot_counties('zip_rent', new_data, targets)




