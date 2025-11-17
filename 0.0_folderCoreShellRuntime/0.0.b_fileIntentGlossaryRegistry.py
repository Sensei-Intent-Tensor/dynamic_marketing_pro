#!/usr/bin/env python3
"""
0.0.b_fileIntentGlossaryRegistry.py

INTENT GLOSSARY REGISTRY
Complete registry of every executable intent glyph in the system
Every function, handler, and operation is registered here

PRINCIPLE: No intent executes without registration
This is the nervous system - signals cannot fire without being mapped here
"""

from typing import Dict, List, Any, Callable
from datetime import datetime


class IntentGlossaryRegistry:
    """
    Central registry of all intent glyphs
    Maps intent keys to their metadata and execution contracts
    """
    
    def __init__(self):
        self.intent_registry_map = self._build_intent_registry_map()
        self.creation_timestamp_glossary = datetime.now().isoformat()
        self.version_intent_glossary = "1.0.0_diamond_standard"
    
    def _build_intent_registry_map(self) -> Dict[str, Dict[str, Any]]:
        """
        Build complete intent registry
        Every intent glyph with its execution contract
        """
        return {
            # 0.0 LEVEL - CORE SHELL RUNTIME INTENTS
            'validateAuthenticationTokenIntent': {
                'type': 'SECURITY_VALIDATION_AUTH',
                'input_contract': {
                    'auth_token': 'str',
                    'request_headers': 'dict'
                },
                'output_contract': {
                    'authenticated_user_object': 'dict or None',
                    'validation_status': 'bool'
                },
                'execution_file': '0.0.d_fileAuthenticationIntentGatekeeper',
                'security_level': 'CRITICAL',
                'must_execute_before': ['ALL_OTHER_INTENTS']
            },
            
            'validateSubscriptionTierAccessIntent': {
                'type': 'SECURITY_VALIDATION_SUBSCRIPTION',
                'input_contract': {
                    'user_id': 'str',
                    'requested_operation': 'str',
                    'usage_count_current_period': 'int'
                },
                'output_contract': {
                    'access_granted': 'bool',
                    'tier_name': 'str',
                    'usage_remaining': 'int'
                },
                'execution_file': '0.0.e_fileSubscriptionValidatorIntentFirewall',
                'security_level': 'CRITICAL',
                'must_execute_before': ['generateFrameIntentFromSeed']
            },
            
            'logIntentExecutionWithContextIntent': {
                'type': 'LOGGING_CONTEXTUAL_TRACE',
                'input_contract': {
                    'intent_key': 'str',
                    'payload': 'any',
                    'outcome': 'str',
                    'timestamp': 'str'
                },
                'output_contract': {
                    'log_entry': 'dict',
                    'log_persisted': 'bool'
                },
                'execution_file': '5.0.a_fileIntentExecutionTraceLogger',
                'security_level': 'AUDIT',
                'executes_alongside': ['ALL_INTENTS']
            },
            
            'validateShellIntegrityAgainstGhostCodeIntent': {
                'type': 'SECURITY_INTEGRITY_VALIDATION',
                'input_contract': {
                    'code_snapshot': 'dict',
                    'expected_glyph_patterns': 'list'
                },
                'output_contract': {
                    'integrity_status': 'bool',
                    'violations_detected': 'list',
                    'ghost_code_found': 'list'
                },
                'execution_file': '5.0.b_fileShellIntegrityValidator',
                'security_level': 'CRITICAL',
                'execution_frequency': 'ON_DEPLOY_AND_PERIODIC'
            }
        }
    
    def register_new_intent_glyph(
        self,
        intent_key: str,
        intent_metadata: Dict[str, Any]
    ) -> bool:
        """
        Register a new intent glyph in the registry
        
        Args:
            intent_key: Unique intent identifier (ghostless glyph)
            intent_metadata: Complete execution contract
        
        Returns:
            bool: Registration success status
        """
        if intent_key in self.intent_registry_map:
            raise IntentRegistryCollisionError(
                f"Intent glyph '{intent_key}' already registered. "
                f"Ghostless principle: One intent = one glyph. No collisions allowed."
            )
        
        required_fields = [
            'type', 
            'input_contract', 
            'output_contract', 
            'execution_file'
        ]
        
        for field in required_fields:
            if field not in intent_metadata:
                raise IntentRegistryValidationError(
                    f"Intent metadata missing required field: {field}"
                )
        
        self.intent_registry_map[intent_key] = intent_metadata
        return True
    
    def get_intent_metadata(self, intent_key: str) -> Dict[str, Any]:
        """
        Retrieve complete metadata for an intent glyph
        
        Args:
            intent_key: Intent glyph to lookup
        
        Returns:
            Complete intent metadata or empty dict
        """
        return self.intent_registry_map.get(intent_key, {})
    
    def validate_intent_exists(self, intent_key: str) -> bool:
        """
        Validate that intent is registered
        CRITICAL: Blocks execution of unregistered intents
        """
        return intent_key in self.intent_registry_map
    
    def get_intents_by_security_level(self, security_level: str) -> List[str]:
        """
        Get all intents matching a security level
        
        Args:
            security_level: CRITICAL | AUDIT | STANDARD
        
        Returns:
            List of intent keys at that security level
        """
        return [
            intent_key 
            for intent_key, metadata in self.intent_registry_map.items()
            if metadata.get('security_level') == security_level
        ]
    
    def get_intents_by_type(self, intent_type: str) -> List[str]:
        """
        Get all intents of a specific type
        
        Args:
            intent_type: e.g., SECURITY_VALIDATION_AUTH, RENDER_INTENT
        
        Returns:
            List of intent keys of that type
        """
        return [
            intent_key 
            for intent_key, metadata in self.intent_registry_map.items()
            if metadata.get('type') == intent_type
        ]
    
    def export_glossary_as_json_intent(self) -> Dict[str, Any]:
        """
        Export complete glossary
        Used for documentation and external tooling
        """
        return {
            'version': self.version_intent_glossary,
            'created': self.creation_timestamp_glossary,
            'total_intents_registered': len(self.intent_registry_map),
            'glossary': self.intent_registry_map
        }


class IntentRegistryCollisionError(Exception):
    """Raised when attempting to register duplicate intent glyph"""
    pass


class IntentRegistryValidationError(Exception):
    """Raised when intent metadata fails validation"""
    pass


intent_glossary_registry_singleton = IntentGlossaryRegistry()


def get_intent_glossary_registry() -> IntentGlossaryRegistry:
    """
    Accessor for intent glossary
    Ensures single source of truth for all intents
    """
    return intent_glossary_registry_singleton
