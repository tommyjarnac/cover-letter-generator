import streamlit as st
import os

from processor import Processor


# Page title
st.set_page_config(page_title='Cover Letter Generator')
st.title('Cover Letter Generator')




# Resume
resume_file = st.file_uploader('Upload a resume', type='pdf')

# File upload
job_description_file = st.file_uploader('Upload a job description', type='txt')
word_count = st.selectbox(
    'How many words for the cover letter?',
    ('100', '200', '300')
    )
tone = st.selectbox(
    'Select a tone',
    ('casual', 'convincing', 'enthusiastic', 'formal', 'humorous', 'thoughtful')
    )


# Form input and query
result = []
with st.form('myform', clear_on_submit=True):
    if "openai_api_key" in st.secrets:
        openai_api_key = st.secrets['openai_api_key']
    else:
        openai_api_key = st.text_input('OpenAI API Key', type='password')
    submitted = st.form_submit_button('Submit', disabled=not(resume_file and job_description_file))
    if submitted:
        with st.spinner('Calculating...'):
            os.environ["OPENAI_API_KEY"] = openai_api_key
            the_processor = Processor(word_count, tone)
            response = the_processor.process(resume_file, job_description_file)
            st.info(response)
            result.append(response)

#if len(result):
#    st.info(response)
