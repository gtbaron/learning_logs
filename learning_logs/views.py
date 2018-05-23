from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    return render(request, 'learning_logs/index.html')


def topics(request):
    saved_topics = Topic.objects.order_by('date_added')
    context = {'topics': saved_topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    req_topic = Topic.objects.get(id=topic_id)
    entries = req_topic.entry_set.order_by('-date_added')
    context = {'topic': req_topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    form = TopicForm()
    if request.method == 'POST':
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    form = EntryForm()
    if request.method == 'POST':
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    form = EntryForm(instance=entry)
    if request.method == 'POST':
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
