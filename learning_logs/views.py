from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Topic, Entry, City
from .forms import TopicForm,EntryForm,CityForm
from django.http import Http404
import requests, json
url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ja&appid=74a6d08853913d2d377ebaf10a9a9056'
def index(request):
    # 学習ノートのホームページ
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    city_weather = []
    # 全てのトピックを表示
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    cities = City.objects.filter(my_city=request.user).order_by('date_added')
    if not cities:
        context = {'topics':topics}
        return render(request, 'learning_logs/topics.html',context)
    else:
        city = cities[0]
        city_weather = requests.get(url.format(city.name)).json()
        if city_weather['cod'] == '404':
            context = {'topics':topics}
            return render(request, 'learning_logs/topics.html',context)
        else:
            weather = {
                'city' : city_weather['name'],
                'temperature' : city_weather['main']['temp'],
                'description' : city_weather['weather'][0]['description'],
                'icon' : city_weather['weather'][0]['icon']
            }
            context = {'topics':topics,'weather':weather,}
            return render(request, 'learning_logs/topics.html',context)

@login_required
def topic(request, topic_id):
    # 全てのトピックを表示
    topic = Topic.objects.get(id=topic_id)
    # トピックが現在のユーザーが所持するものであることを確認する
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries,}
    return render(request, 'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    # 新規トピックを追加
    if request.method != 'POST':
        # データは送信していないので空のフォーム
        form = TopicForm()
    else:
        # POSTでデータが送信されたのでこれを処理
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    # 空または無効のフォームを表示
    context = {'form':form}
    return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request, topic_id):
    # 特定のトピックに新規記事を追加
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # データは送信していないので空のフォーム
        form = EntryForm()
    else:
        # POSTでデータが送信されたのでこれを処理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic',topic_id=topic_id)
    # 空または無効のフォームを表示
    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request, entry_id):
    # 既存の記事を修正する
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    if topic.owner != request.user:
        raise Http404    
    if request.method != 'POST':
        # 初回リクエスト時は現在の記事の内容がフォームに埋め込まれている
        form = EntryForm(instance=entry)
    else:
        # POSTでデータが送信されたのでこれを処理する
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'entry':entry, 'topic':topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def test(request):
    return render(request, 'learning_logs/test.html')

@login_required
def delete_city(request, city_id):
    city = City.objects.get(pk=city_id)
    city.delete()
    return redirect('learning_logs:weather')

@login_required
def weather(request):
    cities = City.objects.filter(my_city=request.user).order_by('name')
    weather_data = []
    weather = {}
    if request.method != 'POST': 
        form = CityForm()
    else:
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.save(commit=False)
            new_city.my_city = request.user
            new_city.save()
            return redirect('learning_logs:weather')
        
    form = CityForm()
    
    for city in cities:
        city_weather = requests.get(url.format(city.name)).json() 
        weather = {
            'city' : city,
            'city_name' : city_weather['name'],
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon'],
        }
        weather_data.append(weather)
    context = {'weather':weather,'weather_data':weather_data,'form':form}
    return render(request, 'learning_logs/weather.html', context)
