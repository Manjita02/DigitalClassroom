from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from classrooms.models import Classroom
from users.models import Profile
from .models import Conversation, Message


@login_required
def conversation_list(request):
    """
    List all conversations for the logged-in user (student or teacher).
    """
    profile = get_object_or_404(Profile, user=request.user)
    
    if profile.is_teacher:
        # Teachers see conversations where they are the teacher
        conversations = Conversation.objects.filter(teacher=request.user).select_related('student', 'teacher', 'classroom')
    else:
        # Students see conversations where they are the student
        conversations = Conversation.objects.filter(student=request.user).select_related('student', 'teacher', 'classroom')
    
    context = {
        'conversations': conversations,
        'is_teacher': profile.is_teacher,
    }
    return render(request, 'messages/conversation_list.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """
    Display a specific conversation and handle sending messages.
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check if the user is part of this conversation
    if request.user not in [conversation.student, conversation.teacher]:
        return redirect('conversation_list')
    
    # Check if messaging is enabled for this classroom
    messaging_enabled = conversation.classroom.messaging_enabled
    
    # Mark unread messages as read for the current user
    unread_messages = conversation.messages.filter(is_read=False).exclude(sender=request.user)
    for msg in unread_messages:
        msg.mark_as_read()
    
    messages = conversation.messages.all()
    
    context = {
        'conversation': conversation,
        'messages': messages,
        'is_teacher': profile.is_teacher,
        'messaging_enabled': messaging_enabled,
    }
    return render(request, 'messages/conversation_detail.html', context)


@login_required
def send_message(request, conversation_id):
    """
    Send a message in a conversation.
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Check if messaging is enabled for this classroom
    if not conversation.classroom.messaging_enabled:
        from django.contrib import messages
        messages.error(request, 'Messaging is disabled for this classroom.')
        return redirect('conversation_detail', conversation_id=conversation_id)
    
    # Check if the user is part of this conversation
    if request.user not in [conversation.student, conversation.teacher]:
        from django.contrib import messages
        messages.error(request, 'Unauthorized.')
        return redirect('conversation_list')
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if not content:
            from django.contrib import messages
            messages.error(request, 'Message cannot be empty.')
            return redirect('conversation_detail', conversation_id=conversation_id)
        
        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        
        # Update conversation's updated_at timestamp
        conversation.updated_at = timezone.now()
        conversation.save(update_fields=['updated_at'])
        
        return redirect('conversation_detail', conversation_id=conversation_id)
    
    return redirect('conversation_detail', conversation_id=conversation_id)


@login_required
def start_conversation(request, classroom_id, recipient_id):
    """
    Start or get an existing conversation with a specific person.
    """
    classroom = get_object_or_404(Classroom, id=classroom_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Check if messaging is enabled for this classroom
    if not classroom.messaging_enabled:
        from django.contrib import messages
        messages.error(request, 'Messaging is disabled for this classroom.')
        return redirect('classroom_detail', pk=classroom_id)
    
    recipient = get_object_or_404(User, id=recipient_id)
    recipient_profile = get_object_or_404(Profile, user=recipient)
    
    # Verify the recipient is in the classroom
    if recipient not in classroom.students.all() and recipient not in classroom.teachers.all():
        return redirect('conversation_list')
    
    # Verify the user is also in the classroom
    if request.user not in classroom.students.all() and request.user not in classroom.teachers.all():
        return redirect('conversation_list')
    
    # Students can only message teachers, teachers can message students
    if profile.is_teacher and not recipient_profile.is_teacher:
        student = recipient
        teacher = request.user
    elif not profile.is_teacher and recipient_profile.is_teacher:
        student = request.user
        teacher = recipient
    else:
        return redirect('conversation_list')
    
    # Get or create conversation
    conversation, created = Conversation.objects.get_or_create(
        student=student,
        teacher=teacher,
        classroom=classroom
    )
    
    return redirect('conversation_detail', conversation_id=conversation.id)


@login_required
def classroom_users(request, classroom_id):
    """
    Get the list of users in a classroom that the logged-in user can message.
    Returns JSON for AJAX requests.
    """
    classroom = get_object_or_404(Classroom, id=classroom_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Verify user is in the classroom
    if request.user not in classroom.students.all() and request.user not in classroom.teachers.all():
        return JsonResponse({'error': 'Not in classroom'}, status=403)
    
    users = []
    
    if profile.is_teacher:
        # Teachers can message students
        for student in classroom.students.all():
            if student != request.user:
                users.append({
                    'id': student.id,
                    'username': student.username,
                    'full_name': student.get_full_name() or student.username,
                })
    else:
        # Students can message the teacher
        teacher = classroom.teacher
        users.append({
            'id': teacher.id,
            'username': teacher.username,
            'full_name': teacher.get_full_name() or teacher.username,
        })
    
    return JsonResponse({'users': users})
