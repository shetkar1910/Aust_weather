# Modules
import streamlit as st
import requests
from datetime import datetime , timedelta
import pandas as pd
import matplotlib.pyplot as plt
import time 

# INSERT YOUR API  KEY WHICH YOU PASTED IN YOUR secrets.toml file 
api_key =  st.secrets["api_key"]

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
url_1 = 'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={}&lon={}&dt={}&appid={}'

# Function for LATEST WEATHER DATA
def getweather(city):
    result = requests.get(url.format(city, api_key))     
    if result:
        json = result.json()
        #st.write(json)
        country = json['sys']['country']
        temp = json['main']['temp'] - 273.15
        temp_feels = json['main']['feels_like'] - 273.15
        humid = json['main']['humidity'] - 273.15
        icon = json['weather'][0]['icon']
        lon = json['coord']['lon']
        lat = json['coord']['lat']
        des = json['weather'][0]['description']
        res = [country, round(temp,1),round(temp_feels,1),
                humid,lon,lat,icon,des]
        return res , json
    else:
        print("error in search !")

# Function for HISTORICAL DATA
def get_hist_data(lat,lon,start):
    res = requests.get(url_1.format(lat,lon,start,api_key))
    data = res.json()
    temp = []
    for hour in data["hourly"]:
        t = hour["temp"]
        temp.append(t)     
    return data , temp

# Let's write the Application

st.header('Australia Weather Report')   
st.info('Rainy Drizzle App')

im1,im2 = st.columns(2)
with im2:  
    image0 = 'aust2.jpg' 
    st.image(image0,use_column_width=True,caption = 'Plan your Vacation , Pack your bags and Lets Go.')
with im1:    
    image1 = 'aust.jpg'
    st.image(image1, caption='Australia map Image.',use_column_width=True)

col1, col2 = st.columns(2)

with col1:
    city_name = st.text_input("Enter a city name")
    #show_hist = st.checkbox('Show me history')
with col2:  
		if city_name:
                       res , json = getweather(city_name)
                       #st.write(res)
                       st.success('Current: ' + str(round(res[1],2)))
                       st.info('Feels Like: ' + str(round(res[2],2)))
                       #st.info('Humidity: ' + str(round(res[3],2)))
                       st.subheader('Status: ' + res[7])
                       web_str = "![Alt Text]"+"(http://openweathermap.org/img/wn/"+str(res[6])+"@2x.png)"
                       st.markdown(web_str)  
		
if city_name:        
    st.map(pd.DataFrame({'lat' : [res[5]] , 'lon' : [res[4]]},columns = ['lat','lon']))

    