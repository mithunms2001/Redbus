import streamlit as st
import pandas as pd
import pymysql

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Mithun252001@',
    'database': 'capstone1_redbus',
    'charset': 'utf8mb4',
}

def fetch_data_from_db(query):
    connection = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        charset=db_config['charset']
    )
    df = pd.read_sql(query, connection)
    connection.close()
    return df

st.title('Bus Booking Data - Filter and Analysis')

with st.sidebar:
    st.header("Filter Options")
    route = st.selectbox("Select the Route", ["All Routes"] + fetch_data_from_db("SELECT DISTINCT Route_Name FROM Bus_Details")['Route_Name'].tolist())
    bustype = st.selectbox("Select the Seat Type", ["All Types", "Sleeper", "Seater", "Non A/C", "A/C"])
    star_rating = st.selectbox("Select the Ratings", ["All Ratings", "1 to 2", "2 to 3", "3 to 4", "4 to 5"])
    price_range = st.selectbox("Bus Fare Range", ["All", "0 - 500", "500 - 1000", "1000 - 1500", "1500+"])
    seat_availability = st.selectbox("Seats Availability", ["All", "0-5", "5-10", "10-20", "20+"])

query = "SELECT * FROM Bus_Details WHERE 1=1"

if route != "All Routes":
    query += f" AND Route_Name = '{route}'"

if bustype != "All Types":
    query += f" AND Bus_Type LIKE '%{bustype}%'" 

if star_rating != "All Ratings":
    rating_min, rating_max = map(float, star_rating.split(' to '))
    query += f" AND Star_Rating BETWEEN {rating_min} AND {rating_max}"

if price_range != "All":
    if price_range == "1500+":
        query += " AND Price > 1500"
    else:
        price_min, price_max = map(int, price_range.split(' - '))
        query += f" AND Price BETWEEN {price_min} AND {price_max}"

if seat_availability != "All":
    seat_min, seat_max = map(int, seat_availability.split('-')) if '-' in seat_availability else (20, 100)
    query += f" AND Seat_Availability BETWEEN {seat_min} AND {seat_max}"

df = fetch_data_from_db(query)

if not df.empty:
    st.dataframe(df)
else:
    st.write("No results found for the selected filters.")

st.subheader("Data Analysis")

if not df.empty:
    st.write(f"**Average Price**: ₹{df['Price'].mean():.2f}")
    st.write(f"**Average Star Rating**: {df['Star_Rating'].mean():.2f}")
    st.write(f"**Total Buses Available**: {df.shape[0]}")
else:
    st.write("No data to analyze")
