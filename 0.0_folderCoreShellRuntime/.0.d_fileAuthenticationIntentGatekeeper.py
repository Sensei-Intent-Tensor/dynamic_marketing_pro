#!/usr/bin/env python3
"""
0.0.d_fileAuthenticationIntentGatekeeper.py

AUTHENTICATION INTENT GATEKEEPER
Critical security layer - nothing executes without passing through here
All requests must present valid authentication before any intent fires

PRINCIPLE: Zero-trust architecture
No operation proceeds without validated authentication token
This is the fortress gate - unauthorized access is impossible
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import hashlib
import secrets


class AuthenticationIntentGatekeeper:
    """
    Authentication validation firewall
    First line of defense - all requests pass through here
    """
    
    def __init__(self):
        self.active_session_tokens_registry = {}
        self.failed_authentication_attempts_log = []
        self.token_expiry_duration_hours = 24
    
    def validate_authentication_token_intent(
        self,
        auth_token: str,
        request_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        CRITICAL: Validate authentication token before ANY execution
        
        Args:
            auth_token: Bearer token from request header
            request_metadata: Request context (IP, user-agent, etc.)
        
        Returns:
            Validation result with user object or rejection
        """
        validation_timestamp = datetime.now().isoformat()
        
        if not auth_token:
            self._log_failed_authentication_attempt(
                reason='NO_TOKEN_PROVIDED',
                request_metadata=request_metadata,
                timestamp=validation_timestamp
            )
            return {
                'authenticated': False,
                'user_object': None,
                'rejection_reason': 'NO_AUTH_TOKEN_PROVIDED',
                'timestamp': validation_timestamp
            }
        
        token_validation_result = self._validate_token_against_registry(auth_token)
        
        if not token_validation_result['valid']:
            self._log_failed_authentication_attempt(
                reason=token_validation_result['rejection_reason'],
                request_metadata=request_metadata,
                timestamp=validation_timestamp
            )
            return {
                'authenticated': False,
                'user_object': None,
                'rejection_reason': token_validation_result['rejection_reason'],
                'timestamp': validation_timestamp
            }
        
        user_object = token_validation_result['user_object']
        
        return {
            'authenticated': True,
            'user_object': user_object,
            'rejection_reason': None,
            'timestamp': validation_timestamp
        }
    
    def _validate_token_against_registry(
        self,
        auth_token: str
    ) -> Dict[str, Any]:
        """
        Internal validation of token against active sessions
        
        Args:
            auth_token: Token to validate
        
        Returns:
            Validation result
        """
        if auth_token not in self.active_session_tokens_registry:
            return {
                'valid': False,
                'rejection_reason': 'TOKEN_NOT_FOUND_IN_REGISTRY',
                'user_object': None
            }
        
        session_data = self.active_session_tokens_registry[auth_token]
        
        token_expiry_timestamp = datetime.fromisoformat(
            session_data['expiry_timestamp']
        )
        
        if datetime.now() > token_expiry_timestamp:
            del self.active_session_tokens_registry[auth_token]
            return {
                'valid': False,
                'rejection_reason': 'TOKEN_EXPIRED',
                'user_object': None
            }
        
        return {
            'valid': True,
            'rejection_reason': None,
            'user_object': session_data['user_object']
        }
    
    def create_authenticated_session_token_intent(
        self,
        user_object: Dict[str, Any]
    ) -> str:
        """
        Create new authentication token for validated user
        Called after successful login validation
        
        Args:
            user_object: Validated user data from login
        
        Returns:
            New authentication token
        """
        auth_token = self._generate_secure_token()
        
        expiry_timestamp = (
            datetime.now() + timedelta(hours=self.token_expiry_duration_hours)
        ).isoformat()
        
        self.active_session_tokens_registry[auth_token] = {
            'user_object': user_object,
            'created_timestamp': datetime.now().isoformat(),
            'expiry_timestamp': expiry_timestamp,
            'token_hash': self._hash_token(auth_token)
        }
        
        return auth_token
    
    def revoke_authentication_token_intent(
        self,
        auth_token: str
    ) -> bool:
        """
        Revoke authentication token (logout)
        
        Args:
            auth_token: Token to revoke
        
        Returns:
            Success status
        """
        if auth_token in self.active_session_tokens_registry:
            del self.active_session_tokens_registry[auth_token]
            return True
        return False
    
    def _generate_secure_token(self) -> str:
        """
        Generate cryptographically secure token
        
        Returns:
            Secure random token
        """
        return secrets.token_urlsafe(64)
    
    def _hash_token(self, token: str) -> str:
        """
        Hash token for logging (never log raw tokens)
        
        Args:
            token: Token to hash
        
        Returns:
            SHA256 hash of token
        """
        return hashlib.sha256(token.encode()).hexdigest()
    
    def _log_failed_authentication_attempt(
        self,
        reason: str,
        request_metadata: Dict[str, Any],
        timestamp: str
    ) -> None:
        """
        Log failed authentication attempt
        CRITICAL: All auth failures must be logged for security audit
        
        Args:
            reason: Rejection reason
            request_metadata: Request context
            timestamp: Attempt timestamp
        """
        self.failed_authentication_attempts_log.append({
            'timestamp': timestamp,
            'rejection_reason': reason,
            'ip_address': request_metadata.get('ip_address'),
            'user_agent': request_metadata.get('user_agent'),
            'request_path': request_metadata.get('request_path')
        })
    
    def get_active_sessions_count(self) -> int:
        """
        Get count of active authenticated sessions
        
        Returns:
            Number of active sessions
        """
        return len(self.active_session_tokens_registry)
    
    def get_failed_attempts_last_n(self, n: int = 50) -> list:
        """
        Get last N failed authentication attempts
        
        Args:
            n: Number of attempts to retrieve
        
        Returns:
            List of failed attempts
        """
        return self.failed_authentication_attempts_log[-n:]
    
    def export_security_metrics_as_json(self) -> Dict[str, Any]:
        """
        Export security metrics for monitoring
        
        Returns:
            Security statistics
        """
        return {
            'active_sessions_count': self.get_active_sessions_count(),
            'failed_attempts_total': len(self.failed_authentication_attempts_log),
            'failed_attempts_recent': self.get_failed_attempts_last_n(10),
            'token_expiry_hours': self.token_expiry_duration_hours
        }


authentication_intent_gatekeeper_singleton = AuthenticationIntentGatekeeper()


def get_authentication_intent_gatekeeper() -> AuthenticationIntentGatekeeper:
    """
    Accessor for authentication gatekeeper
    Ensures single source of truth for authentication
    """
    return authentication_intent_gatekeeper_singleton
