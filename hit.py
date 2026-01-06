"""
Simple Test Client - For Career AI Agent
Tests all endpoints with base64 encoding
"""

import requests
import json
import base64
import os

BASE_URL = "http://localhost:8000"

def print_header(text):
    print(f"\n{'='*70}")
    print(f"{text}")
    print(f"{'='*70}\n")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

# ==========================================
# TEST 1: HEALTH CHECK
# ==========================================
def test_health():
    print_header("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        
        data = response.json()
        print_success(f"Status: {data['status']}")
        print_info(f"Details: {data['details']}")
        print("\nComponents:")
        for component, status in data['components'].items():
            icon = "✅" if status in ["active", "healthy", "configured"] else "⚠️"
            print(f"  {icon} {component}: {status}")
        
        return data['components']
        
    except Exception as e:
        print_error(f"Health check failed: {e}")
        return None

# ==========================================
# TEST 2: CHAT (Routing Test)
# ==========================================
def test_chat():
    print_header("TEST 2: Chat Agent (Orchestrator Routing)")
    
    queries = [
        ("General Chat", "Hallo, kamu siapa?"),
        ("SQL Query", "How many jobs are in the database?"),
        ("RAG Query", "What skills are needed for data scientist?"),
    ]
    
    for label, query in queries:
        print_info(f"{label}: {query}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": query},
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            print_success("Response received")
            print(f"  {data['response'][:200]}...\n")
            
        except Exception as e:
            print_error(f"Failed: {e}\n")

# ==========================================
# TEST 3: CV ANALYSIS
# ==========================================
def test_cv_analysis():
    print_header("TEST 3: CV Analysis Agent")
    
    # Check if CV file exists
    cv_files = ["cv.jpg"]
    cv_file = None
    
    for f in cv_files:
        if os.path.exists(f):
            cv_file = f
            break
    
    if not cv_file:
        print_error("No CV file found. Skipping test.")
        print_info("Create a CV file (cv.pdf) to test this feature")
        return
    
    try:
        print_info(f"Using CV file: {cv_file}")
        
        # Read and encode
        with open(cv_file, "rb") as f:
            cv_base64 = base64.b64encode(f.read()).decode()
        
        print_info(f"CV encoded to base64 ({len(cv_base64)} chars)")
        print_info("Sending to API (this may take 30-60 seconds)...")
        
        response = requests.post(
            f"{BASE_URL}/cv/analyze",
            json={"cv_base64": cv_base64},
            timeout=90
        )
        response.raise_for_status()
        
        data = response.json()
        print_success("CV Analysis completed!")
        print(f"\n{data['analysis'][:500]}...\n")
        
    except FileNotFoundError:
        print_error("CV file not found")
    except Exception as e:
        print_error(f"CV Analysis failed: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text[:200]}")

# ==========================================
# TEST 4: COVER LETTER
# ==========================================
def test_cover_letter():
    print_header("TEST 4: Cover Letter Generator")
    
    # Check for CV file
    cv_files = ["cv.pdf"]
    cv_file = None
    
    for f in cv_files:
        if os.path.exists(f):
            cv_file = f
            break
    
    if not cv_file:
        print_error("No CV file found. Skipping test.")
        print_info("Create a CV file (cv.pdf) to test this feature")
        return
    
    job_description = """
Software Engineer - Python & Django

We are seeking a talented Software Engineer to join our team.

Requirements:
- 3+ years experience with Python
- Strong knowledge of Django framework
- Experience with REST APIs and microservices
- Understanding of Docker and Kubernetes
- Excellent problem-solving skills

Responsibilities:
- Develop and maintain web applications
- Write clean, maintainable, and testable code
- Collaborate with cross-functional teams
- Participate in code reviews and technical discussions
"""
    
    try:
        print_info(f"Using CV file: {cv_file}")
        
        # Encode CV
        with open(cv_file, "rb") as f:
            cv_base64 = base64.b64encode(f.read()).decode()
        
        print_info("Generating cover letter (this may take 30-60 seconds)...")
        
        response = requests.post(
            f"{BASE_URL}/cover-letter/generate",
            json={
                "cv_base64": cv_base64,
                "job_description": job_description
            },
            timeout=90
        )
        response.raise_for_status()
        
        data = response.json()
        print_success("Cover Letter generated!")
        print(f"\n{data['cover_letter']}\n")
        
    except Exception as e:
        print_error(f"Cover Letter generation failed: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text[:200]}")

# ==========================================
# TEST 5: MOCK INTERVIEW
# ==========================================
def test_interview():
    print_header("TEST 5: Mock Interview Agent")
    
    # Start interview
    try:
        print_info("Starting interview session...")
        response = requests.get(f"{BASE_URL}/interview/start")
        response.raise_for_status()
        
        data = response.json()
        print_success("Interview started!")
        print(f"\n🎤 Interviewer: {data['first_question']}\n")
        
    except Exception as e:
        print_error(f"Failed to start interview: {e}")
        return
    
    # Simulate conversation
    # Answer 1
    answer1 = "I am a software engineer with 3 years of experience in Python and Django. I have worked on several web applications, built REST APIs, and implemented microservices architecture. I'm passionate about writing clean, maintainable code."
    
    print_info(f"👤 Candidate: {answer1[:80]}...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/interview/chat",
            json={
                "candidate_answer": answer1,
                "conversation_history": ""
            },
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        print_success("Interviewer responded!")
        print(f"\n🎤 Interviewer: {data['interviewer_response']}\n")
        
        # Answer 2
        answer2 = "I start by thoroughly understanding the requirements, then I design the architecture considering scalability and maintainability. I follow TDD principles and write comprehensive tests. I also focus on code reviews and documentation."
        
        print_info(f"👤 Candidate: {answer2[:80]}...")
        
        # Build conversation history
        history = f"Q: Tell me about yourself\nA: {answer1}\n"
        
        response = requests.post(
            f"{BASE_URL}/interview/chat",
            json={
                "candidate_answer": answer2,
                "conversation_history": history
            },
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        print_success("Interviewer responded!")
        print(f"\n🎤 Interviewer: {data['interviewer_response']}\n")
        
    except Exception as e:
        print_error(f"Interview chat failed: {e}")

# ==========================================
# RUN ALL TESTS
# ==========================================
def run_all_tests():
    print("\n" + "="*70)
    print("🧪 CAREER AI AGENT - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    # Test 1: Health
    components = test_health()
    
    if not components:
        print_error("\n⚠️  Server not ready. Please check if Docker container is running:")
        print("   docker-compose ps")
        print("   docker-compose logs -f")
        return
    
    # Test 2: Chat
    test_chat()
    
    # Test 3: CV Analysis
    if components.get('advisor_agent') == 'active':
        test_cv_analysis()
    else:
        print_header("TEST 3: CV Analysis")
        print_error("Advisor Agent not available - SKIPPED")
    
    # Test 4: Cover Letter
    if components.get('cover_letter_agent') == 'active':
        test_cover_letter()
    else:
        print_header("TEST 4: Cover Letter")
        print_error("Cover Letter Agent not available - SKIPPED")
    
    # Test 5: Interview
    if components.get('interview_agent') == 'active':
        test_interview()
    else:
        print_header("TEST 5: Mock Interview")
        print_error("Interview Agent not available - SKIPPED")
    
    # Summary
    print_header("TEST SUMMARY")
    print_success("All available tests completed!")
    print_info("Check output above for details")
    print("\n📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Test individual endpoints: http://localhost:8000/docs\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")