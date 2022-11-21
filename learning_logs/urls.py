from django.urls import path
from . import views

app_name='learning_logs'
urlpatterns = [
    # HP
    path('',views.index, name='index'),
    # 全てぼトピックを表示
    path('topics/',views.topics, name='topics'),
    # 個別トピックの詳細
    path('topics/<int:topic_id>',views.topic, name='topic'),
    # 新規トピックの追加ページ
    path('new_topic/',views.new_topic, name='new_topic'),
    # 新規記事の追加ページ
    path('new_entry/<int:topic_id>/',views.new_entry, name='new_entry'),
    # 記事の編集ページ
    path('edit_entry/<int:entry_id>/',views.edit_entry, name='edit_entry'),
    
    path('test/',views.test, name='test'),
    
    path('weather/',views.weather, name='weather'),
    
    path('delete_city/<city_id>/',views.delete_city, name='delete_city'),
]