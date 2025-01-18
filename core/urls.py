from django.urls import path
from .views import IslandListView, IslandDetailView, SubGoalListView, SubGoalDetailView, ArticleListView

urlpatterns = [
    # Islands
    path('islands/', IslandListView.as_view(), name='island-list'),
    path('islands/<int:pk>/', IslandDetailView.as_view(), name='island-detail'),

    # SubGoals
    path('islands/<int:island_id>/subgoals/', SubGoalListView.as_view(), name='subgoal-list'),
    path('subgoals/<int:pk>/', SubGoalDetailView.as_view(), name='subgoal-detail'),

    # Articles
    path('subgoals/<int:subgoal_id>/articles/', ArticleListView.as_view(), name='article-list'),
]
