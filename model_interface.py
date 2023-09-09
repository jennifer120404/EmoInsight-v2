# in new conda env install below pakages
# pip install tensorflow==2.13.0
# pip install -U "tensorflow-text==2.13.*"
# pip install -q streamlit==1.26.0
# pip install openai==0.28.0

import openai
import streamlit as st
import tensorflow as tf
import tensorflow_text
import numpy as np

###############################################
# Setting up styles for app
###############################################
# Set page title and icon
# st.set_page_config(page_title="Bard ChatBot",
#                    page_icon=":robot_face:",
#                    initial_sidebar_state="collapsed",)

# # Custom css styles
# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# st.title("ChatGPT-like clone")

openai.api_key = "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"
reloaded_model = tf.saved_model.load('one_2')

emotion_categories = {
    0: 'anger',
    1: 'fear',
    2: 'joy',
    3: 'love',
    4: 'neutral',
    5: 'sadness',
    6: 'surprise'
}

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# col1, col2 = st.columns([4, 3])

# with col1:
#     st.markdown('helow')
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])


# with col2:
    # a = st.session_state.messages[-1]['content']
    # st.markdown(len(st.session_state.messages) > 1)
    # if len(st.session_state.messages) != 0:
    # st.markdown('prediction:')
    # st.markdown(st.session_state.messages[-2])
    # q = st.session_state.messages[-2]['content']
    # emotion = reloaded_model([q])
    # true_classes = np.argmax(emotion, axis=1)
    # emotion_category = emotion_categories.get(int(true_classes))
    # st.markdown(emotion_category)


if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # USER
    with st.chat_message("user"):
        st.markdown(prompt)

    # EMOTION
    with st.chat_message("Emotion", avatar='😶'):
        emotion = reloaded_model([prompt])
        true_classes = np.argmax(emotion, axis=1)
        emotion_category = emotion_categories.get(int(true_classes))
        st.write("Emotion: {}".format(emotion_category))

    # AI BOT
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")

            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})


uploaded_files = st.file_uploader(
    "Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)
