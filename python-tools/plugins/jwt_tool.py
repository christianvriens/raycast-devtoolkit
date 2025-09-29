"""
JWT Decoder Plugin
Decodes and validates JSON Web Tokens (JWT)
"""

import json
import base64
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel, Field, validator

from core.base import BaseTool, ToolInput, ToolOutput, ToolConfig, registry


class JWTInput(ToolInput):
    """Input model for JWT decoding"""
    token: str = Field(description="JWT token to decode")
    
    @validator('token')
    def token_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("JWT token cannot be empty")
        return v.strip()


class JWTOutput(ToolOutput):
    """Output model for JWT decoding"""
    header: Dict[str, Any] = Field(description="JWT header")
    payload: Dict[str, Any] = Field(description="JWT payload")
    signature: str = Field(description="JWT signature (raw)")
    issued_at: Optional[int] = Field(default=None, description="Issued at timestamp")
    expires_at: Optional[int] = Field(default=None, description="Expires at timestamp")
    issued_at_readable: Optional[str] = Field(default=None, description="Issued at human readable")
    expires_at_readable: Optional[str] = Field(default=None, description="Expires at human readable")
    is_expired: Optional[bool] = Field(default=None, description="Whether token is expired")
    valid_format: bool = Field(description="Whether JWT format is valid")


class JWTTool(BaseTool):
    """JWT decoder tool for analyzing JSON Web Tokens"""
    
    def get_config(self) -> ToolConfig:
        return ToolConfig(
            name="jwt",
            description="Decode and analyze JSON Web Tokens (JWT)",
            category="security",
            keywords=["jwt", "json", "web", "token", "decode", "auth", "security"]
        )
    
    def get_input_model(self) -> Type[ToolInput]:
        return JWTInput
    
    def get_output_model(self) -> Type[ToolOutput]:
        return JWTOutput
    
    def _decode_base64_url(self, data: str) -> Dict[str, Any]:
        """Decode base64url encoded JWT part"""
        # Add padding if needed
        data += '=' * (4 - len(data) % 4)
        try:
            decoded = base64.urlsafe_b64decode(data)
            return json.loads(decoded.decode('utf-8'))
        except Exception as e:
            raise ValueError(f"Invalid base64url encoding: {e}")
    
    def _format_timestamp(self, timestamp: int) -> str:
        """Format timestamp to human readable string"""
        try:
            dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except Exception:
            return "Invalid timestamp"
    
    def execute(self, input_data: JWTInput) -> JWTOutput:
        """Decode JWT token"""
        token = input_data.token.strip()
        
        # Split JWT into parts
        parts = token.split('.')
        if len(parts) != 3:
            return JWTOutput(
                header={},
                payload={},
                signature="",
                issued_at=None,
                expires_at=None,
                issued_at_readable=None,
                expires_at_readable=None,
                is_expired=None,
                valid_format=False
            )
        
        try:
            # Decode header and payload
            header = self._decode_base64_url(parts[0])
            payload = self._decode_base64_url(parts[1])
            signature = parts[2]
            
            # Extract timestamps
            issued_at = payload.get('iat')
            expires_at = payload.get('exp')
            
            # Format readable timestamps
            issued_at_readable = self._format_timestamp(issued_at) if issued_at else None
            expires_at_readable = self._format_timestamp(expires_at) if expires_at else None
            
            # Check if expired
            is_expired = None
            if expires_at:
                current_time = int(datetime.now(timezone.utc).timestamp())
                is_expired = expires_at < current_time
            
            return JWTOutput(
                header=header,
                payload=payload,
                signature=signature,
                issued_at=issued_at,
                expires_at=expires_at,
                issued_at_readable=issued_at_readable,
                expires_at_readable=expires_at_readable,
                is_expired=is_expired,
                valid_format=True
            )
            
        except Exception as e:
            raise ValueError(f"Failed to decode JWT: {e}")


# Register the tool
registry.register_tool(JWTTool, 'jwt')