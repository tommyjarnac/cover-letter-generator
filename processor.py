import os
import json

from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from langsmith.wrappers import wrap_openai
from langsmith import traceable

from parser import ResumeParser


OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

COVER_LETTER_TEMPLATE ="""
You're a professional resume coach and can help candidates write the perfect cover letter that gets an interview 100% of the time.

Your task is to write a compelling cover letter for a specific candidate (described by a resume below) and for a given position (described by a job description below)

Guidelines:
- tailor the cover letter to:
    1) match the company's mission, culture and values (information provided in the job description) and 
    2) highlight the candidate's experience and achievements matching the job description requirements
- Have a strong opening statement that makes clear why you want the job and what you bring to the table.
- when possible, share an accomplishment that shows you can address the challenges the employer is facing.
- convey enthusiasm, make it clear you want the position, but keep flattery to a minimum
- keep the cover letter grounded, realistic and believable. Don't exaggerate.
- do not include placeholders
- write the letter in maximum {word_count} words. 
- write with a {tone} tone

=== job description ===
{job}

=== resume ===
{resume}
"""


class Processor(object):
    def __init__(self, word_count, tone):
        self.word_count = word_count
        self.tone = tone

    def process(self, resume_file, job_description_file):
        resume = self.process_resume(resume_file)
        job_description = self.process_job_description(job_description_file)
        response = self.generate_cover_letter(resume, job_description)
        return response

    def process_job_description(self, job_description_file):
        # Load document if file is uploaded
        if job_description_file is not None:
            job_description = job_description_file.read().decode()
            return job_description
        return None

    def generate_cover_letter(self, resume, job_description):
        model = ChatOpenAI(model="gpt-3.5-turbo-0125", max_tokens=4000)
        prompt = PromptTemplate.from_template(COVER_LETTER_TEMPLATE)
        chain = LLMChain(llm=model, prompt=prompt, verbose=True)
        response = chain.run(
            resume=resume, job=job_description, word_count=self.word_count, tone=self.tone)
        return response

    def process_resume(self, resume_file):
        resume_parser = ResumeParser(OPENAI_API_KEY)
        response = resume_parser.query_resume(resume_file)
        try:
            json.loads(response)
        except ValueError:
            raise Exception("we didn't get a proper JSON resume")
        return response


