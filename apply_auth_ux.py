import re

# 1. Login Page Polish
login_path = 'digiclassrooms/users/templates/users/login.html'
with open(login_path, 'r', encoding='utf-8') as f:
    login_html = f.read()

# Replace the layout
polished_login = '''{% extends 'users/base.html' %}
{% block title %}Login - DigiClassroom{% endblock %}

{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-6 col-lg-5">
        <div class="card shadow-lg border-0 rounded-4 overflow-hidden">
            <div class="card-header bg-white border-0 text-center pt-5 pb-0">
                <div class="d-inline-flex align-items-center justify-content-center bg-primary bg-opacity-10 rounded-circle mb-3" style="width: 80px; height: 80px;">
                    <i class="fas fa-sign-in-alt fa-2x text-primary"></i>
                </div>
                <h2 class="fw-bold mb-1">Welcome Back</h2>
                <p class="text-muted">Sign in to your account</p>
            </div>
            <div class="card-body p-5 pt-4">
                <form method="post">
                    {% csrf_token %}
                    <div class="form-floating mb-3">
                        {{ form.username }}
                        <label for="{{ form.username.id_for_label }}"><i class="fas fa-user text-muted me-2"></i>Username</label>
                        {% if form.username.errors %}
                            <div class="text-danger small mt-1 fw-medium">{{ form.username.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <div class="form-floating mb-4">
                        {{ form.password }}
                        <label for="{{ form.password.id_for_label }}"><i class="fas fa-lock text-muted me-2"></i>Password</label>
                        {% if form.password.errors %}
                            <div class="text-danger small mt-1 fw-medium">{{ form.password.errors }}</div>
                        {% endif %}
                    </div>
                    
                    {% if form.non_field_errors %}
                        <div class="alert alert-danger rounded-3 py-2 px-3 mb-4">
                            <i class="fas fa-exclamation-circle me-2"></i>{{ form.non_field_errors|striptags }}
                        </div>
                    {% endif %}
                    
                    <button type="submit" class="btn btn-primary btn-lg w-100 mb-3 fw-semibold shadow-sm">
                        Login
                    </button>
                    
                    <div class="text-center mb-4">
                        <a href="{% url 'reset_password' %}" class="text-decoration-none text-muted small hover-primary">
                            <i class="fas fa-key me-1"></i>Forgot Password?
                        </a>
                    </div>
                </form>
            </div>
            <div class="card-footer bg-light border-0 text-center py-4">
                <p class="mb-0 text-muted">Don't have an account? 
                    <a href="{% url 'register' %}" class="fw-bold text-primary text-decoration-none ms-1">Sign Up</a>
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_css %}
<style>
    .form-floating > .form-control {
        border-radius: 0.5rem;
    }
    .hover-primary:hover { color: var(--primary-color) !important; }
</style>
<script>
    // Add form-control class to django generated inputs
    document.addEventListener("DOMContentLoaded", function() {
        document.querySelectorAll('input[type="text"], input[type="password"]').forEach(el => {
            el.classList.add('form-control');
            el.setAttribute('placeholder', ' '); // Required for form-floating
        });
    });
</script>
{% endblock %}'''
with open(login_path, 'w', encoding='utf-8') as f:
    f.write(polished_login)

# 2. Register Page Polish
register_path = 'digiclassrooms/users/templates/users/register.html'
polished_register = '''{% extends 'users/base.html' %}
{% block title %}Register - DigiClassroom{% endblock %}

{% block content %}
<div class="row justify-content-center mt-4 mb-5">
    <div class="col-md-7 col-lg-6">
        <div class="card shadow-lg border-0 rounded-4 overflow-hidden">
            <div class="card-header bg-white border-0 text-center pt-5 pb-0">
                <div class="d-inline-flex align-items-center justify-content-center bg-success bg-opacity-10 rounded-circle mb-3" style="width: 80px; height: 80px;">
                    <i class="fas fa-user-plus fa-2x text-success"></i>
                </div>
                <h2 class="fw-bold mb-1">Create Account</h2>
                <p class="text-muted">Join DigiClassroom today</p>
            </div>
            <div class="card-body p-4 p-md-5 pt-3">
                <form method="post">
                    {% csrf_token %}
                    
                    <div class="row g-3 mb-3">
                        <div class="col-md-12 form-floating">
                            {{ form.username }}
                            <label for="{{ form.username.id_for_label }}"><i class="fas fa-user text-muted me-2 ms-2"></i>Username</label>
                            {% if form.username.errors %}
                                <div class="text-danger small mt-1 fw-medium px-2">{{ form.username.errors }}</div>
                            {% endif %}
                        </div>
                    </div>
                    
                    <div class="form-floating mb-3">
                        {{ form.email }}
                        <label for="{{ form.email.id_for_label }}"><i class="fas fa-envelope text-muted me-2"></i>Email Address</label>
                        {% if form.email.errors %}
                            <div class="text-danger small mt-1 fw-medium">{{ form.email.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <div class="row g-3 mb-4">
                        <div class="col-md-6 form-floating">
                            {{ form.password1 }}
                            <label for="{{ form.password1.id_for_label }}"><i class="fas fa-lock text-muted me-2 ms-2"></i>Password</label>
                            {% if form.password1.errors %}
                                <div class="text-danger small mt-1 fw-medium px-2">{{ form.password1.errors }}</div>
                            {% endif %}
                        </div>
                        <div class="col-md-6 form-floating">
                            {{ form.password2 }}
                            <label for="{{ form.password2.id_for_label }}"><i class="fas fa-check-circle text-muted me-2 ms-2"></i>Confirm</label>
                            {% if form.password2.errors %}
                                <div class="text-danger small mt-1 fw-medium px-2">{{ form.password2.errors }}</div>
                            {% endif %}
                        </div>
                    </div>
                    
                    <div class="mb-4 p-3 bg-light rounded-3 border">
                        <label for="{{ form.user_type.id_for_label }}" class="form-label fw-semibold mb-2">
                            <i class="fas fa-user-tag text-primary me-2"></i>I am joining as a:
                        </label>
                        {{ form.user_type }}
                        {% if form.user_type.errors %}
                            <div class="text-danger small mt-1 fw-medium">{{ form.user_type.errors }}</div>
                        {% endif %}
                    </div>
                    
                    {% if form.non_field_errors %}
                        <div class="alert alert-danger rounded-3 py-2 px-3 mb-4">
                            <i class="fas fa-exclamation-circle me-2"></i>{{ form.non_field_errors|striptags }}
                        </div>
                    {% endif %}
                    
                    <button type="submit" class="btn btn-success btn-lg w-100 mb-2 fw-semibold shadow-sm">
                        Create Account
                    </button>
                </form>
            </div>
            <div class="card-footer bg-light border-0 text-center py-4">
                <p class="mb-0 text-muted">Already have an account? 
                    <a href="{% url 'login' %}" class="fw-bold text-success text-decoration-none ms-1">Login here</a>
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_css %}
<style>
    .form-floating > .form-control { border-radius: 0.5rem; }
    /* Fix form-select height to match form-floating inputs visually */
    select.form-control, select.form-select { height: calc(3.5rem + 2px); padding-top: 1rem; padding-bottom: 0.5rem; }
</style>
<script>
    document.addEventListener("DOMContentLoaded", function() {
        document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"]').forEach(el => {
            el.classList.add('form-control');
            el.setAttribute('placeholder', ' ');
        });
        document.querySelectorAll('select').forEach(el => {
            el.classList.add('form-select');
        });
    });
</script>
{% endblock %}'''
with open(register_path, 'w', encoding='utf-8') as f:
    f.write(polished_register)

# 3. Profile Page Polish
profile_path = 'digiclassrooms/users/templates/users/profile.html'
with open(profile_path, 'r', encoding='utf-8') as f:
    profile_html = f.read()

# Replace the specific card structure for the profile
profile_html = profile_html.replace('class="card h-100"', 'class="card h-100 border-0 shadow-sm"')
profile_html = profile_html.replace('rounded-circle bg-primary text-white', 'rounded-circle text-white shadow-sm')
profile_html = profile_html.replace('style="width: 84px; height: 84px; font-size: 2rem;"', 'style="width: 100px; height: 100px; font-size: 2.5rem; background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);"')
profile_html = profile_html.replace('<div class="list-group list-group-flush">', '<div class="list-group list-group-flush mt-4">')

# Polish edit profile form
profile_html = profile_html.replace('class="card mt-4 border-0 bg-light-subtle"', 'class="card mt-4 border border-light bg-light rounded-4 shadow-sm"')

with open(profile_path, 'w', encoding='utf-8') as f:
    f.write(profile_html)

print("Auth and profile pages polished successfully.")
