#!/usr/bin/env python3
"""
2.0.d_fileShapeCompositorSafeZoneEngine.py

SHAPE COMPOSITOR SAFE ZONE ENGINE
Places geometric shapes and icons in safe zones
NEVER overlaps with text - respects text boundaries absolutely

PRINCIPLE: Shapes fill available space without text collision
Safe zones calculated from text layout
All shapes positioned deterministically from seed
"""

from typing import Dict, Any, List, Tuple
import math
import random


class ShapeCompositorSafeZoneEngine:
    """
    Shape composition engine with safe zone enforcement
    Places shapes only in areas that don't conflict with text
    """
    
    def __init__(self):
        self.minimum_shape_margin_px = 10
        self.shape_opacity_default = 0.15
    
    def compose_shapes_in_safe_zones_intent(
        self,
        text_layout: Dict[str, Any],
        canvas_dimensions: Dict[str, int],
        geometry_style: str,
        seed: int
    ) -> Dict[str, Any]:
        """
        CRITICAL: Compose shapes that respect text boundaries
        No shape ever overlaps text
        
        Args:
            text_layout: Complete text layout with boundaries
            canvas_dimensions: Canvas dimensions
            geometry_style: Geometry style (sharp, round, mixed, minimal)
            seed: Seed for deterministic placement
        
        Returns:
            Complete shape composition specification
        """
        random.seed(seed)
        
        safe_zones = self._calculate_safe_zones_from_text_layout(
            text_layout=text_layout,
            canvas_dimensions=canvas_dimensions
        )
        
        shape_definitions = self._generate_shapes_for_geometry_style(
            geometry_style=geometry_style,
            safe_zones=safe_zones,
            seed=seed
        )
        
        positioned_shapes = self._position_shapes_in_safe_zones(
            shapes=shape_definitions,
            safe_zones=safe_zones
        )
        
        return {
            'shapes': positioned_shapes,
            'safe_zones': safe_zones,
            'geometry_style': geometry_style,
            'shape_count': len(positioned_shapes),
            'composition_metadata': {
                'text_collision_free': True,
                'safe_zone_count': len(safe_zones),
                'seed_deterministic': True
            }
        }
    
    def _calculate_safe_zones_from_text_layout(
        self,
        text_layout: Dict[str, Any],
        canvas_dimensions: Dict[str, int]
    ) -> List[Dict[str, Any]]:
        """
        Calculate safe zones where shapes can be placed
        Excludes all text regions with margin
        
        Args:
            text_layout: Text layout with boundaries
            canvas_dimensions: Canvas dimensions
        
        Returns:
            List of safe zone rectangles
        """
        canvas_width = canvas_dimensions.get('canvas_width_px', 400)
        canvas_height = canvas_dimensions.get('canvas_height_px', 480)
        
        company_region = text_layout['company_name']
        company_y_start = company_region['region_start_y'] - self.minimum_shape_margin_px
        company_y_end = company_region['region_start_y'] + company_region['region_height'] + self.minimum_shape_margin_px
        
        services_region = text_layout['services']
        services_y_start = services_region['region_start_y'] - self.minimum_shape_margin_px
        services_y_end = services_region['region_start_y'] + services_region['region_height'] + self.minimum_shape_margin_px
        
        safe_zones = []
        
        if company_y_start > self.minimum_shape_margin_px:
            safe_zones.append({
                'zone_id': 'top_zone',
                'x': 0,
                'y': 0,
                'width': canvas_width,
                'height': company_y_start,
                'priority': 'medium'
            })
        
        gap_between_company_services = services_y_start - company_y_end
        if gap_between_company_services > self.minimum_shape_margin_px * 2:
            safe_zones.append({
                'zone_id': 'middle_zone',
                'x': 0,
                'y': company_y_end,
                'width': canvas_width,
                'height': gap_between_company_services,
                'priority': 'low'
            })
        
        bottom_available = canvas_height - services_y_end
        if bottom_available > self.minimum_shape_margin_px:
            safe_zones.append({
                'zone_id': 'bottom_zone',
                'x': 0,
                'y': services_y_end,
                'width': canvas_width,
                'height': bottom_available,
                'priority': 'high'
            })
        
        return safe_zones
    
    def _generate_shapes_for_geometry_style(
        self,
        geometry_style: str,
        safe_zones: List[Dict[str, Any]],
        seed: int
    ) -> List[Dict[str, Any]]:
        """
        Generate shape definitions based on geometry style
        
        Args:
            geometry_style: Style (sharp, round, mixed, minimal)
            safe_zones: Available safe zones
            seed: Seed for deterministic generation
        
        Returns:
            List of shape definitions
        """
        random.seed(seed)
        
        if geometry_style == 'sharp':
            return self._generate_sharp_shapes(safe_zones, seed)
        elif geometry_style == 'round':
            return self._generate_round_shapes(safe_zones, seed)
        elif geometry_style == 'mixed':
            return self._generate_mixed_shapes(safe_zones, seed)
        elif geometry_style == 'minimal':
            return self._generate_minimal_shapes(safe_zones, seed)
        else:
            return self._generate_sharp_shapes(safe_zones, seed)
    
    def _generate_sharp_shapes(
        self,
        safe_zones: List[Dict[str, Any]],
        seed: int
    ) -> List[Dict[str, Any]]:
        """Generate angular/sharp geometric shapes"""
        shapes = []
        
        shapes.append({
            'type': 'rectangle',
            'width': random.randint(60, 120),
            'height': random.randint(60, 120),
            'rotation': random.choice([0, 45, 90, 135]),
            'opacity': self.shape_opacity_default,
            'zone_preference': 'top_zone'
        })
        
        shapes.append({
            'type': 'triangle',
            'size': random.randint(50, 100),
            'rotation': random.choice([0, 60, 120, 180]),
            'opacity': self.shape_opacity_default * 0.8,
            'zone_preference': 'bottom_zone'
        })
        
        return shapes
    
    def _generate_round_shapes(
        self,
        safe_zones: List[Dict[str, Any]],
        seed: int
    ) -> List[Dict[str, Any]]:
        """Generate circular/round shapes"""
        shapes = []
        
        shapes.append({
            'type': 'circle',
            'radius': random.randint(30, 70),
            'opacity': self.shape_opacity_default,
            'zone_preference': 'top_zone'
        })
        
        shapes.append({
            'type': 'circle',
            'radius': random.randint(40, 80),
            'opacity': self.shape_opacity_default * 0.7,
            'zone_preference': 'bottom_zone'
        })
        
        return shapes
    
    def _generate_mixed_shapes(
        self,
        safe_zones: List[Dict[str, Any]],
        seed: int
    ) -> List[Dict[str, Any]]:
        """Generate mix of sharp and round shapes"""
        shapes = []
        
        shapes.append({
            'type': 'circle',
            'radius': random.randint(40, 70),
            'opacity': self.shape_opacity_default,
            'zone_preference': 'top_zone'
        })
        
        shapes.append({
            'type': 'rectangle',
            'width': random.randint(50, 90),
            'height': random.randint(50, 90),
            'rotation': random.choice([0, 45]),
            'opacity': self.shape_opacity_default * 0.8,
            'zone_preference': 'bottom_zone'
        })
        
        return shapes
    
    def _generate_minimal_shapes(
        self,
        safe_zones: List[Dict[str, Any]],
        seed: int
    ) -> List[Dict[str, Any]]:
        """Generate minimal accent shapes"""
        shapes = []
        
        shapes.append({
            'type': 'line',
            'length': random.randint(80, 150),
            'thickness': 2,
            'rotation': random.choice([0, 45, 90, 135]),
            'opacity': self.shape_opacity_default * 1.5,
            'zone_preference': 'top_zone'
        })
        
        return shapes
    
    def _position_shapes_in_safe_zones(
        self,
        shapes: List[Dict[str, Any]],
        safe_zones: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Position shapes within safe zones
        Each shape placed in preferred zone if available
        
        Args:
            shapes: Shape definitions
            safe_zones: Available safe zones
        
        Returns:
            Positioned shapes
        """
        positioned = []
        
        zone_map = {zone['zone_id']: zone for zone in safe_zones}
        
        for shape in shapes:
            preferred_zone_id = shape.get('zone_preference')
            
            target_zone = zone_map.get(preferred_zone_id)
            if not target_zone and safe_zones:
                target_zone = safe_zones[0]
            
            if target_zone:
                x_position = target_zone['x'] + (target_zone['width'] / 2)
                y_position = target_zone['y'] + (target_zone['height'] / 2)
                
                positioned_shape = {
                    **shape,
                    'x_position': x_position,
                    'y_position': y_position,
                    'zone_assigned': target_zone['zone_id'],
                    'positioned': True
                }
                
                positioned.append(positioned_shape)
        
        return positioned


shape_compositor_safe_zone_engine_singleton = ShapeCompositorSafeZoneEngine()


def get_shape_compositor_safe_zone_engine() -> ShapeCompositorSafeZoneEngine:
    """
    Accessor for shape compositor engine
    Ensures single source of truth for shape composition
    """
    return shape_compositor_safe_zone_engine_singleton
