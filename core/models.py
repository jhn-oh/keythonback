from django.db import models

# 섬 모델
class Userdata(models.Model):
    islands = 

class Islands(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)  # 완료 여부

    def __str__(self):
        return self.name

class SubGoals(models.Model):
    island = models.ForeignKey(Islands, on_delete=models.CASCADE, related_name="subgoals")
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)  # 완료 여부

    def __str__(self):
        return self.name

class Articles(models.Model):
    subgoal = models.ForeignKey(SubGoals, on_delete=models.CASCADE, related_name="articles")
    article = models.TextField()
    image = models.ImageField(upload_to='articles/')
    uploaddate = models.DateField(auto_now_add=True)  # 자동으로 업로드 날짜 기록

    def __str__(self):
        return f"Article for {self.subgoal.name} on {self.uploaddate}"