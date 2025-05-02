import pprint
from django.shortcuts import get_object_or_404, redirect, render

from a_rtchat.forms import ChatMessageCreateForm
from a_rtchat.models import ChatGroup

# Create your views here.
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name='public_chat')  # Assuming you have a ChatGroup model
    chat_messages = chat_group.chat_messages.all()[:30]  #
    # if request.method == 'POST':
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
    return render(request,'a_rtchat/chat.html', {'chat_messages': chat_messages, 'form':form})