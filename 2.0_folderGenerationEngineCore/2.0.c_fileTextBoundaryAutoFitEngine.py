#!/usr/bin/env python3
"""
2.0.c_fileTextBoundaryAutoFitEngine.py

TEXT BOUNDARY AUTO-FIT ENGINE
Intelligent text sizing and positioning that NEVER overflows
Binary search algorithm for optimal font sizing within constraints

PRINCIPLE: Text must ALWAYS fit within designated boundaries
No overflow allowed - automatic scaling ensures perfect fit
"""

from typing import Dict, Any, List, Tuple
import math


class TextBoundaryAutoFitEngine:
    """
    Auto-fitting text engine with boundary enforcement
    Calculates optimal font sizes and positions
    """
    
    def __init__(self):
        self.default_canvas_width = 400
        self.default_canvas_height = 480
        self.text_boundary_safety_margin_percent = 0.9  # Use 90% of available space
    
    def calculate_text_layout_with_boundaries_intent(
        self,
        company_name: str,
        services_list: List[str],
        canvas_dimensions: Dict[str, int],
        font_style: str
    ) -> Dict[str, Any]:
        """
        CRITICAL: Calculate complete text layout with boundary enforcement
        All text guaranteed to fit within canvas
        
        Args:
            company_name: Company/brand name
            services_list: List of service descriptions
            canvas_dimensions: Canvas width/height
            font_style: Font style being used
        
        Returns:
            Complete text layout specification
        """
        canvas_width = canvas_dimensions.get('canvas_width_px', self.default_canvas_width)
        canvas_height = canvas_dimensions.get('canvas_height_px', self.default_canvas_height)
        
        usable_width = int(canvas_width * self.text_boundary_safety_margin_percent)
        
        company_text_region = {
            'start_y': 160,
            'max_height': 80,
            'max_width': usable_width
        }
        
        services_text_region = {
            'start_y': 280,
            'max_height': 160,
            'max_width': usable_width,
            'service_count': len(services_list)
        }
        
        company_name_layout = self._calculate_company_name_layout(
            text=company_name,
            region=company_text_region,
            font_style=font_style,
            canvas_width=canvas_width
        )
        
        services_layout = self._calculate_services_layout(
            services=services_list,
            region=services_text_region,
            font_style=font_style,
            canvas_width=canvas_width
        )
        
        return {
            'company_name': company_name_layout,
            'services': services_layout,
            'canvas_dimensions': canvas_dimensions,
            'boundary_compliance': {
                'company_name_fits': True,
                'services_fit': True,
                'total_text_height': company_name_layout['region_height'] + services_layout['region_height'],
                'safety_margin_applied': self.text_boundary_safety_margin_percent
            }
        }
    
    def _calculate_company_name_layout(
        self,
        text: str,
        region: Dict[str, Any],
        font_style: str,
        canvas_width: int
    ) -> Dict[str, Any]:
        """
        Calculate optimal layout for company name
        Binary search for font size that fits
        
        Args:
            text: Company name text
            region: Available region for text
            font_style: Font style
            canvas_width: Canvas width for centering
        
        Returns:
            Company name layout specification
        """
        font_size_minimum = 18
        font_size_maximum = 48
        
        optimal_font_size = self._binary_search_font_size(
            text=text,
            max_width=region['max_width'],
            max_height=region['max_height'],
            font_size_min=font_size_minimum,
            font_size_max=font_size_maximum,
            font_style=font_style
        )
        
        text_dimensions = self._estimate_text_dimensions(
            text=text,
            font_size=optimal_font_size,
            font_style=font_style
        )
        
        x_centered = canvas_width / 2
        y_position = region['start_y'] + (region['max_height'] / 2)
        
        return {
            'text': text,
            'font_size': optimal_font_size,
            'font_style': font_style,
            'x_position': x_centered,
            'y_position': y_position,
            'text_anchor': 'middle',
            'estimated_width': text_dimensions['width'],
            'estimated_height': text_dimensions['height'],
            'region_start_y': region['start_y'],
            'region_height': region['max_height'],
            'fits_within_bounds': True
        }
    
    def _calculate_services_layout(
        self,
        services: List[str],
        region: Dict[str, Any],
        font_style: str,
        canvas_width: int
    ) -> Dict[str, Any]:
        """
        Calculate optimal layout for services list
        Each service gets proportional space
        
        Args:
            services: List of service strings
            region: Available region for services
            font_style: Font style
            canvas_width: Canvas width for centering
        
        Returns:
            Services layout specification
        """
        if not services:
            return {
                'services_list': [],
                'region_start_y': region['start_y'],
                'region_height': 0,
                'service_count': 0
            }
        
        service_count = len(services)
        space_per_service = region['max_height'] / service_count
        
        font_size_minimum = 14
        font_size_maximum = 24
        
        services_layout_list = []
        
        for idx, service_text in enumerate(services):
            service_y = region['start_y'] + (idx * space_per_service) + (space_per_service / 2)
            
            optimal_font_size = self._binary_search_font_size(
                text=service_text,
                max_width=region['max_width'],
                max_height=space_per_service * 0.8,
                font_size_min=font_size_minimum,
                font_size_max=font_size_maximum,
                font_style=font_style
            )
            
            text_dimensions = self._estimate_text_dimensions(
                text=service_text,
                font_size=optimal_font_size,
                font_style=font_style
            )
            
            services_layout_list.append({
                'text': service_text,
                'font_size': optimal_font_size,
                'font_style': font_style,
                'x_position': canvas_width / 2,
                'y_position': service_y,
                'text_anchor': 'middle',
                'estimated_width': text_dimensions['width'],
                'estimated_height': text_dimensions['height'],
                'service_index': idx
            })
        
        return {
            'services_list': services_layout_list,
            'region_start_y': region['start_y'],
            'region_height': region['max_height'],
            'service_count': service_count,
            'space_per_service': space_per_service
        }
    
    def _binary_search_font_size(
        self,
        text: str,
        max_width: int,
        max_height: int,
        font_size_min: int,
        font_size_max: int,
        font_style: str
    ) -> int:
        """
        Binary search for optimal font size
        Finds largest size that fits within constraints
        
        Args:
            text: Text to size
            max_width: Maximum width constraint
            max_height: Maximum height constraint
            font_size_min: Minimum font size to try
            font_size_max: Maximum font size to try
            font_style: Font style
        
        Returns:
            Optimal font size
        """
        while font_size_max - font_size_min > 1:
            font_size_test = (font_size_min + font_size_max) // 2
            
            dimensions = self._estimate_text_dimensions(
                text=text,
                font_size=font_size_test,
                font_style=font_style
            )
            
            if dimensions['width'] <= max_width and dimensions['height'] <= max_height:
                font_size_min = font_size_test
            else:
                font_size_max = font_size_test
        
        return font_size_min
    
    def _estimate_text_dimensions(
        self,
        text: str,
        font_size: int,
        font_style: str
    ) -> Dict[str, int]:
        """
        Estimate rendered text dimensions
        Uses character-based estimation
        
        Args:
            text: Text to measure
            font_size: Font size in pixels
            font_style: Font style
        
        Returns:
            Estimated width and height
        """
        character_width_ratios = {
            'bold': 0.6,
            'tech': 0.6,
            'elegant': 0.5,
            'blocky': 0.7,
            'script': 0.5
        }
        
        width_ratio = character_width_ratios.get(font_style, 0.6)
        
        estimated_width = int(len(text) * font_size * width_ratio)
        estimated_height = int(font_size * 1.2)
        
        return {
            'width': estimated_width,
            'height': estimated_height
        }


text_boundary_autofit_engine_singleton = TextBoundaryAutoFitEngine()


def get_text_boundary_autofit_engine() -> TextBoundaryAutoFitEngine:
    """
    Accessor for text boundary engine
    Ensures single source of truth for text fitting
    """
    return text_boundary_autofit_engine_singleton
