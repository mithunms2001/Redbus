import streamlit as st
import pandas as pd
import pymysql

db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Mithun252001@',
    'database': 'bus_data',
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
    route = st.selectbox("Select the Route", ["All Routes"] + fetch_data_from_db("SELECT DISTINCT route_name FROM bus_routes")['route_name'].tolist())
    bustype = st.selectbox("Select the Seat Type", ["All Types", "Sleeper", "Seater", "Non A/C", "A/C"])
    star_rating = st.selectbox("Select the Ratings", ["All Ratings", "1 to 2", "2 to 3", "3 to 4", "4 to 5"])
    time_filter = st.selectbox("Starting time", ["All", "06:00 - 12:00", "12:00 - 18:00", "18:00 - 00:00", "00:00 - 06:00"])
    price_range = st.selectbox("Bus Fare Range", ["All", "0 - 500", "500 - 1000", "1000 - 1500", "1500+"])
    seat_availability = st.selectbox("Seats Availability", ["All", "0-5", "5-10", "10-20", "20+"])

query = "SELECT * FROM bus_routes WHERE 1=1"

if route != "All Routes":
    query += f" AND route_name = '{route}'"

if bustype != "All Types":
    query += f" AND bustype LIKE '%{bustype}%'"

if star_rating != "All Ratings":
    rating_min, rating_max = map(float, star_rating.split(' to '))
    query += f" AND star_rating BETWEEN {rating_min} AND {rating_max}"

if time_filter != "All":
    time_ranges = {
        "06:00 - 12:00": ("06:00:00", "12:00:00"),
        "12:00 - 18:00": ("12:00:00", "18:00:00"),
        "18:00 - 00:00": ("18:00:00", "23:59:59"),
        "00:00 - 06:00": ("00:00:00", "06:00:00")
    }
    time_min, time_max = time_ranges[time_filter]
    query += f" AND departing_time BETWEEN '{time_min}' AND '{time_max}'"

if price_range != "All":
    price_min, price_max = map(int, price_range.split(' - ')) if ' - ' in price_range else (1500, 10000)
    query += f" AND price BETWEEN {price_min} AND {price_max}"

if seat_availability != "All":
    seat_min, seat_max = map(int, seat_availability.split('-')) if '-' in seat_availability else (20, 100)
    query += f" AND seats_available BETWEEN {seat_min} AND {seat_max}"

df = fetch_data_from_db(query)

if 'route_link' in df.columns:
    df = df.drop(columns=['route_link'])

if not df.empty:
    st.dataframe(df)
else:
    st.write("No results found for the selected filters.")

st.subheader("Data Analysis")

if not df.empty:
    st.write(f"**Average Price**: ₹{df['price'].mean():.2f}")
    st.write(f"**Average Star Rating**: {df['star_rating'].mean():.2f}")
    st.write(f"**Total Buses Available**: {df.shape[0]}")
else:
    st.write("No data to analyze")
