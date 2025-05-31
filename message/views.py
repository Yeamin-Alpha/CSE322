from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.db.models import Q

@login_required
def chat_interface(request, username=None):
  
    chat_users = User.objects.filter(
        Q(sent_messages__receiver=request.user) | Q(received_messages__sender=request.user)
    ).distinct()

    selected_user = None
    messages = []

    if username:
        selected_user = get_object_or_404(User, username=username)
        messages = Message.objects.filter(
            Q(sender=request.user, receiver=selected_user) |
            Q(sender=selected_user, receiver=request.user)
        ).order_by('sent_time')


        Message.objects.filter(receiver=request.user, sender=selected_user, is_read=False).update(is_read=True)


    if request.method == 'POST' and selected_user:
        message_text = request.POST.get('message')
        if message_text:
            Message.objects.create(sender=request.user, receiver=selected_user, message=message_text)
            return redirect('chat_interface', username=username)

    context = {
        'chat_users': chat_users,
        'selected_user': selected_user,
        'messages': messages,
    }
    return render(request, 'chat_interface.html', context)
@login_required
def mark_as_read(request, message_id):

    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    message.is_read = True
    message.save()
    return redirect('message_list')

@login_required
def message_list(request):

    received_messages = Message.objects.filter(receiver=request.user).order_by('-sent_time')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-sent_time')
    return render(request, 'message_list.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
    })
@login_required
def search_users(request):

    query = request.GET.get('query', '').strip()
    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id) if query else []
    return render(request, 'user_search.html', {'users': users, 'query': query})

