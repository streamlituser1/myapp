import streamlit as st
import numpy as np

st.write("Hello Greenhouse!")

first_name = st.text_input('First name')
if st.checkbox('Add last name'):
    last_name = st.text_input('Last name')
else:
    last_name = ''
repetitions = st.slider('Repetitions')

st.write(' '.join([first_name, last_name] * repetitions))
