from fastapi import Depends, Header, HTTPException, status

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)



async def api_key_auth(x_api_key: str | None = Header(default=None)) -> None:
    """
    API Key authentication dependency.
    """

    if x_api_key is None:
        logger.warning("Missing API key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
        )

    if x_api_key != settings.API_KEY:
        logger.warning("Invalid API key")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
