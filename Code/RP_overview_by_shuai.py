
'''
use matplotlib to show the average monthly change of rent and home values
in the country (presented by different areas with teh highlghts of couple areas
in San Diego). We also plot the rent of different areas in one month
specifically to showcase where san diego is located among all other cities (
some areas like Santa Clara and San Francisco and etc are also highlighted for
comparison purpose.) 
'''

import matplotlib.pyplot as plt
import csv
import numpy as np
import collections as c

#####open file#####
def openfile(filename):
	'''
	open and read the file into the list

	:param filename: name of the file
	:type filename: str with the postfix .csv representing csv file
	'''
	assert isinstance(filename, str)
	assert filename[-4:] == '.csv'

    content = []
    with open(filename, 'r') as csvfile:
        r = csv.reader(csvfile)
        for row in r:
            content.append(row)
    return content


#open and read different files and store the data into data structures
# zri as rent data
# zhvi as hoem value data
# zip contains zip code data while cicty does not
sources = ['../Data/City_Zri_AllHomes.csv', 
           '../Data/Zip_Zri_AllHomes.csv',
           '../Data/Zip_Zhvi_AllHomes.csv',
           '../Data/City_Zhvi_AllHomes.csv']
datafiles = c.defaultdict(list)
for source in sources:
    datafiles[source] = openfile(source)


def get_month_keys(keys):
	'''
	keys are the different months, but for the purpose of the project,
	we only want the months with data. After viewing every months, we found
	that last 70 months over the course of roughly 6 years are good amount 
	of quality data

	:param keys: list of name of months
	:type keys: list	
	'''
	assert isinstance(keys, list)
	assert len(keys) >= 70
	for i in keys:                                                              
        assert isinstance(i, str) 
    return keys[-70:]


def get_attr(keys):
    '''                                                                            
    keys are the different atributes like region, counties, but for the 
	purpose of the project, we only want some of them, to name a few:
	RegionName, CountyName, Metro.                                                                
                                                                                   
    :param keys: list of name of attributes                                          
    :type  keys: list 
	'''
	assert isinstance(keys, list)
	assert len(keys) >= 5
	for i in keys:                                                              
        assert isinstance(i, str) 
    return keys[:6]

#combine the desire keys to form a new set of keys
months = get_month_keys(datafiles['../Data/City_Zri_AllHomes.csv'][0])
attr = get_attr(datafiles['../Data/Zip_Zhvi_AllHomes.csv'][0])
keys= attr + months


def form_list(keys, content):
	'''
	reform the dictioanry that incorporates the new set of keys
	
	:param keys: new set of keys
	:type keys: list
	
	:param content: a list of lists that contain info for each palce
	:type  content: a list of lists
	'''
	assert isinstance(keys, list)
	assert len(keys) == 75
	for i in keys:
		assert isinstance(i, str)
	assert isinstance(content, list)
	assert len(content) > 0
	for i in content:
		assert isinstance(i, list)
		assert len(i) > 0

    ls = []
    for line in content:
        temp= {}
        for key, val in zip(keys[:6], (line[:6])):
            temp[key] = val
        for key, val in zip(keys[6:], (line[-70:])):
            temp[key] = val
        ls.append(temp)
    return ls

def preprocess_data(keys, datafiles):
	'''
	for each of four files, we preprocess the data by move the data into the
	data structure and reform it in the preffered way using new keys
	
	:param keys: list of new keys
	:type keys: list
	
	:param datafiles: dictionary of files with value of its content
	:type datafiles: dictionary  
	'''	
	assert isinstance(keys, list)
	assert len(keys) > 0
	for i in keys:                                                              
		assert isinstance(i, str) 
	assert isinstance(datafiles, dict)
	for i in datafiles:                                                              
        assert isinstance(datafiles[i], list) 
		assert len(datafiles[i]) > 0

    dataset = {}
    for i in datafiles:
        print(i)
        dataset[i] = form_list(keys, datafiles[i][1:])
    return dataset
########reconstruct the dataset
dataset = preprocess_data(keys, datafiles)

def astype_float(dataset, months):
	'''
	cleaning up ther data: if there is empty, filled it with previous data
	else, convert the data to float for future computation
	
	:param dataset: the whole dataset loaded file after reformation
	:type dataset: dictionary

	:param months: a list of months
	:type months: list 
	'''	
	assert len(dataset) == 4
	assert isinstance(dataset, dict)
	for i in dataset:
		assert isinstance(i, list)
		assert len(i) > 0
	assert isinstance(months, list)
	assert len(months) == 70
	
    for i in dataset:
        ls = dataset[i]
        for d in ls:
            for m in months:
                if d[m]=='':
                    d[m] = float(d[months[months.index(m)-1]])
                else:
                    d[m] = float(d[m])
    return dataset
# covert the rent/price data to float for feture computation
dataset = astype_float(dataset, months)


def get_data(category, dataset, s = sources):
	'''
	find the data inside the data collection by specifying the type of the data
	
	:param category: type of data we want to get
	:type category: str
	
	:param dataset: a collection of 4 different dataset
	:type dataset: dicionary
	
	:param s: the key that directs to the data content
	:type s: list
	'''
	assert isinstance(s, list)
	assert len(s) > 0	
	assert isinstance(category, str)                                                  
    assert len(category > 0
	assert isinstance(dataset, dict)
	assert len(dataset) > 0
    for i in dataset:                                                           
        assert isinstance(i, list)                                              
        assert len(i) > 0 
	
    if category == 'zip_rent':
        return dataset[s[1]]
    elif category == 'zip_home':
        return dataset[s[2]]
    elif category == 'city_home':
        return dataset[s[3]]
    else:
        return dataset[s[0]]

######################process teh data for graph#########################
def calc_average(name, dataset, m = months, excludes = 'San Diego'):
	'''
	calculate the average that excludes certain area
	
	:param name: type of data, what data the user wants
	:type name: str

	:param months: a list of months
	:type months: list

	:param excludes: the arae that wants to be excluded in the calculation
	:type excludes: str
	'''
	assert isinstance(name, str)
	assert len(name) > 0 
    assert len(dataset) > 0                                                     
    for i in dataset:                                                           
        assert isinstance(i, list)                                              
        assert len(i) > 0    
	assert isinstance(m, list)
	assert len(m) > 0
	assert isinstance(excludes, str)
	assert len(excludes) > 0

    month_average = []
    for month in m:
        month_average.append(np.mean([i[month] for i in get_data(name, dataset) if i['City'] != excludes]))
    return month_average

home_month_average = calc_average('zip_home', dataset)
rent_month_average = calc_average('zip_rent', dataset)
# record areas to show on the graph
sd =[92101,92037, 92109, 92122]


def get_plotdata(name, county, dataset, selection_zip = sd):
    '''
	pot data for average over months for default areas, san diego areas
	
	:param name: name of the data wnated 
	:type name: str
	
	:param county: county name
	:type county: str
	
	:param dataset: a collection of data
	:type dataset: a dictionary that has filename as key and content as value
	
	:param selection_zip: the areas that are desired
	:type selection_zip: a list of strs
	'''	
	assert isinstance(name, str)
	assert len(name) > 0
	assert isinstance(county, str)
	assert len(county) > 0
    assert len(dataset) > 0                                                     
    for i in dataset:                                                           
        assert isinstance(i, list)                                              
        assert len(i) > 0 
	assert isinstance(selection_zip, list)
	assert len(selection_zip) > 0

	data = get_data(name, dataset)
    target_areas = [d for d in data if d['City'] == county and int(d['RegionName']) in selection_zip]
    target_index = [data.index(d) for d in target_areas]
    target_months = [[d[month] for month in months] for d in target_areas]
    return target_areas, target_months, target_index

##### form data of san diego areas from the dataset
sd_areas, sd_months, sd_indices = get_plotdata('zip_home', 'San Diego', dataset)
sd_areas_rent, sd_months_rent, sd_indices_rent = get_plotdata('zip_rent', 'San Diego', dataset)

def plot_month_price(name, target_areas, target_months, target_index, month_average, m = months):
	'''
	plot the data for average monthly change
	
	:param name: type of value -> home value or rent
	:type name: str
	
	:param target_areas: list of desired areas with highlight
		   target_months: list of months
		   target_index:  list of indices of the areas in the dataset for emphasis
	:type target_areas, target_months, target_index: list
	
	:param months_average: list of rent/home value over months
	:type months_average: list
	
	:param m: list of months
	:type m:list
	'''
	assert isinstance(name, str)
	assert len(name) > 0
	assert isinstance(target_areas, list)
	assert isinstance(target_months, list) 
	assert isinstance(target_index, list) 
	assert isinstance(target_months, list) 
	assert isinstance(m, list) 
	assert len(m) > 0 && len(month_average) > 0

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
data = get_data('zip_rent', dataset)
counties =  list(set([d['CountyName'] for d in data])) 

new_data=[]
for i in counties:
	temp = [d for d in data if d['CountyName'] == i]
    rent = sum([d[months[-1]] for d in temp])/len(temp)
    new_data.append({'CountyName': i, 'Rent': rent})

targets = ['San Diego', 'New York', 'Santa Clara', 'San Francisco']

def plot_counties(category, new_data, c_list, m = months):
	'''
	plot the rent for each county in last mointh 2018-01 with some
	highlights
	
	:param category: rent/home val
	:type category: str
	
	:param new_data: list of dictionary that stores county name and rent
	:type new_data: list of dictionary
	
	:param c_list: county list desired
	:type c_list: list
	
	:param m : months
	:type m: list
	'''
        assert isinstance(category, str)
	assert len(category) > 0
	assert isinstance(new_data, list)
	assert len(new_data) > 0
	assert isinstance(c_list, list)
	assert len(c_list) > 0
        assert isinstance(m, list)    
    assert len(m) > 0                                                      

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
