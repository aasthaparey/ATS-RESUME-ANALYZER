#import streamlit as st
# import google.generativeai as genai
# import os
# import PyPDF2 as pdf
# from dotenv import load_dotenv
# import json

# # Load environment variables
# load_dotenv()

# # Configure the Generative AI API
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # --- Helper Function to get Gemini Response ---
# def get_gemini_response(input_text):
#     try:
#         # Change this line:
#         model = genai.GenerativeModel('models/gemini-1.5-flash-latest') # <--- Use this model
#         response = model.generate_content(input_text)
#         return response.text
#     except Exception as e:
#         st.error(f"Error communicating with Gemini: {e}")
#         st.info("Please ensure your API key is correct and 'models/gemini-1.5-flash-latest' is available.")
#         return "Error generating response."
    
# # --- Helper Function to Extract Text from PDF ---
# def input_pdf_text(uploaded_file):
#     reader = pdf.PdfReader(uploaded_file)
#     text = ""
#     for page_num in range(len(reader.pages)): # Changed loop variable to avoid conflict
#         page_obj = reader.pages[page_num]
#         text += str(page_obj.extract_text())
#     return text

# # --- Prompt Template ---
# input_prompt = """
# Hey Act Like a skilled or very experience ATS(Application Tracking System) with a deep understanding of tech field, software engineering, data science, data analyst, and big data engineer. Your task is to evaluate the resume based on the given job description. You must consider the job market is very competitive and you should provide best assistance for improving the resumes. Assign the percentage Matching based on Jd and the missing keywords with high accuracy.

# Resume: {text}
# Job Description: {jd}

# I want the response in one single string having the JSON structure:
# {{"JD Match":"%","MissingKeywords":[],"Profile Summary":""}}
# """

# # --- Streamlit App Layout ---
# st.set_page_config(page_title="Smart ATS Resume Analyzer", layout="centered")
# st.title("🚀 Smart ATS Resume Analyzer")
# st.markdown("### Improve Your Resume for ATS with AI")

# jd = st.text_area("📋 Paste the Job Description Here:", height=200, help="Copy and paste the entire job description.")
# uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF):", type="pdf", help="Please upload your resume in PDF format.")

# submit = st.button("Analyze My Resume")

# # --- Submission Logic ---
# if submit:
#     if uploaded_file is not None:
#         if not jd.strip(): # Check if JD is empty
#             st.warning("Please paste the Job Description before analyzing.")
#         else:
#             with st.spinner("Analyzing your resume... This might take a moment."):
#                 try:
#                     text = input_pdf_text(uploaded_file)
#                     final_prompt = input_prompt.format(text=text, jd=jd)
#                     response_text = get_gemini_response(final_prompt)

#                     st.subheader("📊 ATS Evaluation Result")
#                     try:
#                         # Clean up response for JSON parsing
#                         if response_text.startswith("```json"):
#                             response_text = response_text.replace("```json", "").replace("```", "").strip()

#                         parsed_response = json.loads(response_text)

#                         st.write(f"**📈 JD Match:** {parsed_response.get('JD Match', 'N/A')}")
#                         st.write("**🔑 Missing Keywords:**")
#                         if parsed_response.get('MissingKeywords'):
#                             for keyword in parsed_response['MissingKeywords']:
#                                 st.markdown(f"- {keyword}")
#                         else:
#                             st.write("No specific missing keywords identified (great job!).")

#                         st.write("**📝 Profile Summary/Suggestions:**")
#                         st.write(parsed_response.get('Profile Summary', 'No summary provided.'))

#                     except json.JSONDecodeError as e:
#                         st.warning("Could not parse the AI response as JSON. Displaying raw output.")
#                         st.code(response_text)
#                         st.error(f"JSON parsing error: {e}")

#                 except Exception as e:
#                     st.error(f"An unexpected error occurred during processing: {e}")
#                     st.info("Please ensure your PDF is valid and the job description is pasted correctly.")
#     else:
#         st.warning("Please upload a PDF resume to proceed with the analysis.")

import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



def get_gemini_response(input):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}  
"""

# Streamlit App Layout ---
st.set_page_config(page_title="Smart ATS Resume Analyzer", layout="centered")
st.title("🚀 Smart ATS Resume Analyzer")
st.markdown("### Improve Your Resume for ATS with AI")

jd = st.text_area("📋 Paste the Job Description Here:", height=200, help="Copy and paste the entire job description.")
uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF):", type="pdf", help="Please upload your resume in PDF format.")

submit = st.button("Analyze My Resume")

# --- Submission Logic ---
if submit:
    if uploaded_file is not None:
        if not jd.strip(): # Check if JD is empty
            st.warning("Please paste the Job Description before analyzing.")
        else:
            with st.spinner("Analyzing your resume... This might take a moment."):
                try:
                    text = input_pdf_text(uploaded_file)
                    final_prompt = input_prompt.format(text=text, jd=jd)
                    response_text = get_gemini_response(final_prompt)

                    st.subheader("📊 ATS Evaluation Result")
                    try:
                        # Clean up response for JSON parsing
                        if response_text.startswith("```json"):
                            response_text = response_text.replace("```json", "").replace("```", "").strip()

                        parsed_response = json.loads(response_text)

                        st.write(f"**📈 JD Match:** {parsed_response.get('JD Match', 'N/A')}")
                        st.write("**🔑 Missing Keywords:**")
                        if parsed_response.get('MissingKeywords'):
                            for keyword in parsed_response['MissingKeywords']:
                                st.markdown(f"- {keyword}")
                        else:
                            st.write("No specific missing keywords identified (great job!).")

                        st.write("**📝 Profile Summary/Suggestions:**")
                        st.write(parsed_response.get('Profile Summary', 'No summary provided.'))

                    except json.JSONDecodeError as e:
                        st.warning("Could not parse the AI response as JSON. Displaying raw output.")
                        st.code(response_text)
                        st.error(f"JSON parsing error: {e}")

                except Exception as e:
                    st.error(f"An unexpected error occurred during processing: {e}")
                    st.info("Please ensure your PDF is valid and the job description is pasted correctly.")
    else:
        st.warning("Please upload a PDF resume to proceed with the analysis.")



# ## streamlit app
# st.title("Smart ATS")
# st.text("Improve Your Resume ATS")
# jd=st.text_area("Paste the Job Description")
# uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

# submit = st.button("Submit")
# if submit:
#     if uploaded_file is not None and jd.strip() != "":
#         text = input_pdf_text(uploaded_file)
#         final_prompt = input_prompt.format(text=text, jd=jd)
#         response = get_gemini_response(final_prompt)

#         try:
#             # Sometimes the model returns double curly braces or improperly formatted JSON
#             response_clean = response.replace("```json", "").replace("```", "").strip()
#             parsed_response = json.loads(response_clean)

#             st.subheader("ATS Evaluation Result")
#             st.write(f"**JD Match:** {parsed_response['JD Match']}")
#             st.write(f"**Missing Keywords:** {', '.join(parsed_response['MissingKeywords'])}")
#             st.write(f"**Profile Summary:** {parsed_response['Profile Summary']}")
#         except Exception as e:
#             st.error("Error parsing the response. Here is the raw response:")
#             st.write(response)







