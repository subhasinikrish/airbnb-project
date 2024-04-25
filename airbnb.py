from pymongo import MongoClient
import pandas as pd

#Creating Mongodb connection and retrieving data from mongodb

connection=MongoClient("mongodb+srv://subhasinikrish:12345@cluster0.thtg8ir.mongodb.net/")


db=connection['sample_airbnb']
col=db['listingsAndReviews']
df = pd.DataFrame(list(col.find()))

#fixing the missing values

df.drop(['listing_url','neighborhood_overview','transit','beds','bathrooms','accommodates','bedrooms','access','space','notes','last_scraped','summary','interaction','cancellation_policy','house_rules','images','first_review','last_review'],axis=1,inplace=True)
df=df.ffill()
df=df.bfill()

#taking only year from that calender value
df['Year'] = pd.DatetimeIndex(df['calendar_last_scraped']).year
df['Month']=pd.DatetimeIndex(df['calendar_last_scraped']).month



#cleaning and storing the required data to form a dataframe

columns={"Id":[],"Name":[],"Description":[],"Room_type":[],"Year":[],"Month":[],"Property_type":[],"Bed_type":[],"Number_of_reviews":[],"Price":[],"Weekly_price":[],"Monthly_price":[],"Minimum_nights":[],"Maximum_nights":[],"Host_id":[],"Host_name":[],"Host_location":[],"Host_listings_count":[],"Host_neighbourhood":[],"Availability_365":[],"Country":[],"Country_code":[],"Location_type":[],"Longitude":[],"Latitude":[],"Rating":[]}
  
for j in range(0,len(df['_id'])):    
     id=df['_id'][j]
     name=df['name'][j]
     description=df['description'][j]
     no_of_reviews=df['number_of_reviews'][j]
     price=df['price'][j]
     year=df['Year'][j]
     month=df['Month'][j]
     property_type=df['property_type'][j]
     roomtype=df['room_type'][j]
     bedtype=df['bed_type'][j]
     minimum_nights	=df['minimum_nights'][j]
     maximum_nights=df['maximum_nights'][j]
          
     host_location=df['host'][j]['host_location']
               

     host_listings_count=df['host'][j]['host_listings_count']


     host_neighbourhood=df['host'][j]['host_neighbourhood']
     
     host_location=df['host'][j]['host_location']


     host_id=df['host'][j]['host_id']
     
     host_name=df['host'][j]['host_name']

     availability_365=df['availability'][j]['availability_365']
     country_code=df['address'][j]['country_code']
     country=df['address'][j]['country']
     location_type=df['address'][j]['location']['type']
     location_latitude=df['address'][j]['location']['coordinates'][1]
     location_longitude=df['address'][j]['location']['coordinates'][0]
     rating=df['review_scores'][j].get('review_scores_rating')
     weekly_price=df['weekly_price'][j]
     monthly_price=df['monthly_price'][j]
     
     
     
     columns['Id'].append(id)
     columns['Name'].append(name)
     columns['Description'].append(description)
     columns['Number_of_reviews'].append(no_of_reviews)
     columns['Price'].append(price)
     columns['Room_type'].append(roomtype)
     columns['Bed_type'].append(bedtype)
     columns['Property_type'].append(property_type)
     columns['Year'].append(year)
     columns['Month'].append(month)
     columns['Minimum_nights'].append(minimum_nights)
     columns['Maximum_nights'].append(maximum_nights)
     columns['Host_id'].append(host_id)
     columns['Host_name'].append(host_name)
     columns['Host_location'].append(host_location)
     columns['Host_listings_count'].append(host_listings_count)
     columns['Host_neighbourhood'].append(host_neighbourhood)
     columns['Weekly_price'].append(weekly_price)
     columns['Monthly_price'].append(monthly_price)
     columns['Availability_365'].append(availability_365)
     columns['Country'].append(country)
     columns['Country_code'].append(country_code)
     columns['Location_type'].append(location_type)
     columns['Longitude'].append(location_longitude)
     columns['Latitude'].append(location_latitude)
     columns['Rating'].append(rating)
     air_bnb=pd.DataFrame(columns)


#copy the dataframe
df_p=air_bnb.copy()
df_p=df_p.ffill()
df_p=df_p.bfill()

#changing the datatypes into correct format

df_p['Price']=df_p["Price"].astype(str).astype(float)
df_p['Weekly_price']=df_p['Weekly_price'].astype(str).astype(float)
df_p['Monthly_price']=df_p['Monthly_price'].astype(str).astype(float)

df_p['Minimum_nights']=pd.to_numeric(df_p['Minimum_nights'],errors='coerce')
df_p['Maximum_nights']=pd.to_numeric(df_p['Maximum_nights'],errors='coerce')
df_p['Number_of_reviews']=pd.to_numeric(df_p['Number_of_reviews'],errors='coerce')

price_month=df_p.groupby(['Month','Country'])['Price'].sum().reset_index()

#Streamlit part
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


#st.set_page_config(layout='wide')
st.title(":green[AIRBNB ANALYSIS PROJECT]")

tab1,tab2=st.tabs(["Exploring Data","GEOSPATIAL REPRESENTATION"])

with tab1:
     col1,col2=st.columns(2)
     with col1:
          country=['Portugal', 'Brazil', 'United States', 'Turkey', 'Canada','Hong Kong', 'Spain', 'Australia', 'China']
          room_type=['Entire home/apt', 'Private room', 'Shared room']

          
          st.bar_chart(df_p,y='Price',x='Room_type')
          st.bar_chart(df_p,x='Price',y='Property_type')
     with col2:
          st.bar_chart(df_p,y='Rating',x='Country')
          st.scatter_chart(df_p,x='Price',y='Number_of_reviews')
          st.bar_chart(price_month,y='Price',x='Month')
with tab2:

          fig=px.scatter_mapbox(df_p,lat="Latitude",lon="Longitude",color="Price",hover_name='Country',color_continuous_scale="rainbow",size_max=15,zoom=10,mapbox_style="open-street-map" )

          st.plotly_chart(fig)

          fig1=px.scatter_mapbox(df_p,lat="Latitude",lon="Longitude",color="Price",hover_name='Host_neighbourhood',color_continuous_scale="rainbow",size_max=15,zoom=10,mapbox_style="open-street-map" )

          st.plotly_chart(fig1)

with st.sidebar:
    st.title(":blue[AIRBNB ANALYSIS]")
    st.header(":red[STEPS FOLLOWED]")
    st.caption("Established a MongoDB connection, retrieved the Airbnb dataset for analysis")
    st.caption("Cleaned the dataset, addressing missing values, duplicates, and data type conversions for accurate analysis")
    st.caption("Developed a streamlit web application with interactive maps showcasing the distribution of Airbnb listings, allowing users to explore prices, ratings, and other relevant factors")
    st.caption("Investigated location-based insights by extracting and visualizing data for specific regions or neighborhoods")
    st.caption("Created interactive visualizations that enable users to filter and drill down into the data.")
    st.caption("Built a comprehensive dashboard using  Power BI, combining various visualizations to present key insights from the analysis.")
    st.header(":red[TECHNOLOGIES USED]")
    st.caption("Python scripting, Data Preprocessing, Visualization,EDA, Streamlit, MongoDb, PowerBI,pandas,seaborn,matplotlib,plotly")


     
    



    

          



    
     
     
