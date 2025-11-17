#!/usr/bin/env python3
"""
3.0.b_fileAssetPathResolver.py

ASSET PATH RESOLVER
Resolves user requests to actual asset paths
Handles partial matches, categories, and seed-based selection

PRINCIPLE: Flexible resolution without ambiguity
User can specify exact path or category
Seed-based selection when user doesn't specify
"""

from typing import Dict, Any, List, Optional, Tuple
import random


class AssetPathResolver:
    """
    Intelligent asset path resolution
    Maps user requests to actual assets
    """
    
    def __init__(self, library_indexer):
        self.library_indexer = library_indexer
    
    def resolve_font_asset_path_intent(
        self,
        font_style_request: Optional[str],
        seed: int
    ) -> Dict[str, Any]:
        """
        Resolve font style request to actual font asset
        
        Args:
            font_style_request: User-requested font style or None
            seed: Seed for deterministic selection if not specified
        
        Returns:
            Resolved font asset
        """
        if font_style_request:
            font_asset = self.library_indexer.get_asset_by_path_intent(
                asset_category='fonts',
                asset_path=font_style_request
            )
            
            if font_asset:
                return {
                    'font_key': font_style_request,
                    'font_asset': font_asset,
                    'resolution_source': 'USER_SPECIFIED',
                    'resolved_successfully': True
                }
        
        random.seed(seed)
        available_fonts = self.library_indexer.list_all_assets_in_category_intent('fonts')
        
        if not available_fonts:
            return {
                'font_key': None,
                'font_asset': None,
                'resolution_source': 'SEED_BASED',
                'resolved_successfully': False,
                'error': 'NO_FONTS_AVAILABLE'
            }
        
        selected_font = random.choice(available_fonts)
        font_asset = self.library_indexer.get_asset_by_path_intent(
            asset_category='fonts',
            asset_path=selected_font
        )
        
        return {
            'font_key': selected_font,
            'font_asset': font_asset,
            'resolution_source': 'SEED_BASED',
            'resolved_successfully': True
        }
    
    def resolve_icon_asset_path_intent(
        self,
        icon_category_request: Optional[str],
        seed: int
    ) -> Dict[str, Any]:
        """
        Resolve icon request to actual icon asset
        Handles category-level or specific icon requests
        
        Args:
            icon_category_request: Requested icon category or specific path
            seed: Seed for deterministic selection
        
        Returns:
            Resolved icon asset
        """
        all_icons = self.library_indexer.list_all_assets_in_category_intent('icons')
        
        if not all_icons:
            return {
                'icon_path': None,
                'icon_asset': None,
                'resolution_source': 'SEED_BASED',
                'resolved_successfully': False,
                'error': 'NO_ICONS_AVAILABLE'
            }
        
        if icon_category_request:
            category_icons = [
                icon for icon in all_icons 
                if icon.startswith(f"{icon_category_request}/")
            ]
            
            if category_icons:
                random.seed(seed)
                selected_icon = random.choice(category_icons)
                
                icon_asset = self.library_indexer.get_asset_by_path_intent(
                    asset_category='icons',
                    asset_path=selected_icon
                )
                
                return {
                    'icon_path': selected_icon,
                    'icon_asset': icon_asset,
                    'resolution_source': 'USER_CATEGORY_SEED_SELECTED',
                    'resolved_successfully': True
                }
        
        random.seed(seed)
        selected_icon = random.choice(all_icons)
        
        icon_asset = self.library_indexer.get_asset_by_path_intent(
            asset_category='icons',
            asset_path=selected_icon
        )
        
        return {
            'icon_path': selected_icon,
            'icon_asset': icon_asset,
            'resolution_source': 'SEED_BASED',
            'resolved_successfully': True
        }
    
    def resolve_decoration_asset_path_intent(
        self,
        decoration_style_request: Optional[str],
        seed: int
    ) -> Dict[str, Any]:
        """
        Resolve decoration request to actual decoration asset
        
        Args:
            decoration_style_request: Requested decoration style or path
            seed: Seed for deterministic selection
        
        Returns:
            Resolved decoration asset
        """
        all_decorations = self.library_indexer.list_all_assets_in_category_intent('decorations')
        
        if not all_decorations:
            return {
                'decoration_path': None,
                'decoration_asset': None,
                'resolution_source': 'SEED_BASED',
                'resolved_successfully': False,
                'error': 'NO_DECORATIONS_AVAILABLE'
            }
        
        if decoration_style_request:
            style_decorations = [
                dec for dec in all_decorations 
                if dec.startswith(f"{decoration_style_request}/")
            ]
            
            if style_decorations:
                random.seed(seed)
                selected_decoration = random.choice(style_decorations)
                
                decoration_asset = self.library_indexer.get_asset_by_path_intent(
                    asset_category='decorations',
                    asset_path=selected_decoration
                )
                
                return {
                    'decoration_path': selected_decoration,
                    'decoration_asset': decoration_asset,
                    'resolution_source': 'USER_STYLE_SEED_SELECTED',
                    'resolved_successfully': True
                }
        
        random.seed(seed)
        selected_decoration = random.choice(all_decorations)
        
        decoration_asset = self.library_indexer.get_asset_by_path_intent(
            asset_category='decorations',
            asset_path=selected_decoration
        )
        
        return {
            'decoration_path': selected_decoration,
            'decoration_asset': decoration_asset,
            'resolution_source': 'SEED_BASED',
            'resolved_successfully': True
        }
    
    def resolve_background_asset_path_intent(
        self,
        background_style_request: Optional[str],
        seed: int
    ) -> Dict[str, Any]:
        """
        Resolve background gradient request
        
        Args:
            background_style_request: Requested background style
            seed: Seed for deterministic selection
        
        Returns:
            Resolved background asset
        """
        if background_style_request:
            background_asset = self.library_indexer.get_asset_by_path_intent(
                asset_category='backgrounds',
                asset_path=background_style_request
            )
            
            if background_asset:
                return {
                    'background_key': background_style_request,
                    'background_asset': background_asset,
                    'resolution_source': 'USER_SPECIFIED',
                    'resolved_successfully': True
                }
        
        random.seed(seed)
        available_backgrounds = self.library_indexer.list_all_assets_in_category_intent('backgrounds')
        
        if not available_backgrounds:
            return {
                'background_key': None,
                'background_asset': None,
                'resolution_source': 'SEED_BASED',
                'resolved_successfully': False,
                'error': 'NO_BACKGROUNDS_AVAILABLE'
            }
        
        selected_background = random.choice(available_backgrounds)
        background_asset = self.library_indexer.get_asset_by_path_intent(
            asset_category='backgrounds',
            asset_path=selected_background
        )
        
        return {
            'background_key': selected_background,
            'background_asset': background_asset,
            'resolution_source': 'SEED_BASED',
            'resolved_successfully': True
        }
    
    def resolve_all_frame_assets_intent(
        self,
        user_parameters: Dict[str, Any],
        seed: int
    ) -> Dict[str, Any]:
        """
        Resolve all assets needed for frame generation
        One-shot resolution of all asset types
        
        Args:
            user_parameters: User-provided parameters
            seed: Seed for deterministic selection
        
        Returns:
            Complete resolved asset bundle
        """
        font_resolution = self.resolve_font_asset_path_intent(
            font_style_request=user_parameters.get('font'),
            seed=seed
        )
        
        icon_resolution = self.resolve_icon_asset_path_intent(
            icon_category_request=user_parameters.get('icon_category'),
            seed=seed + 1
        )
        
        decoration_resolution = self.resolve_decoration_asset_path_intent(
            decoration_style_request=user_parameters.get('decoration'),
            seed=seed + 2
        )
        
        background_resolution = self.resolve_background_asset_path_intent(
            background_style_request=user_parameters.get('background'),
            seed=seed + 3
        )
        
        return {
            'font': font_resolution,
            'icon': icon_resolution,
            'decoration': decoration_resolution,
            'background': background_resolution,
            'all_resolved_successfully': all([
                font_resolution['resolved_successfully'],
                icon_resolution['resolved_successfully'],
                decoration_resolution['resolved_successfully'],
                background_resolution['resolved_successfully']
            ])
        }
    
    def search_assets_by_semantic_tags_intent(
        self,
        search_tags: List[str],
        asset_category: str
    ) -> List[Dict[str, Any]]:
        """
        Search assets by semantic tags
        Enables intelligent asset discovery
        
        Args:
            search_tags: Tags to search for
            asset_category: Category to search in
        
        Returns:
            List of matching assets
        """
        matching_assets = []
        
        all_asset_paths = self.library_indexer.list_all_assets_in_category_intent(asset_category)
        
        for asset_path in all_asset_paths:
            asset = self.library_indexer.get_asset_by_path_intent(asset_category, asset_path)
            
            if not asset or not asset.get('indexed_successfully'):
                continue
            
            asset_metadata = asset.get('metadata', {})
            asset_tags = asset_metadata.get('semantic_tags', [])
            
            tags_match = any(tag.lower() in [t.lower().strip() for t in asset_tags] for tag in search_tags)
            
            if tags_match:
                matching_assets.append({
                    'asset_path': asset_path,
                    'asset_data': asset,
                    'matched_tags': [tag for tag in search_tags if tag.lower() in [t.lower().strip() for t in asset_tags]]
                })
        
        return matching_assets


def create_asset_path_resolver(library_indexer) -> AssetPathResolver:
    """
    Factory function to create asset path resolver
    
    Args:
        library_indexer: Initialized library indexer instance
    
    Returns:
        Configured asset path resolver
    """
    return AssetPathResolver(library_indexer)
