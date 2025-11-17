#!/usr/bin/env python3
"""
4.0.b_fileParameterParserIntentResolver.py

PARAMETER PARSER INTENT RESOLVER
Parses URL parameters into normalized format for generation
Handles defaults, type conversion, and semantic enrichment

PRINCIPLE: URL → Normalized Parameters → Ready for Generation
Clean separation between HTTP layer and generation layer
All parameters have consistent types and defaults
"""

from typing import Dict, Any, List, Optional
import random


class ParameterParserIntentResolver:
    """
    URL parameter parser and resolver
    Converts raw URL params to generation-ready format
    """
    
    def __init__(self):
        self.default_seed_base = 0
        self.default_frame_count = 3
        self.default_company_name = 'Your Company'
        self.default_services = []
    
    def parse_parameters_for_generation_intent(
        self,
        writable_parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        CRITICAL: Parse writable parameters into generation format
        Normalizes types, applies defaults, enriches semantics
        
        Args:
            writable_parameters: Validated writable parameters
        
        Returns:
            Normalized parameters ready for generation
        """
        parsed_parameters = {}
        
        parsed_parameters['base_seed'] = self._parse_seed_parameter(
            writable_parameters.get('seed')
        )
        
        parsed_parameters['count'] = self._parse_count_parameter(
            writable_parameters.get('count')
        )
        
        parsed_parameters['company'] = self._parse_company_parameter(
            writable_parameters.get('company')
        )
        
        parsed_parameters['services'] = self._parse_services_parameter(
            writable_parameters.get('services')
        )
        
        parsed_parameters['color_primary'] = writable_parameters.get('bg')
        parsed_parameters['color_text'] = writable_parameters.get('text')
        parsed_parameters['color_accent'] = writable_parameters.get('accent')
        
        parsed_parameters['font_style'] = writable_parameters.get('font')
        parsed_parameters['geometry'] = writable_parameters.get('geometry')
        
        parsed_parameters['icon_category'] = writable_parameters.get('icon_category')
        parsed_parameters['decoration_style'] = writable_parameters.get('decoration')
        parsed_parameters['background_gradient'] = writable_parameters.get('background')
        
        parsed_parameters['random_mode'] = self._parse_random_mode_parameter(
            writable_parameters.get('random')
        )
        
        return parsed_parameters
    
    def _parse_seed_parameter(self, seed_value: Optional[Any]) -> int:
        """
        Parse seed parameter
        
        Args:
            seed_value: Raw seed value
        
        Returns:
            Normalized seed integer
        """
        if seed_value is None:
            return random.randint(0, 3145728)
        
        try:
            seed_int = int(seed_value)
            return abs(seed_int) % 3145728
        except (ValueError, TypeError):
            return random.randint(0, 3145728)
    
    def _parse_count_parameter(self, count_value: Optional[Any]) -> int:
        """
        Parse frame count parameter
        
        Args:
            count_value: Raw count value
        
        Returns:
            Normalized frame count
        """
        if count_value is None:
            return self.default_frame_count
        
        try:
            count_int = int(count_value)
            return max(1, min(100, count_int))
        except (ValueError, TypeError):
            return self.default_frame_count
    
    def _parse_company_parameter(self, company_value: Optional[str]) -> str:
        """
        Parse company name parameter
        
        Args:
            company_value: Raw company name
        
        Returns:
            Normalized company name
        """
        if not company_value or not isinstance(company_value, str):
            return self.default_company_name
        
        return company_value.strip()
    
    def _parse_services_parameter(self, services_value: Optional[Any]) -> List[str]:
        """
        Parse services parameter
        Handles both comma-separated string and list
        
        Args:
            services_value: Raw services value
        
        Returns:
            Normalized services list
        """
        if not services_value:
            return self.default_services
        
        if isinstance(services_value, str):
            services_list = [s.strip() for s in services_value.split(',') if s.strip()]
            return services_list
        
        elif isinstance(services_value, list):
            return [str(s).strip() for s in services_value if str(s).strip()]
        
        return self.default_services
    
    def _parse_random_mode_parameter(self, random_value: Optional[Any]) -> bool:
        """
        Parse random mode parameter
        
        Args:
            random_value: Raw random mode value
        
        Returns:
            Boolean random mode flag
        """
        if random_value is None:
            return False
        
        if isinstance(random_value, bool):
            return random_value
        
        if isinstance(random_value, str):
            return random_value.lower() in ['true', '1', 'yes', 'on']
        
        return bool(random_value)
    
    def extract_url_parameters_from_request_intent(
        self,
        request_args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract and normalize URL parameters from request
        
        Args:
            request_args: Flask request.args dict
        
        Returns:
            Extracted parameters
        """
        extracted = {}
        
        parameter_mappings = {
            'seed': ['seed', 's'],
            'count': ['count', 'c', 'frames'],
            'company': ['company', 'name', 'brand'],
            'services': ['services', 'service', 'offerings'],
            'bg': ['bg', 'background', 'bgcolor'],
            'text': ['text', 'textcolor', 'txt'],
            'accent': ['accent', 'accentcolor', 'highlight'],
            'font': ['font', 'fontStyle', 'typography'],
            'geometry': ['geometry', 'geo', 'shapes'],
            'icon_category': ['icon', 'icon_category', 'icons'],
            'decoration': ['decoration', 'deco', 'accent_style'],
            'background': ['background_gradient', 'gradient', 'bg_style'],
            'random': ['random', 'rand', 'auto']
        }
        
        for param_name, param_aliases in parameter_mappings.items():
            for alias in param_aliases:
                if alias in request_args:
                    extracted[param_name] = request_args[alias]
                    break
        
        return extracted
    
    def build_example_urls_intent(self) -> Dict[str, str]:
        """
        Build example URLs showing parameter usage
        Useful for documentation
        
        Returns:
            Dictionary of example URLs with descriptions
        """
        base_url = "http://localhost:5000/generate"
        
        examples = {
            'basic': f"{base_url}?count=3",
            'custom_company': f"{base_url}?company=TechCorp&services=AI,Cloud,Data",
            'custom_colors': f"{base_url}?bg=blue&text=white&accent=yellow",
            'custom_style': f"{base_url}?font=tech&geometry=sharp",
            'specific_seed': f"{base_url}?seed=12345&count=5",
            'random_mode': f"{base_url}?random=true&count=3",
            'complete_custom': f"{base_url}?company=Brand&services=A,B,C&bg=%231a4d7a&text=white&font=bold&geometry=sharp&count=5"
        }
        
        return examples


parameter_parser_intent_resolver_singleton = ParameterParserIntentResolver()


def get_parameter_parser_intent_resolver() -> ParameterParserIntentResolver:
    """
    Accessor for parameter parser
    Ensures single source of truth for parameter parsing
    """
    return parameter_parser_intent_resolver_singleton
