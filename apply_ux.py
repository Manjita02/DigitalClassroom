import re
import os

# 1. Update base.html to use Toasts
base_html_path = 'digiclassrooms/users/templates/users/base.html'
with open(base_html_path, 'r', encoding='utf-8') as f:
    base_html = f.read()

alert_pattern = re.compile(r'\{\% if messages \%\}.*?\{\% endif \%\}', re.DOTALL)
toast_html = '''{% if messages %}
    <div class="toast-container position-fixed bottom-0 end-0 p-4" style="z-index: 1060">
        {% for message in messages %}
            <div class="toast align-items-center text-bg-{{ message.tags|default:'primary' }} border-0 mb-3 shadow-lg" role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="5000">
                <div class="d-flex">
                    <div class="toast-body fw-medium px-3 py-3">
                        {% if message.tags == 'success' %}
                            <i class="fas fa-check-circle me-2 fs-5 align-middle"></i>
                        {% elif message.tags == 'error' or message.tags == 'danger' %}
                            <i class="fas fa-exclamation-circle me-2 fs-5 align-middle"></i>
                        {% elif message.tags == 'warning' %}
                            <i class="fas fa-exclamation-triangle me-2 fs-5 align-middle"></i>
                        {% else %}
                            <i class="fas fa-info-circle me-2 fs-5 align-middle"></i>
                        {% endif %}
                        <span class="align-middle">{{ message }}</span>
                    </div>
                    <button type="button" class="btn-close btn-close-white me-3 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
        {% endfor %}
    </div>
{% endif %}'''

new_base = alert_pattern.sub(toast_html, base_html)
with open(base_html_path, 'w', encoding='utf-8') as f:
    f.write(new_base)

# 2. Update main.css to support text-bg-error
with open('digiclassrooms/users/static/css/main.css', 'a', encoding='utf-8') as f:
    f.write('\n/* Toast overrides */\n.text-bg-error { background-color: var(--danger-color) !important; color: white !important; }\n')

# 3. Update main.js to initialize toasts
with open('digiclassrooms/users/static/js/main.js', 'a', encoding='utf-8') as f:
    f.write('''
    // Initialize Toasts
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl);
    });
    toastList.forEach(function(toast) { toast.show(); });
''')

# 4. Polish empty states in templates
empty_state_templates = [
    'digiclassrooms/classrooms/templates/classrooms/teacher_home.html',
    'digiclassrooms/classrooms/templates/classrooms/student_home.html',
    'digiclassrooms/lectures/templates/lectures/lecture_list.html',
    'digiclassrooms/assignments/templates/assignments/assignment_list.html'
]

empty_block_pattern = re.compile(r'\{\% empty \%\}\s*<div class="col-12">\s*<div class="card text-center py-5">\s*<div class="card-body">.*?</div>\s*</div>\s*</div>', re.DOTALL)

def polish_empty_state(match):
    content = match.group(0)
    # Upgrade standard Bootstrap empty state to premium empty state
    # Adding subtle background, softer text, and better padding
    new_content = content.replace('card text-center py-5', 'card text-center py-5 bg-light border-0 shadow-sm')
    new_content = new_content.replace('fa-4x text-muted', 'fa-4x text-secondary opacity-50')
    new_content = new_content.replace('h4 class="text-muted"', 'h4 class="fw-semibold text-secondary mt-3"')
    return new_content

for template_path in empty_state_templates:
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            t_content = f.read()
        
        updated_content = empty_block_pattern.sub(polish_empty_state, t_content)
        
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

print("UX Improvements applied successfully.")
