# {{ release.version }} ({{ release.release_date }}) {{ release.name or '' }}
{{ release.description or '' }}
{%- for label, properties in release.changes.items() %}
{%- if properties.pull_requests %}
## {{ properties.description }}
    {% for pull_request in properties.pull_requests %}
* #{{ pull_request.number }} {{ pull_request.title }}
    {% endfor %}
{% endif %}{% endfor %}
