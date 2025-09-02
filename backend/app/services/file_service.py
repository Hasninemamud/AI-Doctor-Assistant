# File upload and processing utilities

import os
import uuid
import aiofiles
from typing import List, Optional, Tuple
from fastapi import UploadFile, HTTPException, status
from PIL import Image
import PyPDF2
import pytesseract
import io

from app.core.config import settings


class FileUploadService:
    """Service for handling file uploads and processing"""
    
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIRECTORY
        self.max_file_size = settings.MAX_FILE_SIZE
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS
        
        # Create upload directory if it doesn't exist
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def validate_file(self, file: UploadFile) -> bool:
        """
        Validate uploaded file
        
        Args:
            file: Uploaded file
            
        Returns:
            bool: True if file is valid
            
        Raises:
            HTTPException: If file is invalid
        """
        # Check file size
        if file.size and file.size > self.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size too large. Maximum size: {self.max_file_size / (1024*1024):.1f}MB"
            )
        
        # Check file extension
        if file.filename:
            file_extension = file.filename.split('.')[-1].lower()
            if file_extension not in self.allowed_extensions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File type not allowed. Allowed types: {', '.join(self.allowed_extensions)}"
                )
        
        return True
    
    async def save_file(self, file: UploadFile) -> Tuple[str, str]:
        """
        Save uploaded file to disk
        
        Args:
            file: Uploaded file
            
        Returns:
            Tuple[str, str]: (file_path, unique_filename)
        """
        # Generate unique filename
        file_extension = file.filename.split('.')[-1].lower() if file.filename else 'bin'
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(self.upload_dir, unique_filename)
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as buffer:
            content = await file.read()
            await buffer.write(content)
        
        return file_path, unique_filename
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete file from disk
        
        Args:
            file_path: Path to file
            
        Returns:
            bool: True if file was deleted
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False


class FileProcessingService:
    """Service for processing uploaded medical files"""
    
    def __init__(self):
        self.upload_service = FileUploadService()
    
    async def extract_text_from_pdf(self, file_path: str) -> str:
        """
        Extract text from PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            str: Extracted text
        """
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing PDF: {str(e)}"
            )
    
    async def extract_text_from_image(self, file_path: str) -> str:
        """
        Extract text from image using OCR
        
        Args:
            file_path: Path to image file
            
        Returns:
            str: Extracted text
        """
        try:
            # Open and process image
            image = Image.open(file_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Extract text using Tesseract OCR
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing image: {str(e)}"
            )
    
    async def process_medical_file(self, file_path: str, file_type: str) -> dict:
        """
        Process medical file and extract relevant information
        
        Args:
            file_path: Path to file
            file_type: Type of file (pdf, jpg, jpeg, png)
            
        Returns:
            dict: Processed file information
        """
        extracted_text = ""
        
        try:
            if file_type.lower() == 'pdf':
                extracted_text = await self.extract_text_from_pdf(file_path)
            elif file_type.lower() in ['jpg', 'jpeg', 'png']:
                extracted_text = await self.extract_text_from_image(file_path)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Unsupported file type: {file_type}"
                )
            
            # Parse medical data from extracted text
            processed_data = await self.parse_medical_data(extracted_text)
            
            return {
                "extracted_text": extracted_text,
                "processed_data": processed_data,
                "processing_status": "completed"
            }
            
        except Exception as e:
            return {
                "extracted_text": extracted_text,
                "processed_data": None,
                "processing_status": "failed",
                "error": str(e)
            }
    
    async def parse_medical_data(self, text: str) -> dict:
        """
        Parse medical data from extracted text
        
        Args:
            text: Extracted text from medical document
            
        Returns:
            dict: Parsed medical data
        """
        # This is a simplified parser - in production, you'd use more sophisticated NLP
        medical_data = {
            "test_results": [],
            "measurements": {},
            "conditions_mentioned": [],
            "medications_mentioned": [],
            "dates": [],
            "patient_info": {}
        }
        
        # Convert text to lowercase for easier parsing
        text_lower = text.lower()
        
        # Common medical test patterns
        test_patterns = [
            "blood pressure", "bp", "cholesterol", "glucose", "hemoglobin", "hgb",
            "white blood cell", "wbc", "red blood cell", "rbc", "platelet",
            "creatinine", "bun", "ast", "alt", "bilirubin", "albumin"
        ]
        
        # Find mentioned tests
        for pattern in test_patterns:
            if pattern in text_lower:
                # Extract value if pattern matches (simplified)
                lines = text.split('\n')
                for line in lines:
                    if pattern in line.lower():
                        medical_data["test_results"].append({
                            "test": pattern,
                            "raw_line": line.strip()
                        })
        
        # Extract numerical values with units
        import re
        
        # Pattern for numbers with common medical units
        number_patterns = re.findall(r'(\d+\.?\d*)\s*(mg/dl|mmol/l|mg|ml|g/dl|%|bpm|mmhg)', text_lower)
        for value, unit in number_patterns:
            medical_data["measurements"][f"{value}_{unit}"] = {
                "value": float(value),
                "unit": unit
            }
        
        # Extract dates
        date_patterns = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text)
        medical_data["dates"] = date_patterns
        
        return medical_data


# Global instances
file_upload_service = FileUploadService()
file_processing_service = FileProcessingService()