from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('conversation/<int:conversation_id>/send/', views.send_message, name='send_message'),
    path('start/<int:classroom_id>/<int:recipient_id>/', views.start_conversation, name='start_conversation'),
    path('classroom/<int:classroom_id>/users/', views.classroom_users, name='classroom_users'),
]
