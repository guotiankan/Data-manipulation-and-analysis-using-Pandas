#!/usr/bin/env python
# coding: utf-8

# <a>Part A</a>

# Setup environment 

# In[1]:


import numpy as np
import os 
import pandas as pd
import re
import matplotlib.pyplot as plt


# Let's first set up variables for the function.
# <br>
# Then use for-loop to create a list than contains all results.
# <br>
# Because the required output uses fixed input, there is no need to create a class or function.
# <br>
# Using fixed parameters and inputs is the most efficient way to solve the question.

# In[2]:


#Parameters a b c:
a = 35.74
b = 0.6215
c = 0.4275

#Exponential factor e:
e = 0.16

#Create a temporary list ans to gather output
ans = []

#Use numpy to create the list of all temperatures and windspeed
temp = np.arange(-20,51,10)
windspeed = np.arange(0,51,5)

#Write each result from the function into the list
for i in windspeed:
    for v in temp:
        num = a + (b * v) - (a*(i ** e)) + (c * v * (i ** e))
        ans.append(float("{0:.2f}".format(num)))   


# The required output format can be archived most easily using pandas dataframe.
# <br>
# It is easier to create a pandas data frame using numpy array.
# <br>
# Use numpy to convert and reshape the list to an array that contains each row as a list and ready for dataframe.
# <br>
# Then create a dataframe.

# In[3]:


nplist = np.asarray(ans)
nplist = np.reshape(nplist,(len(windspeed), len(temp)))
df = pd.DataFrame(nplist, index = windspeed, columns = temp)
df


# <a>Part B i<a/>

# Again, check my working directory so that I know where to place the data files and avoid coding exact directory of files

# In[4]:


pwd


# Read data files seperately

# In[5]:


airline = pd.read_csv('airlines.csv')
airport = pd.read_csv('airports.csv')
flight = pd.read_csv('flights.csv')
plane = pd.read_csv("planes.csv")
weather = pd.read_csv("weather.csv")


# Print the number of rows in each file

# In[6]:


print("number of rows in airlines file: ",len(airline))
print("number of rows in airport file: ", len(airport))
print("number of rows in flights file: ", len(flight))
print("number of rows in planes file: ", len(plane))
print("number of rows in weather file: ", len(weather))


# <a>Part B ii</a>

# To determine delay, let's first look into datas

# In[7]:


airport.head()


# No useful info in airport data, check flight data

# In[8]:


flight.head()


# In[9]:


flight.describe()


# dep_delay and carrier are what we need to plot histogram

# Histogram using pandas

# We need to group the data by carrier first, then plot histogram for each carrier's dep_delay. I gonna normalize the data instead of using frequency so it's easier to understand which airline is good at on-time departure.
# <br>
# I am not sure if negative dep_delay time is counted as on-time departure as well because the question did not specify whether early departure is counted as on-time or not.
# <br>
# I will look into both conditions.

# Situation when negative dep_delay is not treated as on-time departure.
# <br>
# I use normal distribution histogram for this situation.

# In[10]:


flight.groupby('carrier').hist('dep_delay', figsize = (10,10), 
                               density = True, sharex = False, sharey = False, bins = 100)


# Looks like WN is the best when we don't consider negative dep_delay as on-time departure.
# <br>
# 

# Now let's look into situation where negative dep_delay (early departure) count as on-time departure as well. 
# <br>
# To do so, use CDF instead of PDF.
# 

# In[11]:


flight.groupby('carrier').hist('dep_delay', figsize = (10,10), 
                               density = True, sharex = False, sharey = False, bins = 200, cumulative = True)


# If we consider negative dep_delay as well, HA is the best in terms of on-time departure

# Histograms using matplotlib

# In[12]:


from matplotlib import pyplot as plt


# From previouse histogram we can know that there are 16 different carrier

# I will use a for loop to iternate on the carrier name list to subplot every carrier's histogram 
# <br>
# Situation where negative dep_delay is not on-time departure.

# In[13]:


'''
Matplotlib seems require us to subplot each group of data manually, 
so let's create a list that contains each carrier's code for the for loop
'''
carrierlist = flight.carrier.unique()
carrierlist

'''
The last argument in the subplot() tells pyplot which plot is processing right now, 

Starts from 1 and ends at length of carrier,

We can use enumerate() function to get the index of each carrier in our list.

enumerate(list) will make the list similar to a dictionary, the key is the index and the value is the element in the list

Because Python starts with 0, we should use n+1 for the subplot() argument
'''
plt.figure(dpi = 128, figsize = (25,25))
for n, i in enumerate(carrierlist):
    plt.subplot(4,4,n+1)
    plt.hist(flight.dep_delay[flight.carrier == i], bins = 100, density = True)
    plt.title(i)
    plt.xlabel("Delay(min)")
    plt.ylabel("Frequency as density")
    plt.grid(True, color = 'gray', linestyle = '-')

plt.tight_layout()
plt.show()       


# WN is the best on on-time departure again.

# Situation where negative dep_delay is on-time.

# In[14]:


plt.figure(dpi = 128, figsize = (25,25))
for n, i in enumerate(carrierlist):
    plt.subplot(4,4,n+1)
    plt.hist(flight.dep_delay[flight.carrier == i], bins = 100, density = True, cumulative = True)
    plt.title(i)
    plt.xlabel("Delay(min)")
    plt.ylabel("Frequency as density")
    plt.grid(True, color = 'gray', linestyle = '-')

plt.tight_layout()
plt.show()       


# HA is the best

# Part B iii

# In[15]:


flight.head(5)


# The inter arrival time should be the time gap between each arr_time for each airpot.
# <br>
# Let's first create a data frame slice that contains top5 busiest airport.
# <br>
# We can identify airport's volume by counting the number of flight's destination for each airport.

# Let's first create a seperate data frame for top 5 airports only 

# To avoid entering each airport's code manually for filtering and slicing dataframe, we can use pd.concat() function with a simple for-loop for searching and filtering by airport's code 

# In[16]:


flight1 = pd.DataFrame(pd.concat([flight[flight.dest == i]
                                  for i in list(flight['dest'].value_counts().nlargest(5).index)], ignore_index = True))
flight1


# Let's check if the above code is returning a dataframe that contains top 5 airports only

# In[17]:


check = flight1.dest.unique()
answer = flight['dest'].value_counts().nlargest(5).index
check == answer


# The new data frame we created correctly contains all top 5 airports. Now let's calculate the inter arrival time.
# <br>
# Not 100% sure which method is asked. First: Time difference between each arrival. Second: Time difference between each unique arrival.
# <br>
# The new data frame we created is already grouped and since we append each sorted group of airports seperately.
# 

# There are a lot of NaN in the data which will affect the axis range of our histogram. Let's create a new copy of flight1 without NaN.

# In[18]:


flight1 = flight1.dropna(subset = ['arr_time'])
flight1.isna()['arr_time'].unique()


# In[19]:


flight1[flight1.sched_arr_time <= 100][['sched_arr_time','time_hour','day']]


# There is a problem. Some flights arrive at next day while all date datas in the data file are recorded for departure date.
# <br>
# We need to create an arrival date in order to plot properly.

# Flights arrive at next day will have a dep_time greater than arr_time.
# <br><br>
# We know from the .describe() function that dep_time and arr_time are all int, therefore can be subtracted or added directly.
# <br><br>
# First let's create a new column called date. Then we fill up the date column by concating column year, month, and day.
# <br>
# Then, if the dep_time is greater than arr_time, we add one day for the date data.
# <br>
# Plus, if the arr_time is 2400.0, we also add one day for the date data.

# In[20]:


import datetime


# Converting the string into date will automatically format month and day into two digit format.

# In[21]:


flight1['date'] = flight1['year'].astype(str) + '-' + flight1['month'].astype(str) + '-' + flight1['day'].astype(str)
flight1['date'] = flight1['date'].astype('datetime64[ns]')
flight1['date']


# If dep_time > arr_time, plus one day for date.

# In[22]:


for i in range(len(flight1)):
    if flight1.iloc[i,4] > flight1.iloc[i,7]:
        flight1.iloc[i,int(flight1.columns.get_loc('date'))] = flight1.iloc[i,int(flight1.columns.get_loc('date'))] + datetime.timedelta(days = 1)


# If arr_time is 2400.0, also plus one day.

# In[23]:


for i in range(len(flight1)):
    if flight1.iloc[i, 7] == 2400.0:
        flight1.iloc[i,int(flight1.columns.get_loc('date'))] = flight1.iloc[i,int(flight1.columns.get_loc('date'))] + datetime.timedelta(days = 1)


# Hour and minutes data are harder to convert because some arr_time does not include hour at all.
# <br>
# First we need to create a new column arr_time1, then clean up the format.
# <br>
# Then we seperate the arr_time1 into hour and minute.
# <br>

# In[24]:


flight1['arr_time1'] = flight1['arr_time'].astype(int)
flight1.columns.get_loc('arr_time1')


# In[25]:


for i in range(len(flight1)):
    if flight1.iloc[i,21] < 10:
        flight1.iloc[i,21] = '000' + str(flight1.iloc[i,21])
    elif flight1.iloc[i,21] < 100:
        flight1.iloc[i,21] = '00' + str(flight1.iloc[i,21])
    elif flight1.iloc[i,21] < 1000:
        flight1.iloc[i,21] = '0' + str(flight1.iloc[i,21])
    else:
        continue


# In[26]:


flight1['hour'] = flight1['arr_time1'].astype(str).str[0:2]


# In[27]:


flight1.columns.get_loc('hour')


# In[28]:


for i in range(len(flight1)):
    if flight1.iloc[i,17] == '24':
        flight1.iloc[i,17] = '00'


# In[29]:


flight1['minute'] = flight1['arr_time1'].astype(str).str[2:4]


# Create a complete date data with hour, minute, and second.

# In[30]:


flight1['date2'] = flight1['date'].astype(str) + '-' + flight1['hour'].astype(str) + '-' + flight1['minute'].astype(str) + '-' + '00'


# In[31]:


flight1['date2'] = pd.to_datetime(flight1.date2, format = '%Y-%m-%d-%H-%M-%S')


# Sort data by dates within each group of airport.

# In[32]:


for i in list(flight1.dest.unique()):
    flight1[flight1.dest == i] = flight1[flight1.dest == i].sort_values('date2')


# Calculate time difference.

# In[33]:


flight1['inter'] = flight1['date2'].diff()


# Plot

# In[35]:


plt.figure(dpi = 128, figsize = (25,25))
carrierlist5 = list(flight1.dest.unique())
for n, i in enumerate(carrierlist5):
    plt.subplot(3,2,n+1)
    plt.hist(flight1[flight1.dest == i]['inter'].astype(str), bins = 1000)
    plt.title(i)
    plt.xlabel("Inter arrival time")
    plt.ylabel("Frequency")

plt.tight_layout()
plt.show() 

