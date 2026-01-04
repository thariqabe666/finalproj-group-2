"""
Test Script for Cloud Run Deployment
URL: https://finproimg-49190470440.asia-southeast2.run.app
"""

import requests
import json
import base64
import time

# ⭐ Your Cloud Run URL
BASE_URL = "https://finproimg-49190470440.asia-southeast2.run.app"

# Colors for terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

# ==========================================
# TEST 1: ROOT ENDPOINT
# ==========================================
def test_root():
    print_header("TEST 1: Root Endpoint")
    print_info(f"Testing: {BASE_URL}/")
    
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/", timeout=10)
        elapsed = time.time() - start_time
        
        response.raise_for_status()
        data = response.json()
        
        print_success(f"Status: {response.status_code} OK")
        print_info(f"Response time: {elapsed:.2f}s")
        print("\nResponse:")
        print(json.dumps(data, indent=2))
        
        return True
        
    except requests.exceptions.Timeout:
        print_error("Request timeout (>10s)")
        print_warning("Cloud Run might be cold starting. Try again in 30s.")
        return False
    except Exception as e:
        print_error(f"Failed: {e}")
        return False

# ==========================================
# TEST 2: HEALTH CHECK
# ==========================================
def test_health():
    print_header("TEST 2: Health Check")
    print_info(f"Testing: {BASE_URL}/health")
    
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/health", timeout=30)
        elapsed = time.time() - start_time
        
        response.raise_for_status()
        data = response.json()
        
        print_success(f"Status: {data['status']}")
        print_info(f"Details: {data['details']}")
        print_info(f"Response time: {elapsed:.2f}s")
        
        print("\n📊 Components Status:")
        for component, status in data['components'].items():
            icon = "✅" if status in ["active", "healthy", "configured"] else "⚠️"
            print(f"  {icon} {component}: {status}")
        
        return data['components']
        
    except Exception as e:
        print_error(f"Health check failed: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text[:200]}")
        return None

# ==========================================
# TEST 3: CHAT - GENERAL
# ==========================================
def test_chat_general():
    print_header("TEST 3: Chat - General Conversation")
    
    messages = [
        "Hello, what can you help me with?",
        "Hai, apa yang bisa kamu bantu?",
    ]
    
    for msg in messages:
        print_info(f"Message: {msg}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": msg},
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            print_success("Response received")
            print(f"\n{data['response'][:300]}...\n")
            
        except Exception as e:
            print_error(f"Failed: {e}")

# ==========================================
# TEST 4: CHAT - SQL QUERY
# ==========================================
def test_chat_sql():
    print_header("TEST 4: Chat - SQL Query (Database)")
    
    queries = [
        "How many jobs are in the database?",
        "Berapa jumlah lowongan pekerjaan di database?",
        "Show me 3 jobs for Python developers",
    ]
    
    for query in queries:
        print_info(f"Query: {query}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": query},
                timeout=60  # SQL queries might take longer
            )
            response.raise_for_status()
            
            data = response.json()
            print_success("Response received")
            print(f"\n{data['response'][:400]}...\n")
            
        except Exception as e:
            print_error(f"Failed: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response: {e.response.text[:200]}")

# ==========================================
# TEST 5: CHAT - RAG QUERY
# ==========================================
def test_chat_rag():
    print_header("TEST 5: Chat - RAG Query (Knowledge Base)")
    
    queries = [
        "What skills do I need to become a data scientist?",
        "What are the requirements for a software engineer position?",
    ]
    
    for query in queries:
        print_info(f"Query: {query}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": query},
                timeout=60
            )
            response.raise_for_status()
            
            data = response.json()
            print_success("Response received")
            print(f"\n{data['response'][:400]}...\n")
            
        except Exception as e:
            print_error(f"Failed: {e}")

# ==========================================
# TEST 6: INTERVIEW
# ==========================================
def test_interview():
    print_header("TEST 6: Mock Interview")
    
    try:
        # Start interview
        print_info("Starting interview...")
        response = requests.get(f"{BASE_URL}/interview/start", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print_success("Interview started!")
        print(f"\n🎤 Interviewer: {data['first_question']}\n")
        
        # Answer 1
        answer1 = "I have 3 years of experience in Python and web development. I've worked with Django, FastAPI, and built several REST APIs."
        
        print_info(f"👤 You: {answer1[:80]}...")
        
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
        print(f"\n🎤 Interviewer:\n{data['interviewer_response']}\n")
        
        # Answer 2
        answer2 = "I focus on writing clean, maintainable code following SOLID principles. I also emphasize testing and documentation."
        
        print_info(f"👤 You: {answer2[:80]}...")
        
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
        print(f"\n🎤 Interviewer:\n{data['interviewer_response']}\n")
        
    except Exception as e:
        print_error(f"Interview test failed: {e}")

# ==========================================
# TEST 7: CV ANALYSIS (if you have CV)
# ==========================================
def test_cv_analysis(cv_path=None):
    print_header("TEST 7: CV Analysis")
    
    if not cv_path:
        print_warning("No CV file provided. Skipping test.")
        print_info("To test: python test_cloud_run.py --cv path/to/cv.pdf")
        return
    
    try:
        print_info(f"Reading CV: {cv_path}")
        
        with open(cv_path, "rb") as f:
            cv_base64 = base64.b64encode(f.read()).decode()
        
        print_info(f"CV encoded: {len(cv_base64)} chars")
        print_info("Sending to Cloud Run (may take 60-90s)...")
        
        response = requests.post(
            f"{BASE_URL}/cv/analyze",
            json={"cv_base64": cv_base64},
            timeout=120  # CV analysis takes time
        )
        response.raise_for_status()
        
        data = response.json()
        print_success("CV Analysis completed!")
        print(f"\n{data['analysis'][:500]}...\n")
        
    except FileNotFoundError:
        print_error(f"CV file not found: {cv_path}")
    except requests.exceptions.Timeout:
        print_error("Request timeout. CV analysis takes time on cold start.")
        print_warning("Try again in 1-2 minutes.")
    except Exception as e:
        print_error(f"CV Analysis failed: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text[:200]}")

# ==========================================
# TEST 8: COVER LETTER
# ==========================================
def test_cover_letter(cv_path=None):
    print_header("TEST 8: Cover Letter Generation")
    
    if not cv_path:
        print_warning("No CV file provided. Skipping test.")
        return
    
    job_description = """
Software Engineer - Python & FastAPI

We are seeking a talented Software Engineer to join our team.

Requirements:
- 3+ years experience with Python
- Strong knowledge of FastAPI or Django
- Experience with REST APIs
- Understanding of Docker and Cloud deployment
- Excellent problem-solving skills

Responsibilities:
- Develop and maintain web applications
- Write clean, maintainable code
- Collaborate with cross-functional teams
- Deploy applications to cloud platforms
"""
    
    try:
        print_info(f"Reading CV: {cv_path}")
        
        with open(cv_path, "rb") as f:
            cv_base64 = base64.b64encode(f.read()).decode()
        
        print_info("Generating cover letter (may take 60-90s)...")
        
        response = requests.post(
            f"{BASE_URL}/cover-letter/generate",
            json={
                "cv_base64": cv_base64,
                "job_description": job_description
            },
            timeout=120
        )
        response.raise_for_status()
        
        data = response.json()
        print_success("Cover Letter generated!")
        print(f"\n{data['cover_letter']}\n")
        
    except Exception as e:
        print_error(f"Cover Letter generation failed: {e}")

# ==========================================
# RUN ALL TESTS
# ==========================================
def run_all_tests(cv_path=None):
    print("\n" + "="*70)
    print("🧪 CLOUD RUN DEPLOYMENT - COMPREHENSIVE TEST")
    print("="*70)
    print(f"\n🌐 URL: {BASE_URL}\n")
    
    results = []
    
    # Basic tests (always run)
    results.append(("Root", test_root()))
    time.sleep(1)
    
    components = test_health()
    results.append(("Health", components is not None))
    time.sleep(1)
    
    if not components:
        print_error("\n⚠️  Server not healthy. Stopping tests.")
        return
    
    # Chat tests
    test_chat_general()
    time.sleep(1)
    
    # SQL test (if database available)
    if components.get('sql_agent') == 'active':
        test_chat_sql()
    else:
        print_header("TEST 4: SQL Query")
        print_warning("SQL Agent not active - SKIPPED")
    time.sleep(1)
    
    # RAG test
    if components.get('rag_agent') == 'active':
        test_chat_rag()
    else:
        print_header("TEST 5: RAG Query")
        print_warning("RAG Agent not active - SKIPPED")
    time.sleep(1)
    
    # Interview test
    if components.get('interview_agent') == 'active':
        test_interview()
    else:
        print_header("TEST 6: Interview")
        print_warning("Interview Agent not active - SKIPPED")
    time.sleep(1)
    
    # CV tests (if CV provided)
    if cv_path:
        if components.get('advisor_agent') == 'active':
            test_cv_analysis(cv_path)
        time.sleep(1)
        
        if components.get('cover_letter_agent') == 'active':
            test_cover_letter(cv_path)
    else:
        print_header("TEST 7 & 8: CV Analysis & Cover Letter")
        print_warning("No CV file provided - SKIPPED")
        print_info("Run with: python test_cloud_run.py --cv your_cv.pdf")
    
    # Summary
    print_header("TEST SUMMARY")
    print_success(f"All available tests completed!")
    print_info(f"Cloud Run URL: {BASE_URL}")
    print_info(f"API Docs: {BASE_URL}/docs")
    print("\n📚 Next steps:")
    print("  - Open Swagger UI: " + BASE_URL + "/docs")
    print("  - View logs: gcloud run services logs tail finproimg --region asia-southeast2")
    print("  - Monitor: https://console.cloud.google.com/run/detail/asia-southeast2/finproimg")
    print()

# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    import sys
    
    # Check for CV path argument
    cv_path = None
    if len(sys.argv) > 1:
        if sys.argv[1] == "--cv" and len(sys.argv) > 2:
            cv_path = sys.argv[2]
        else:
            cv_path = sys.argv[1]
    
    try:
        run_all_tests(cv_path)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")