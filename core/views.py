from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Islands, SubGoals, Articles
from .serializers import IslandSerializer, SubGoalSerializer, ArticleSerializer

# 1. 섬 관련 API
class IslandListView(APIView):
    def get(self, request):
        islands = Islands.objects.all()
        serializer = IslandSerializer(islands, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IslandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IslandDetailView(APIView):
    def get(self, request, pk):
        try:
            island = Islands.objects.get(pk=pk)
        except Islands.DoesNotExist:
            return Response({"error": "Island not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = IslandSerializer(island)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            island = Islands.objects.get(pk=pk)
        except Islands.DoesNotExist:
            return Response({"error": "Island not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = IslandSerializer(island, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            island = Islands.objects.get(pk=pk)
        except Islands.DoesNotExist:
            return Response({"error": "Island not found"}, status=status.HTTP_404_NOT_FOUND)
        island.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 2. 소목표 관련 API
class SubGoalListView(APIView):
    def get(self, request, island_id):
        try:
            subgoals = SubGoals.objects.filter(island_id=island_id)
        except Islands.DoesNotExist:
            return Response({"error": "Island not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubGoalSerializer(subgoals, many=True)
        return Response(serializer.data)


class SubGoalDetailView(APIView):
    def get(self, request, pk):
        try:
            subgoal = SubGoals.objects.get(pk=pk)
        except SubGoals.DoesNotExist:
            return Response({"error": "SubGoal not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubGoalSerializer(subgoal)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            subgoal = SubGoals.objects.get(pk=pk)
        except SubGoals.DoesNotExist:
            return Response({"error": "SubGoal not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubGoalSerializer(subgoal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 3. 인증 글 관련 API
class ArticleListView(APIView):
    def get(self, request, subgoal_id):
        try:
            articles = Articles.objects.filter(subgoal_id=subgoal_id)
        except SubGoals.DoesNotExist:
            return Response({"error": "SubGoal not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
