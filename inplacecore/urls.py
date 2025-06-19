from django.contrib import admin
from django.urls import path
from chatbot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('whatsapp-meta-webhook/', views.meta_webhook, name='meta_webhook'),
    
    
    # 🚨 Escalation Views
    path('get-escalated/', views.get_escalated, name='get_escalated'),
    path('get-chat-history/', views.get_chat_history, name='get_chat_history'),
    path('send-admin-reply/', views.send_admin_reply, name='send_admin_reply'),
    path('resume-bot/', views.resume_bot, name='resume_bot'),
]
