"""
Database Schemas for EDmin (SaaS-based Student & Education Management)

Each Pydantic model represents a MongoDB collection.
Collection name = lowercase of class name (e.g., Tenant -> "tenant").

These schemas are also exposed via GET /schema for tooling/validation.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import date, datetime

# -----------------------------------------------------------------------------
# MULTI-TENANCY
# -----------------------------------------------------------------------------
class Tenant(BaseModel):
    name: str = Field(..., description="Institution name")
    code: str = Field(..., description="Unique short code for the institution")
    address: Optional[str] = Field(None, description="Institution address")
    contact_email: Optional[EmailStr] = Field(None, description="Primary contact email")
    contact_phone: Optional[str] = Field(None, description="Primary contact phone")
    timezone: Optional[str] = Field("UTC", description="Institution timezone")
    status: str = Field("active", description="active | suspended | archived")

# -----------------------------------------------------------------------------
# USERS & ROLES
# -----------------------------------------------------------------------------
class User(BaseModel):
    tenant_id: str = Field(..., description="Related tenant (institution)")
    name: str
    email: EmailStr
    role: str = Field(..., description="admin | teacher | student | parent | district_admin")
    password_hash: Optional[str] = Field(None, description="Hash only; never store plain text")
    is_active: bool = True

class Teacher(BaseModel):
    tenant_id: str
    user_id: Optional[str] = Field(None, description="User account ID if linked")
    employee_id: Optional[str] = None
    subjects: List[str] = []
    hire_date: Optional[date] = None
    status: str = "active"

class Parent(BaseModel):
    tenant_id: str
    user_id: Optional[str] = None
    children_ids: List[str] = []

# -----------------------------------------------------------------------------
# STUDENTS & ACADEMICS
# -----------------------------------------------------------------------------
class Student(BaseModel):
    tenant_id: str
    user_id: Optional[str] = None
    student_number: str
    first_name: str
    last_name: str
    grade_level: str
    dob: Optional[date] = None
    guardian_contact: Optional[str] = None
    address: Optional[str] = None
    status: str = "active"

class Class(BaseModel):
    tenant_id: str
    name: str
    code: str
    subject: str
    grade_level: str
    teacher_id: Optional[str] = None
    schedule: Dict[str, Any] = Field(default_factory=dict, description="Timetable/schedule data")

class Enrollment(BaseModel):
    tenant_id: str
    class_id: str
    student_id: str
    enrollment_date: Optional[date] = None
    status: str = "enrolled"

class Attendance(BaseModel):
    tenant_id: str
    class_id: str
    student_id: str
    date: date
    status: str = Field(..., description="present | absent | late | excused")
    method: Optional[str] = Field(None, description="manual | biometric | rfid")

class GradeRecord(BaseModel):
    tenant_id: str
    student_id: str
    class_id: str
    term: str
    scores: Dict[str, float] = Field(default_factory=dict, description="e.g., { 'midterm': 88, 'final': 92 }")
    remarks: Optional[str] = None

# -----------------------------------------------------------------------------
# FINANCE
# -----------------------------------------------------------------------------
class Invoice(BaseModel):
    tenant_id: str
    student_id: str
    title: str
    amount: float
    due_date: Optional[date] = None
    status: str = Field("unpaid", description="unpaid | paid | overdue | cancelled")
    meta: Dict[str, Any] = Field(default_factory=dict)

class Payment(BaseModel):
    tenant_id: str
    invoice_id: str
    method: str = Field(..., description="stripe | upi | card | netbanking | paypal | cash")
    amount: float
    reference: Optional[str] = None
    status: str = Field("success", description="success | failed | pending")

# -----------------------------------------------------------------------------
# COMMUNICATION
# -----------------------------------------------------------------------------
class Announcement(BaseModel):
    tenant_id: str
    title: str
    message: str
    audience: List[str] = Field(default_factory=lambda: ["students", "teachers", "parents"])  # segments
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None

class Notification(BaseModel):
    tenant_id: str
    user_id: str
    title: str
    message: str
    type: str = Field("info", description="info | success | warning | error")
    is_read: bool = False

# -----------------------------------------------------------------------------
# CURRICULUM, ASSIGNMENTS & ASSESSMENTS
# -----------------------------------------------------------------------------
class Resource(BaseModel):
    tenant_id: str
    title: str
    subject: str
    grade_level: str
    difficulty: Optional[str] = None
    url: Optional[str] = None
    tags: List[str] = []

class Assignment(BaseModel):
    tenant_id: str
    class_id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class Quiz(BaseModel):
    tenant_id: str
    class_id: str
    title: str
    questions: List[Dict[str, Any]] = Field(default_factory=list, description="Array of questions with options/answers")

class QuizSubmission(BaseModel):
    tenant_id: str
    quiz_id: str
    student_id: str
    answers: List[Any] = []
    score: Optional[float] = None

# -----------------------------------------------------------------------------
# ANALYTICS TRACKING (BASIC)
# -----------------------------------------------------------------------------
class ActivityLog(BaseModel):
    tenant_id: str
    user_id: Optional[str] = None
    action: str
    entity: str
    entity_id: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)
