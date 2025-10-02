"""
Color Converter Plugin
Converts between different color formats (HEX, RGB, HSL, etc.)
"""

import re
from typing import Type, Dict, Any, Tuple
from pydantic import BaseModel, Field, field_validator

from core.base import BaseTool, ToolInput, ToolOutput, ToolConfig, registry


class ColorInput(ToolInput):
    """Input model for color conversion"""
    color: str = Field(description="Color value in any supported format")
    
    @field_validator('color')
    def color_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Color value cannot be empty")
        return v.strip()


class ColorOutput(ToolOutput):
    """Output model for color conversion"""
    input_color: str = Field(description="Original input color")
    input_format: str = Field(description="Detected input format")
    hex: str = Field(description="Hexadecimal color (#RRGGBB)")
    rgb: Dict[str, int] = Field(description="RGB values")
    hsl: Dict[str, Any] = Field(description="HSL values")
    css_rgb: str = Field(description="CSS rgb() format")
    css_hsl: str = Field(description="CSS hsl() format")


class ColorTool(BaseTool):
    """Color format converter tool"""
    
    def get_config(self) -> ToolConfig:
        return ToolConfig(
            name="color",
            description="Convert between color formats (HEX, RGB, HSL)",
            category="design",
            keywords=["color", "hex", "rgb", "hsl", "convert", "css", "design"]
        )
    
    def get_input_model(self) -> Type[ToolInput]:
        return ColorInput
    
    def get_output_model(self) -> Type[ToolOutput]:
        return ColorOutput
    
    def _parse_hex(self, color: str) -> Tuple[int, int, int]:
        """Parse hex color to RGB"""
        color = color.lstrip('#')
        if len(color) == 3:
            color = ''.join([c*2 for c in color])
        if len(color) != 6:
            raise ValueError("Invalid hex color format")
        
        try:
            return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        except ValueError:
            raise ValueError("Invalid hex color values")
    
    def _parse_rgb(self, color: str) -> Tuple[int, int, int]:
        """Parse RGB color string"""
        match = re.match(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', color, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid RGB format")
        
        r, g, b = map(int, match.groups())
        if not all(0 <= val <= 255 for val in [r, g, b]):
            raise ValueError("RGB values must be between 0 and 255")
        
        return r, g, b
    
    def _parse_hsl(self, color: str) -> Tuple[int, int, int]:
        """Parse HSL color string and convert to RGB"""
        match = re.match(r'hsl\s*\(\s*(\d+)\s*,\s*(\d+)%\s*,\s*(\d+)%\s*\)', color, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid HSL format")
        
        h, s, l = map(int, match.groups())
        return self._hsl_to_rgb(h, s/100, l/100)
    
    def _rgb_to_hsl(self, r: int, g: int, b: int) -> Tuple[int, int, int]:
        """Convert RGB to HSL"""
        r, g, b = r/255.0, g/255.0, b/255.0
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        h, s, l = 0, 0, (max_val + min_val) / 2
        
        if max_val == min_val:
            h = s = 0  # achromatic
        else:
            d = max_val - min_val
            s = d / (2 - max_val - min_val) if l > 0.5 else d / (max_val + min_val)
            
            if max_val == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_val == g:
                h = (b - r) / d + 2
            elif max_val == b:
                h = (r - g) / d + 4
            h /= 6
        
        return int(h * 360), int(s * 100), int(l * 100)
    
    def _hsl_to_rgb(self, h: int, s: float, l: float) -> Tuple[int, int, int]:
        """Convert HSL to RGB"""
        def hue_to_rgb(p: float, q: float, t: float) -> float:
            if t < 0: t += 1
            if t > 1: t -= 1
            if t < 1/6: return p + (q - p) * 6 * t
            if t < 1/2: return q
            if t < 2/3: return p + (q - p) * (2/3 - t) * 6
            return p
        
        if s == 0:
            r = g = b = l  # achromatic
        else:
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            h = h / 360
            r = hue_to_rgb(p, q, h + 1/3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1/3)
        
        return int(r * 255), int(g * 255), int(b * 255)
    
    def execute(self, input_data: ColorInput) -> ColorOutput:
        """Convert color between formats"""
        color = input_data.color.strip()
        input_format = "unknown"
        
        try:
            # Try to parse different formats
            if color.startswith('#'):
                r, g, b = self._parse_hex(color)
                input_format = "hex"
            elif color.startswith('rgb'):
                r, g, b = self._parse_rgb(color)
                input_format = "rgb"
            elif color.startswith('hsl'):
                r, g, b = self._parse_hsl(color)
                input_format = "hsl"
            else:
                # Try as hex without #
                r, g, b = self._parse_hex(color)
                input_format = "hex"
            
            # Convert to other formats
            h, s, l = self._rgb_to_hsl(r, g, b)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            return ColorOutput(
                input_color=color,
                input_format=input_format,
                hex=hex_color,
                rgb={"r": r, "g": g, "b": b},
                hsl={"h": h, "s": s, "l": l},
                css_rgb=f"rgb({r}, {g}, {b})",
                css_hsl=f"hsl({h}, {s}%, {l}%)"
            )
            
        except ValueError as e:
            raise ValueError(f"Invalid color format: {e}")


# Register the tool
registry.register_tool(ColorTool, 'color')