# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests as re
import pandas as pd


cntx = st.connection("snowflake")
session = cntx.session()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothe!")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# option = st.selectbox(
#     'What is your Favorite fruit?',
#     ('Banana', 'Strawberries', 'Peaches', 'Kiwi'))

# st.write('Your favorite fruit is:', option)
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be: ', name_on_order)



#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
p_df = my_dataframe.to_pandas()
# st.dataframe(p_df)
# st.stop


ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    ingredients_string = ''
    for fruits_chosen in ingredients_list:
        
        ingredients_string+= fruits_chosen + ' '
        search_on = p_df.loc[p_df['FRUIT_NAME']==fruits_chosen, 'SEARCH_ON'].iloc[0]
        st.write('You searched value: ' + fruits_chosen + 'searched value: ' + search_on + '...')
        st.subheader(fruits_chosen+ ' Nutrition Info')
        response = re.get("https://fruityvice.com/api/fruit/"+ search_on)
        df = st.dataframe(data=response.json(), use_container_width=True)

    # st.write(ingredients_string)
    my_insert_smt = """insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredients_string + """', '"""+ name_on_order+"""')"""
    # st.write(my_insert_smt)
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_smt).collect()
        st.success('Your Smoothie is ordered, '+ name_on_order+ '!', icon="✅")
