import re
import os

teacher_html_path = 'digiclassrooms/classrooms/templates/classrooms/teacher_home.html'
student_html_path = 'digiclassrooms/classrooms/templates/classrooms/student_home.html'

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# ----------------- TEACHER HOME -----------------
teacher_html = read_file(teacher_html_path)

# Insert stat cards after the header
header_end_pattern = re.compile(r'</div>\s*</div>\s*(<div class="row">)', re.DOTALL)
stat_cards_teacher = '''</div>
</div>

<!-- Stat Cards -->
<div class="row mb-4">
    <div class="col-md-4 mb-3 mb-md-0">
        <div class="card h-100 border-0 bg-primary text-white shadow-sm" style="background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);">
            <div class="card-body d-flex align-items-center">
                <div class="display-6 me-3"><i class="fas fa-chalkboard-teacher opacity-50"></i></div>
                <div>
                    <h6 class="text-uppercase fw-semibold mb-1 opacity-75" style="letter-spacing: 0.5px; font-size: 0.8rem;">Active Classes</h6>
                    <h2 class="mb-0 fw-bold">{{ classrooms|length }}</h2>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-4 mb-3 mb-md-0">
        <div class="card h-100 border-0 bg-warning text-dark shadow-sm">
            <div class="card-body d-flex align-items-center">
                <div class="display-6 me-3"><i class="fas fa-hourglass-half opacity-50"></i></div>
                <div>
                    <h6 class="text-uppercase fw-semibold mb-1 opacity-75" style="letter-spacing: 0.5px; font-size: 0.8rem;">Pending Requests</h6>
                    <h2 class="mb-0 fw-bold" id="statPendingReqs">{{ pending_join_requests|length }}</h2>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card h-100 border-0 text-white shadow-sm" style="background: linear-gradient(135deg, var(--secondary-color) 0%, var(--secondary-dark) 100%);">
            <div class="card-body d-flex align-items-center">
                <div class="display-6 me-3"><i class="fas fa-plus-circle opacity-50"></i></div>
                <div>
                    <h6 class="text-uppercase fw-semibold mb-1 opacity-75" style="letter-spacing: 0.5px; font-size: 0.8rem;">Available to Teach</h6>
                    <h2 class="mb-0 fw-bold" id="statAvailClasses">{{ available_classrooms|length }}</h2>
                </div>
            </div>
        </div>
    </div>
</div>

\\1'''
teacher_html = header_end_pattern.sub(stat_cards_teacher, teacher_html, count=1)

# Polish teacher course cards
course_card_pattern = re.compile(r'<div class="col-md-6 mb-4">\s*<div class="card h-100">\s*<div class="card-body d-flex flex-column">\s*<h5 class="fw-bold mb-1"><i class="fas fa-school text-primary me-2"></i>\{\{ classroom\.name \}\}</h5>\s*<p class="text-muted mb-2">\{\{ classroom\.description\|default:\'No description yet\.\'\|truncatewords:18 \}\}</p>\s*<p class="mb-3"><span class="badge bg-info">\{\{ classroom\.students\.count \}\} students</span></p>\s*<div class="mt-auto d-grid gap-2">\s*<a href="\{\% url \'classroom_detail\' classroom\.pk \%\}" class="btn btn-primary">\s*<i class="fas fa-door-open me-2"></i>Open Classroom\s*</a>\s*</div>\s*</div>\s*</div>\s*</div>', re.DOTALL)

polished_course_card = '''<div class="col-md-4 mb-4">
            <div class="card h-100 border-0 shadow-sm overflow-hidden course-card">
                <div class="card-header border-0 py-3" style="background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);">
                    <h5 class="fw-bold mb-0 text-white text-truncate"><i class="fas fa-school me-2 opacity-50"></i>{{ classroom.name }}</h5>
                </div>
                <div class="card-body d-flex flex-column">
                    <p class="text-muted mb-3 flex-grow-1">{{ classroom.description|default:'No description yet.'|truncatewords:15 }}</p>
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <span class="badge bg-light text-dark border"><i class="fas fa-users me-1 text-primary"></i>{{ classroom.students.count }} students</span>
                    </div>
                    <div class="mt-auto">
                        <a href="{% url 'classroom_detail' classroom.pk %}" class="btn btn-primary w-100">
                            <i class="fas fa-door-open me-2"></i>Open Classroom
                        </a>
                    </div>
                </div>
            </div>
        </div>'''
teacher_html = course_card_pattern.sub(polished_course_card, teacher_html)

# Ensure javascript polling updates the new stat badges too
js_update_pattern = re.compile(r'const nextAvail = Number\(data\.available_classrooms \|\| 0\);')
teacher_html = js_update_pattern.sub(r'const nextAvail = Number(data.available_classrooms || 0);\n            const statPendingReqs = document.getElementById("statPendingReqs");\n            const statAvailClasses = document.getElementById("statAvailClasses");\n            if(statPendingReqs) statPendingReqs.textContent = nextPending;\n            if(statAvailClasses) statAvailClasses.textContent = nextAvail;', teacher_html)

write_file(teacher_html_path, teacher_html)


# ----------------- STUDENT HOME -----------------
student_html = read_file(student_html_path)

header_end_student_pattern = re.compile(r'</div>\s*</div>\s*\{\% if urgent_deadlines \%\}', re.DOTALL)
stat_cards_student = '''</div>
</div>

<!-- Stat Cards -->
<div class="row mb-4">
    <div class="col-md-6 mb-3 mb-md-0">
        <div class="card h-100 border-0 text-white shadow-sm" style="background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);">
            <div class="card-body d-flex align-items-center">
                <div class="display-6 me-3"><i class="fas fa-book-reader opacity-50"></i></div>
                <div>
                    <h6 class="text-uppercase fw-semibold mb-1 opacity-75" style="letter-spacing: 0.5px; font-size: 0.8rem;">Enrolled Classes</h6>
                    <h2 class="mb-0 fw-bold">{{ enrolled_classrooms|length }}</h2>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card h-100 border-0 text-white shadow-sm" style="background: linear-gradient(135deg, var(--info-color) 0%, var(--info-dark) 100%);">
            <div class="card-body d-flex align-items-center">
                <div class="display-6 me-3"><i class="fas fa-calendar-alt opacity-50"></i></div>
                <div>
                    <h6 class="text-uppercase fw-semibold mb-1 opacity-75" style="letter-spacing: 0.5px; font-size: 0.8rem;">Upcoming Deadlines</h6>
                    <h2 class="mb-0 fw-bold">{{ upcoming_deadlines|length }}</h2>
                </div>
            </div>
        </div>
    </div>
</div>

{% if urgent_deadlines %}'''
student_html = header_end_student_pattern.sub(stat_cards_student, student_html, count=1)

student_course_card_pattern = re.compile(r'<div class="col-md-4 mb-4">\s*<div class="card h-100">\s*<div class="card-body d-flex flex-column">\s*<div class="mb-3">\s*<h5 class="card-title fw-bold mb-2">\s*<i class="fas fa-chalkboard text-primary me-2"></i>\{\{ classroom\.name \}\}\s*</h5>\s*<h6 class="card-subtitle text-muted">\s*<i class="fas fa-user-tie me-1"></i>\{\{ classroom\.teacher\.username \}\}\s*</h6>\s*</div>\s*<p class="card-text flex-grow-1 text-muted">\{\{ classroom\.description\|truncatewords:20 \}\}</p>\s*<div class="d-grid gap-2 mt-auto">\s*<a href="\{\% url \'classroom_detail\' classroom\.pk \%\}" class="btn btn-primary w-100">\s*<i class="fas fa-door-open me-2"></i>Enter Classroom\s*</a>\s*<form method="post" action="\{\% url \'leave_classroom\' classroom\.pk \%\}" onsubmit="return confirm\(\'Request to leave this classroom\?\'\);">\s*\{\% csrf_token \%\}\s*<button type="submit" class="btn btn-outline-danger w-100">\s*<i class="fas fa-sign-out-alt me-2"></i>Request Leave\s*</button>\s*</form>\s*</div>\s*</div>\s*</div>\s*</div>', re.DOTALL)

student_polished_card = '''<div class="col-md-4 mb-4">
            <div class="card h-100 border-0 shadow-sm overflow-hidden course-card">
                <div class="card-header border-0 py-3" style="background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);">
                    <h5 class="fw-bold mb-1 text-white text-truncate"><i class="fas fa-chalkboard me-2 opacity-50"></i>{{ classroom.name }}</h5>
                    <h6 class="mb-0 text-white-50 small"><i class="fas fa-user-tie me-1"></i>{{ classroom.teacher.username }}</h6>
                </div>
                <div class="card-body d-flex flex-column">
                    <p class="text-muted mb-3 flex-grow-1">{{ classroom.description|default:'No description yet.'|truncatewords:15 }}</p>
                    <div class="d-grid gap-2 mt-auto">
                        <a href="{% url 'classroom_detail' classroom.pk %}" class="btn btn-primary w-100">
                            <i class="fas fa-door-open me-2"></i>Enter Classroom
                        </a>
                        <form method="post" action="{% url 'leave_classroom' classroom.pk %}" onsubmit="return confirm('Request to leave this classroom?');">
                            {% csrf_token %}
                            <button type="submit" class="btn btn-light w-100 text-danger fw-semibold border-0">
                                Request Leave
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>'''
student_html = student_course_card_pattern.sub(student_polished_card, student_html)

write_file(student_html_path, student_html)

print("Milestone 5 UX changes applied successfully.")
