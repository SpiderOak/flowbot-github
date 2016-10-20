"""template_env.py - A wrapper around the Jinja2 Template environment."""

import os
from jinja2 import Environment, FileSystemLoader


_jinja_env = Environment(
    loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__))
)

template = _jinja_env
