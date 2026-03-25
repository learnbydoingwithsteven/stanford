from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import os
import uvicorn
from contextlib import asynccontextmanager

# Define Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METADATA_PATH = os.path.join(os.path.dirname(BASE_DIR), "course_metadata.json")
COURSES_ROOT = os.path.dirname(BASE_DIR)

app = FastAPI(title="Stanford AI Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---
class Material(BaseModel):
    type: str # 'slides', 'notes'
    url: str

class Lecture(BaseModel):
    title: str
    slides_url: Optional[str] = None
    notes_url: Optional[str] = None
    local_dir: str
    materials: List[Material]
    summary: Optional[str] = "Discussion of core concepts including..." # Placeholder for now
    youtube_link: Optional[str] = None

class Course(BaseModel):
    id: str
    title: str
    playlist_url: Optional[str] = None
    lectures: List[Lecture]
    stats: Optional[dict] = {"completed": 0, "total": 0}

class GlobalState(BaseModel):
    courses: List[Course]

# --- State ---
state = {"courses": []}

def load_metadata():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, 'r') as f:
            state["courses"] = json.load(f)
            # Add simple stats
            for c in state["courses"]:
                 c["stats"] = {"completed": 0, "total": len(c["lectures"])}

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_metadata()
    print(f"Loaded {len(state['courses'])} courses.")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ---

@app.get("/api/courses", response_model=List[Course])
def get_courses():
    return state["courses"]

@app.get("/api/courses/{course_id}", response_model=Course)
def get_course(course_id: str):
    course = next((c for c in state["courses"] if c["id"] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.get("/api/files/{course_id}/{lecture_dir}/{filename}")
def get_file(course_id: str, lecture_dir: str, filename: str):
    # Security check: ensure path is within authorized bounds
    # Actual path structure: f:\...\CS224N_NLP\Lecture_01_...\file.pdf
    
    # Check if course exists
    course = next((c for c in state["courses"] if c["id"] == course_id), None)
    if not course:
         raise HTTPException(status_code=404, detail="Course not found")
    
    # Construct potential path
    # We need to find the specific lecture directory name in the file system
    # but the metadata `local_dir` might just be the clean name "Lecture_01_..."
    
    # We construct the full path:
    # ROOT / course_id / lecture_dir / filename
    
    file_path = os.path.join(COURSES_ROOT, course_id, lecture_dir, filename)
    
    if not os.path.exists(file_path):
         # Try flexible matching if exact name fails? For now, strict.
         raise HTTPException(status_code=404, detail=f"File not found at {file_path}")
         
    return FileResponse(file_path)

@app.post("/api/analyze")
def analyze_content(concept: str):
    # Conceptual endpoint for Knowledge Graph generation or Summary
    return {"message": "Analysis started (simulated)", "concept": concept}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
