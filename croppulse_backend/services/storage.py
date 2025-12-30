"""
Storage Service for CropPulse Africa
Handles file uploads to AWS S3 or local storage
"""
import os
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.files.storage import default_storage
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class StorageService:
    """Service for managing file storage"""
    
    def __init__(self):
        self.use_s3 = settings.DEFAULT_FILE_STORAGE == 'storages.backends.s3boto3.S3Boto3Storage'
        
        if self.use_s3:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
            self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    def upload_file(self, file, file_path: str) -> Optional[str]:
        """
        Upload file to storage
        
        Args:
            file: File object
            file_path: Path where file should be stored
            
        Returns:
            str: URL of uploaded file or None if failed
        """
        try:
            # Save file using Django's storage backend
            saved_path = default_storage.save(file_path, file)
            
            # Get URL
            url = self.get_file_url(saved_path)
            
            logger.info(f'File uploaded successfully: {saved_path}')
            return url
            
        except Exception as e:
            logger.error(f'File upload failed: {str(e)}')
            return None
    
    def delete_file(self, file_path: str) -> bool:
        """
        Delete file from storage
        
        Args:
            file_path: Path of file to delete
            
        Returns:
            bool: True if deleted successfully
        """
        try:
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
                logger.info(f'File deleted: {file_path}')
                return True
            else:
                logger.warning(f'File not found: {file_path}')
                return False
                
        except Exception as e:
            logger.error(f'File deletion failed: {str(e)}')
            return False
    
    def get_file_url(self, file_path: str) -> str:
        """
        Get URL for accessing a file
        
        Args:
            file_path: Path of file
            
        Returns:
            str: Public URL of file
        """
        try:
            return default_storage.url(file_path)
        except Exception as e:
            logger.error(f'Failed to get file URL: {str(e)}')
            return ''
    
    def generate_presigned_url(self, file_path: str, expiration: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL for temporary access to a private file
        
        Args:
            file_path: Path of file
            expiration: URL expiration time in seconds
            
        Returns:
            str: Presigned URL or None if failed
        """
        if not self.use_s3:
            # For local storage, just return the regular URL
            return self.get_file_url(file_path)
        
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': file_path
                },
                ExpiresIn=expiration
            )
            return url
            
        except ClientError as e:
            logger.error(f'Failed to generate presigned URL: {str(e)}')
            return None
    
    def file_exists(self, file_path: str) -> bool:
        """
        Check if file exists in storage
        
        Args:
            file_path: Path of file
            
        Returns:
            bool: True if file exists
        """
        return default_storage.exists(file_path)
    
    def get_file_size(self, file_path: str) -> Optional[int]:
        """
        Get size of file in bytes
        
        Args:
            file_path: Path of file
            
        Returns:
            int: File size in bytes or None if failed
        """
        try:
            return default_storage.size(file_path)
        except Exception as e:
            logger.error(f'Failed to get file size: {str(e)}')
            return None
    
    def copy_file(self, source_path: str, destination_path: str) -> bool:
        """
        Copy file from one location to another
        
        Args:
            source_path: Source file path
            destination_path: Destination file path
            
        Returns:
            bool: True if copied successfully
        """
        try:
            if not default_storage.exists(source_path):
                logger.error(f'Source file does not exist: {source_path}')
                return False
            
            # Read source file
            with default_storage.open(source_path, 'rb') as source_file:
                # Save to destination
                default_storage.save(destination_path, source_file)
            
            logger.info(f'File copied from {source_path} to {destination_path}')
            return True
            
        except Exception as e:
            logger.error(f'File copy failed: {str(e)}')
            return False
    
    def list_files(self, directory: str) -> list:
        """
        List all files in a directory
        
        Args:
            directory: Directory path
            
        Returns:
            list: List of file paths
        """
        try:
            dirs, files = default_storage.listdir(directory)
            return [os.path.join(directory, f) for f in files]
            
        except Exception as e:
            logger.error(f'Failed to list files: {str(e)}')
            return []


# Singleton instance
storage_service = StorageService()
