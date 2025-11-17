#!/usr/bin/env python3
"""
3.0.a_fileDynamicLibraryIndexer.py

DYNAMIC LIBRARY INDEXER
Auto-discovers and indexes all assets in library folders
Scan once at startup, build complete searchable index

PRINCIPLE: Drop files → Auto-discovered → Immediately available
No code changes needed to add assets
File system IS the database
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import os


class DynamicLibraryIndexer:
    """
    Dynamic asset library indexer
    Automatically discovers and indexes all library assets
    """
    
    def __init__(self, libraries_base_path: str = 'libraries'):
        self.libraries_base_path = Path(libraries_base_path)
        self.indexed_assets_registry = {}
        self.indexing_timestamp = None
        self.total_assets_indexed_count = 0
    
    def index_all_library_assets_intent(self) -> Dict[str, Any]:
        """
        CRITICAL: Index all assets in library folders
        Walks directory tree, catalogs everything
        
        Returns:
            Complete indexed asset registry
        """
        from datetime import datetime
        
        self.indexing_timestamp = datetime.now().isoformat()
        
        self.indexed_assets_registry = {
            'fonts': self._index_fonts_library_intent(),
            'icons': self._index_icons_library_intent(),
            'decorations': self._index_decorations_library_intent(),
            'backgrounds': self._index_backgrounds_library_intent()
        }
        
        self.total_assets_indexed_count = self._count_total_indexed_assets()
        
        return {
            'indexed_assets': self.indexed_assets_registry,
            'indexing_timestamp': self.indexing_timestamp,
            'total_assets_indexed': self.total_assets_indexed_count,
            'categories_indexed': len(self.indexed_assets_registry)
        }
    
    def _index_fonts_library_intent(self) -> Dict[str, Any]:
        """
        Index all font style definitions
        
        Returns:
            Indexed fonts registry
        """
        fonts_path = self.libraries_base_path / 'fonts'
        
        if not fonts_path.exists():
            return {}
        
        fonts_registry = {}
        
        for font_file in fonts_path.glob('*.json'):
            font_key = font_file.stem
            
            try:
                with open(font_file, 'r') as f:
                    font_definition = json.load(f)
                
                fonts_registry[font_key] = {
                    'definition': font_definition,
                    'file_path': str(font_file),
                    'asset_type': 'FONT_STYLE_DEFINITION',
                    'indexed_successfully': True
                }
            except Exception as e:
                fonts_registry[font_key] = {
                    'definition': None,
                    'file_path': str(font_file),
                    'asset_type': 'FONT_STYLE_DEFINITION',
                    'indexed_successfully': False,
                    'error_message': str(e)
                }
        
        return fonts_registry
    
    def _index_icons_library_intent(self) -> Dict[str, Any]:
        """
        Index all icon SVG files with category structure
        
        Returns:
            Indexed icons registry with categories
        """
        icons_path = self.libraries_base_path / 'icons'
        
        if not icons_path.exists():
            return {}
        
        icons_registry = {}
        
        for category_folder in icons_path.iterdir():
            if category_folder.is_dir():
                category_name = category_folder.name
                icons_registry[category_name] = {}
                
                for icon_file in category_folder.glob('*.svg'):
                    icon_key = icon_file.stem
                    
                    try:
                        with open(icon_file, 'r') as f:
                            icon_svg_content = f.read()
                        
                        icon_metadata = self._extract_svg_metadata(icon_svg_content)
                        
                        icons_registry[category_name][icon_key] = {
                            'svg_content': icon_svg_content,
                            'file_path': str(icon_file),
                            'asset_type': 'ICON_SVG',
                            'category': category_name,
                            'metadata': icon_metadata,
                            'indexed_successfully': True
                        }
                    except Exception as e:
                        icons_registry[category_name][icon_key] = {
                            'svg_content': None,
                            'file_path': str(icon_file),
                            'asset_type': 'ICON_SVG',
                            'category': category_name,
                            'indexed_successfully': False,
                            'error_message': str(e)
                        }
        
        return icons_registry
    
    def _index_decorations_library_intent(self) -> Dict[str, Any]:
        """
        Index all decoration SVG files with style structure
        
        Returns:
            Indexed decorations registry
        """
        decorations_path = self.libraries_base_path / 'decorations'
        
        if not decorations_path.exists():
            return {}
        
        decorations_registry = {}
        
        for style_folder in decorations_path.iterdir():
            if style_folder.is_dir():
                style_name = style_folder.name
                decorations_registry[style_name] = {}
                
                for decoration_file in style_folder.glob('*.svg'):
                    decoration_key = decoration_file.stem
                    
                    try:
                        with open(decoration_file, 'r') as f:
                            decoration_svg_content = f.read()
                        
                        decoration_metadata = self._extract_svg_metadata(decoration_svg_content)
                        
                        decorations_registry[style_name][decoration_key] = {
                            'svg_content': decoration_svg_content,
                            'file_path': str(decoration_file),
                            'asset_type': 'DECORATION_SVG',
                            'style': style_name,
                            'metadata': decoration_metadata,
                            'indexed_successfully': True
                        }
                    except Exception as e:
                        decorations_registry[style_name][decoration_key] = {
                            'svg_content': None,
                            'file_path': str(decoration_file),
                            'asset_type': 'DECORATION_SVG',
                            'style': style_name,
                            'indexed_successfully': False,
                            'error_message': str(e)
                        }
        
        return decorations_registry
    
    def _index_backgrounds_library_intent(self) -> Dict[str, Any]:
        """
        Index all background gradient definitions
        
        Returns:
            Indexed backgrounds registry
        """
        backgrounds_path = self.libraries_base_path / 'backgrounds'
        
        if not backgrounds_path.exists():
            return {}
        
        backgrounds_registry = {}
        
        for background_file in backgrounds_path.glob('*.json'):
            background_key = background_file.stem
            
            try:
                with open(background_file, 'r') as f:
                    background_definition = json.load(f)
                
                backgrounds_registry[background_key] = {
                    'definition': background_definition,
                    'file_path': str(background_file),
                    'asset_type': 'GRADIENT_BACKGROUND_DEFINITION',
                    'indexed_successfully': True
                }
            except Exception as e:
                backgrounds_registry[background_key] = {
                    'definition': None,
                    'file_path': str(background_file),
                    'asset_type': 'GRADIENT_BACKGROUND_DEFINITION',
                    'indexed_successfully': False,
                    'error_message': str(e)
                }
        
        return backgrounds_registry
    
    def _extract_svg_metadata(self, svg_content: str) -> Dict[str, Any]:
        """
        Extract metadata from SVG content
        Looks for metadata tags in SVG
        
        Args:
            svg_content: SVG file content
        
        Returns:
            Extracted metadata or empty dict
        """
        import re
        
        metadata = {}
        
        intent_match = re.search(r'<intent_glyph>(.*?)</intent_glyph>', svg_content)
        if intent_match:
            metadata['intent_glyph'] = intent_match.group(1)
        
        tags_match = re.search(r'<semantic_tags>(.*?)</semantic_tags>', svg_content)
        if tags_match:
            metadata['semantic_tags'] = tags_match.group(1).split(',')
        
        industries_match = re.search(r'<optimal_industries>(.*?)</optimal_industries>', svg_content)
        if industries_match:
            metadata['optimal_industries'] = industries_match.group(1).split(',')
        
        return metadata
    
    def _count_total_indexed_assets(self) -> int:
        """
        Count total assets indexed across all categories
        
        Returns:
            Total asset count
        """
        total = 0
        
        total += len(self.indexed_assets_registry.get('fonts', {}))
        
        for category in self.indexed_assets_registry.get('icons', {}).values():
            total += len(category)
        
        for style in self.indexed_assets_registry.get('decorations', {}).values():
            total += len(style)
        
        total += len(self.indexed_assets_registry.get('backgrounds', {}))
        
        return total
    
    def get_asset_by_path_intent(
        self,
        asset_category: str,
        asset_path: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve asset by category and path
        
        Args:
            asset_category: Category (fonts, icons, decorations, backgrounds)
            asset_path: Path within category (e.g., 'tech/rocket' for icons)
        
        Returns:
            Asset data or None
        """
        if asset_category not in self.indexed_assets_registry:
            return None
        
        if asset_category in ['fonts', 'backgrounds']:
            return self.indexed_assets_registry[asset_category].get(asset_path)
        
        elif asset_category in ['icons', 'decorations']:
            path_parts = asset_path.split('/')
            if len(path_parts) == 2:
                category_or_style = path_parts[0]
                asset_name = path_parts[1]
                
                category_data = self.indexed_assets_registry[asset_category].get(category_or_style, {})
                return category_data.get(asset_name)
        
        return None
    
    def list_all_assets_in_category_intent(
        self,
        asset_category: str
    ) -> List[str]:
        """
        List all asset paths in a category
        
        Args:
            asset_category: Category to list
        
        Returns:
            List of asset path strings
        """
        if asset_category not in self.indexed_assets_registry:
            return []
        
        if asset_category in ['fonts', 'backgrounds']:
            return list(self.indexed_assets_registry[asset_category].keys())
        
        elif asset_category in ['icons', 'decorations']:
            paths = []
            for subcategory, assets in self.indexed_assets_registry[asset_category].items():
                for asset_name in assets.keys():
                    paths.append(f"{subcategory}/{asset_name}")
            return paths
        
        return []
    
    def get_indexing_statistics_intent(self) -> Dict[str, Any]:
        """
        Get indexing statistics
        
        Returns:
            Statistics about indexed assets
        """
        return {
            'total_assets_indexed': self.total_assets_indexed_count,
            'indexing_timestamp': self.indexing_timestamp,
            'categories': {
                'fonts': len(self.indexed_assets_registry.get('fonts', {})),
                'icons': sum(len(cat) for cat in self.indexed_assets_registry.get('icons', {}).values()),
                'decorations': sum(len(style) for style in self.indexed_assets_registry.get('decorations', {}).values()),
                'backgrounds': len(self.indexed_assets_registry.get('backgrounds', {}))
            },
            'libraries_base_path': str(self.libraries_base_path)
        }


dynamic_library_indexer_singleton = DynamicLibraryIndexer()


def get_dynamic_library_indexer() -> DynamicLibraryIndexer:
    """
    Accessor for dynamic library indexer
    Ensures single source of truth for asset indexing
    """
    return dynamic_library_indexer_singleton
