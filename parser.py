import pdftotext
import openai
import json

from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains import LLMChain


JSON_OUTPUT_FORMAT ="""
{
   "basic_info":{
      "first_name",
      "last_name",
      "full_name",
      "email",
      "phone_number",
      "location",
      "portfolio_website_url",
      "linkedin_url",
      "github_main_page_url",
      "university",
      "education_level (BS",
      "MS",
      "or PhD)",
      "graduation_year",
      "graduation_month",
   },
   "work_experience":[
      {
         "job_title",
         "company",
         "location",
         "duration",
         "job_summary"
      }
   ]
}
"""

RESUME_EXTRACTION_PROMPT = """
Summarize the professional resume below into a JSON with exactly the following structure: {output_format} 
=== resume text ====
{resume}
"""


class ResumeParser:
    def __init__(self, OPENAI_API_KEY):
        # set GPT-3 API key from the environment vairable
        openai.api_key = OPENAI_API_KEY

    def get_format_instructions(self):
        return JSON_OUTPUT_FORMAT
    
    def query_resume(self, f):
        """
        """
        pdf = pdftotext.PDF(f)
        resume = '/n/n'.join(pdf)
        prompt = PromptTemplate(
            template=RESUME_EXTRACTION_PROMPT,
            input_variables=["resume"],
            partial_variables={"output_format": self.get_format_instructions()}
            )
        model = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.0, max_tokens=3000)
        chain = LLMChain(llm=model, prompt=prompt, verbose=True)

        output = chain.run(resume=resume)
        #resume = json.loads(response_text)
        return output
