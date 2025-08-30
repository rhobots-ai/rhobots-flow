"""
API Views for Interactive Browser Automation.
Provides endpoints for starting, stopping, and monitoring automation sessions.
"""

import threading
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from .automation import run_automation_script, test_browser_connection, get_browser_status
from .consumers import get_pause_flag, set_pause_flag, clear_session

logger = logging.getLogger(__name__)


class StartAutomationView(APIView):
    """
    Start a new interactive browser automation session.
    
    POST /api/system/automations/start/
    Body: {"sessionId": "unique_session_id"}
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        session_id = request.data.get('sessionId')
        
        if not session_id:
            return Response(
                {"error": "sessionId is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Clear any existing session data
            clear_session(session_id)
            
            # Run the automation script in a background thread to avoid blocking the request
            thread = threading.Thread(
                target=run_automation_script, 
                args=(session_id,),
                daemon=True  # Thread will die when main thread dies
            )
            thread.start()
            
            logger.info(f"Automation started for session: {session_id}")
            
            return Response({
                "status": "success",
                "message": "Automation task initiated.",
                "sessionId": session_id
            })
            
        except Exception as e:
            logger.error(f"Failed to start automation for {session_id}: {str(e)}")
            return Response(
                {"error": f"Failed to start automation: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StopAutomationView(APIView):
    """
    Stop an active automation session.
    
    POST /api/system/automations/stop/
    Body: {"sessionId": "session_id_to_stop"}
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        session_id = request.data.get('sessionId')
        
        if not session_id:
            return Response(
                {"error": "sessionId is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Clear session to stop automation
            clear_session(session_id)
            
            logger.info(f"Automation stopped for session: {session_id}")
            
            return Response({
                "status": "success",
                "message": "Automation stopped.",
                "sessionId": session_id
            })
            
        except Exception as e:
            logger.error(f"Failed to stop automation for {session_id}: {str(e)}")
            return Response(
                {"error": f"Failed to stop automation: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AutomationStatusView(APIView):
    """
    Get the current status of an automation session.
    
    GET /api/system/automations/status/{session_id}/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id, *args, **kwargs):
        try:
            is_paused = get_pause_flag(session_id)
            
            return Response({
                "sessionId": session_id,
                "isPaused": is_paused,
                "status": "paused" if is_paused else "running"
            })
            
        except Exception as e:
            logger.error(f"Failed to get status for {session_id}: {str(e)}")
            return Response(
                {"error": f"Failed to get status: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BrowserHealthView(APIView):
    """
    Check the health of the browser service.
    
    GET /api/system/browser/health/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            browser_status = get_browser_status()
            
            if browser_status['connected']:
                return Response({
                    "status": "healthy",
                    "browser": browser_status
                })
            else:
                return Response({
                    "status": "unhealthy",
                    "browser": browser_status
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                
        except Exception as e:
            logger.error(f"Browser health check failed: {str(e)}")
            return Response({
                "status": "unhealthy",
                "error": str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class TestBrowserConnectionView(APIView):
    """
    Test browser connection for debugging.
    
    GET /api/system/browser/test/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            success, message = test_browser_connection()
            
            if success:
                return Response({
                    "status": "success",
                    "message": message
                })
            else:
                return Response({
                    "status": "failed",
                    "message": message
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                
        except Exception as e:
            logger.error(f"Browser connection test failed: {str(e)}")
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
