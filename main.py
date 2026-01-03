"""
Career AI Agent - FastAPI Application
Compatible with new agents (Langfuse, no python-multipart)
"""

import os
import sys
import logging
import base64
import tempfile
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Setup path untuk Docker & local
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))

load_dotenv()

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("CareerAI")

# Global agents
agents = {}

# Safe imports dengan multiple fallback
def safe_import_orchestrator():
    """Import Orchestrator dengan fallback"""
    try:
        from src.agents.orchestrator import Orchestrator
        logger.info("✅ Orchestrator imported from src.agents")
        return Orchestrator
    except ImportError:
        try:
            from agents.orchestrator import Orchestrator
            logger.info("✅ Orchestrator imported from agents")
            return Orchestrator
        except ImportError:
            logger.error("❌ Could not import Orchestrator")
            return None

def safe_import_advisor():
    """Import AdvisorAgent dengan fallback"""
    try:
        from src.agents.advisor_agent import AdvisorAgent
        logger.info("✅ AdvisorAgent imported from src.agents")
        return AdvisorAgent
    except ImportError:
        try:
            from agents.advisor_agent import AdvisorAgent
            logger.info("✅ AdvisorAgent imported from agents")
            return AdvisorAgent
        except ImportError:
            logger.error("❌ Could not import AdvisorAgent")
            return None

def safe_import_cover_letter():
    """Import CoverLetterAgent dengan fallback"""
    try:
        from src.agents.cover_letter_agent import CoverLetterAgent
        logger.info("✅ CoverLetterAgent imported from src.agents")
        return CoverLetterAgent
    except ImportError:
        try:
            from agents.cover_letter_agent import CoverLetterAgent
            logger.info("✅ CoverLetterAgent imported from agents")
            return CoverLetterAgent
        except ImportError:
            logger.error("❌ Could not import CoverLetterAgent")
            return None

def safe_import_interview():
    """Import InterviewAgent dengan fallback"""
    try:
        from src.agents.interview_agent import InterviewAgent
        logger.info("✅ InterviewAgent imported from src.agents")
        return InterviewAgent
    except ImportError:
        try:
            from agents.interview_agent import InterviewAgent
            logger.info("✅ InterviewAgent imported from agents")
            return InterviewAgent
        except ImportError:
            logger.error("❌ Could not import InterviewAgent")
            return None

# Import all agent classes
OrchestratorClass = safe_import_orchestrator()
AdvisorClass = safe_import_advisor()
CoverLetterClass = safe_import_cover_letter()
InterviewClass = safe_import_interview()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("=" * 70)
    logger.info("🚀 Starting Career AI Agent Service...")
    logger.info("=" * 70)
    
    # Validate API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("❌ CRITICAL: OPENAI_API_KEY not found!")
    else:
        logger.info(f"✅ OpenAI API Key: {api_key[:10]}...{api_key[-4:]}")
    
    # Initialize Orchestrator (includes SQL & RAG agents)
    if OrchestratorClass:
        try:
            logger.info("🔧 Initializing Orchestrator (SQL + RAG)...")
            agents['orchestrator'] = OrchestratorClass()
            logger.info("✅ Orchestrator ready")
        except Exception as e:
            logger.error(f"❌ Orchestrator failed: {e}")
    
    # Initialize Advisor Agent
    if AdvisorClass:
        try:
            logger.info("🔧 Initializing AdvisorAgent...")
            agents['advisor'] = AdvisorClass()
            logger.info("✅ AdvisorAgent ready")
        except Exception as e:
            logger.error(f"❌ AdvisorAgent failed: {e}")
    
    # Initialize Cover Letter Agent
    if CoverLetterClass:
        try:
            logger.info("🔧 Initializing CoverLetterAgent...")
            agents['cover_letter'] = CoverLetterClass()
            logger.info("✅ CoverLetterAgent ready")
        except Exception as e:
            logger.error(f"❌ CoverLetterAgent failed: {e}")
    
    # Initialize Interview Agent (without speech recognition)
    if InterviewClass:
        try:
            logger.info("🔧 Initializing InterviewAgent...")
            agents['interview'] = InterviewClass()
            logger.info("✅ InterviewAgent ready")
        except Exception as e:
            logger.error(f"❌ InterviewAgent failed: {e}")
            logger.info("ℹ️  Interview agent may need speech_recognition removed")
    
    logger.info("=" * 70)
    logger.info(f"✅ Server READY! Active agents: {len(agents)}")
    logger.info(f"📍 API Docs: http://localhost:8000/docs")
    logger.info("=" * 70)
    
    yield
    
    # Cleanup
    agents.clear()
    logger.info("🛑 Server shutdown complete")

# Initialize FastAPI
app = FastAPI(
    title="Career AI Agent API",
    description="CV Analysis, Cover Letter, Interview, Chat (base64 upload)",
    version="3.0.0-final",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================
# REQUEST/RESPONSE MODELS
# ========================================

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)

class ChatResponse(BaseModel):
    query: str
    response: str
    status: str

class CVAnalysisRequest(BaseModel):
    cv_base64: str = Field(..., description="CV PDF encoded in base64")

class CVAnalysisResponse(BaseModel):
    analysis: str
    status: str

class CoverLetterRequest(BaseModel):
    cv_base64: str = Field(..., description="CV PDF in base64")
    job_description: str = Field(..., min_length=10)

class CoverLetterResponse(BaseModel):
    cover_letter: str
    status: str

class InterviewRequest(BaseModel):
    candidate_answer: str = Field(..., min_length=1)
    conversation_history: Optional[str] = ""

class InterviewResponse(BaseModel):
    interviewer_response: str
    status: str

# ========================================
# ENDPOINTS
# ========================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "service": "Career AI Agent",
        "version": "3.0.0-final",
        "status": "online",
        "agents": {
            "orchestrator": "active" if "orchestrator" in agents else "inactive",
            "advisor": "active" if "advisor" in agents else "inactive",
            "cover_letter": "active" if "cover_letter" in agents else "inactive",
            "interview": "active" if "interview" in agents else "inactive"
        },
        "endpoints": {
            "health": "GET /health",
            "chat": "POST /chat",
            "cv_analysis": "POST /cv/analyze",
            "cover_letter": "POST /cover-letter/generate",
            "interview_start": "GET /interview/start",
            "interview_chat": "POST /interview/chat",
            "docs": "GET /docs"
        },
        "note": "Use base64 encoding for CV files (no multipart needed)"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Comprehensive health check"""
    components = {
        "api_server": "healthy",
        "openai_key": "configured" if os.getenv("OPENAI_API_KEY") else "missing",
        "orchestrator": "active" if "orchestrator" in agents else "inactive",
        "sql_agent": "active" if "orchestrator" in agents else "inactive",
        "rag_agent": "active" if "orchestrator" in agents else "inactive",
        "advisor_agent": "active" if "advisor" in agents else "inactive",
        "cover_letter_agent": "active" if "cover_letter" in agents else "inactive",
        "interview_agent": "active" if "interview" in agents else "inactive"
    }
    
    active_count = sum(1 for v in components.values() if v in ["active", "healthy", "configured"])
    total_count = len(components)
    
    status_val = "healthy" if active_count >= total_count - 2 else "degraded"
    
    return {
        "status": status_val,
        "details": f"{active_count}/{total_count} components active",
        "components": components
    }

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint - Routes to SQL/RAG/General Chat
    
    Orchestrator will automatically route to:
    - SQL Agent for statistics queries
    - RAG Agent for career advice queries  
    - General chat for greetings/casual conversation
    """
    orchestrator = agents.get("orchestrator")
    
    if not orchestrator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Orchestrator not available. Please check server logs."
        )
    
    try:
        logger.info(f"📩 Chat: {request.message[:80]}...")
        
        # Orchestrator will handle routing
        response = orchestrator.route_query(request.message)
        
        return ChatResponse(
            query=request.message,
            response=response,
            status="success"
        )
        
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )

@app.post("/cv/analyze", response_model=CVAnalysisResponse, tags=["CV Analysis"])
async def analyze_cv(request: CVAnalysisRequest):
    """
    Analyze CV and get career recommendations
    
    **Usage:**
    1. Encode your CV (PDF) to base64
    2. Send in request body as JSON
    
    **Python Example:**
    ```python
    import base64, requests
    
    with open("cv.pdf", "rb") as f:
        cv_base64 = base64.b64encode(f.read()).decode()
    
    response = requests.post(
        "http://localhost:8000/cv/analyze",
        json={"cv_base64": cv_base64}
    )
    print(response.json())
    ```
    
    **Features:**
    - Extracts text from PDF
    - Analyzes skills and experience
    - Retrieves matching jobs from RAG database
    - Provides career recommendations
    """
    advisor = agents.get("advisor")
    
    if not advisor:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Advisor Agent not available"
        )
    
    try:
        logger.info("📄 Analyzing CV...")
        
        # Decode base64 to bytes
        try:
            cv_data = base64.b64decode(request.cv_base64)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid base64 encoding: {str(e)}"
            )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as temp_file:
            temp_file.write(cv_data)
            temp_path = temp_file.name
        
        try:
            # Analyze using AdvisorAgent
            # This will: extract text, profile user, retrieve jobs, generate recommendation
            recommendation = advisor.analyze_and_recommend(temp_path)
            
            return CVAnalysisResponse(
                analysis=recommendation,
                status="success"
            )
            
        finally:
            # Cleanup temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ CV Analysis error: {e}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@app.post("/cover-letter/generate", response_model=CoverLetterResponse, tags=["Cover Letter"])
async def generate_cover_letter(request: CoverLetterRequest):
    """
    Generate tailored cover letter
    
    **Usage:**
    ```python
    import base64, requests
    
    with open("cv.pdf", "rb") as f:
        cv_base64 = base64.b64encode(f.read()).decode()
    
    job_desc = '''
    Software Engineer - Python
    Requirements: 3+ years Python, Django, REST APIs
    '''
    
    response = requests.post(
        "http://localhost:8000/cover-letter/generate",
        json={
            "cv_base64": cv_base64,
            "job_description": job_desc
        }
    )
    print(response.json()["cover_letter"])
    ```
    
    **Features:**
    - Analyzes CV and job requirements
    - Writes professional cover letter
    - Tailored to specific job
    - 300-400 words, business format
    """
    cover_letter_agent = agents.get("cover_letter")
    
    if not cover_letter_agent:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cover Letter Agent not available"
        )
    
    try:
        logger.info("📝 Generating cover letter...")
        
        # Decode base64
        try:
            cv_data = base64.b64decode(request.cv_base64)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid base64 encoding: {str(e)}"
            )
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as temp_file:
            temp_file.write(cv_data)
            temp_path = temp_file.name
        
        try:
            # Generate cover letter
            cover_letter = cover_letter_agent.generate_cover_letter(
                cv_path=temp_path,
                job_description=request.job_description
            )
            
            return CoverLetterResponse(
                cover_letter=cover_letter,
                status="success"
            )
            
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Cover Letter error: {e}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Generation failed: {str(e)}"
        )

@app.get("/interview/start", tags=["Interview"])
async def start_interview():
    """
    Start new mock interview session
    
    Returns initial interview question.
    Use /interview/chat to continue the conversation.
    """
    interview_agent = agents.get("interview")
    
    if not interview_agent:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Interview Agent not available"
        )
    
    try:
        # Initial question
        first_question = "Tell me about yourself and your professional background."
        
        return {
            "message": "Interview session started",
            "first_question": first_question,
            "status": "success",
            "instruction": "Send your answer to POST /interview/chat with conversation_history"
        }
        
    except Exception as e:
        logger.error(f"❌ Start interview error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/interview/chat", response_model=InterviewResponse, tags=["Interview"])
async def interview_chat(request: InterviewRequest):
    """
    Continue mock interview conversation
    
    **Usage:**
    ```python
    import requests
    
    # First answer
    response = requests.post(
        "http://localhost:8000/interview/chat",
        json={
            "candidate_answer": "I have 3 years of Python experience...",
            "conversation_history": ""
        }
    )
    
    # Get feedback and next question
    result = response.json()
    print(result["interviewer_response"])
    
    # Continue conversation
    history = f"Q: Tell me about yourself\\nA: {first_answer}\\n"
    response = requests.post(
        "http://localhost:8000/interview/chat",
        json={
            "candidate_answer": "I focus on clean code...",
            "conversation_history": history
        }
    )
    ```
    
    **Features:**
    - Provides feedback on answers
    - Asks follow-up questions
    - Adapts to candidate's language
    - Professional interview simulation
    """
    interview_agent = agents.get("interview")
    
    if not interview_agent:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Interview Agent not available"
        )
    
    try:
        logger.info(f"🎤 Interview: {request.candidate_answer[:50]}...")
        
        # Get interviewer response
        response = interview_agent.get_response(
            history=request.conversation_history or "",
            user_answer=request.candidate_answer
        )
        
        return InterviewResponse(
            interviewer_response=response,
            status="success"
        )
        
    except Exception as e:
        logger.error(f"❌ Interview error: {e}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Interview failed: {str(e)}"
        )

@app.get("/test", tags=["Testing"])
async def test_endpoint():
    """Simple test endpoint"""
    return {
        "message": "API is working!",
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "active_agents": list(agents.keys())
    }

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.exception("Full traceback:")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status_code": 500}
    )

# Run server
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )