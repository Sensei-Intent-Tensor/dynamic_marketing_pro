#!/usr/bin/env python3
"""
2.0.f_fileParameterWritableValidatorIntentGate.py

PARAMETER WRITABLE VALIDATOR INTENT GATE
Implements "Writable Doctrine" for generation parameters
Only validated "writable" parameters proceed to generation

PRINCIPLE: Pre-execution validation prevents runtime errors
Invalid parameters rejected at gate with clear messaging
All rejections logged for audit
"""

from typing import Dict, Any, List, Tuple
import re


class ParameterWritableValidatorIntentGate:
    """
    Parameter validation gate implementing Writable Doctrine
    Ensures only valid parameters enter generation pipeline
    """
    
    def __init__(self):
        self.validation_failures_log = []
        self.total_validations_executed_count = 0
    
    def validate_parameters_as_writable_for_generation_intent(
        self,
        raw_parameters: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        CRITICAL: Validate all parameters before generation
        Only writable parameters proceed
        
        Args:
            raw_parameters: Raw user-provided parameters
            user_id: ID of requesting user
        
        Returns:
            Validation result with writable parameters or rejections
        """
        from typing import Optional
        
        self.total_validations_executed_count += 1
        
        validation_timestamp = datetime.now().isoformat()
        
        writable_parameters = {}
        validation_log = []
        
        if 'company' in raw_parameters:
            validation_result = self._validate_company_name_writable(
                raw_parameters['company']
            )
            if validation_result['writable']:
                writable_parameters['company'] = validation_result['validated_value']
                validation_log.append({
                    'parameter': 'company',
                    'status': 'WRITABLE',
                    'value': validation_result['validated_value']
                })
            else:
                validation_log.append({
                    'parameter': 'company',
                    'status': 'NON_WRITABLE',
                    'rejection_reason': validation_result['rejection_reason']
                })
        
        if 'services' in raw_parameters:
            validation_result = self._validate_services_list_writable(
                raw_parameters['services']
            )
            if validation_result['writable']:
                writable_parameters['services'] = validation_result['validated_value']
                validation_log.append({
                    'parameter': 'services',
                    'status': 'WRITABLE',
                    'value_count': len(validation_result['validated_value'])
                })
            else:
                validation_log.append({
                    'parameter': 'services',
                    'status': 'NON_WRITABLE',
                    'rejection_reason': validation_result['rejection_reason']
                })
        
        if 'count' in raw_parameters:
            validation_result = self._validate_frame_count_writable(
                raw_parameters['count']
            )
            if validation_result['writable']:
                writable_parameters['count'] = validation_result['validated_value']
                validation_log.append({
                    'parameter': 'count',
                    'status': 'WRITABLE',
                    'value': validation_result['validated_value']
                })
            else:
                validation_log.append({
                    'parameter': 'count',
                    'status': 'NON_WRITABLE',
                    'rejection_reason': validation_result['rejection_reason']
                })
        
        if 'bg' in raw_parameters:
            validation_result = self._validate_color_writable(
                raw_parameters['bg'], 'background'
            )
            if validation_result['writable']:
                writable_parameters['bg'] = validation_result['validated_value']
                validation_log.append({
                    'parameter': 'bg',
                    'status': 'WRITABLE',
                    'value': validation_result['validated_value']
                })
            else:
                validation_log.append({
                    'parameter': 'bg',
                    'status': 'NON_WRITABLE',
                    'rejection_reason': validation_result['rejection_reason']
                })
        
        if 'text' in raw_parameters:
            validation_result = self._validate_color_writable(
                raw_parameters['text'], 'text'
            )
            if validation_result['writable']:
                writable_parameters['text'] = validation_result['validated_value']
                validation_log.append({
                    'parameter': 'text',
                    'status': 'WRITABLE',
                    'value': validation_result['validated_value']
                })
            else:
                validation_log.append({
                    'parameter': 'text',
                    'status': 'NON_WRITABLE',
                    'rejection_reason': validation_result['rejection_reason']
                })
        
        if 'accent' in raw_parameters:
            validation_result = self._validate_color_writable(
                raw_parameters['accent'], 'accent'
            )
            if validation_result['writable']:
                writable_parameters['accent'] = validation_result['validated_value']
                validation_log.append({
                    'parameter': 'accent',
                    'status': 'WRITABLE',
                    'value': validation_result['validated_value']
                })
            else:
                validation_log.append({
                    'parameter': 'accent',
                    'status': 'NON_WRITABLE',
                    'rejection_reason': validation_result['rejection_reason']
                })
        
        if 'font' in raw_parameters:
            validation_result = self._validate_font_style_writable(
                raw_parameters['font']
            )
            if validation_result['writable']:
                writable_parameters['font'] = validation_result['validated_value']
                validation_log.append({
                    'parameter': 'font',
                    'status': 'WRITABLE',
                    'value': validation_result['validated_value']
                })
            else:
                validation_log.append({
                    'parameter': 'font',
                    'status': 'NON_WRITABLE',
                    'rejection_reason': validation_result['rejection_reason']
                })
        
        if 'geometry' in raw_parameters:
            validation_result = self._validate_geometry_style_writable(
                raw_parameters['geometry']
            )
            if validation_result['writable']:
                writable_parameters['geometry'] = validation_result['validated_value']
                validation_log.append({
                    'parameter': 'geometry',
                    'status': 'WRITABLE',
                    'value': validation_result['validated_value']
                })
            else:
                validation_log.append({
                    'parameter': 'geometry',
                    'status': 'NON_WRITABLE',
                    'rejection_reason': validation_result['rejection_reason']
                })
        
        non_writable_count = sum(
            1 for entry in validation_log if entry['status'] == 'NON_WRITABLE'
        )
        
        if non_writable_count > 0:
            self._log_validation_failures(
                user_id=user_id,
                raw_parameters=raw_parameters,
                validation_log=validation_log,
                timestamp=validation_timestamp
            )
        
        return {
            'writable_parameters': writable_parameters,
            'validation_log': validation_log,
            'total_parameters_submitted': len(raw_parameters),
            'writable_parameters_count': len(writable_parameters),
            'non_writable_parameters_count': non_writable_count,
            'validation_timestamp': validation_timestamp,
            'all_parameters_writable': non_writable_count == 0
        }
    
    def _validate_company_name_writable(
        self,
        company_name: str
    ) -> Dict[str, Any]:
        """
        Validate company name is writable
        
        Args:
            company_name: Company name to validate
        
        Returns:
            Validation result
        """
        if not isinstance(company_name, str):
            return {
                'writable': False,
                'rejection_reason': 'COMPANY_NAME_NOT_STRING',
                'validated_value': None
            }
        
        if len(company_name) == 0:
            return {
                'writable': False,
                'rejection_reason': 'COMPANY_NAME_EMPTY',
                'validated_value': None
            }
        
        if len(company_name) > 50:
            return {
                'writable': False,
                'rejection_reason': 'COMPANY_NAME_TOO_LONG',
                'validated_value': None
            }
        
        return {
            'writable': True,
            'rejection_reason': None,
            'validated_value': company_name.strip()
        }
    
    def _validate_services_list_writable(
        self,
        services: Any
    ) -> Dict[str, Any]:
        """
        Validate services list is writable
        
        Args:
            services: Services list to validate
        
        Returns:
            Validation result
        """
        if isinstance(services, str):
            services = [s.strip() for s in services.split(',') if s.strip()]
        
        if not isinstance(services, list):
            return {
                'writable': False,
                'rejection_reason': 'SERVICES_NOT_LIST',
                'validated_value': None
            }
        
        if len(services) > 10:
            return {
                'writable': False,
                'rejection_reason': 'SERVICES_LIST_TOO_LONG',
                'validated_value': None
            }
        
        validated_services = []
        for service in services:
            if isinstance(service, str) and len(service.strip()) > 0:
                if len(service) <= 100:
                    validated_services.append(service.strip())
        
        return {
            'writable': True,
            'rejection_reason': None,
            'validated_value': validated_services
        }
    
    def _validate_frame_count_writable(
        self,
        count: Any
    ) -> Dict[str, Any]:
        """
        Validate frame count is writable
        
        Args:
            count: Frame count to validate
        
        Returns:
            Validation result
        """
        try:
            count_int = int(count)
        except (ValueError, TypeError):
            return {
                'writable': False,
                'rejection_reason': 'FRAME_COUNT_NOT_INTEGER',
                'validated_value': None
            }
        
        if count_int < 1:
            return {
                'writable': False,
                'rejection_reason': 'FRAME_COUNT_TOO_LOW',
                'validated_value': None
            }
        
        if count_int > 100:
            return {
                'writable': False,
                'rejection_reason': 'FRAME_COUNT_TOO_HIGH',
                'validated_value': None
            }
        
        return {
            'writable': True,
            'rejection_reason': None,
            'validated_value': count_int
        }
    
    def _validate_color_writable(
        self,
        color: str,
        color_type: str
    ) -> Dict[str, Any]:
        """
        Validate color format is writable
        
        Args:
            color: Color value to validate
            color_type: Type of color (background, text, accent)
        
        Returns:
            Validation result
        """
        if not isinstance(color, str):
            return {
                'writable': False,
                'rejection_reason': f'{color_type.upper()}_COLOR_NOT_STRING',
                'validated_value': None
            }
        
        color_clean = color.strip().lower()
        
        valid_named_colors = [
            'white', 'black', 'red', 'green', 'blue',
            'yellow', 'cyan', 'magenta', 'gray', 'grey'
        ]
        
        if color_clean in valid_named_colors:
            return {
                'writable': True,
                'rejection_reason': None,
                'validated_value': color_clean
            }
        
        hex_pattern = re.compile(r'^#[0-9a-f]{6}$')
        if hex_pattern.match(color_clean):
            return {
                'writable': True,
                'rejection_reason': None,
                'validated_value': color_clean
            }
        
        return {
            'writable': False,
            'rejection_reason': f'{color_type.upper()}_COLOR_INVALID_FORMAT',
            'validated_value': None
        }
    
    def _validate_font_style_writable(
        self,
        font_style: str
    ) -> Dict[str, Any]:
        """
        Validate font style is writable
        
        Args:
            font_style: Font style to validate
        
        Returns:
            Validation result
        """
        valid_fonts = ['bold', 'tech', 'elegant', 'blocky', 'script']
        
        font_clean = font_style.strip().lower()
        
        if font_clean not in valid_fonts:
            return {
                'writable': False,
                'rejection_reason': 'FONT_STYLE_NOT_RECOGNIZED',
                'validated_value': None
            }
        
        return {
            'writable': True,
            'rejection_reason': None,
            'validated_value': font_clean
        }
    
    def _validate_geometry_style_writable(
        self,
        geometry: str
    ) -> Dict[str, Any]:
        """
        Validate geometry style is writable
        
        Args:
            geometry: Geometry style to validate
        
        Returns:
            Validation result
        """
        valid_geometries = ['sharp', 'round', 'mixed', 'minimal']
        
        geometry_clean = geometry.strip().lower()
        
        if geometry_clean not in valid_geometries:
            return {
                'writable': False,
                'rejection_reason': 'GEOMETRY_STYLE_NOT_RECOGNIZED',
                'validated_value': None
            }
        
        return {
            'writable': True,
            'rejection_reason': None,
            'validated_value': geometry_clean
        }
    
    def _log_validation_failures(
        self,
        user_id: Optional[str],
        raw_parameters: Dict[str, Any],
        validation_log: List[Dict[str, Any]],
        timestamp: str
    ) -> None:
        """
        Log validation failures for audit
        
        Args:
            user_id: User who submitted parameters
            raw_parameters: Raw parameters submitted
            validation_log: Complete validation log
            timestamp: Validation timestamp
        """
        from datetime import datetime
        from typing import Optional
        
        self.validation_failures_log.append({
            'timestamp': timestamp,
            'user_id': user_id,
            'raw_parameters': raw_parameters,
            'validation_log': validation_log
        })
        
        if len(self.validation_failures_log) > 500:
            self.validation_failures_log = self.validation_failures_log[-500:]


parameter_writable_validator_intent_gate_singleton = ParameterWritableValidatorIntentGate()


def get_parameter_writable_validator_intent_gate() -> ParameterWritableValidatorIntentGate:
    """
    Accessor for parameter validator gate
    Ensures single source of truth for parameter validation
    """
    return parameter_writable_validator_intent_gate_singleton
