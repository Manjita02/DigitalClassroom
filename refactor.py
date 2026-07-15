import re

with open('digiclassrooms/users/templates/users/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace style block
style_pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
css_link = '<link rel="stylesheet" href="{% static \'css/main.css\' %}">'
content = style_pattern.sub(css_link, content)

# Replace script block
script_pattern = re.compile(r'<script>\s*\(function \(\) \{.*?const markReadTemplate.*?\}\)\(\);\s*</script>', re.DOTALL)
js_include = '''<script>
    window.DjangoConfig = {
        markReadTemplate: '{% url "notifications_mark_read" 0 %}',
        notificationsFeedUrl: '{% url "notifications_feed" %}',
        markAllReadUrl: '{% url "notifications_mark_all_read" %}'
    };
</script>
<script src="{% static \'js/main.js\' %}"></script>'''
content = script_pattern.sub(js_include, content)

with open('digiclassrooms/users/templates/users/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated base.html successfully')
