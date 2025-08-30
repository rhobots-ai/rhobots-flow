"""
WebSocket consumers for interactive browser automation.
Handles real-time communication between frontend and automation engine.
"""

import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

# A simple in-memory store for automation pause flags
# In production, this should be stored in Redis or database
pause_flags = {}


class AutomationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling automation session communication.
    
    Features:
    - Real-time status updates
    - Interactive pause/resume control
    - Session management
    """
    
    async def connect(self):
        """Accept WebSocket connection and join automation group."""
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group_name = f'automation_{self.session_id}'

        # Join automation group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
        logger.info(f"WebSocket connected for automation session: {self.session_id}")

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection and cleanup."""
        # Leave automation group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Clean up pause flags
        pause_flags.pop(self.session_id, None)
        
        logger.info(f"WebSocket disconnected for automation session: {self.session_id}")

    async def receive(self, text_data):
        """Handle incoming messages from WebSocket."""
        try:
            data = json.loads(text_data)
            command = data.get('command')
            
            if command == 'resume':
                # Signal automation to resume
                pause_flags[self.session_id] = False
                logger.info(f"Resume command received for session: {self.session_id}")
                
                # Notify group that automation is resuming
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'automation_status',
                        'status': 'running',
                        'message': 'Automation resumed by user.'
                    }
                )
            elif command == 'pause':
                # Signal automation to pause
                pause_flags[self.session_id] = True
                logger.info(f"Pause command received for session: {self.session_id}")
                
            elif command == 'status':
                # Request current status
                await self.send(text_data=json.dumps({
                    'type': 'status_response',
                    'session_id': self.session_id,
                    'is_paused': pause_flags.get(self.session_id, False)
                }))
                
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received from session: {self.session_id}")
        except Exception as e:
            logger.error(f"Error handling message for session {self.session_id}: {str(e)}")

    async def automation_status(self, event):
        """Send automation status update to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'status': event['status'],
            'message': event['message'],
            'timestamp': event.get('timestamp'),
            'step_info': event.get('step_info')
        }))


# Utility functions for automation control
def set_pause_flag(session_id: str, paused: bool = True):
    """Set pause flag for a specific session."""
    pause_flags[session_id] = paused


def get_pause_flag(session_id: str) -> bool:
    """Get pause flag for a specific session."""
    return pause_flags.get(session_id, False)


def clear_session(session_id: str):
    """Clear session data."""
    pause_flags.pop(session_id, None)
