import streamlit as st
import requests
from typing import Dict

def analyze_resume(file, job_role: str) -> Dict:
    url = "https://utkarsh134-fastapiexperience2.hf.space/analyze-resume"
    
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
                
                # Personal Information Section
                st.header("Personal Information")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Name:**", result.get("candidate_name") or "Not found")
                    st.write("**Gender:**", result.get("gender") or "Not specified")
                    st.write("**Date of Birth:**", result.get("date_of_birth") or "Not specified")
                    st.write("**Email:**", result.get("email") or "Not found")
                    st.write("**Mobile:**", result.get("mobile_number") or "Not found")
                
                with col2:
                    st.write("**Address:**", result.get("address") or "Not specified")
                    st.write("**Region:**", result.get("region") or "Not specified")
                    if result.get("pan_number"):
                        st.write("**PAN Number:**", result["pan_number"])
                    if result.get("aadhar_number"):
                        st.write("**Aadhar Number:**", result["aadhar_number"])
                    if result.get("passport_number"):
                        st.write("**Passport Number:**", result["passport_number"])
                
                # Education and Professional Details
                st.header("Education & Professional Details")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Highest Education:**", result.get("highest_education") or "Not specified")
                    st.write("**Current Designation:**", result.get("designation") or "Not specified")
                    # Handle total_experience as both string and float
                    total_exp = result.get('total_experience')
                    if total_exp is not None:
                        if isinstance(total_exp, (int, float)):
                            total_exp = f"{total_exp:g}"  # Remove trailing zeros
                        st.write("**Total Experience:**", f"{total_exp} years")
                    else:
                        st.write("**Total Experience:**", "Not specified")
                
                with col2:
                    if result.get("skills"):
                        st.write("**Skills:**")
                        skills = result["skills"].split(",")
                        for skill in skills:
                            st.write("- " + skill.strip())
                
                # Experience Analysis
                st.header(f"Experience Analysis for {job_role}")
                if result.get("relevant_experience"):
                    st.subheader("Relevant Experience")
                    st.write(result["relevant_experience"])
                else:
                    st.info("No directly relevant experience found for the specified job role.")
                
                st.subheader("Experience Summary")
                st.write(result.get("experience_summary") or "No experience summary available")
                
                if result.get("file_modified_date"):
                    st.caption(f"Resume last modified: {result['file_modified_date']}")

if __name__ == "__main__":
    main()
