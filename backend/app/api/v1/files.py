# File upload API endpoints

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.models import User, TestReport, Consultation, ProcessingStatusEnum
from app.schemas.schemas import FileUploadResponse, TestReport as TestReportSchema
from app.services.file_service import file_upload_service, file_processing_service

router = APIRouter()


@router.post("/upload/{consultation_id}", response_model=FileUploadResponse)
async def upload_test_report(
    consultation_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Upload a test report file for a consultation
    
    Args:
        consultation_id: Consultation ID
        file: Uploaded file
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        FileUploadResponse: Upload response with file information
        
    Raises:
        HTTPException: If consultation not found or file invalid
    """
    # Verify consultation exists and belongs to user
    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not consultation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consultation not found"
        )
    
    # Validate file
    file_upload_service.validate_file(file)
    
    # Save file
    file_path, unique_filename = await file_upload_service.save_file(file)
    
    # Get file type
    file_type = file.filename.split('.')[-1].lower() if file.filename else 'bin'
    
    # Create test report record
    test_report = TestReport(
        consultation_id=consultation_id,
        file_name=file.filename or unique_filename,
        file_path=file_path,
        file_type=file_type,
        file_size=file.size or 0,
        processing_status=ProcessingStatusEnum.PENDING
    )
    
    db.add(test_report)
    db.commit()
    db.refresh(test_report)
    
    # Start background processing (in a real app, you'd use Celery or similar)
    # For now, we'll process it immediately
    try:
        processing_result = await file_processing_service.process_medical_file(
            file_path, file_type
        )
        
        # Update test report with processing results
        test_report.extracted_text = processing_result.get("extracted_text")
        test_report.processed_data = processing_result.get("processed_data")
        test_report.processing_status = ProcessingStatusEnum.COMPLETED
        
        db.commit()
        
    except Exception as e:
        # Mark as failed if processing fails
        test_report.processing_status = ProcessingStatusEnum.FAILED
        db.commit()
    
    return FileUploadResponse(
        file_id=test_report.id,
        file_name=test_report.file_name,
        file_size=test_report.file_size,
        upload_url=f"/uploads/{unique_filename}",
        processing_status=test_report.processing_status
    )


@router.get("/{file_id}", response_model=TestReportSchema)
async def get_test_report(
    file_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get test report information
    
    Args:
        file_id: Test report ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        TestReportSchema: Test report information
        
    Raises:
        HTTPException: If test report not found
    """
    # Get test report with consultation check
    test_report = db.query(TestReport).join(Consultation).filter(
        TestReport.id == file_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not test_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test report not found"
        )
    
    return test_report


@router.delete("/{file_id}")
async def delete_test_report(
    file_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a test report
    
    Args:
        file_id: Test report ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If test report not found
    """
    # Get test report with consultation check
    test_report = db.query(TestReport).join(Consultation).filter(
        TestReport.id == file_id,
        Consultation.user_id == current_user.id
    ).first()
    
    if not test_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test report not found"
        )
    
    # Delete file from disk
    file_upload_service.delete_file(test_report.file_path)
    
    # Delete from database
    db.delete(test_report)
    db.commit()
    
    return {"message": "Test report deleted successfully"}