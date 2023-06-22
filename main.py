import streamlit as st
from foodnotfoodcheck import *
from gpt import *
import os

st.markdown("<h1 style='text-align: center;'>FoodAI</h1>", unsafe_allow_html=True)

if ['openai', 'personality', 'clarifai'] not in st.session_state:
    st.session_state['openai'] = False
    st.session_state['personality'] = False
    st.session_state['clarifai'] = False


openai_key = st.text_input("Input OpenAI key", value="", key='1', type="password")

clarifai_key = st.text_input("Input Clarifai key", value="", key='2', type="password")

personality = st.text_input("Input personality", value="", key='3')

image = st.file_uploader("Upload an image file", type=".jpg")

media_dir = "media"
if not os.path.exists(media_dir):
    os.makedirs(media_dir)

if image is not None:
    image_path = os.path.join(media_dir, image.name)
    with open(os.path.join(image_path), "wb") as f:
        f.write(image.getbuffer())

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        pass
    with col2:
        pass
    with col4:
        pass
    with col5:
        pass
    with col3:
        st.write("\n")
        st.write("\n")
        button = st.button('Get Result')
    if button:
        if openai_key == "":
            st.write('No openai input')
            st.session_state['openai'] = False
        else:
            st.session_state['openai'] = True

        if clarifai_key == "":
            st.write('No clarifai_key input')
            st.session_state['clarifai'] = False
        else:
            st.session_state['clarifai'] = True

        if personality == "":
            st.write('No personality input')
            st.session_state['personality'] = False
        else:
            st.session_state['personality'] = True

        if st.session_state['openai'] and st.session_state['clarifai'] and st.session_state['personality'] is True:
            check = foodnotfood(image_path)
            result1, result2 = gpt(check, personality, image_path, openai_key, clarifai_key)

            if result2 == "openai":
                st.write("Error: Check your openai key")
            elif result2 == "clarifai":
                st.write("Error: Check your clarifai key")
            else:
                st.write("\n")
                st.write("\n")
                st.header(f"Speaking like {personality} :", anchor=False)
                st.markdown(f'<div style="text-align: justify;">{result1}</div>', unsafe_allow_html=True)

                if result2 != "true":
                    st.write("\n")
                    st.write("\n")
                    st.subheader("Alternatives", anchor=False)
                    st.markdown(f'<div style="text-align: justify;">{result2}</div>', unsafe_allow_html=True)
