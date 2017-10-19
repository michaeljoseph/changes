# {{ release.name }} {{ release.release_date }} {{ release.version }} {{ release.description }}
{% for label, properties in release.changes.items() %}
## {{ properties.description }}
    {% for pull_request in properties.pull_requests %}
* #{{ pull_request.number }} {{ pull_request.title }}
    {% endfor %}
{% endfor %}