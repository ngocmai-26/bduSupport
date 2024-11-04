from django.conf import settings
from urllib.parse import urlparse
from uuid import uuid4
from django.core.files.uploadedfile import InMemoryUploadedFile
from firebase_admin import storage
import logging

class FirebaseStorageProvider():
    __bucket = None
    
    def __init__(self) -> None:
        self.initialize_firebase()

    def initialize_firebase(self):
        self.__bucket = storage.bucket()

    def upload_file(self, file: InMemoryUploadedFile) -> str:
        try:
            blob = self.__bucket.blob(f"{str(uuid4())}_{file.name}")
            blob.upload_from_file(file, content_type=file.content_type)
            blob.make_public()
            
            return blob.public_url
        except Exception as e:
            logging.getLogger().exception("FirebaseStorageProvider.upload_file exc=%s", e)
            raise e
        
    def delete_file(self, url: str):
        try:
            url_parse = urlparse(url)
            blob = self.__bucket.blob(url_parse.path.replace(f"/{settings.FIREBASE_STORAGE_BUCKET_URL}/", ""))
            
            if blob.exists():
                blob.delete()
                logging.getLogger().info("FirebaseStorageProvider.delete_file File deleted successfully: %s", url)
            else:
                logging.getLogger().error("FirebaseStorageProvider.delete_file File not found: %s", url)
                
        except Exception as e:
            logging.getLogger().exception("FirebaseStorageProvider.delete_file exc=%s, url=%s", e, url)
            raise e