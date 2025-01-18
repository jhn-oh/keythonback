from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Users, Islands, SubGoals, Articles
from .serializers import UsersSerializer, IslandSerializer, SubGoalSerializer, ArticleSerializer
from django.conf import settings
from django.http import FileResponse, Http404
import os

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


class UserDreamUpdateView(APIView):
    """
    API to update or set the dream for a user.
    """
    def post(self, request):
        username = request.data.get("username")
        dream = request.data.get("dream")

        if not username or not dream:
            return Response({"error": "Username and dream are required"}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자 생성 또는 업데이트
        user, created = Users.objects.get_or_create(username=username)
        user.dream = dream
        user.save()

        return Response(
            {
                "message": "Dream updated successfully",
                "username": user.username,
                "dream": user.dream,
            },
            status=status.HTTP_200_OK,
        )

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


class ArticleImageView(APIView):
    """
    API to retrieve the URL of an uploaded article image.
    """
    def get(self, request, filename):
        image_url = f"{settings.MEDIA_URL}{filename}"
        return Response({"image_url": request.build_absolute_uri(image_url)})
    
class ServeArticleImageView(APIView):
    """
    Serve images stored in the 'articles/' directory.
    """
    def get(self, request, filename):
        file_path = os.path.join(settings.MEDIA_ROOT, 'articles', filename)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), content_type='image/png')
        raise Http404("Image not found")
    


# HTML RENDERING
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def welcome_view(request):
    return render(request, 'welcome.html')


@method_decorator(csrf_exempt, name='dispatch')
class SaveDreamView(APIView):
    """
    View to save the dream submitted via form.
    """
    def post(self, request):
        dream = request.POST.get("dream", "").strip()
        username = "akaraka"  # 고정된 username

        if not dream:
            return HttpResponse("꿈을 입력해주세요.", status=400)

        try:
            user, created = Users.objects.get_or_create(username=username)
            user.dream = dream
            user.save()
            return redirect("/selectislands/")  # 성공 페이지로 리다이렉트
        except Exception as e:
            return HttpResponse(f"저장 중 오류 발생: {str(e)}", status=500)