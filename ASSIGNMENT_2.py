import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import geopandas as gpd


df=pd.read_csv("Pandas_Project.csv")
st.title("PANDAS PROJECT")

st.markdown("## About ")
st.markdown("### This is a dashboard showing a companies shipment date. it contains relevant KPIs and Charts")
# CLEANING
df["Amount"]=pd.to_numeric(df["Amount"].replace({r"[\$,]":""},regex=True))
df["Date"]=pd.to_datetime(df["Date"],errors="coerce")
df["month"]=df["Date"].dt.month_name()

# ..................SLICERS...............
st.sidebar.header("Data Filter")

country_filter= st.sidebar.multiselect(
      "Select Country",
    options=df["Country"].dropna().unique(),
    default=df["Country"].dropna().unique()
)

product_filter= st.sidebar.multiselect(
    "Select Product",
    options=df["Product"].dropna().unique(),
    default=df["Product"].dropna().unique()
)

salesperson_filter=st.sidebar.multiselect(
    "Select Sales Person",
    options=df["Sales Person"].dropna().unique(),
    default=df["Sales Person"].dropna().unique()
)
# date slicer

date_range= st.sidebar.date_input(
    "Select Date Range",
    [df["Date"].min(),df["Date"].max()]
)

#...............FILTERING.............
filtered_df=df[
    (df["Country"].isin(country_filter))&
    (df["Product"].isin(product_filter))&
    (df["Sales Person"].isin(salesperson_filter))&
    (df["Date"]>=pd.to_datetime(date_range[0]))

    &
    (df["Date"]<=pd.to_datetime(date_range[1]))
]

# CALCULATIONS
# ......................
filtered_df["revenue_per_box"]=filtered_df["Amount"]/ df["Boxes Shipped"]
avg_revenue_per_box=round(filtered_df["revenue_per_box"].mean())



highest_sales_person=filtered_df.groupby("Sales Person")["Amount"].sum()
highest_sales_person.sort_values(ascending=False)

total_no_per_product=filtered_df.groupby("Product")["Boxes Shipped"].count()
total_no_per_product.sort_values(ascending=False)
monthly_sales_trend=filtered_df.groupby("month")["Amount"].sum()
monthly_sales_trend.sort_values(ascending=False)
monthly_sales_trend.index=pd.to_datetime(monthly_sales_trend.index,format="%B")
monthly_sales_trend=monthly_sales_trend.sort_index()
revenue_per_country=filtered_df.groupby("Country")["Amount"].sum()
revenue_per_country=revenue_per_country.sort_values(ascending=False)
average_revenue_product=filtered_df.groupby("Product")["Amount"].mean()
average_revenue_product=average_revenue_product.sort_values(ascending=False)

col1,col2,col3=st.columns(3)
with col1:
    st.metric(label="Total Revenue Generated",value= round(filtered_df["Amount"].sum()))
with col2:
    st.metric(label="Total products Sampled",value=filtered_df["Product"].nunique())
with col3:
    st.metric(label="Average Revenue per Box",value=avg_revenue_per_box)
top_10_sales_person=filtered_df["Sales Person"].value_counts().head(10).index.to_list()
top_10_product=filtered_df["Product"].value_counts().head(10).index.to_list()

chart1,chart2=st.columns(2)

with chart1:
    fig, ax=plt.subplots()
    ax=highest_sales_person[top_10_sales_person].plot(kind="bar",color="blue")
    plt.title("Revenue Generated per Sales Person")
    plt.ylabel("Revenue")
    ax.ticklabel_format(style="plain",axis="y")
    st.pyplot(fig)

with chart2:
    fig, ax=plt.subplots()
    ax=total_no_per_product[top_10_product].plot(kind="bar",color="red")
    plt.title("Boxes Shipped per Product")
    plt.ylabel("Boxes Shipped")
    st.pyplot(fig)

chart3,chart4=st.columns(2)

with chart3:
    fig, ax= plt.subplots()
    ax= monthly_sales_trend.plot(kind="line",marker="o",color="green")
    plt.title("Total Sales per Month")
    plt.ylabel("Month Count")
    st.pyplot(fig)

with chart4:
    fig, ax= plt.subplots()
    ax= revenue_per_country.plot(kind="bar",color= "purple")
    ax.ticklabel_format(style="plain",axis="y")
    plt.title("Revenue per Country")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    st.pyplot(fig)

chart5=st.container()
with chart5:
    fig, ax= plt.subplots()
    ax=average_revenue_product.plot(kind="bar",color="yellow")
    ax.ticklabel_format(style="plain",axis="y")
    plt.title("Revenue per Product")
    plt.ylabel("Revenue")
    st.pyplot(fig)


#........................GEOPANDAS
# LOADING WORLD MAP DATA
url="https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
world=gpd.read_file(url)

merged= world.merge(revenue_per_country,how="left",left_on="name",right_on="Country")


fig,ax=plt.subplots(figsize=(15,8))
fig.patch.set_facecolor("skyblue") #sets the background of the map as royal_blue

# PLOT

merged.plot(column="Amount",cmap="coolwarm",linewidth=0.5, ax=ax,
            edgecolor="yellow",legend=True)
# basedv on the colorworm, color scheme: Orange->Red-light = low revenue-dark =high revenue and linewidth is border
# thickness of countries


# CUSTOMIZE MAP
# SET ocean color

ax.set_title(label="Country_Revenue", fontsize=25)
ax.set_axis_off() # to remove axes

# streamlit setup

st.title("Revenue by country")
st.pyplot(fig)

st.markdown("### Sample Dataset")
st.dataframe(data=df.head(20))


