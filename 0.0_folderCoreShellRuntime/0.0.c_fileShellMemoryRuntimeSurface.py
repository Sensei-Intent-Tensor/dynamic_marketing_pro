#!/usr/bin/env python3
"""
0.0.c_fileShellMemoryRuntimeSurface.py

SHELL MEMORY RUNTIME SURFACE
Active runtime state tracking and execution memory
Real-time operational surface for intent execution

PRINCIPLE: This is the living memory - current execution context
All active state lives here during runtime
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import traceback


class ShellMemoryRuntimeSurface:
    """
    Real-time runtime state and execution surface
    Tracks active intents, execution paths, and system state
    """
    
    def __init__(self):
        self.active_intent_key_current = None
        self.authenticated_user_session_current = None
        self.execution_path_history_stack = []
        self.last_render_state_snapshot = {}
        self.current_selection_hierarchy_path = []
        self.runtime_initialization_timestamp = datetime.now().isoformat()
        self.total_intents_executed_count = 0
        self.failed_intents_log = []
    
    def set_active_intent_execution(
        self,
        intent_key: str,
        execution_payload: Any
    ) -> None:
        """
        Set currently executing intent
        Updates runtime surface to reflect active operation
        
        Args:
            intent_key: Intent glyph being executed
            execution_payload: Data being passed to intent
        """
        self.active_intent_key_current = intent_key
        
        execution_record = {
            'intent_key': intent_key,
            'timestamp': datetime.now().isoformat(),
            'payload': execution_payload,
            'stack_trace': traceback.format_stack()
        }
        
        self.execution_path_history_stack.append(execution_record)
        self.total_intents_executed_count += 1
    
    def clear_active_intent_execution(self) -> None:
        """
        Clear active intent after execution completes
        Resets runtime surface to neutral state
        """
        self.active_intent_key_current = None
    
    def log_intent_execution_failure(
        self,
        intent_key: str,
        error_message: str,
        error_traceback: str
    ) -> None:
        """
        Log failed intent execution
        CRITICAL: All failures must be recorded for audit
        
        Args:
            intent_key: Intent that failed
            error_message: Error description
            error_traceback: Full stack trace
        """
        failure_record = {
            'intent_key': intent_key,
            'timestamp': datetime.now().isoformat(),
            'error_message': error_message,
            'traceback': error_traceback,
            'user_session': self.authenticated_user_session_current
        }
        
        self.failed_intents_log.append(failure_record)
    
    def set_authenticated_user_session(
        self,
        user_object: Dict[str, Any]
    ) -> None:
        """
        Set authenticated user for current session
        
        Args:
            user_object: Validated user data from auth gatekeeper
        """
        self.authenticated_user_session_current = {
            'user_id': user_object.get('user_id'),
            'email': user_object.get('email'),
            'subscription_tier': user_object.get('subscription_tier'),
            'authenticated_at': datetime.now().isoformat()
        }
    
    def clear_authenticated_user_session(self) -> None:
        """
        Clear user session (logout or session end)
        """
        self.authenticated_user_session_current = None
    
    def get_current_user_id(self) -> Optional[str]:
        """
        Get current authenticated user ID
        
        Returns:
            User ID or None if not authenticated
        """
        if self.authenticated_user_session_current:
            return self.authenticated_user_session_current.get('user_id')
        return None
    
    def update_render_state_snapshot(
        self,
        state_snapshot: Dict[str, Any]
    ) -> None:
        """
        Update last render state snapshot
        Used for state diffing and debugging
        
        Args:
            state_snapshot: Current render state
        """
        self.last_render_state_snapshot = {
            'timestamp': datetime.now().isoformat(),
            'state': state_snapshot
        }
    
    def get_execution_history_last_n(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        Get last N executed intents
        
        Args:
            n: Number of history entries to retrieve
        
        Returns:
            List of execution records
        """
        return self.execution_path_history_stack[-n:]
    
    def get_runtime_statistics(self) -> Dict[str, Any]:
        """
        Get runtime statistics
        
        Returns:
            Current runtime stats
        """
        return {
            'runtime_initialized_at': self.runtime_initialization_timestamp,
            'total_intents_executed': self.total_intents_executed_count,
            'failed_intents_count': len(self.failed_intents_log),
            'active_intent_current': self.active_intent_key_current,
            'authenticated_user': self.get_current_user_id(),
            'execution_history_length': len(self.execution_path_history_stack)
        }
    
    def export_runtime_state_as_json(self) -> Dict[str, Any]:
        """
        Export complete runtime state
        Used for debugging and state inspection
        """
        return {
            'statistics': self.get_runtime_statistics(),
            'active_session': self.authenticated_user_session_current,
            'recent_executions': self.get_execution_history_last_n(20),
            'recent_failures': self.failed_intents_log[-10:],
            'last_render_snapshot': self.last_render_state_snapshot
        }


shell_memory_runtime_surface_singleton = ShellMemoryRuntimeSurface()


def get_shell_memory_runtime_surface() -> ShellMemoryRuntimeSurface:
    """
    Accessor for shell runtime memory
    Ensures single source of truth for runtime state
    """
    return shell_memory_runtime_surface_singleton
