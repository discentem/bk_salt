base:
  '*':
    {% set role = grains.get('role', none) %}
    {% if role != none %}
    - {{ role }}
    {% endif %}
