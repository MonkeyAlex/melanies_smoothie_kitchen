# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title("🥤 Pending Smoothie Orders 🥤")
st.write("Orders that need to be filled.")

cnx = st.connect("snowflake")
session = cnx.session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.ORDERS") \
    .filter(col("ORDER_FILLED") == 0) \
    .collect()

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    
    if submitted:
        og_dataset = session.table("SMOOTHIES.PUBLIC.ORDERS")
        edited_dataset = session.create_dataframe(editable_df)
        
        try:
            og_dataset.merge(edited_dataset
                 , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                 , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                )
            
            st.success('Order(s) Updated!', icon = '👍')
        except:
            st.write('Something went wrong.')
else:
    st.success('There are no pending orders right now', icon = '👍')
