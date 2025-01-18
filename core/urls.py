from django.urls import path
from .views import *
# #IslandListView, IslandDetailView, SubGoalListView, ArticleListView, ServeArticleImageView, UserDreamUpdateView

from . import views

urlpatterns = [
    # Islands
    path('islands/', IslandListView.as_view(), name='island-list'),
    path('islands/<int:pk>/', IslandDetailView.as_view(), name='island-detail'),

    # SubGoals
    path('islands/<int:island_id>/subgoals/', SubGoalListView.as_view(), name='subgoal-list'),
    #path('subgoals/<int:pk>/', SubGoalDetailView.as_view(), name='subgoal-detail'),

    # Articles
    path('', views.welcome_view, name='welcome'),
    path('subgoals/<int:subgoal_id>/articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/<str:filename>/', ServeArticleImageView.as_view(), name='serve_article_image'),
    path('welcome', views.welcome_view, name='welcome'),
    path("api/update_dream/", UserDreamUpdateView.as_view(), name="update_dream"),
    path('save_dream/', SaveDreamView.as_view(), name='save_dream'),
    path('selectislands/', views.select_islands_view, name='select_islands'),
    path('<str:island_name>/select_episodes/', views.select_episodes_view, name='select_episodes'),
    path('update_selected_islands/', views.update_selected_islands, name='update_selected_islands'),
    path('home/', views.home, name='home'),  # 홈 화면 URL 추가
    # path('<str:island_name>/select_episodes/', views.select_episodes_view, name='select_episodes'), <a href="/{{ island}}/{{ episode}}/articles" class="card"> 형식으로...

]
