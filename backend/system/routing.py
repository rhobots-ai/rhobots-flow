"""
WebSocket URL routing for the system app.
Handles WebSocket connections for interactive browser automation.
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/automation/(?P<session_id>\w+)/$', consumers.AutomationConsumer.as_asgi()),
]
