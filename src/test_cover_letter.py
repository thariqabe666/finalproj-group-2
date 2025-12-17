import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.agents import CoverLetterAgent

def main():
    agent = CoverLetterAgent()
    
    # User provided path
    cv_path = r"C:\Users\Thariq Ahmad Baihaqi\Documents\#AI ENGINEERING\LATIHAN KODING PURRRWADHIKA\#FinalProj\Thariq Ahmad B.A. - AI Engineering - CV.pdf"
    
    # Sample Job Description
    job_description = """
    Job Title: AI Engineer
    Company: Tech Innovators Inc.
    
    Responsibilities:
    - Design and implement AI agents using LLMs.
    - specialized in RAG framework and Vector Database.
    - Work with Python, LangChain, and OpenAI API.
    - Collaborate with cross-functional teams to deploy AI solutions.
    - Optimize model performance and cost.
    
    Requirements:
    - Strong proficiency in Python.
    - Experience with LangChain, LlamaIndex, or similar frameworks.
    - Familiarity with Vector Databases like Qdrant or Pinecone.
    - Problem-solving mindset and ability to work in an agile environment.
    """
    
    print("Generating cover letter...")
    cover_letter = agent.generate_cover_letter(cv_path, job_description)
    
    print("\n" + "="*50)
    print("GENERATED COVER LETTER")
    print("="*50 + "\n")
    print(cover_letter)

if __name__ == "__main__":
    main()
