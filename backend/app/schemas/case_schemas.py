"""
Pydantic schemas for case management
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class CaseCreate(BaseModel):
    """Schema for creating a new case"""
    client_name: str = Field(..., description="Client full name")
    client_email: str = Field(..., description="Client email address")
    client_phone: Optional[str] = Field(None, description="Client phone number")
    
    property_address: str = Field(..., description="Property address")
    property_type: str = Field(..., description="Property type (house/flat)")
    property_value: int = Field(..., description="Estimated property value")
    
    urgency_level: str = Field(default="MEDIUM", description="Case urgency (LOW/MEDIUM/HIGH)")
    
    # Probate-specific fields
    deceased_name: Optional[str] = Field(None, description="Name of deceased person")
    estate_value: Optional[int] = Field(None, description="Total estate value")
    executor_name: Optional[str] = Field(None, description="Executor name")
    
    # Divorce-specific fields
    marriage_duration: Optional[int] = Field(None, description="Marriage duration in years")
    children_count: Optional[int] = Field(None, description="Number of children")
    dispute_level: Optional[str] = Field(None, description="Level of dispute (LOW/MEDIUM/HIGH)")
    
    additional_notes: Optional[str] = Field(None, description="Additional case notes")

class CaseResponse(BaseModel):
    """Schema for case response"""
    case_id: str
    case_type: str
    status: str
    client_name: str
    property_address: str
    created_at: datetime
    
    class Config:
        from_attributes = True