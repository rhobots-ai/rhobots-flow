"""
Interactive Browser Automation Engine using Playwright.
Provides live, interactive browser automation with VNC streaming.
"""

import time
import logging
from datetime import datetime
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from .consumers import get_pause_flag, set_pause_flag, clear_session

logger = logging.getLogger(__name__)

# Browser connection endpoint from settings
BROWSER_CDP_ENDPOINT = getattr(settings, 'PLAYWRIGHT_BROWSER_CDP_ENDPOINT', 'http://playwright-vnc:9222')


class AutomationEngine:
    """
    Core automation engine for interactive browser automation.
    
    Features:
    - Playwright browser control via CDP
    - Real-time status updates via WebSocket
    - Interactive pause/resume functionality
    - Error handling and recovery
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.channel_layer = get_channel_layer()
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        
    def send_status(self, status: str, message: str, step_info: dict = None):
        """Send status update via WebSocket."""
        try:
            async_to_sync(self.channel_layer.group_send)(
                f'automation_{self.session_id}',
                {
                    "type": "automation_status",
                    "status": status,
                    "message": message,
                    "timestamp": datetime.now().isoformat(),
                    "step_info": step_info
                }
            )
            logger.info(f"Status sent to {self.session_id}: {status} - {message}")
        except Exception as e:
            logger.error(f"Failed to send status for {self.session_id}: {str(e)}")
    
    def wait_for_resume(self):
        """Wait for user to resume automation."""
        logger.info(f"Automation paused for session: {self.session_id}")
        while get_pause_flag(self.session_id):
            time.sleep(1)  # Check every second
        logger.info(f"Automation resumed for session: {self.session_id}")
    
    def connect_to_browser(self, playwright: Playwright) -> bool:
        """Connect to the remote browser via CDP."""
        try:
            self.send_status('connecting', 'Connecting to browser...')
            # Connect to existing browser instance
            self.browser = playwright.chromium.connect_over_cdp(
                BROWSER_CDP_ENDPOINT,
                timeout=30000
            )

            # Get or create context
            if self.browser.contexts:
                self.context = self.browser.contexts[0]
            else:
                self.context = self.browser.new_context(
                    viewport={'width': 1920, 'height': 1080}
                )

            # Create new page
            self.page = self.context.new_page()

            self.send_status('connected', 'Browser connected successfully.')
            return True
                
        except Exception as e:
            error_msg = f"Failed to connect to browser: {str(e)}"
            self.send_status('error', error_msg)
            logger.error(f"Browser connection failed for {self.session_id}: {error_msg}")
            return False
    
    def disconnect_browser(self):
        """Safely disconnect from browser."""
        try:
            if self.browser and self.browser.is_connected():
                self.browser.close()
                self.send_status('disconnected', 'Browser disconnected.')
                logger.info(f"Browser disconnected for session: {self.session_id}")
        except Exception as e:
            logger.error(f"Error disconnecting browser for {self.session_id}: {str(e)}")
        finally:
            # Clean up session data
            clear_session(self.session_id)
    
    def execute_automation_script(self):
        """Execute the main automation script."""
        try:
            # Keep Playwright context alive for the full duration
            with sync_playwright() as p:
                if not self.connect_to_browser(p):
                    return
            
            # Step 1: Navigate to target website
            self.send_status('running', 'Navigating to target website...')
            self.page.goto("https://angularformadd.netlify.app/", timeout=30000)
            self.send_status('running', 'Website loaded successfully.')
            
            # Wait a moment for the page to fully load
            time.sleep(2)
            
            # Step 2: Interactive handover
            self.send_status('paused', 'Handing over control. Please interact with the form and click Resume when ready.')
            set_pause_flag(self.session_id, True)
            
            # Wait for user interaction
            self.wait_for_resume()
            
            # Step 3: Resume automation
            self.send_status('running', 'Resuming automation...')
            
            try:
                # Look for and click the "Add Route" button
                add_route_button = self.page.locator('text=Add Route').first
                if add_route_button.is_visible():
                    add_route_button.click()
                    self.send_status('running', 'Clicked "Add Route" button.')
                else:
                    # Try alternative selectors
                    button_selectors = [
                        'button:has-text("Add Route")',
                        'input[value="Add Route"]',
                        '[onclick*="addRoute"]',
                        '.btn:has-text("Add")'
                    ]
                    
                    button_clicked = False
                    for selector in button_selectors:
                        try:
                            element = self.page.locator(selector).first
                            if element.is_visible():
                                element.click()
                                self.send_status('running', f'Clicked button using selector: {selector}')
                                button_clicked = True
                                break
                        except Exception:
                            continue
                    
                    if not button_clicked:
                        self.send_status('warning', 'Could not find "Add Route" button. Please check the form.')
                
            except Exception as e:
                logger.warning(f"Error clicking Add Route button: {str(e)}")
                self.send_status('warning', f'Could not click Add Route button: {str(e)}')
            
            # Step 4: Observe result
            time.sleep(3)
            
            # Final status
            self.send_status('completed', 'Automation completed successfully!')

        except Exception as e:
            error_msg = f"Automation error: {str(e)}"
            self.send_status('error', error_msg)
            logger.error(f"Automation failed for {self.session_id}: {error_msg}")
        
        finally:
            # Always disconnect
            self.disconnect_browser()


def run_automation_script(session_id: str):
    """
    Main entry point for running automation script.
    This function is called from the API endpoint in a background thread.
    """
    logger.info(f"Starting automation for session: {session_id}")
    
    try:
        engine = AutomationEngine(session_id)
        engine.execute_automation_script()
    except Exception as e:
        logger.error(f"Critical error in automation for {session_id}: {str(e)}")
        # Send final error status
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'automation_{session_id}',
                {
                    "type": "automation_status",
                    "status": "error",
                    "message": f"Critical automation error: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception:
            pass  # Fail silently if we can't even send error status
    
    logger.info(f"Automation completed for session: {session_id}")


# Utility functions for testing and development
def test_browser_connection():
    """Test function to verify browser connectivity."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(BROWSER_CDP_ENDPOINT, timeout=5000)
            version = browser.version
            browser.close()
            return True, f"Connected successfully. Browser version: {version}"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"


def get_browser_status():
    """Get current browser status for health checks."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(BROWSER_CDP_ENDPOINT, timeout=5000)
            contexts = len(browser.contexts)
            pages = sum(len(context.pages) for context in browser.contexts)
            browser.close()
            return {
                'connected': True,
                'contexts': contexts,
                'pages': pages,
                'endpoint': BROWSER_CDP_ENDPOINT
            }
    except Exception as e:
        return {
            'connected': False,
            'error': str(e),
            'endpoint': BROWSER_CDP_ENDPOINT
        }
