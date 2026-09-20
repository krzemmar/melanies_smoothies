# Import python packages
import streamlit as st
import os
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests 

#session = get_active_session()


cnx = st.connection("snowflake")
session = cnx.session()

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

name_on_order = st.text_input("Name on Smoothie:")
if name_on_order:
    st.write("The name on your Smoothie will be:", name_on_order)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list and name_on_order:
    ingredients_string = " ".join(ingredients_list)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(
            "insert into smoothies.public.orders(ingredients, name_on_order) values (?, ?)",
            params=[ingredients_string, name_on_order]
        ).collect()

        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")

 
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

