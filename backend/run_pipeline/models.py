from django.db import models

class UploadProcess(models.Model):
    process_id = models.AutoField(primary_key=True)  # Auto-incremented ID for each process
    description = models.TextField()

class FileUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    process = models.ForeignKey(UploadProcess, related_name='uploads', on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name