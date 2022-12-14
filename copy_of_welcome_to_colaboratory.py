# -*- coding: utf-8 -*-
"""Copy of Welcome To Colaboratory

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B_f09w_6cPsNLAto0kOmoApBgVxst9SO

##importig the libraries

# EDA of Hotel Bookings Demand
"""

import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

"""## importing and understanding the dataset

"""

df=pd.read_csv("hotel_bookings.csv")
df.shape
df.head

"""###"""

pd.set_option('display.max_columns',32)

df.columns

df.nunique()

df['hotel'].value_counts()

df['meal'].value_counts()

df['market_segment'].value_counts()

df['distribution_channel'].value_counts()

df['deposit_type'].value_counts()

df['customer_type'].value_counts()

df['total_of_special_requests'].value_counts()

sns.countplot(data=df,x='hotel')

sns.countplot(data=df,x='is_canceled',hue='is_repeated_guest')

sns.countplot(data=df,x='hotel',hue='is_canceled')

"""# Data Preparation

### Missing Data
"""

df.isnull().values.any()

df.isnull().sum()

df.fillna(0,inplace=True)

df.isnull().sum()

df["meal"].replace("Undefined","SC", inplace=True)

df["meal"].unique()

Subset=df[(df['children']==0) & (df['adults']==0) & (df['babies']==0)]

Subset[['adults','babies','children']]

type(Subset)

Delete=(df['children']==0) & (df['adults']==0) & (df['babies']==0)

type(Delete)

Delete

data=df[~Delete]

data.head()

Subset=data[(data['children']==0) & (data['adults']==0) & (data['babies']==0)]

Subset

data.shape

119390-119210

data.to_csv('Updataed_Hotel_Booking.csv', index=False)

"""## Home country of Guests """

guest_country=data[data['is_canceled']==0  ]['country'].value_counts().reset_index()
guest_country.columns=['country','Number of guests']

guest_country

import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.express as px

total_guests = guest_country["Number of guests"].sum()
print(total_guests)

guest_country["Guests in %"] = round(guest_country["Number of guests"] / total_guests * 100, 2)
guest_country

trace= go.Bar(
    x=guest_country["country"],
    y=guest_country['Number of guests'],
    marker=dict(color='#CD7F32') 
)
data1 = [ trace]
layout = go.Layout(
    title='Guests by Country'
)
fig = go.Figure(data=data1, layout=layout)
pyo.plot(fig)

map_guest = px.choropleth(guest_country,
                    locations=guest_country['country'],
                    color=guest_country['Number of guests'], 
                    hover_name=guest_country['country'], 
                    title="Home country of guests")
map_guest.show()

"""## Misinterpreting Data"""

resort = data[(data["hotel"] == "Resort Hotel") & (data["is_canceled"] == 0)]
city = data[(data["hotel"] == "City Hotel") & (data["is_canceled"] == 0)]

resort

resort_hotel=resort.groupby(['arrival_date_month'])['adr'].mean().reset_index()
resort_hotel

city_hotel=city.groupby(['arrival_date_month'])['adr'].mean().reset_index()
city_hotel

final=resort_hotel.merge(city_hotel,on='arrival_date_month')
final.columns=['month','price_for_resort','price_for_city_hotel']
final

"""## Room price per night over the months"""

px.line(final, x='month',
        y=['price_for_resort','price_for_city_hotel'],
        title='Room price per night over the Months')

"""#### Guests Pay For A Room Per Night  """

df['reserved_room_type'].unique()

"""## Plotting the graph"""

data["adr_Updated"]=data["adr"]/(data["adults"]+data["children"])
data

data["adr_Updated"]=data["adr"]/(data["adults"]+data["children"])
valid_guest= data.loc[data["is_canceled"] == 0]
prices = valid_guest[["hotel", "reserved_room_type", "adr_Updated"]].sort_values("reserved_room_type")

plt.figure(figsize=(12, 8))
sns.boxplot(x="reserved_room_type",
            y="adr_Updated",
            hue="hotel",
            data=prices
           )
plt.title("Price of room types per night and person", fontsize=16)
plt.xlabel("Room type", fontsize=16)
plt.ylabel("Price [EUR]", fontsize=16)

plt.ylim(0, 160)
plt.show()

prices_C=prices[prices['reserved_room_type']=='C']
prices_C

prices_City=prices_C[prices_C['hotel']=='City Hotel']
prices_Resort=prices_C[prices_C['hotel']=='Resort Hotel']
prices_Resort

prices_City

prices_Resort.describe()

"""#### Stay time"""

df3=data[data['is_canceled']==0]
df3["total_nights"] = df3["stays_in_weekend_nights"] + df3["stays_in_week_nights"]

df3

df4=df3[['total_nights','hotel','is_canceled']]
df4

hotel_stay=df4.groupby(['total_nights','hotel']).agg('count').reset_index()

hotel_stay

hotel_stay=hotel_stay.rename(columns={'is_canceled':'Number of stays'})
hotel_stay.head()

hotel_stay_r=hotel_stay[hotel_stay['hotel']=='Resort Hotel']
hotel_stay_r

hotel_stay_c=hotel_stay[hotel_stay['hotel']=='City Hotel']
hotel_stay_c

trace = go.Bar(
    x=hotel_stay_r["total_nights"],
    y=hotel_stay_r["Number of stays"],
    name='Resort Stay'
    )

trace1=go.Bar(
    x=hotel_stay_c["total_nights"],
    y=hotel_stay_c["Number of stays"],
    name='City stay'
    )


data5 = [trace,trace1]
layout = go.Layout(
    title='Total Number of stays by Guest'
)
fig = go.Figure(data=data5, layout=layout)
pyo.plot(fig)

"""#### Bookings by market segment"""

segments=data["market_segment"].value_counts()
segments

segments=data["market_segment"].value_counts()

# pie plot
fig = px.pie(segments,
             values=segments.values,
             names=segments.index,
             title="Bookings per market segment",
             template="seaborn")
fig.update_traces(rotation=-90, textinfo="percent+label")
fig.show()

plt.figure(figsize=(12, 8))
sns.barplot(x="market_segment",
            y="adr_Updated",
            hue="reserved_room_type",
            data=data,
            ci=None)
plt.title("ADR by market segment and room type", fontsize=16)
plt.xlabel("Market segment", fontsize=16)
plt.xticks(rotation=45)
plt.ylabel("ADR per person [EUR]", fontsize=16)
plt.legend(loc="upper left")
plt.show()

"""#### Number of bookings get canceled"""

Cancel=data['is_canceled']==1

cancel=Cancel.sum()

resort_cancelation = data.loc[data["hotel"] == "Resort Hotel"]["is_canceled"].sum()
city_cancelation = data.loc[data["hotel"] == "City Hotel"]["is_canceled"].sum()

resort_cancelation

city_cancelation

print(f"Total Booking Cancelled : {cancel} . ")
print(f"Total Resort Hotel Booking Cancelled : {resort_cancelation} . ")
print(f"Total City Hotel Booking Cancelled : {city_cancelation} . ")

"""#### Month having the highest number of cancelations"""

res_book_per_month = data.loc[(data["hotel"] == "Resort Hotel")].groupby("arrival_date_month")["hotel"].count()
res_cancel_per_month = data.loc[(data["hotel"] == "Resort Hotel")].groupby("arrival_date_month")["is_canceled"].sum()

cty_book_per_month = data.loc[(data["hotel"] == "City Hotel")].groupby("arrival_date_month")["hotel"].count()
cty_cancel_per_month = data.loc[(data["hotel"] == "City Hotel")].groupby("arrival_date_month")["is_canceled"].sum()

res_cancel_data = pd.DataFrame({"Hotel": "Resort Hotel",
                                "Month": list(res_book_per_month.index),
                                "Bookings": list(res_book_per_month.values),
                                "Cancelations": list(res_cancel_per_month.values)})
cty_cancel_data = pd.DataFrame({"Hotel": "City Hotel",
                                "Month": list(cty_book_per_month.index),
                                "Bookings": list(cty_book_per_month.values),
                                "Cancelations": list(cty_cancel_per_month.values)})

res_cancel_data

plt.figure(figsize=(12, 8))

trace = go.Bar(
    x=res_cancel_data["Month"],
    y=res_cancel_data["Cancelations"],
    name="Rst Cancelled"
    )
trace1 = go.Bar(
    x=cty_cancel_data["Month"],
    y=cty_cancel_data["Cancelations"],
    name="Cty Cancelled"
    )


data6 = [trace,trace1]
layout = go.Layout(
    title='Total Number of stays by Guest'
)
fig = go.Figure(data=data6, layout=layout)
pyo.plot(fig)