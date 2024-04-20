GPT-3 based cover letter generator.

Generates a cover letter based on:
1) a resume
2) a job description

This will create a customized cover letter:
1) highlighting candidate's skills and experience based on job description requirements
2) targeting specific company values or statements expressed in the job description


### Install
1. Install the system dependencies for pdftotext [see here](https://github.com/jalan/pdftotext)
2. Install Python dependencies
    
    pip install -r requirements.txt

### Getting started
Start the local Streamlit server
    
    streamlit run app.py

1. Pick a PDF file with your resume. You can use resume-example.pdf
2. Pick a TXT file with the job description. You can use job_description_example.txt
3. Indicate the number of words you'd like for the cover letter
4. Indicate the tone of the cover letter
5. Indicate your OpenAI API key in the "OpenAI API Key" field.

Enjoy your customized cover letter!
