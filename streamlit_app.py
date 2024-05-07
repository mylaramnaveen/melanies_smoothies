import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!"""
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Snowflake connection - Remove if not needed
# cnx = st.connection("snowflake")
# session = cnx.session()

# Assuming my_dataframe is retrieved correctly from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:", my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '
    st.subheader(fruit_chosen + ' Nutrition Information')
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_chosen}")
    if fruityvice_response.status_code == 200:
        fv_data = fruityvice_response.json()
        # Print the nutritional information
        st.write(fv_data)
    else:
        st.error(f"Failed to fetch nutritional information for {fruit_chosen}. Status code: {fruityvice_response.status_code}")


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
        values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
     
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        success_message = f'Your Smoothie is ordered, {name_on_order}!'
        st.success(success_message, icon="✅")
