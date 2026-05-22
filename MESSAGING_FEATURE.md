# Private Messaging Feature

## Overview

DigiClassroom now includes a **private one-on-one messaging feature** that allows students and teachers to communicate privately within a classroom context. Teachers can enable or disable messaging on a per-classroom basis.

## Features

### For Students
- Send private messages to their teachers in each classroom
- View message history with teachers
- Mark messages as read automatically
- Simple, intuitive interface
- Messages disabled in classrooms where teacher has turned off the feature

### For Teachers
- Receive and send private messages to students in their classrooms
- View conversations with all students they teach
- Track which messages have been read
- Respond to student inquiries directly
- **Enable/Disable messaging for each classroom** to control student communication
- View messaging status in the classroom roster

## Teacher Controls

### Enabling/Disabling Messaging

Teachers can control messaging on a per-classroom basis:

1. Go to the classroom detail page
2. Expand the **"Messaging Settings"** section (in the teacher dashboard section)
3. Toggle the **"Allow students to send private messages"** checkbox
4. Click **"Save Settings"**

When messaging is **disabled**:
- Students cannot send new messages
- Existing messages remain visible (read-only)
- A warning message appears: "Messaging has been disabled for this classroom by the teacher"

When messaging is **enabled** (default):
- Students can send and receive messages
- Full two-way communication is available
- Message input field is visible in the conversation view

## How It Works

### Starting a Conversation

#### Students
1. Go to a classroom detail page
2. Click the **"Message Teacher"** button at the top (only visible if messaging enabled)
3. The conversation will open (or be created if it's the first message)
4. If messaging is enabled: Type your message and click **Send**
5. If messaging is disabled: You'll see a notice that messaging is disabled

#### Teachers
1. Go to a classroom detail page
2. In the class roster, click the **"Message"** button next to a student
3. The conversation will open
4. Type your message and click **Send**

### Accessing Messages

- Click **Messages** in the main navigation menu to view all conversations
- Conversations are sorted by most recent activity
- Each conversation shows:
  - Student/Teacher name
  - Associated classroom
  - Last message preview
  - Unread message count (if any)

### In Conversation View

- View full message history
- Sender and timestamp for each message
- "Double check" icon indicates messages that have been read
- If messaging is **enabled**: Simple text area to compose and send new messages
- If messaging is **disabled**: Read-only view with status notification

## Database Structure

### Classroom Model
- New field: `messaging_enabled` (BooleanField, default=True)
- Controls whether private messaging is allowed for each classroom

### Conversation Model
- Unique conversation between a specific student and teacher in a classroom
- One conversation per student-teacher-classroom combination
- Stores creation and update timestamps

### Message Model
- Individual messages within a conversation
- Tracks sender, content, and read status
- Records read timestamp when message is marked as read

## URLs

- `/messages/` - View all conversations
- `/messages/conversation/<id>/` - View specific conversation
- `/messages/conversation/<id>/send/` - Send a message (POST)
- `/messages/start/<classroom_id>/<recipient_id>/` - Start or get existing conversation
- `/messages/classroom/<classroom_id>/users/` - Get users in a classroom (JSON)
- `/classroom/<classroom_id>/messaging-settings/` - Update messaging settings (POST, teacher only)

## Technical Details

### App Name
The app is named `user_messages` (not `messages` to avoid conflict with Django's built-in messages framework).

### Permissions
- Conversations are created only between students and teachers
- Users can only access conversations they are part of
- Teachers can only message students in their classrooms
- Students can only message their classroom teacher
- **Only teachers can modify messaging settings for their classrooms**

### Features Implemented
- Automatic message read tracking
- Per-classroom messaging enable/disable toggle
- Conversation list with sorting by latest activity
- Unread message badges
- AJAX message sending with page reload
- Profile-aware messaging (distinguishes teachers from students)
- Messaging status displayed in classroom settings and conversation list

## Integration Points

1. **Navigation**: Added "Messages" link in main navbar
2. **Classroom View**: 
   - "Message Teacher" button for students (visible only if messaging enabled)
   - "Message" buttons next to each student for teachers
   - **New: Messaging Settings panel in teacher view** with enable/disable toggle
3. **Admin Interface**: Full admin support for managing conversations and messages
4. **Settings**: Teacher-controlled per-classroom setting

## Default Behavior

- Messaging is **enabled by default** for all existing and new classrooms
- Teachers can disable it at any time
- Disabling does not delete existing messages
- Students cannot enable messaging if disabled by teacher

## Future Enhancements

Potential improvements for future versions:
- Real-time messaging with WebSockets
- Message notifications
- Typing indicators
- File attachments
- Message search
- Bulk messaging to multiple students
- Message templates for teachers
- Read receipts
