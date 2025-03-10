from rest_framework import serializers
from .models import Islands, SubGoals, Articles, Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username']

class IslandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Islands
        fields = '__all__'

class SubGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubGoals
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = '__all__'
