from django.urls import path
from . import views

app_name='learning_logs'
urlpatterns = [
    # HP
    path('',views.index, name='index'),

    path('topics/',views.topics, name='topics'),

    path('topics/<int:topic_id>',views.topic, name='topic'),

    path('new_topic/',views.new_topic, name='new_topic'),

    path('new_entry/<int:topic_id>/',views.new_entry, name='new_entry'),

    path('edit_entry/<int:entry_id>/',views.edit_entry, name='edit_entry'),
    
    # path('test/',views.test, name='test'),
    
    path('save_order/', views.save_order, name='save_order'),
    
    # path('load_order/', views.load_order, name='load_order'),
    
    path('weather/',views.weather, name='weather'),
    
    path('delete_city/<city_id>/',views.delete_city, name='delete_city'),
    
    path('weather/<city_id>', views.setPlt, name='setPlt'),
    
    path('recipe/', views.recipe_page, name='recipe_page'),
    
    path('make_recipe/', views.make_recipe, name='make_recipe'),
]