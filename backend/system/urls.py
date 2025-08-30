"""
URL configuration for the system app.
Defines API endpoints for interactive browser automation.
"""

from django.urls import path
from .views import (
    StartAutomationView,
    StopAutomationView, 
    AutomationStatusView,
    BrowserHealthView,
    TestBrowserConnectionView
)

urlpatterns = [
    # Automation control endpoints
    path('automations/start/', StartAutomationView.as_view(), name='start-automation'),
    path('automations/stop/', StopAutomationView.as_view(), name='stop-automation'),
    path('automations/status/<str:session_id>/', AutomationStatusView.as_view(), name='automation-status'),
    
    # Browser health and testing endpoints
    path('browser/health/', BrowserHealthView.as_view(), name='browser-health'),
    path('browser/test/', TestBrowserConnectionView.as_view(), name='test-browser-connection'),
]
