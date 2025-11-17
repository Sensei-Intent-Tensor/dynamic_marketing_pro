#!/usr/bin/env python3
"""
0.0.a_fileShellIndexTopology.py

GHOSTLESS CORE SHELL INDEX
Complete structural topology map of dynamic_marketing_pro application
Every folder, file, and intent glyph registered here

PRINCIPLE: This is the brain map. Nothing exists in the app without registration here.
"""

from typing import Dict, List, Any
from datetime import datetime


class ShellIndexTopology:
    """
    Central registry of all application structure
    Self-documenting architectural map
    Zero ambiguity - every node is intent-bound
    """
    
    def __init__(self):
        self.topology_map_intent_registry = self._build_topology_map_intent_registry()
        self.creation_timestamp_shell_index = datetime.now().isoformat()
        self.version_shell_topology = "1.0.0_diamond_standard"
    
    def _build_topology_map_intent_registry(self) -> Dict[str, Any]:
        """
        Build complete topology map
        Hierarchical structure mirrors file system exactly
        """
        return {
            '0.0_folderCoreShellRuntime': {
                'purpose_intent': 'CORE_RUNTIME_AUTHENTICATION_REGISTRY',
                'execution_order': 0,
                'files': {
                    '0.0.a_fileShellIndexTopology': {
                        'type': 'TOPOLOGY_REGISTRY_MAP',
                        'intent': 'Central structural map of entire application',
                        'exports': ['ShellIndexTopology']
                    },
                    '0.0.b_fileIntentGlossaryRegistry': {
                        'type': 'INTENT_FUNCTION_REGISTRY',
                        'intent': 'Complete registry of all intent glyphs and their metadata',
                        'exports': ['IntentGlossaryRegistry']
                    },
                    '0.0.c_fileShellMemoryRuntimeSurface': {
                        'type': 'RUNTIME_MEMORY_STATE',
                        'intent': 'Active runtime state and execution surface',
                        'exports': ['ShellMemoryRuntimeSurface']
                    },
                    '0.0.d_fileAuthenticationIntentGatekeeper': {
                        'type': 'SECURITY_AUTH_GATE',
                        'intent': 'Authentication validation - nothing executes without this',
                        'exports': ['AuthenticationIntentGatekeeper']
                    },
                    '0.0.e_fileSubscriptionValidatorIntentFirewall': {
                        'type': 'SECURITY_SUBSCRIPTION_FIREWALL',
                        'intent': 'Subscription tier validation and usage limits',
                        'exports': ['SubscriptionValidatorIntentFirewall']
                    }
                }
            },
            '1.0_folderLibrariesDynamicAssets': {
                'purpose_intent': 'DYNAMIC_ASSET_LIBRARY_REGISTRY',
                'execution_order': 1,
                'files': {}
            },
            '2.0_folderGenerationEngineCore': {
                'purpose_intent': 'FRAME_GENERATION_ENGINE_CORE',
                'execution_order': 2,
                'files': {}
            },
            '3.0_folderDynamicLibraryLoader': {
                'purpose_intent': 'ASSET_LOADER_INDEXER_ENGINE',
                'execution_order': 3,
                'files': {}
            },
            '4.0_folderServerIntentDispatcher': {
                'purpose_intent': 'HTTP_SERVER_REQUEST_DISPATCHER',
                'execution_order': 4,
                'files': {}
            },
            '5.0_folderContextualLoggingTrace': {
                'purpose_intent': 'LOGGING_TRACE_VALIDATION_SYSTEM',
                'execution_order': 5,
                'files': {}
            }
        }
    
    def get_file_intent_metadata(self, file_path_glyph: str) -> Dict[str, Any]:
        """
        Retrieve metadata for any file by its glyph path
        
        Args:
            file_path_glyph: e.g., '0.0.a_fileShellIndexTopology'
        
        Returns:
            Complete metadata for that file
        """
        for folder_name, folder_data in self.topology_map_intent_registry.items():
            if file_path_glyph in folder_data['files']:
                return folder_data['files'][file_path_glyph]
        
        return {}
    
    def validate_file_exists_in_topology(self, file_path_glyph: str) -> bool:
        """
        Validate that a file is registered in topology
        CRITICAL: Prevents execution of unregistered code
        """
        metadata = self.get_file_intent_metadata(file_path_glyph)
        return len(metadata) > 0
    
    def get_execution_order_sequence(self) -> List[str]:
        """
        Get folders in execution order
        Returns ordered list for initialization sequence
        """
        folders_with_order = [
            (name, data['execution_order']) 
            for name, data in self.topology_map_intent_registry.items()
        ]
        
        sorted_folders = sorted(folders_with_order, key=lambda x: x[1])
        
        return [folder[0] for folder in sorted_folders]
    
    def export_topology_as_json_intent(self) -> Dict[str, Any]:
        """
        Export complete topology map
        Used for documentation and external tooling
        """
        return {
            'version': self.version_shell_topology,
            'created': self.creation_timestamp_shell_index,
            'topology': self.topology_map_intent_registry
        }


shell_index_topology_singleton = ShellIndexTopology()


def get_shell_topology_registry() -> ShellIndexTopology:
    """
    Accessor for shell topology
    Ensures single source of truth
    """
    return shell_index_topology_singleton
