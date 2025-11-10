import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, Optional

from database import create_document, get_documents, db
from schemas import (
    Tenant, User, Teacher, Parent, Student, Class, Enrollment, Attendance,
    GradeRecord, Invoice, Payment, Announcement, Notification, Resource,
    Assignment, Quiz, QuizSubmission, ActivityLog
)

app = FastAPI(title="EDmin API", version="1.0", description="SaaS-based Student & Education Management Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------
# Health & Diagnostics
# ---------------------------------------------
@app.get("/")
def read_root():
    return {"message": "EDmin Backend is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:20]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# ---------------------------------------------
# Helper to map model to collection name
# ---------------------------------------------

def collection_name(model_cls: Any) -> str:
    return model_cls.__name__.lower()

# ---------------------------------------------
# Minimal CRUD Endpoints (Create + List) for key entities
# Using database helper functions for persistence
# ---------------------------------------------

class CreateResponse(BaseModel):
    id: str

@app.post("/tenants", response_model=CreateResponse)
async def create_tenant(payload: Tenant):
    _id = create_document(collection_name(Tenant), payload)
    return {"id": _id}

@app.get("/tenants")
async def list_tenants():
    return get_documents(collection_name(Tenant))

@app.post("/users", response_model=CreateResponse)
async def create_user(payload: User):
    _id = create_document(collection_name(User), payload)
    return {"id": _id}

@app.get("/users")
async def list_users(tenant_id: Optional[str] = None):
    filt: Dict[str, Any] = {"tenant_id": tenant_id} if tenant_id else {}
    return get_documents(collection_name(User), filt)

@app.post("/students", response_model=CreateResponse)
async def create_student(payload: Student):
    _id = create_document(collection_name(Student), payload)
    return {"id": _id}

@app.get("/students")
async def list_students(tenant_id: Optional[str] = None, grade_level: Optional[str] = None):
    filt: Dict[str, Any] = {}
    if tenant_id:
        filt["tenant_id"] = tenant_id
    if grade_level:
        filt["grade_level"] = grade_level
    return get_documents(collection_name(Student), filt)

@app.post("/classes", response_model=CreateResponse)
async def create_class(payload: Class):
    _id = create_document(collection_name(Class), payload)
    return {"id": _id}

@app.get("/classes")
async def list_classes(tenant_id: Optional[str] = None):
    filt: Dict[str, Any] = {"tenant_id": tenant_id} if tenant_id else {}
    return get_documents(collection_name(Class), filt)

@app.post("/enrollments", response_model=CreateResponse)
async def create_enrollment(payload: Enrollment):
    _id = create_document(collection_name(Enrollment), payload)
    return {"id": _id}

@app.get("/enrollments")
async def list_enrollments(tenant_id: Optional[str] = None, class_id: Optional[str] = None, student_id: Optional[str] = None):
    filt: Dict[str, Any] = {}
    if tenant_id:
        filt["tenant_id"] = tenant_id
    if class_id:
        filt["class_id"] = class_id
    if student_id:
        filt["student_id"] = student_id
    return get_documents(collection_name(Enrollment), filt)

@app.post("/attendance", response_model=CreateResponse)
async def mark_attendance(payload: Attendance):
    _id = create_document(collection_name(Attendance), payload)
    return {"id": _id}

@app.get("/attendance")
async def list_attendance(tenant_id: Optional[str] = None, class_id: Optional[str] = None, student_id: Optional[str] = None, date: Optional[str] = None):
    filt: Dict[str, Any] = {}
    if tenant_id:
        filt["tenant_id"] = tenant_id
    if class_id:
        filt["class_id"] = class_id
    if student_id:
        filt["student_id"] = student_id
    if date:
        filt["date"] = date
    return get_documents(collection_name(Attendance), filt)

@app.post("/grades", response_model=CreateResponse)
async def create_grade(payload: GradeRecord):
    _id = create_document(collection_name(GradeRecord), payload)
    return {"id": _id}

@app.get("/grades")
async def list_grades(tenant_id: Optional[str] = None, student_id: Optional[str] = None, class_id: Optional[str] = None, term: Optional[str] = None):
    filt: Dict[str, Any] = {}
    if tenant_id:
        filt["tenant_id"] = tenant_id
    if student_id:
        filt["student_id"] = student_id
    if class_id:
        filt["class_id"] = class_id
    if term:
        filt["term"] = term
    return get_documents(collection_name(GradeRecord), filt)

@app.post("/invoices", response_model=CreateResponse)
async def create_invoice(payload: Invoice):
    _id = create_document(collection_name(Invoice), payload)
    return {"id": _id}

@app.get("/invoices")
async def list_invoices(tenant_id: Optional[str] = None, student_id: Optional[str] = None, status: Optional[str] = None):
    filt: Dict[str, Any] = {}
    if tenant_id:
        filt["tenant_id"] = tenant_id
    if student_id:
        filt["student_id"] = student_id
    if status:
        filt["status"] = status
    return get_documents(collection_name(Invoice), filt)

@app.post("/payments", response_model=CreateResponse)
async def create_payment(payload: Payment):
    _id = create_document(collection_name(Payment), payload)
    return {"id": _id}

@app.get("/payments")
async def list_payments(tenant_id: Optional[str] = None, invoice_id: Optional[str] = None, status: Optional[str] = None):
    filt: Dict[str, Any] = {}
    if tenant_id:
        filt["tenant_id"] = tenant_id
    if invoice_id:
        filt["invoice_id"] = invoice_id
    if status:
        filt["status"] = status
    return get_documents(collection_name(Payment), filt)

@app.post("/announcements", response_model=CreateResponse)
async def create_announcement(payload: Announcement):
    _id = create_document(collection_name(Announcement), payload)
    return {"id": _id}

@app.get("/announcements")
async def list_announcements(tenant_id: Optional[str] = None):
    filt: Dict[str, Any] = {"tenant_id": tenant_id} if tenant_id else {}
    return get_documents(collection_name(Announcement), filt)

@app.post("/resources", response_model=CreateResponse)
async def create_resource(payload: Resource):
    _id = create_document(collection_name(Resource), payload)
    return {"id": _id}

@app.get("/resources")
async def list_resources(tenant_id: Optional[str] = None, subject: Optional[str] = None, grade_level: Optional[str] = None):
    filt: Dict[str, Any] = {}
    if tenant_id:
        filt["tenant_id"] = tenant_id
    if subject:
        filt["subject"] = subject
    if grade_level:
        filt["grade_level"] = grade_level
    return get_documents(collection_name(Resource), filt)

@app.post("/assignments", response_model=CreateResponse)
async def create_assignment(payload: Assignment):
    _id = create_document(collection_name(Assignment), payload)
    return {"id": _id}

@app.get("/assignments")
async def list_assignments(tenant_id: Optional[str] = None, class_id: Optional[str] = None):
    filt: Dict[str, Any] = {}
    if tenant_id:
        filt["tenant_id"] = tenant_id
    if class_id:
        filt["class_id"] = class_id
    return get_documents(collection_name(Assignment), filt)

@app.post("/quizzes", response_model=CreateResponse)
async def create_quiz(payload: Quiz):
    _id = create_document(collection_name(Quiz), payload)
    return {"id": _id}

@app.get("/quizzes")
async def list_quizzes(tenant_id: Optional[str] = None, class_id: Optional[str] = None):
    filt: Dict[str, Any] = {}
    if tenant_id:
        filt["tenant_id"] = tenant_id
    if class_id:
        filt["class_id"] = class_id
    return get_documents(collection_name(Quiz), filt)

@app.post("/quiz-submissions", response_model=CreateResponse)
async def create_quiz_submission(payload: QuizSubmission):
    _id = create_document(collection_name(QuizSubmission), payload)
    return {"id": _id}

@app.get("/quiz-submissions")
async def list_quiz_submissions(tenant_id: Optional[str] = None, quiz_id: Optional[str] = None, student_id: Optional[str] = None):
    filt: Dict[str, Any] = {}
    if tenant_id:
        filt["tenant_id"] = tenant_id
    if quiz_id:
        filt["quiz_id"] = quiz_id
    if student_id:
        filt["student_id"] = student_id
    return get_documents(collection_name(QuizSubmission), filt)

@app.post("/activity", response_model=CreateResponse)
async def track_activity(payload: ActivityLog):
    _id = create_document(collection_name(ActivityLog), payload)
    return {"id": _id}

@app.get("/activity")
async def list_activity(tenant_id: Optional[str] = None, user_id: Optional[str] = None, action: Optional[str] = None):
    filt: Dict[str, Any] = {}
    if tenant_id:
        filt["tenant_id"] = tenant_id
    if user_id:
        filt["user_id"] = user_id
    if action:
        filt["action"] = action
    return get_documents(collection_name(ActivityLog), filt)

# ---------------------------------------------
# Schema exposure for tooling
# ---------------------------------------------
@app.get("/schema")
async def get_schema():
    return {
        "tenant": Tenant.model_json_schema(),
        "user": User.model_json_schema(),
        "teacher": Teacher.model_json_schema(),
        "parent": Parent.model_json_schema(),
        "student": Student.model_json_schema(),
        "class": Class.model_json_schema(),
        "enrollment": Enrollment.model_json_schema(),
        "attendance": Attendance.model_json_schema(),
        "graderecord": GradeRecord.model_json_schema(),
        "invoice": Invoice.model_json_schema(),
        "payment": Payment.model_json_schema(),
        "announcement": Announcement.model_json_schema(),
        "notification": Notification.model_json_schema(),
        "resource": Resource.model_json_schema(),
        "assignment": Assignment.model_json_schema(),
        "quiz": Quiz.model_json_schema(),
        "quizsubmission": QuizSubmission.model_json_schema(),
        "activitylog": ActivityLog.model_json_schema(),
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
