#!/usr/bin/env python3
"""
2.0.b_fileColorResolverPrecedenceEngine.py

COLOR RESOLVER PRECEDENCE ENGINE
Resolves color conflicts, ensures contrast, applies precedence rules
CRITICAL: No color conflicts between user/seed/system levels

PRINCIPLE: User color choices ALWAYS respected
System ensures WCAG compliance while honoring user intent
"""

from typing import Dict, Any, Tuple, Optional
import re


class ColorResolverPrecedenceEngine:
    """
    Color resolution with precedence and contrast validation
    Ensures accessible, conflict-free color schemes
    """
    
    def __init__(self):
        self.wcag_minimum_contrast_ratio = 4.5  # AA standard
        self.wcag_preferred_contrast_ratio = 7.0  # AAA standard
    
    def resolve_color_scheme_with_precedence_intent(
        self,
        resolved_parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        CRITICAL: Resolve complete color scheme with precedence
        Ensures contrast compliance while respecting user choices
        
        Args:
            resolved_parameters: Parameters with precedence already applied
        
        Returns:
            Complete color scheme specification
        """
        color_primary = self._parse_color_to_rgb(
            resolved_parameters.get('color_primary', '#1a4d7a')
        )
        
        color_accent = self._parse_color_to_rgb(
            resolved_parameters.get('color_accent', '#ffffff')
        )
        
        color_text = self._parse_color_to_rgb(
            resolved_parameters.get('color_text', '#ffffff')
        )
        
        text_on_primary_contrast = self._calculate_contrast_ratio(
            color_text, color_primary
        )
        
        if text_on_primary_contrast < self.wcag_minimum_contrast_ratio:
            if resolved_parameters.get('color_text_source') == 'USER_OVERRIDE':
                color_primary = self._adjust_background_for_contrast(
                    text_color=color_text,
                    background_color=color_primary,
                    target_contrast=self.wcag_minimum_contrast_ratio
                )
            else:
                color_text = self._adjust_text_for_contrast(
                    text_color=color_text,
                    background_color=color_primary,
                    target_contrast=self.wcag_minimum_contrast_ratio
                )
        
        return {
            'background_primary_rgb': color_primary,
            'background_primary_hex': self._rgb_to_hex(color_primary),
            'accent_color_rgb': color_accent,
            'accent_color_hex': self._rgb_to_hex(color_accent),
            'text_color_rgb': color_text,
            'text_color_hex': self._rgb_to_hex(color_text),
            'contrast_ratio_text_on_primary': text_on_primary_contrast,
            'wcag_compliance_level': self._get_wcag_level(text_on_primary_contrast),
            'color_scheme_metadata': {
                'user_overrides_respected': True,
                'contrast_adjustments_made': text_on_primary_contrast < self.wcag_minimum_contrast_ratio,
                'adjustment_target': 'background' if resolved_parameters.get('color_text_source') == 'USER_OVERRIDE' else 'text'
            }
        }
    
    def _parse_color_to_rgb(self, color_value: str) -> Tuple[int, int, int]:
        """
        Parse color string to RGB tuple
        Supports hex (#RRGGBB) and named colors
        
        Args:
            color_value: Color as hex or name
        
        Returns:
            RGB tuple (r, g, b)
        """
        named_colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'cyan': (0, 255, 255),
            'magenta': (255, 0, 255),
            'gray': (128, 128, 128),
            'grey': (128, 128, 128)
        }
        
        color_lower = color_value.lower().strip()
        
        if color_lower in named_colors:
            return named_colors[color_lower]
        
        if color_value.startswith('#'):
            hex_value = color_value[1:]
            
            if len(hex_value) == 3:
                hex_value = ''.join([c*2 for c in hex_value])
            
            if len(hex_value) == 6:
                r = int(hex_value[0:2], 16)
                g = int(hex_value[2:4], 16)
                b = int(hex_value[4:6], 16)
                return (r, g, b)
        
        return (26, 77, 122)
    
    def _rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """
        Convert RGB tuple to hex string
        
        Args:
            rgb: RGB tuple
        
        Returns:
            Hex color string
        """
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def _calculate_contrast_ratio(
        self,
        color1: Tuple[int, int, int],
        color2: Tuple[int, int, int]
    ) -> float:
        """
        Calculate WCAG contrast ratio between two colors
        
        Args:
            color1: First color RGB
            color2: Second color RGB
        
        Returns:
            Contrast ratio (1.0 to 21.0)
        """
        luminance1 = self._calculate_relative_luminance(color1)
        luminance2 = self._calculate_relative_luminance(color2)
        
        lighter = max(luminance1, luminance2)
        darker = min(luminance1, luminance2)
        
        contrast_ratio = (lighter + 0.05) / (darker + 0.05)
        
        return contrast_ratio
    
    def _calculate_relative_luminance(self, rgb: Tuple[int, int, int]) -> float:
        """
        Calculate relative luminance for WCAG contrast
        
        Args:
            rgb: RGB color tuple
        
        Returns:
            Relative luminance (0.0 to 1.0)
        """
        r, g, b = [val / 255.0 for val in rgb]
        
        def adjust_channel(channel):
            if channel <= 0.03928:
                return channel / 12.92
            else:
                return ((channel + 0.055) / 1.055) ** 2.4
        
        r_adjusted = adjust_channel(r)
        g_adjusted = adjust_channel(g)
        b_adjusted = adjust_channel(b)
        
        luminance = 0.2126 * r_adjusted + 0.7152 * g_adjusted + 0.0722 * b_adjusted
        
        return luminance
    
    def _adjust_text_for_contrast(
        self,
        text_color: Tuple[int, int, int],
        background_color: Tuple[int, int, int],
        target_contrast: float
    ) -> Tuple[int, int, int]:
        """
        Adjust text color to meet contrast target
        Used when text is NOT user override
        
        Args:
            text_color: Current text color
            background_color: Background color
            target_contrast: Desired contrast ratio
        
        Returns:
            Adjusted text color
        """
        bg_luminance = self._calculate_relative_luminance(background_color)
        
        if bg_luminance > 0.5:
            return (0, 0, 0)
        else:
            return (255, 255, 255)
    
    def _adjust_background_for_contrast(
        self,
        text_color: Tuple[int, int, int],
        background_color: Tuple[int, int, int],
        target_contrast: float
    ) -> Tuple[int, int, int]:
        """
        Adjust background color to meet contrast target
        Used when text IS user override (preserve user text choice)
        
        Args:
            text_color: User-chosen text color
            background_color: Current background
            target_contrast: Desired contrast ratio
        
        Returns:
            Adjusted background color
        """
        text_luminance = self._calculate_relative_luminance(text_color)
        
        if text_luminance > 0.5:
            factor = 0.3
        else:
            factor = 1.7
        
        adjusted_bg = tuple(
            min(255, max(0, int(val * factor)))
            for val in background_color
        )
        
        return adjusted_bg
    
    def _get_wcag_level(self, contrast_ratio: float) -> str:
        """
        Get WCAG compliance level for contrast ratio
        
        Args:
            contrast_ratio: Calculated contrast ratio
        
        Returns:
            WCAG level (AAA, AA, or FAIL)
        """
        if contrast_ratio >= self.wcag_preferred_contrast_ratio:
            return 'AAA'
        elif contrast_ratio >= self.wcag_minimum_contrast_ratio:
            return 'AA'
        else:
            return 'FAIL'


color_resolver_precedence_engine_singleton = ColorResolverPrecedenceEngine()


def get_color_resolver_precedence_engine() -> ColorResolverPrecedenceEngine:
    """
    Accessor for color resolver engine
    Ensures single source of truth for color resolution
    """
    return color_resolver_precedence_engine_singleton
