# chatbot/views.py
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Conversation, Message
from .forms import MessageForm, ConversationForm
from .ollama_client import generate_with_llm  # this should now call DeepSeek (or your chosen API)


# ✅ Conversation List Page (Home)
@login_required
def conversations(request):
    convos = Conversation.objects.filter(user=request.user).order_by('-created_at')

    if request.method == "POST":
        form = ConversationForm(request.POST)
        if form.is_valid():
            convo = form.save(commit=False)
            convo.user = request.user
            convo.save()
            return redirect('conversation_detail', pk=convo.pk)
    else:
        form = ConversationForm()

    return render(request, "chatbot/conversations.html", {
        "conversations": convos,
        "form": form
    })


# ✅ View a Single Conversation
@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, user=request.user)
    messages = Message.objects.filter(conversation=conversation).order_by("created_at")
    form = MessageForm()
    return render(request, "chatbot/conversation_detail.html", {
        "conversation": conversation,
        "messages": messages,
        "form": form
    })


# ✅ Send Message + Get AI Reply (uses generate_with_llm)
@login_required
def add_message(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk, user=request.user)

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            # Save user message
            user_message = form.save(commit=False)
            user_message.conversation = conversation
            user_message.role = "user"
            user_message.save()

            # Call the LLM through your helper (DeepSeek / other)
            try:
                prompt = user_message.text.strip()
                if not prompt:
                    assistant_reply = "[No input provided]"
                else:
                    # generate_with_llm should return a string (or an error string)
                    assistant_reply = generate_with_llm(prompt)
                    if assistant_reply is None:
                        assistant_reply = "[LLM returned empty response]"

            except Exception as e:
                assistant_reply = f"[Error contacting AI server: {e}]"

            # Save assistant reply
            Message.objects.create(
                conversation=conversation,
                role="assistant",
                text=assistant_reply
            )

    return redirect('conversation_detail', pk=pk)
