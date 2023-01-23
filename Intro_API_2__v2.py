#!/usr/bin/env python
# coding: utf-8

# <p style="text-align:center">
#     <a href="https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0101ENSkillsNetwork1005-2022-01-01" target="_blank">
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo"  />
#     </a>
# </p>
# 
# # Application Programming Interface
# 
# 
# Estimated time needed: **15** minutes
#     
# 
# ## Objectives
# 
# After completing this lab you will be able to:
# 
# * Create and Use APIs in Python
# 

# 
# ### Introduction
# 
# An API lets two pieces of software talk to each other. Just like a function,  you don’t have to know how the API works only its inputs and outputs.  An essential type of API is a REST API that allows you to access resources via the internet. In this lab, we will review the Pandas Library  in the context of an API, we will also review a basic REST API  
# 

# ## Table of Contents
# <div class="alert alert-block alert-info" style="margin-top: 20px">
# <li><a href="#ref0">Pandas is an API</a></li>
# <li><a href="#ref1">REST APIs Basics  </a></li>
# <li><a href="#ref2">Quiz on Tuples</a></li>
# 
# </div>
# 
# <hr>
# 

# In[1]:


get_ipython().system('pip install pycoingecko')
get_ipython().system('pip install plotly')
get_ipython().system('pip install mplfinance')
get_ipython().system('pip install --upgrade nbformat')


# <h2 id="PandasAPI">Pandas is an API </h2>
# 

# Pandas is actually set of software components , much of  which is not even written in Python.
# 

# In[5]:


import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
import matplotlib.pyplot as plt
import datetime
from pycoingecko import CoinGeckoAPI
from mplfinance.original_flavor import candlestick2_ohlc


# You create a dictionary, this is just data.
# 

# In[6]:


dict_={'a':[11,21,31],'b':[12,22,32]}


# When you create a Pandas object with the Dataframe constructor in API lingo, this is an "instance". The data in the dictionary is passed along to the pandas API. You then use the dataframe to communicate with the API.
# 

# In[7]:


df=pd.DataFrame(dict_)
type(df)


# <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0101EN-SkillsNetwork/labs/Module%205/images/pandas_api.png" width="800," align="center" alt="logistic regression block diagram">
# 

# When you call the method head the dataframe communicates with the API displaying the first few rows of the dataframe.
# 
# 
# 

# In[8]:


df.head()


# When you call the method mean,the API will calculate the mean and return the value.
# 

# In[9]:


df.mean()


# <h2 id="ref1">REST APIs</h2>
# 

# Rest API’s function by sending a request,  the request is communicated via HTTP message. The HTTP message usually contains a JSON file. This contains instructions for what operation we would like the service or resource to perform. In a similar manner, API returns a response, via an HTTP message, this response is usually contained within a JSON.
# 
# In cryptocurrency a popular method to display the movements of the price of a currency.
# 
# ![Example Candlestick Graph](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0101EN-SkillsNetwork/labs/Module%205/candlestick.png)
# 
# Here is a description of the candle sticks.
# 
# <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0101EN-SkillsNetwork/labs/Module%205/explanation.png" alt="Candle Stick Definition" width="800" height="600">
# 
# In this lab, we will be using the <a href=https://www.coingecko.com/en/api?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0101ENSkillsNetwork1005-2022-01-01>CoinGecko API</a> to create one of these candlestick graphs for Bitcoin. We will use the API to get the price data for 30 days with 24 observation per day, 1 per hour. We will find the max, min, open, and close price per day meaning we will have 30 candlesticks and use that to generate the candlestick graph. Although we are using the CoinGecko API we will use a Python client/wrapper for the API called <a href=https://github.com/man-c/pycoingecko>PyCoinGecko</a>. PyCoinGecko will make performing the requests easy and it will deal with the enpoint targeting.
# 

# Lets start off by getting the data we need. Using the <code>get_coin_market_chart_by_id(id, vs_currency, days)</code>. <code>id</code> is the name of the coin you want, <code>vs_currency</code> is the currency you want the price in, and <code>days</code> is how many days back from today you want.
# 

# In[10]:


cg = CoinGeckoAPI()

bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=30)


# In[11]:


type(bitcoin_data )


# The response we get is in the form of a JSON which includes the price, market caps, and total volumes along with timestamps for each observation. We are focused on the prices so we will select that data.
# 

# In[12]:


bitcoin_price_data = bitcoin_data['prices']

bitcoin_price_data[0:5]


# Finally lets turn this data into a Pandas DataFrame.
# 

# In[13]:


data = pd.DataFrame(bitcoin_price_data, columns=['TimeStamp', 'Price'])


# Now that we have the DataFrame we will convert the timestamp to datetime and save it as a column called <code>Date</code>. We will map our <code>unix_to_datetime</code> to each timestamp and convert it to a readable datetime.
# 

# In[15]:


data['date'] = data['TimeStamp'].apply(lambda d: datetime.date.fromtimestamp(d/1000.0))


# Using this modified dataset we can now group by the <code>Date</code> and find the min, max, open, and close for the candlesticks.
# 

# In[16]:


candlestick_data = data.groupby(data.date, as_index=False).agg({"Price": ['min', 'max', 'first', 'last']})


# Finally we are now ready to use plotly to create our Candlestick Chart.
# 

# In[17]:


fig = go.Figure(data=[go.Candlestick(x=candlestick_data['date'],
                open=candlestick_data['Price']['first'], 
                high=candlestick_data['Price']['max'],
                low=candlestick_data['Price']['min'], 
                close=candlestick_data['Price']['last'])
                ])

fig.update_layout(xaxis_rangeslider_visible=False)

fig.show()


# ## Authors:   
# 
# 
# ## Change Log
# 
# 
# |  Date (YYYY-MM-DD) |  Version | Changed By  |  Change Description |
# |---|---|---|---|
# | 2020-11-23 | 3.0 | Azim Hirjani | New API |
# | 2020-09-09 | 2.1 | Malika Singla | Spell Check |
# | 2020-08-26  | 2.0  | Lavanya | Moved lab to course repo in GitLab |
# |   |   |   |   |
# 
# 
# 
# 
# <hr/>
# 
# ## <h3 align="center"> © IBM Corporation 2020. All rights reserved. <h3/>
# 

# In[ ]:





# In[ ]:




