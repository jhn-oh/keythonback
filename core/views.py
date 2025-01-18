from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Users, Islands, SubGoals, Articles
from .serializers import UsersSerializer, IslandSerializer, SubGoalSerializer, ArticleSerializer

# 사용자 API
class UserListView(APIView):
    """
    API to list all users and create a new user.
    """
    def get(self, request):
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 섬 API
class IslandListView(APIView):
    """
    API to list all islands.
    """
    def get(self, request):
        islands = Islands.objects.all()
        serializer = IslandSerializer(islands, many=True)
        return Response(serializer.data)


class IslandDetailView(APIView):
    """
    API to retrieve and update a specific island.
    """
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


# 소목표 API
class SubGoalListView(APIView):
    """
    API to list all subgoals for a specific island.
    """
    def get(self, request, island_id):
        try:
            subgoals = SubGoals.objects.filter(island_id=island_id)
        except Islands.DoesNotExist:
            return Response({"error": "Island not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubGoalSerializer(subgoals, many=True)
        return Response(serializer.data)


class SubGoalStatusUpdateView(APIView):
    """
    API to update the completion status of a specific subgoal.
    """
    def put(self, request, pk):
        try:
            subgoal = SubGoals.objects.get(pk=pk)
        except SubGoals.DoesNotExist:
            return Response({"error": "SubGoal not found"}, status=status.HTTP_404_NOT_FOUND)
        subgoal.is_completed = request.data.get("is_completed", subgoal.is_completed)
        subgoal.save()
        return Response({"message": "SubGoal status updated successfully"})


# 인증 글 API
class ArticleListView(APIView):
    """
    API to list all articles for a specific subgoal.
    """
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
