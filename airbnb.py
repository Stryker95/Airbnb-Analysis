import pandas as pd
df = pd.read_csv("D:\project 4\sample_airbnb.listingsAndReviews.csv")
columns_to_transfer = ['_id', 'room_type', 'minimum_nights', 'maximum_nights', 'accommodates',
                       'bedrooms', 'beds', 'bathrooms', 'price', 'security_deposit',
                       'cleaning_fee', 'extra_people', 'guests_included', 'address.street',
                       'address.suburb', 'address.country', 'address.location.coordinates[0]',
                       'address.location.coordinates[1]', 'availability.availability_365',
                       'review_scores.review_scores_accuracy',
                       'review_scores.review_scores_cleanliness',
                       'review_scores.review_scores_rating', 'weekly_price', 'monthly_price',
                       'availability.availability_30', 'address.government_area']

# Transfer the columns from df to df2
df2 = df[columns_to_transfer].copy()

df2.fillna(0,inplace=True)

# Assuming df is your DataFrame
column_mapping = {
    '_id': '_id',
    'room_type': 'room_type',
    'minimum_nights': 'minimum_nights',
    'maximum_nights': 'maximum_nights',
    'accommodates': 'accommodates',
    'bedrooms': 'bedrooms',
    'beds': 'beds',
    'bathrooms': 'bathrooms',
    'price': 'price',
    'security_deposit': 'security_deposit',
    'cleaning_fee': 'cleaning_fee',
    'extra_people': 'extra_people',
    'guests_included': 'guests_included',
    'address.street': 'address_street',
    'address.suburb': 'address_suburb',
    'address.country': 'address_country',
    'address.location.coordinates[0]': 'Longitude',
    'address.location.coordinates[1]': 'Lattitude',
    'availability.availability_365': 'availability_365',
    'review_scores.review_scores_accuracy': 'review_scores_review_scores_accuracy',
    'review_scores.review_scores_cleanliness': 'review_scores_review_scores_cleanliness',
    'review_scores.review_scores_rating': 'review_scores_review_scores_rating',
    'weekly_price': 'weekly_price',
    'monthly_price': 'monthly_price',
    'availability.availability_30': "availability_30", 
    'address.government_area':"address_government_area"
}

df2.rename(columns=column_mapping, inplace=True)

#start with this, insert selectbox to select options
import geopandas as gpd
from shapely.geometry import Point
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px


st.set_page_config(layout="wide")
# Display the title
st.markdown("<h1 style='text-align: center; font-weight: bold;'>AirBnb Analysis Dashboard</h1>", unsafe_allow_html=True)

geometry =[Point(xy) for xy in zip(df2["Longitude"],df2["Lattitude"])]
gdf=gpd.GeoDataFrame(df2,geometry =geometry)

#create the plot
fig,ax=plt.subplots(figsize=(15,10))
world=gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world.plot(ax=ax,color="whitesmoke",linestyle=":",edgecolor="black")
gdf.plot(ax=ax,marker="o",color="red",markersize=5)


# Display the plot using st.pyplot
st.pyplot(fig)


def display_country_data_portugal(country_name):
    col1,col2=st.columns(2)
    with col1:
        # Filter the geodataframe for the specified country
        country_data = df2[df2["address_country"] == country_name]

        # Create geodataframe for filtered data
        geometry = [Point(xy) for xy in zip(country_data["Longitude"], country_data["Lattitude"])]
        gdf = gpd.GeoDataFrame(country_data, geometry=geometry)

        # Read the GeoJSON file for the country
        geojson_file = f"D:\project 4\portugal-with-regions_.geojson"
        provinces = gpd.read_file(geojson_file)

        # Create choropleth map
        fig = px.choropleth_mapbox(provinces, geojson=provinces.geometry,
                                locations=provinces.index,
                                color_discrete_sequence=["yellow"], opacity=0.5,
                                mapbox_style="carto-positron",
                                hover_name="name",
                                title=f"{country_name} Provinces")

        # Add scatter plot for the locations with hover information
        fig.add_trace(px.scatter_mapbox(gdf, lat=gdf.geometry.y,
                                        lon=gdf.geometry.x,
                                        hover_name="address_street",
                                        hover_data={"price": True, "availability_30": True,
                                                    "address_government_area": True},
                                        color_discrete_sequence=["green"]).data[0])

        # Update layout and show the figure
        fig.update_layout(mapbox_zoom=5, mapbox_center={"lat": 39.5, "lon": -8.0},
                          width=1000, height=800)
        st.plotly_chart(fig)

        # Filter the DataFrame for the selected country
        country_data_filtered = df2[df2["address_country"] == country_name]
        pie_fig = px.pie(country_data_filtered, names='room_type', title=f'Room Type Distribution in {country_name}')
        st.plotly_chart(pie_fig)

    with col2:
        # Calculate and display the unique prices of government areas
        gormint_area_prices = country_data_filtered.groupby("address_government_area")['price'].unique()
        hover_data = pd.DataFrame({"address_government_area": gormint_area_prices.index,
                                "price": gormint_area_prices.values})
        hover_data["min_price"] = hover_data["price"].apply(lambda x: min(x))
        hover_data["max_price"] = hover_data["price"].apply(lambda x: max(x))
        bar_fig = px.bar(hover_data, x="address_government_area", y=hover_data["price"].apply(lambda x: len(x)),
                        title=f"Number of Unique Prices of Government Areas in {country_name}",
                        labels={"address_government_area": "Government Area", "y": "Number of Unique Prices"},
                        text=hover_data.apply(lambda row: f"Min: {row['min_price']}, Max: {row['max_price']}", axis=1),
                        hover_name="address_government_area",
                        hover_data={"price": False, "min_price": True, "max_price": True},
                        color_discrete_sequence=["green"])
        bar_fig.update_traces(texttemplate="%{text}<extra></extra>", textfont_size=12,
                            selector=dict(type="bar", marker=dict(color="green")))
        bar_fig.update_layout(xaxis_tickangle=-45, bargap=0.2, hovermode="x unified", hoverlabel=dict(font_size=15),
                              width=800,height=600)
        st.plotly_chart(bar_fig)
        
def display_country_data_brazil(country_name):
    col1,col2=st.columns(2)
    with col1:
        #brazil
        #filter the geodataframe for specified country
        country_data=df2[df2["address_country"]=="Brazil"]

        #create geodataframe for filtered data
        geometry=[Point(xy) for xy in zip(country_data["Longitude"],country_data["Lattitude"])]
        gdf=gpd.GeoDataFrame(country_data,geometry=geometry)

        provinces=gpd.read_file(r"D:\project 4\brazil\archive (1)\brazil_geo.json")

        fig=px.choropleth_mapbox(provinces,geojson=provinces.geometry,
                                locations=provinces.index,
                                color_discrete_sequence=["yellow"],opacity=0.5,
                                mapbox_style="carto-positron",
                                hover_name="name",
                                title="Brazil Provinces")

        #add scatter plot for the locations with hover information
        fig.add_trace(px.scatter_mapbox(gdf,lat=gdf.geometry.y,
                                        lon=gdf.geometry.x,
                                        hover_name="address_street",
                                        hover_data={"price":True,"availability_30":True,
                                                    "address_government_area":True},
                                        color_discrete_sequence=["green"]).data[0])

        #update layout and show the figure
        fig.update_layout(mapbox_center={"lat": -22.9068, "lon": -43.1729},
                          width=1000, height=800)
        st.plotly_chart(fig)


        brazil_data=df2[df2["address_country"]=="Brazil"]
        pie_fig=px.pie(brazil_data,names='room_type',title='Room Type Distribution in Brazil')
        st.plotly_chart(pie_fig)
        
    with col2:

        # Filter the DataFrame for Portugal
        gormint_area = df2[df2["address_country"] == "Brazil"]
        gormint_area_prices = gormint_area.groupby("address_government_area")['price'].unique()

        # Create a DataFrame with government area names and prices for hover information
        hover_data = pd.DataFrame({"address_government_area": gormint_area_prices.index,
                                "price": gormint_area_prices.values})

        # Add columns for minimum and maximum prices
        hover_data["min_price"] = hover_data["price"].apply(lambda x: min(x))
        hover_data["max_price"] = hover_data["price"].apply(lambda x: max(x))

        # Create a bar chart with hover information
        bar_fig = px.bar(hover_data, x="address_government_area", y=hover_data["price"].apply(lambda x: len(x)),
                    title="Number of Unique Prices of Government Areas in Brazil",
                    labels={"address_government_area": "Government Area", "y": "Number of Unique Prices"},
                    text=hover_data.apply(lambda row: f"Min: {row['min_price']}, Max: {row['max_price']}", axis=1),
                    hover_name="address_government_area",
                    hover_data={"price": False, "min_price": True, "max_price": True},
                    color_discrete_sequence=["green"])

        # Adjust text font size based on bar height
        bar_fig.update_traces(texttemplate="%{text}<extra></extra>",
                        textfont_size=12,
                        selector=dict(type="bar",marker=dict(color="green")))

        bar_fig.update_layout(xaxis_tickangle=-45,bargap=0.2,hovermode="x unified",hoverlabel=dict(font_size=15))
        st.plotly_chart(bar_fig)

def display_country_data_usa(country_name):
    col1,col2=st.columns(2)
    with col1:
        #USA
        #filter the geodataframe for specified country
        country_data=df2[df2["address_country"]=="United States"]

        #create geodataframe for filtered data
        geometry=[Point(xy) for xy in zip(country_data["Longitude"],country_data["Lattitude"])]
        gdf=gpd.GeoDataFrame(country_data,geometry=geometry)

        provinces=gpd.read_file(r"D:\project 4\usa\gz_2010_us_040_00_20m.json")

        fig=px.choropleth_mapbox(provinces,geojson=provinces.geometry,
                                locations=provinces.index,
                                color_discrete_sequence=["yellow"],opacity=0.5,
                                mapbox_style="carto-positron",
                                hover_name="NAME",
                                title="USA Provinces")

        #add scatter plot for the locations with hover information
        fig.add_trace(px.scatter_mapbox(gdf,lat=gdf.geometry.y,
                                        lon=gdf.geometry.x,
                                        hover_name="address_street",
                                        hover_data={"price":True,"availability_30":True,
                                                    "address_government_area":True},
                                        color_discrete_sequence=["green"]).data[0])

        #update layout and show the figure
        fig.update_layout(mapbox_center={"lat": 40.7128, "lon": -74.0060},
                          width=1000, height=800)
        st.plotly_chart(fig)


        usa_data=df2[df2["address_country"]=="United States"]
        pie_fig=px.pie(usa_data,names='room_type',title='Room Type Distribution in United States')
        st.plotly_chart(pie_fig)

        
    with col2:
        
        # Filter the DataFrame for Portugal
        gormint_area = df2[df2["address_country"] == "United States"]
        gormint_area_prices = gormint_area.groupby("address_government_area")['price'].unique()

        # Create a DataFrame with government area names and prices for hover information
        hover_data = pd.DataFrame({"address_government_area": gormint_area_prices.index,
                                "price": gormint_area_prices.values})

        # Add columns for minimum and maximum prices
        hover_data["min_price"] = hover_data["price"].apply(lambda x: min(x))
        hover_data["max_price"] = hover_data["price"].apply(lambda x: max(x))

        # Create a bar chart with hover information
        bar_fig = px.bar(hover_data, x="address_government_area", y=hover_data["price"].apply(lambda x: len(x)),
                    title="Number of Unique Prices of Government Areas in United States",
                    labels={"address_government_area": "Government Area", "y": "Number of Unique Prices"},
                    text=hover_data.apply(lambda row: f"Min: {row['min_price']}, Max: {row['max_price']}", axis=1),
                    hover_name="address_government_area",
                    hover_data={"price": False, "min_price": True, "max_price": True},
                    color_discrete_sequence=["green"])

        # Adjust text font size based on bar height
        bar_fig.update_traces(texttemplate="%{text}<extra></extra>",
                        textfont_size=12,
                        selector=dict(type="bar",marker=dict(color="green")))

        bar_fig.update_layout(xaxis_tickangle=-45,bargap=0.2,hovermode="x unified",hoverlabel=dict(font_size=15))
        st.plotly_chart(bar_fig)




def display_country_data_turkey():
    col1,col2=st.columns(2)
    with col1:
        #Turkey
        #filter the geodataframe for specified country
        country_data=df2[df2["address_country"]=="Turkey"]

        #create geodataframe for filtered data
        geometry=[Point(xy) for xy in zip(country_data["Longitude"],country_data["Lattitude"])]
        gdf=gpd.GeoDataFrame(country_data,geometry=geometry)

        provinces=gpd.read_file(r"D:\project 4\turkey\tr-cities.json")

        fig=px.choropleth_mapbox(provinces,geojson=provinces.geometry,
                                locations=provinces.index,
                                color_discrete_sequence=["yellow"],opacity=0.5,
                                mapbox_style="carto-positron",
                                hover_name="name",
                                title="Turkey Provinces")

        #add scatter plot for the locations with hover information
        fig.add_trace(px.scatter_mapbox(gdf,lat=gdf.geometry.y,
                                        lon=gdf.geometry.x,
                                        hover_name="address_street",
                                        hover_data={"price":True,"availability_30":True,
                                                    "address_government_area":True},
                                        color_discrete_sequence=["green"]).data[0])

        #update layout and show the figure
        fig.update_layout(mapbox_center={"lat": 41.0082, "lon": 28.9784},
                          width=1000, height=800)
        st.plotly_chart(fig)

        Turkey_data=df2[df2["address_country"]=="Turkey"]
        pie_fig=px.pie(Turkey_data,names='room_type',title='Room Type Distribution in Turkey')
        st.plotly_chart(pie_fig)  
        
    with col2:
        
        # Filter the DataFrame for Portugal
        gormint_area = df2[df2["address_country"] == "Turkey"]
        gormint_area_prices = gormint_area.groupby("address_government_area")['price'].unique()

        # Create a DataFrame with government area names and prices for hover information
        hover_data = pd.DataFrame({"address_government_area": gormint_area_prices.index,
                                "price": gormint_area_prices.values})

        # Add columns for minimum and maximum prices
        hover_data["min_price"] = hover_data["price"].apply(lambda x: min(x))
        hover_data["max_price"] = hover_data["price"].apply(lambda x: max(x))

        # Create a bar chart with hover information
        bar_fig = px.bar(hover_data, x="address_government_area", y=hover_data["price"].apply(lambda x: len(x)),
                    title="Number of Unique Prices of Government Areas in Turkey",
                    labels={"address_government_area": "Government Area", "y": "Number of Unique Prices"},
                    text=hover_data.apply(lambda row: f"Min: {row['min_price']}, Max: {row['max_price']}", axis=1),
                    hover_name="address_government_area",
                    hover_data={"price": False, "min_price": True, "max_price": True},
                    color_discrete_sequence=["green"])

        # Adjust text font size based on bar height
        bar_fig.update_traces(texttemplate="%{text}<extra></extra>",
                        textfont_size=12,
                        selector=dict(type="bar",marker=dict(color="green")))

        bar_fig.update_layout(xaxis_tickangle=-45,bargap=0.2,hovermode="x unified",hoverlabel=dict(font_size=15))
        st.plotly_chart(bar_fig)


def display_country_data_canada():
    col1,col2=st.columns(2)
    with col1:
        #Montreal Canada
        #filter the geodataframe for specified country
        country_data=df2[df2["address_country"]=="Canada"]

        #create geodataframe for filtered data
        geometry=[Point(xy) for xy in zip(country_data["Longitude"],country_data["Lattitude"])]
        gdf=gpd.GeoDataFrame(country_data,geometry=geometry)

        provinces=gpd.read_file(r"D:\project 4\canada\georef-canada-province@public.geojson")

        fig=px.choropleth_mapbox(provinces,geojson=provinces.geometry,
                                locations=provinces.index,
                                color_discrete_sequence=["yellow"],opacity=0.5,
                                mapbox_style="carto-positron",
                                hover_name="prov_name_en",
                                title="Canada Provinces")

        #add scatter plot for the locations with hover information
        fig.add_trace(px.scatter_mapbox(gdf,lat=gdf.geometry.y,
                                        lon=gdf.geometry.x,
                                        hover_name="address_street",
                                        hover_data={"price":True,"availability_30":True,
                                                    "address_government_area":True},
                                        color_discrete_sequence=["green"]).data[0])

        #update layout and show the figure
        fig.update_layout(mapbox_center={"lat": 45.5017, "lon":  -73.5673},
                                width=1000, height=800)
        st.plotly_chart(fig)

        canada_data=df2[df2["address_country"]=="Canada"]
        pie_fig=px.pie(canada_data,names='room_type',title='Room Type Distribution in Canada')
        st.plotly_chart(pie_fig)
    
    with col2:
        
        # Filter the DataFrame for Portugal
        gormint_area = df2[df2["address_country"] == "Canada"]
        gormint_area_prices = gormint_area.groupby("address_government_area")['price'].unique()

        # Create a DataFrame with government area names and prices for hover information
        hover_data = pd.DataFrame({"address_government_area": gormint_area_prices.index,
                                "price": gormint_area_prices.values})

        # Add columns for minimum and maximum prices
        hover_data["min_price"] = hover_data["price"].apply(lambda x: min(x))
        hover_data["max_price"] = hover_data["price"].apply(lambda x: max(x))

        # Create a bar chart with hover information
        bar_fig = px.bar(hover_data, x="address_government_area", y=hover_data["price"].apply(lambda x: len(x)),
                    title="Number of Unique Prices of Government Areas in Montreal,Canada",
                    labels={"address_government_area": "Government Area", "y": "Number of Unique Prices"},
                    text=hover_data.apply(lambda row: f"Min: {row['min_price']}, Max: {row['max_price']}", axis=1),
                    hover_name="address_government_area",
                    hover_data={"price": False, "min_price": True, "max_price": True},
                    color_discrete_sequence=["green"])

        # Adjust text font size based on bar height
        bar_fig.update_traces(texttemplate="%{text}<extra></extra>",
                        textfont_size=12,
                        selector=dict(type="bar",marker=dict(color="green")))

        bar_fig.update_layout(xaxis_tickangle=-45,bargap=0.2,hovermode="x unified",hoverlabel=dict(font_size=15))
        st.plotly_chart(bar_fig)

def display_country_data_hongkong():
    col1,col2=st.columns(2)
    with col1:
        #Hong Kong
        #filter the geodataframe for specified country
        country_data=df2[df2["address_country"]=="Hong Kong"]

        #create geodataframe for filtered data
        geometry=[Point(xy) for xy in zip(country_data["Longitude"],country_data["Lattitude"])]
        gdf=gpd.GeoDataFrame(country_data,geometry=geometry)

        provinces=gpd.read_file(r"D:\project 4\hong kong\polygon.json")

        fig=px.choropleth_mapbox(provinces,geojson=provinces.geometry,
                                locations=provinces.index,
                                color_discrete_sequence=["yellow"],opacity=0.5,
                                mapbox_style="carto-positron",
                                hover_name="ENAME",
                                title="Hong Kong Provinces")

        #add scatter plot for the locations with hover information
        fig.add_trace(px.scatter_mapbox(gdf,lat=gdf.geometry.y,
                                        lon=gdf.geometry.x,
                                        hover_name="address_street",
                                        hover_data={"price":True,"availability_30":True,
                                                    "address_government_area":True},
                                        color_discrete_sequence=["green"]).data[0])

        #update layout and show the figure
        fig.update_layout(mapbox_center={"lat": 22.3193, "lon":  114.1694},
                                width=1000, height=800)
        st.plotly_chart(fig)

        hong_kong_data=df2[df2["address_country"]=="Hong Kong"]
        pie_fig=px.pie(hong_kong_data,names='room_type',title='Room Type Distribution in Hong Kong')
        st.plotly_chart(pie_fig)
        
    with col2:
        
        # Filter the DataFrame for Hong Kong
        gormint_area = df2[df2["address_country"] == "Hong Kong"]
        gormint_area_prices = gormint_area.groupby("address_government_area")['price'].unique()

        # Create a DataFrame with government area names and prices for hover information
        hover_data = pd.DataFrame({"address_government_area": gormint_area_prices.index,
                                "price": gormint_area_prices.values})

        # Add columns for minimum and maximum prices
        hover_data["min_price"] = hover_data["price"].apply(lambda x: min(x))
        hover_data["max_price"] = hover_data["price"].apply(lambda x: max(x))

        # Create a bar chart with hover information
        bar_fig = px.bar(hover_data, x="address_government_area", y=hover_data["price"].apply(lambda x: len(x)),
                    title="Number of Unique Prices of Government Areas in Hong Kong",
                    labels={"address_government_area": "Government Area", "y": "Number of Unique Prices"},
                    text=hover_data.apply(lambda row: f"Min: {row['min_price']}, Max: {row['max_price']}", axis=1),
                    hover_name="address_government_area",
                    hover_data={"price": False, "min_price": True, "max_price": True},
                    color_discrete_sequence=["green"])

        # Adjust text font size based on bar height
        bar_fig.update_traces(texttemplate="%{text}<extra></extra>",
                        textfont_size=12,
                        selector=dict(type="bar",marker=dict(color="green")))

        bar_fig.update_layout(xaxis_tickangle=-45,bargap=0.2,hovermode="x unified",hoverlabel=dict(font_size=15))
        st.plotly_chart(bar_fig)


def display_country_data_spain():
    col1,col2=st.columns(2)
    with col1:
        #Barcelona,Spain
        #filter the geodataframe for specified country
        country_data=df2[df2["address_country"]=="Spain"]

        #create geodataframe for filtered data
        geometry=[Point(xy) for xy in zip(country_data["Longitude"],country_data["Lattitude"])]
        gdf=gpd.GeoDataFrame(country_data,geometry=geometry)

        provinces=gpd.read_file(r"D:\project 4\spain\spain-provinces.geojson")

        fig=px.choropleth_mapbox(provinces,geojson=provinces.geometry,
                                locations=provinces.index,
                                color_discrete_sequence=["yellow"],opacity=0.5,
                                mapbox_style="carto-positron",
                                hover_name="name",
                                title="Spain Provinces")

        #add scatter plot for the locations with hover information
        fig.add_trace(px.scatter_mapbox(gdf,lat=gdf.geometry.y,
                                        lon=gdf.geometry.x,
                                        hover_name="address_street",
                                        hover_data={"price":True,"availability_30":True,
                                                    "address_government_area":True},
                                        color_discrete_sequence=["green"]).data[0])

        #update layout and show the figure
        fig.update_layout(mapbox_center={"lat":41.3851, "lon":2.1734},
                                        width=1000, height=800)
        st.plotly_chart(fig)

        spain_data=df2[df2["address_country"]=="Spain"]
        pie_fig=px.pie(spain_data,names='room_type',title='Room Type Distribution in Barcelona,Spain')
        st.plotly_chart(pie_fig)
        
    with col2:
        # Filter the DataFrame for Spain
        gormint_area = df2[df2["address_country"] == "Spain"]
        gormint_area_prices = gormint_area.groupby("address_government_area")['price'].unique()

        # Create a DataFrame with government area names and prices for hover information
        hover_data = pd.DataFrame({"address_government_area": gormint_area_prices.index,
                                "price": gormint_area_prices.values})

        # Add columns for minimum and maximum prices
        hover_data["min_price"] = hover_data["price"].apply(lambda x: min(x))
        hover_data["max_price"] = hover_data["price"].apply(lambda x: max(x))

        # Create a bar chart with hover information
        bar_fig = px.bar(hover_data, x="address_government_area", y=hover_data["price"].apply(lambda x: len(x)),
                    title="Number of Unique Prices of Government Areas in Barcelona,Spain",
                    labels={"address_government_area": "Government Area", "y": "Number of Unique Prices"},
                    text=hover_data.apply(lambda row: f"Min: {row['min_price']}, Max: {row['max_price']}", axis=1),
                    hover_name="address_government_area",
                    hover_data={"price": False, "min_price": True, "max_price": True},
                    color_discrete_sequence=["green"])

        # Adjust text font size based on bar height
        bar_fig.update_traces(texttemplate="%{text}<extra></extra>",
                        textfont_size=12,
                        selector=dict(type="bar",marker=dict(color="green")))

        bar_fig.update_layout(xaxis_tickangle=-45,bargap=0.2,hovermode="x unified",hoverlabel=dict(font_size=15))
        st.plotly_chart(bar_fig)


def display_country_data_australia():
    col1,col2=st.columns(2)
    with col1:
        #Australia
        #filter the geodataframe for specified country
        country_data=df2[df2["address_country"]=="Australia"]

        #create geodataframe for filtered data
        geometry=[Point(xy) for xy in zip(country_data["Longitude"],country_data["Lattitude"])]
        gdf=gpd.GeoDataFrame(country_data,geometry=geometry)

        provinces=gpd.read_file(r"D:\project 4\australia\australian-states.json")

        fig=px.choropleth_mapbox(provinces,geojson=provinces.geometry,
                                locations=provinces.index,
                                color_discrete_sequence=["yellow"],opacity=0.5,
                                mapbox_style="carto-positron",
                                hover_name="STATE_NAME",
                                title="Australia Provinces")

        #add scatter plot for the locations with hover information
        fig.add_trace(px.scatter_mapbox(gdf,lat=gdf.geometry.y,
                                        lon=gdf.geometry.x,
                                        hover_name="address_street",
                                        hover_data={"price":True,"availability_30":True,
                                                    "address_government_area":True},
                                        color_discrete_sequence=["green"]).data[0])

        #update layout and show the figure
        fig.update_layout(mapbox_center={"lat": -33.8688, "lon":151.2093},
                                                width=1000, height=800)
        st.plotly_chart(fig)

        australia_data=df2[df2["address_country"]=="Australia"]
        pie_fig=px.pie(australia_data,names='room_type',title='Room Type Distribution in Australia')
        st.plotly_chart(pie_fig)

    with col2:
        # Filter the DataFrame for Australia
        gormint_area = df2[df2["address_country"] == "Australia"]
        gormint_area_prices = gormint_area.groupby("address_government_area")['price'].unique()

        # Create a DataFrame with government area names and prices for hover information
        hover_data = pd.DataFrame({"address_government_area": gormint_area_prices.index,
                                "price": gormint_area_prices.values})

        # Add columns for minimum and maximum prices
        hover_data["min_price"] = hover_data["price"].apply(lambda x: min(x))
        hover_data["max_price"] = hover_data["price"].apply(lambda x: max(x))

        # Create a bar chart with hover information
        bar_fig = px.bar(hover_data, x="address_government_area", y=hover_data["price"].apply(lambda x: len(x)),
                    title="Number of Unique Prices of Government Areas in Australia",
                    labels={"address_government_area": "Government Area", "y": "Number of Unique Prices"},
                    text=hover_data.apply(lambda row: f"Min: {row['min_price']}, Max: {row['max_price']}", axis=1),
                    hover_name="address_government_area",
                    hover_data={"price": False, "min_price": True, "max_price": True},
                    color_discrete_sequence=["green"])

        # Adjust text font size based on bar height
        bar_fig.update_traces(texttemplate="%{text}<extra></extra>",
                        textfont_size=12,
                        selector=dict(type="bar",marker=dict(color="green")))

        bar_fig.update_layout(xaxis_tickangle=-45,bargap=0.2,hovermode="x unified",hoverlabel=dict(font_size=15))
        st.plotly_chart(bar_fig)


def display_country_data_china():
   col1,col2=st.columns(2)
   with col1:
        #China
        #filter the geodataframe for specified country
        country_data=df2[df2["address_country"]=="China"]

        #create geodataframe for filtered data
        geometry=[Point(xy) for xy in zip(country_data["Longitude"],country_data["Lattitude"])]
        gdf=gpd.GeoDataFrame(country_data,geometry=geometry)

        provinces=gpd.read_file(r"D:\project 4\china\archive (1)\gadm36_CHN_1.json")

        fig=px.choropleth_mapbox(provinces,geojson=provinces.geometry,
                                locations=provinces.index,
                                color_discrete_sequence=["yellow"],opacity=0.5,
                                mapbox_style="carto-positron",
                                hover_name="NAME_1",
                                title="Shenzen,China")

        #add scatter plot for the locations with hover information
        fig.add_trace(px.scatter_mapbox(gdf,lat=gdf.geometry.y,
                                        lon=gdf.geometry.x,
                                        hover_name="address_street",
                                        hover_data={"price":True,"availability_30":True,
                                                    "address_government_area":True},
                                        color_discrete_sequence=["green"]).data[0])

        #update layout and show the figure
        fig.update_layout(mapbox_center={"lat": 22.5431, "lon":114.0579},
                                                        width=1000, height=800)
        st.plotly_chart(fig)

        china_data=df2[df2["address_country"]=="China"]
        pie_fig=px.pie(china_data,names='room_type',title='Room Type Distribution in Shenzen,China')
        st.plotly_chart(pie_fig)

   with col2:
        # Filter the DataFrame for China
        gormint_area = df2[df2["address_country"] == "China"]
        gormint_area_prices = gormint_area.groupby("address_government_area")['price'].unique()

        # Create a DataFrame with government area names and prices for hover information
        hover_data = pd.DataFrame({"address_government_area": gormint_area_prices.index,
                                "price": gormint_area_prices.values})

        # Add columns for minimum and maximum prices
        hover_data["min_price"] = hover_data["price"].apply(lambda x: min(x))
        hover_data["max_price"] = hover_data["price"].apply(lambda x: max(x))

        # Create a bar chart with hover information
        bar_fig = px.bar(hover_data, x="address_government_area", y=hover_data["price"].apply(lambda x: len(x)),
                    title="Number of Unique Prices of Government Areas in Shenzen,China",
                    labels={"address_government_area": "Government Area", "y": "Number of Unique Prices"},
                    text=hover_data.apply(lambda row: f"Min: {row['min_price']}, Max: {row['max_price']}", axis=1),
                    hover_name="address_government_area",
                    hover_data={"price": False, "min_price": True, "max_price": True},
                    color_discrete_sequence=["green"])

        # Adjust text font size based on bar height
        bar_fig.update_traces(texttemplate="%{text}<extra></extra>",
                        textfont_size=12,
                        selector=dict(type="bar",marker=dict(color="green")))

        bar_fig.update_layout(xaxis_tickangle=-45,bargap=0.2,hovermode="x unified",hoverlabel=dict(font_size=15))
        st.plotly_chart(bar_fig)
 
 
selected_country=st.radio("Select a Place",["Porto,Portugal",
                                              "Rio de Janeiro,Brazil",
                                              "New York,United States",
                                              "Istanbul,Turkey",
                                              "Montreal,Canada",
                                              "Hong Kong",
                                              "Barcelona,Spain",
                                              "Sydney,Australia",
                                              "Shenzen,China"])

if selected_country=="Shenzen,China":
   display_country_data_china()

if selected_country=="Sydney,Australia":
    display_country_data_australia()
    
if selected_country=="Barcelona,Spain":
    display_country_data_spain()
    
if selected_country=="Hong Kong":
    display_country_data_hongkong()

if selected_country=="Montreal,Canada":
    display_country_data_canada()   
if selected_country=="Istanbul,Turkey":
    display_country_data_turkey()
    
if selected_country=="New York,United States":
    display_country_data_usa("United States")  
          
if selected_country=="Rio de Janeiro,Brazil":
    display_country_data_brazil("Brazil")
    
if selected_country=="Porto,Portugal":
    display_country_data_portugal("Portugal")
