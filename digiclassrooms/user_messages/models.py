from django.db import models
from django.contrib.auth.models import User
from classrooms.models import Classroom
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager


class Conversation(models.Model):
    """
    Represents a private conversation between a student and a teacher.
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_student')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_as_teacher')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='conversations')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    if TYPE_CHECKING:
        id: int
        messages: 'RelatedManager[Message]'
    
    class Meta:
        ordering = ['-updated_at']
        unique_together = ('student', 'teacher', 'classroom')
    
    def __str__(self):
        return f"Conversation: {self.student.username} & {self.teacher.username} ({self.classroom.name})"
    
    @property
    def latest_message(self):
        """Get the most recent message in this conversation."""
        return self.messages.last()
    
    @property
    def unread_count(self):
        """Get the count of unread messages."""
        return self.messages.filter(is_read=False).count()


class Message(models.Model):
    """
    Represents a single message in a conversation.
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at}"
    
    def mark_as_read(self):
        """Mark this message as read."""
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
