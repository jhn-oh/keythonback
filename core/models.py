from django.db import models

# 섬 모델
class Islands(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)  # 섬의 전역 상태로 완료 여부 관리

    def __str__(self):
        return self.name

# 사용자 모델
class Users(models.Model):
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username

# 소목표 모델
class SubGoals(models.Model):
    island = models.ForeignKey(Islands, on_delete=models.CASCADE, related_name="subgoals")
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)  # 소목표의 전역 상태로 완료 여부 관리

    def __str__(self):
        return self.name

# 인증 글 모델s
class Articles(models.Model):
    subgoal = models.ForeignKey(SubGoals, on_delete=models.CASCADE, related_name="articles")
    writer = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="articles", default=0)
    article = models.TextField()
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    uploaddate = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Article by {self.writer.username} on {self.uploaddate}"
