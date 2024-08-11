from uuid import uuid4
from django.core.files.uploadedfile import InMemoryUploadedFile
from firebase_admin import storage

class FirebaseStorageProvider():
    __bucket = None
    
    def __init__(self) -> None:
        self.initialize_firebase()

    def initialize_firebase(self):
        self.__bucket = storage.bucket()

    def upload_image(self, file: InMemoryUploadedFile) -> str:
        try:
            print(file)
            blob = self.__bucket.blob(f"{str(uuid4())}_{file.name}")
            blob.upload_from_file(file, content_type=file.content_type)
            blob.make_public()
            
            return blob.public_url
        except Exception as e:
            print("FirebaseStorageProvider.upload_image exc=", e)
            raise e