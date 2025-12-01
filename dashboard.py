import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/data"  # Flask backend


def get_ir_data():
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Error: Status code {response.status_code}"
    except Exception as e:
        return None, f"Error: {e}"


st.set_page_config(page_title="irSight Dashboard", page_icon="🌫️")

st.title("🌫️ irSight – Industrial Emission Monitor (MVP)")

st.caption("Live data from API + smart risk classification")


if st.button("🔄 Refresh Data"):
    data, error = get_ir_data()

    if error:
        st.error(error)
    else:
        st.success("Data fetched successfully!")

        st.write(f"**Timestamp:** {data['timestamp']}")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("PM2.5 (µg/m³)", round(data["pm2_5"], 2))
        with col2:
            st.metric("PM10 (µg/m³)", round(data["pm10"], 2))

        st.subheader("Risk Level")
        st.write(f"**{data['risk']}**")

        st.subheader("Alert")
        st.write(data["alert"])
else:
    st.info("Click 'Refresh Data' to fetch latest reading.")
