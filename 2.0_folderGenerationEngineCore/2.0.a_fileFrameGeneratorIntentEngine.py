#!/usr/bin/env python3
"""
2.0.a_fileFrameGeneratorIntentEngine.py

FRAME GENERATOR INTENT ENGINE
Core orchestrator for generating marketing frames from seed and parameters
Coordinates all generation layers with strict precedence rules

PRINCIPLE: Deterministic generation from seed + user intent
Every frame is reproducible from its seed
User parameters ALWAYS override seed-based generation
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib
import random


class FrameGeneratorIntentEngine:
    """
    Core frame generation engine
    Orchestrates generation from seed through all layers
    """
    
    def __init__(self):
        self.total_frames_generated_count = 0
        self.frame_generation_history_log = []
        self.seed_range_maximum = 3145728  # 3.1M+ frame space
    
    def generate_frame_from_seed_and_parameters_intent(
        self,
        frame_seed: int,
        user_parameters: Dict[str, Any],
        authenticated_user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        CRITICAL: Generate complete marketing frame
        
        Args:
            frame_seed: Deterministic seed (0 to 3145728)
            user_parameters: User-provided overrides
            authenticated_user_id: ID of requesting user
        
        Returns:
            Complete frame specification ready for rendering
        """
        generation_timestamp = datetime.now().isoformat()
        
        frame_seed_normalized = self._normalize_seed_to_valid_range(frame_seed)
        
        random.seed(frame_seed_normalized)
        
        base_frame_structure = self._generate_base_frame_structure_intent(
            seed=frame_seed_normalized
        )
        
        seed_generated_defaults = self._generate_seed_based_defaults_intent(
            seed=frame_seed_normalized
        )
        
        resolved_parameters = self._resolve_parameters_with_precedence_intent(
            user_parameters=user_parameters,
            seed_defaults=seed_generated_defaults
        )
        
        frame_specification = {
            'frame_id': self._generate_frame_id_from_seed(frame_seed_normalized),
            'seed': frame_seed_normalized,
            'generation_timestamp': generation_timestamp,
            'authenticated_user_id': authenticated_user_id,
            'base_structure': base_frame_structure,
            'resolved_parameters': resolved_parameters,
            'generation_metadata': {
                'user_override_count': len(user_parameters),
                'seed_default_count': len(seed_generated_defaults),
                'precedence_applied': True
            }
        }
        
        self._log_frame_generation(frame_specification)
        self.total_frames_generated_count += 1
        
        return frame_specification
    
    def _generate_base_frame_structure_intent(
        self,
        seed: int
    ) -> Dict[str, Any]:
        """
        Generate base frame structure from seed
        Dimensions, viewBox, canvas properties
        
        Args:
            seed: Normalized seed value
        
        Returns:
            Base structure specification
        """
        return {
            'canvas_width_px': 400,
            'canvas_height_px': 480,
            'viewbox_definition': '0 0 400 480',
            'aspect_ratio': '5:6',
            'dpi_resolution': 72,
            'color_space': 'sRGB'
        }
    
    def _generate_seed_based_defaults_intent(
        self,
        seed: int
    ) -> Dict[str, Any]:
        """
        Generate default parameters from seed
        These are BASELINE - user params override
        
        Args:
            seed: Normalized seed value
        
        Returns:
            Seed-based default parameters
        """
        random.seed(seed)
        
        geometry_options = ['sharp', 'round', 'mixed', 'minimal']
        font_options = ['bold', 'tech', 'elegant', 'blocky', 'script']
        
        color_primary_options = [
            '#1a4d7a',  # Professional blue
            '#2c5f2d',  # Business green
            '#7a1a1a',  # Corporate red
            '#4a4a4a',  # Neutral gray
            '#1a3a52'   # Deep blue
        ]
        
        color_accent_options = [
            '#ffffff',  # White
            '#f0f0f0',  # Light gray
            '#ffd700',  # Gold
            '#ff6b35',  # Orange
            '#4ecdc4'   # Teal
        ]
        
        return {
            'geometry': random.choice(geometry_options),
            'font_style': random.choice(font_options),
            'color_primary': random.choice(color_primary_options),
            'color_accent': random.choice(color_accent_options),
            'color_text': '#ffffff',
            'icon_category': random.choice(['tech', 'business', 'nature']),
            'decoration_style': random.choice(['tech_corner', 'elegant_corner', 'grid_pattern']),
            'background_gradient': random.choice(['vertical', 'radial', 'diagonal'])
        }
    
    def _resolve_parameters_with_precedence_intent(
        self,
        user_parameters: Dict[str, Any],
        seed_defaults: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        CRITICAL: Resolve parameters using precedence
        User > Seed > System default
        
        Args:
            user_parameters: User-provided overrides
            seed_defaults: Seed-generated defaults
        
        Returns:
            Resolved parameters with precedence applied
        """
        resolved = {}
        
        all_parameter_keys = set(seed_defaults.keys()) | set(user_parameters.keys())
        
        for param_key in all_parameter_keys:
            if param_key in user_parameters and user_parameters[param_key] is not None:
                resolved[param_key] = user_parameters[param_key]
                resolved[f'{param_key}_source'] = 'USER_OVERRIDE'
            elif param_key in seed_defaults:
                resolved[param_key] = seed_defaults[param_key]
                resolved[f'{param_key}_source'] = 'SEED_GENERATED'
            else:
                resolved[param_key] = self._get_system_default_for_parameter(param_key)
                resolved[f'{param_key}_source'] = 'SYSTEM_DEFAULT'
        
        return resolved
    
    def _get_system_default_for_parameter(self, param_key: str) -> Any:
        """
        Get system-level default for parameter
        Last resort fallback
        
        Args:
            param_key: Parameter to get default for
        
        Returns:
            System default value
        """
        system_defaults = {
            'geometry': 'sharp',
            'font_style': 'bold',
            'color_primary': '#1a4d7a',
            'color_accent': '#ffffff',
            'color_text': '#ffffff',
            'icon_category': 'tech',
            'decoration_style': 'tech_corner',
            'background_gradient': 'vertical',
            'company_name': 'Your Company',
            'services': []
        }
        
        return system_defaults.get(param_key, None)
    
    def _normalize_seed_to_valid_range(self, seed: int) -> int:
        """
        Normalize seed to valid range (0 to 3145728)
        
        Args:
            seed: Input seed
        
        Returns:
            Normalized seed
        """
        return abs(seed) % self.seed_range_maximum
    
    def _generate_frame_id_from_seed(self, seed: int) -> str:
        """
        Generate unique frame ID from seed
        
        Args:
            seed: Frame seed
        
        Returns:
            Unique frame identifier
        """
        seed_hash = hashlib.sha256(str(seed).encode()).hexdigest()[:16]
        return f"frame_{seed}_{seed_hash}"
    
    def _log_frame_generation(self, frame_spec: Dict[str, Any]) -> None:
        """
        Log frame generation for audit trail
        
        Args:
            frame_spec: Generated frame specification
        """
        self.frame_generation_history_log.append({
            'frame_id': frame_spec['frame_id'],
            'seed': frame_spec['seed'],
            'timestamp': frame_spec['generation_timestamp'],
            'user_id': frame_spec['authenticated_user_id'],
            'user_override_count': frame_spec['generation_metadata']['user_override_count']
        })
        
        if len(self.frame_generation_history_log) > 1000:
            self.frame_generation_history_log = self.frame_generation_history_log[-1000:]
    
    def get_generation_statistics(self) -> Dict[str, Any]:
        """
        Get generation statistics
        
        Returns:
            Statistics about frame generation
        """
        return {
            'total_frames_generated': self.total_frames_generated_count,
            'seed_range_maximum': self.seed_range_maximum,
            'recent_generations': len(self.frame_generation_history_log),
            'recent_generation_log': self.frame_generation_history_log[-10:]
        }


frame_generator_intent_engine_singleton = FrameGeneratorIntentEngine()


def get_frame_generator_intent_engine() -> FrameGeneratorIntentEngine:
    """
    Accessor for frame generator engine
    Ensures single source of truth for frame generation
    """
    return frame_generator_intent_engine_singleton
