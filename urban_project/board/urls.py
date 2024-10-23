from django.urls import path  # Импорт функции, которая используется для определения шаблонов URL
from . import views  # Импорт модуля из текущего пакета для ссылки на функции представлений

app_name = 'board'  # Задаем пространство имен для приложения (URL-имена будут уникальными для разных приложений).

urlpatterns = [
    # Список шаблонов URL, которые сопоставляют URL с представлениями.
    path('', views.advertisement_list, name='advertisement_list'),
    path('advertisement/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),
    path('add/', views.add_advertisement, name='add_advertisement'),
    path('advertisement/<int:pk>/edit/', views.edit_advertisement, name='edit_advertisement'),
]
