from django.db import models

from bduSuport.models.admission_registration import AdmissionRegistration

class AdmissionRegistrationFile(models.Model):
    class Meta:
        db_table = "admission_registration_file"
    
    admission_registration = models.ForeignKey(AdmissionRegistration, on_delete=models.CASCADE, related_name="admission_registration_files")
    url = models.TextField()