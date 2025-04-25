import streamlit as st
import requests
from typing import Dict

def analyze_resume(file, job_role: str) -> Dict:
    url = "https://utkarsh134-fastapi-experience-extractor.hf.space/analyze-resume"
    
    content_type = file.type
    
    files = {
        'resume_file': (file.name, file.getvalue(), content_type),
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
    
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF or DOCX)*", 
        type=["pdf", "docx"],
        help="Supported formats: PDF (.pdf) and Microsoft Word (.docx) documents"
    )
    
    job_role = st.text_input(
        "Enter the Job Role*", 
        placeholder="e.g., Python Developer, React Developer, Data Scientist"
    )
    
    if st.button("Analyze Resume"):
        if not uploaded_file:
            st.error("Please upload a resume file (PDF or DOCX)")
            return
        if not job_role:
            st.error("Please enter the job role")
            return
            
        file_type = uploaded_file.type
        if file_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            st.error("Please upload either a PDF or DOCX file")
            return
            
        with st.spinner("Analyzing resume..."):
            result = analyze_resume(uploaded_file, job_role)
            
            if result:
                st.success("Analysis completed!")
                
                st.header(f"Relevant Experience for {job_role}")
                if result["relevant_experiences"]:
                    for exp in result["relevant_experiences"]:
                        st.subheader(f"{exp['position']} at {exp['company']}")
                        st.write(f"**Duration:** {exp['duration']}")
                        if 'relevant_experience' in exp:
                            st.write("**Relevant Experience:**")
                            st.write(exp['relevant_experience'])
                        st.divider()
                else:
                    st.info("No directly relevant experiences found for the specified job role.")
                
                st.header("Overall Experience Summary")
                st.write(result["experience_summary"])

if __name__ == "__main__":
    main()
