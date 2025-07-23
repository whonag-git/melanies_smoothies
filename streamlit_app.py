# Import python packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col
from snowflake.snowpark import Session

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie"""
)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be', name_on_order)

connection_parameters = {
    "account": "ZJAUCLZ-NPB86736",
    "user": "NAGARJUNASUNKARA",
    "password": "NenuNag#123456",
    "role": "SYSADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "SMOOTHIES",
    "schema": "PUBLIC"
}

session = Session.builder.configs(connection_parameters).create()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'), col('Search_On'))
#st.dataframe(data=my_dataframe, use_container_width=True)
pd_df = mydataframe.to_pandas()

ingredients_list = st.multiselect(
'Choose up to 5 ingredients:'
, my_dataframe
, max_selections = 5
)

if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on = pd_df.loc[pd_df["FRUIT_NAME"] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" +name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session. sql(my_insert_stmt). collect()

        st.success('Your Smoothie is ordered!, ' + name_on_order, icon="✅")
      


