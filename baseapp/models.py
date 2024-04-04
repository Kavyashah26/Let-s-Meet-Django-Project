from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(default='')
    first_name = models.CharField(max_length=100, default='Kavya')  
    last_name = models.CharField(max_length=100, default="Shah")

    def __str__(self):
        return self.user.username

class VideoCall(models.Model):
    meeting_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.meeting_id} - {self.user.username}'

class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_call = models.ForeignKey(VideoCall, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.video_call.meeting_id}'

