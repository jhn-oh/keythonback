from django.db import models

# 섬 모델
class Islands(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# 사용자 모델
class Users(models.Model):
    username = models.CharField(max_length=100)
    # password = models.CharField(max_length=100)
    final_goal = models.CharField(max_length=100)
    selected_islands = models.ManyToManyField(
        Islands, through='UserIsland', related_name="users"
    )

    def __str__(self):
        return self.username

# 사용자별 섬 상태 모델
class UserIsland(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_islands")
    island = models.ForeignKey(Islands, on_delete=models.CASCADE, related_name="user_status")
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)  # 완료 날짜

    def __str__(self):
        return f"{self.user.username} - {self.island.name}"

# 소목표 모델
class SubGoals(models.Model):
    island = models.ForeignKey(Islands, on_delete=models.CASCADE, related_name="subgoals")
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

# 사용자별 소목표 상태 모델
class UserSubGoal(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_subgoals")
    subgoal = models.ForeignKey(SubGoals, on_delete=models.CASCADE, related_name="user_status")
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)  # 완료 날짜

    def __str__(self):
        return f"{self.user.username} - {self.subgoal.name}"

# 인증 글 모델
class Articles(models.Model):
    subgoal = models.ForeignKey(SubGoals, on_delete=models.CASCADE, related_name="articles")
    writer = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="articles")
    #title = models.CharField(max_length=255, null=True, blank=True)  # 제목 추가
    article = models.TextField()
    image = models.ImageField(upload_to='articles/')
    uploaddate = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Article by {self.writer.username} on {self.uploaddate}"
