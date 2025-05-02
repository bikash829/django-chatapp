import pprint
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from a_rtchat.forms import ChatMessageCreateForm
from a_rtchat.models import ChatGroup

# Create your views here.
def chat_view(request, chatroom_name='public_chat'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)  # Assuming you have a ChatGroup model
    chat_messages = chat_group.chat_messages.all()[:30]  #
    # if request.method == 'POST':
    other_user = None 
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break
    
    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user,
            }
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)
            # return redirect('home')
    else:
        form = ChatMessageCreateForm()
        
    context = {
        'chat_messages': chat_messages, 
        'form':form,
        'other_user':other_user,
        'chatroom_name': chatroom_name,
        
    }
    return render(request,'a_rtchat/chat.html', context)


@login_required
def get_or_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')
    
    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)
    
    
    if my_chatrooms.exists():
        for ichatroom in my_chatrooms:
            if other_user in ichatroom.members.all():
                chatroom = ichatroom
                break
            else:
                chatroom = ChatGroup.objects.create(is_private=True)
                chatroom.members.add(other_user, request.user)
    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)
        
    return redirect('chatroom', chatroom.group_name)
                