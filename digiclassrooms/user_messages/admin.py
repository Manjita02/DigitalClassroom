from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'teacher', 'classroom', 'created_at', 'updated_at')
    list_filter = ('classroom', 'created_at', 'updated_at')
    search_fields = ('student__username', 'teacher__username', 'classroom__name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Participants', {
            'fields': ('student', 'teacher', 'classroom')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'get_conversation', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at', 'conversation__classroom')
    search_fields = ('sender__username', 'content', 'conversation__student__username', 'conversation__teacher__username')
    readonly_fields = ('created_at', 'updated_at', 'read_at')
    fieldsets = (
        ('Message Details', {
            'fields': ('conversation', 'sender', 'content')
        }),
        ('Read Status', {
            'fields': ('is_read', 'read_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_conversation(self, obj):
        return f"{obj.conversation.student.username} & {obj.conversation.teacher.username}"
    get_conversation.short_description = 'Conversation'
