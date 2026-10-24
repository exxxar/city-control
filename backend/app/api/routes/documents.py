from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.document import Document, DocumentType
from app.models.problem import Problem
from app.models.user import User
from app.api.deps import get_current_user, require_permission

router = APIRouter()

@router.post("/generate", dependencies=[Depends(require_permission("problem.moderate"))])
def generate_docx(problem_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.get(Problem, problem_id): raise HTTPException(404, "Problem not found")
    # Мок генерации DOCX
    doc = Document(
        doc_type=DocumentType.PROBLEM_CARD, file_url=f"/storage/documents/problems/{problem_id}.docx",
        file_name=f"problem_{problem_id}.docx", problem_id=problem_id, generated_by_id=current_user.id
    )
    db.add(doc); db.commit(); db.refresh(doc)
    return {"id": doc.id, "url": doc.file_url, "message": "DOCX generated (mock)"}

@router.get("/{doc_id}/download")
def download_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.get(Document, doc_id)
    if not doc: raise HTTPException(404, "Document not found")
    return {"url": doc.file_url, "message": "Redirect to file storage in production"}