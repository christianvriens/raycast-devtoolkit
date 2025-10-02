"""
Epoch/Timestamp Converter Plugin
Converts epoch timestamps to human-readable formats and vice versa
"""

import time
from datetime import datetime, timezone
from typing import Type, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator

from core.base import BaseTool, ToolInput, ToolOutput, ToolConfig, registry


class EpochInput(ToolInput):
    """Input model for epoch conversion"""
    timestamp: Optional[str] = Field(default=None, description="Epoch timestamp (leave empty for current time)")
    
    @field_validator('timestamp', mode='before')
    def validate_timestamp(cls, v):
        if v is None or v == "":
            return None
        if isinstance(v, (int, float)):
            return str(v)
        if not str(v).strip():
            return None
        return str(v).strip()


class EpochOutput(ToolOutput):
    """Output model for epoch conversion"""
    epoch: int = Field(description="Unix epoch timestamp")
    utc: Dict[str, str] = Field(description="UTC time representations")
    local: Dict[str, str] = Field(description="Local time representations")
    relative: Dict[str, Any] = Field(description="Relative time information")


class EpochTool(BaseTool):
    """Epoch timestamp converter tool"""
    
    def get_config(self) -> ToolConfig:
        return ToolConfig(
            name="epoch",
            description="Convert epoch timestamps to human-readable formats",
            category="time",
            keywords=["epoch", "timestamp", "unix", "time", "convert", "date"]
        )
    
    def get_input_model(self) -> Type[ToolInput]:
        return EpochInput
    
    def get_output_model(self) -> Type[ToolOutput]:
        return EpochOutput
    
    def execute(self, input_data: EpochInput) -> EpochOutput:
        """Convert epoch timestamp"""
        if input_data.timestamp is None:
            epoch = int(time.time())
        else:
            try:
                # Handle both seconds and milliseconds
                timestamp_str = input_data.timestamp.strip()
                if len(timestamp_str) >= 13:  # milliseconds
                    epoch = int(timestamp_str) // 1000
                else:  # seconds
                    epoch = int(timestamp_str)
            except ValueError:
                raise ValueError(f"Invalid epoch timestamp: {input_data.timestamp}")
        
        # Convert to datetime objects
        utc_dt = datetime.fromtimestamp(epoch, tz=timezone.utc)
        local_dt = datetime.fromtimestamp(epoch)
        current_dt = datetime.now(timezone.utc)
        
        # Calculate relative time
        time_diff = current_dt - utc_dt
        days_diff = time_diff.days
        seconds_diff = int(time_diff.total_seconds())
        
        # Human readable relative time
        if abs(seconds_diff) < 60:
            human_relative = f"{abs(seconds_diff)} seconds {'ago' if seconds_diff > 0 else 'from now'}"
        elif abs(seconds_diff) < 3600:
            minutes = abs(seconds_diff) // 60
            human_relative = f"{minutes} minutes {'ago' if seconds_diff > 0 else 'from now'}"
        elif abs(seconds_diff) < 86400:
            hours = abs(seconds_diff) // 3600
            human_relative = f"{hours} hours {'ago' if seconds_diff > 0 else 'from now'}"
        else:
            human_relative = f"{abs(days_diff)} days {'ago' if days_diff > 0 else 'from now'}"
        
        return EpochOutput(
            epoch=epoch,
            utc={
                "readable": utc_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
                "iso": utc_dt.isoformat(),
                "ddmmyyyy": utc_dt.strftime("%d/%m/%Y %H:%M:%S")
            },
            local={
                "readable": local_dt.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "iso": local_dt.isoformat(),
                "ddmmyyyy": local_dt.strftime("%d/%m/%Y %H:%M:%S")
            },
            relative={
                "days": days_diff,
                "seconds": seconds_diff,
                "human": human_relative
            }
        )


# Register the tool
registry.register_tool(EpochTool, 'epoch')