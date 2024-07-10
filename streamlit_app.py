# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests



# Set the title of the app
st.title('Welcome to the Smoothie Store!')

name_on_smoothie = st.text_input("Name on the Smoothie:")
st.write("""Name on the Smoothie: """, name_on_smoothie)

st.write("""Choose the fruits you want in your custom Smoothie!!""")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/kiwi")
st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width = True)

#option = st.selectbox(
#    'What is your favorite fruit?',
#    ('Banana','Strawberries','Peaches')
#

#st.write('Your favorite fruit is:', option)
#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
     , my_dataframe
    )


if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

       ingredients_string = ''
       #name_on_order = 'Rafeeq'

       for fruit_chosen in ingredients_list:
           ingredients_string += fruit_chosen + ' '
           st.subheader(fruit_chosen + ' Nutrition Information')
           fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
           fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width = True)

           #st.write(ingredients_string)


       my_insert_stmt = """insert into smoothies.public.orders(ingredients,name_on_order)
       values ('""" + ingredients_string + """','""" +name_on_smoothie+ """')"""

       #st.write(my_insert_stmt)
       #st.stop()
       #yes_emoji = "\u2714"

       # Using Unicode characters
       yes_emoji = "\u2705"  # White Heavy Check Mark         
       time_to_insert = st.button('Submit Your Order')
       yes_emoji = "\u2705"  # White Heavy Check Mark
       if time_to_insert:
               
               session.sql(my_insert_stmt).collect()
               st.write(f"Your Smoothie is ordered! {name_on_smoothie} {yes_emoji}")




