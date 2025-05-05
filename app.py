import streamlit as st
import requests
from typing import Dict
import urllib.parse

def analyze_resume(file, job_role: str) -> Dict:
    url = "https://utkarsh134-fastapiexperience2.hf.space/analyze-resume"
    content_type = file.type
    encoded_filename = urllib.parse.quote(file.name)
    files = {
        'resume_file': (encoded_filename, file.getvalue(), content_type),
        'job_role': (None, job_role)
    }
    
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with backend: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="Resume Experience Analyzer",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("Resume Experience Analyzer")
    st.write("Upload a resume and specify the job role to analyze relevant experience.")
    
    uploaded_files = st.file_uploader(
        "Upload Resumes (PDF or DOCX)*", 
        type=["pdf", "docx"],
        accept_multiple_files=True,
        help="Supported formats: PDF (.pdf) and Microsoft Word (.docx) documents"
    )
    
    job_role = st.text_input(
        "Enter the Job Role*", 
        placeholder="e.g., Python Developer, React Developer, Data Scientist"
    )
    
    if st.button("Analyze Resumes"):
        if not uploaded_files:
            st.error("Please upload at least one resume file (PDF or DOCX)")
            return
        if not job_role:
            st.error("Please enter the job role")
            return
            
        for uploaded_file in uploaded_files:
            file_type = uploaded_file.type
            if file_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                st.error(f"Invalid file type for {uploaded_file.name}. Please upload either PDF or DOCX files")
                continue
                
            with st.spinner(f"Analyzing {uploaded_file.name}..."):
                result = analyze_resume(uploaded_file, job_role)
                
                if result:
                    with st.expander(f"Results for {uploaded_file.name}", expanded=True):
                        name = result.get("candidate_name") or "Not found"
                        designation = result.get("designation") or "Not specified"
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Name:**", name)
                        with col2:
                            st.write("**Current Designation:**", designation)
                        
                        st.subheader(f"Relevant Experience for {job_role}")
                        if result.get("relevant_experience"):
                            st.write(result["relevant_experience"])
                        else:
                            st.info("No directly relevant experience found for the specified job role.")
                        
                        st.divider()

if __name__ == "__main__":
    main()
