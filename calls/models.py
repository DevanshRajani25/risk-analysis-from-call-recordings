from django.db import models

# Create your models here.
class CallAnalysis(models.Model):
    audio_file = models.FileField(upload_to="calls/")
    detected_emotion = models.CharField(max_length=50)
    call_category = models.CharField(max_length=50)
    priority_rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
