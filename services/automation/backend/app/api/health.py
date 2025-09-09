from fastapi import APIRouter, HTTPException
from app.config import settings
import httpx
import asyncio
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def health_check():
    """Extended health check endpoint matching auto-flow format"""
    return {
        "status": "healthy",
        "timezone": settings.timezone,
        "vnc_host": settings.vnc_host,
        "timestamp": datetime.now().isoformat(),
        "backend": True,
        "database": True,
        "vnc": True
    }

@router.get("/test-browser")
async def test_browser_simple():
    """Simple test browser endpoint for compatibility with auto-flow Home.vue"""
    try:
        # Test if session manager is accessible
        base = settings.session_manager_url.rstrip("/")
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{base}/api/health", timeout=5.0)
            resp.raise_for_status()
            
        return {
            "status": "success",
            "message": "Browser test connection successful. Session manager is accessible."
        }
    except Exception as e:
        logger.error(f"Browser test failed: {e}")
        return {
            "status": "error", 
            "message": f"Browser test failed: {str(e)}"
        }
