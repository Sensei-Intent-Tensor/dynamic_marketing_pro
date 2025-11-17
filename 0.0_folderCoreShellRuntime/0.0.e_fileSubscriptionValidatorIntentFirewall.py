#!/usr/bin/env python3
"""
0.0.e_fileSubscriptionValidatorIntentFirewall.py

SUBSCRIPTION VALIDATOR INTENT FIREWALL
Subscription tier validation and usage limit enforcement
Ensures users only access features and quotas allowed by their tier

PRINCIPLE: Fair usage enforcement
Every operation is validated against subscription tier limits
No user can exceed their tier's allocation
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from enum import Enum


class SubscriptionTierEnum(Enum):
    """
    Defined subscription tiers
    Each tier has specific usage limits and feature access
    """
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class SubscriptionValidatorIntentFirewall:
    """
    Subscription validation firewall
    Enforces tier limits and feature access
    """
    
    def __init__(self):
        self.tier_limits_definition_registry = self._build_tier_limits_definition()
        self.user_usage_tracking_registry = {}
        self.tier_violations_log = []
    
    def _build_tier_limits_definition(self) -> Dict[str, Dict[str, Any]]:
        """
        Define usage limits for each subscription tier
        
        Returns:
            Complete tier limits definition
        """
        return {
            SubscriptionTierEnum.FREE.value: {
                'max_generations_per_month': 10,
                'max_frames_per_generation': 3,
                'max_custom_urls': 0,
                'random_mode_enabled': False,
                'custom_colors_enabled': False,
                'custom_fonts_enabled': False,
                'api_access_enabled': False,
                'monthly_cost_usd': 0
            },
            SubscriptionTierEnum.STARTER.value: {
                'max_generations_per_month': 1000,
                'max_frames_per_generation': 10,
                'max_custom_urls': 1,
                'random_mode_enabled': True,
                'custom_colors_enabled': True,
                'custom_fonts_enabled': True,
                'api_access_enabled': False,
                'monthly_cost_usd': 29
            },
            SubscriptionTierEnum.PROFESSIONAL.value: {
                'max_generations_per_month': 10000,
                'max_frames_per_generation': 50,
                'max_custom_urls': 5,
                'random_mode_enabled': True,
                'custom_colors_enabled': True,
                'custom_fonts_enabled': True,
                'api_access_enabled': True,
                'monthly_cost_usd': 99
            },
            SubscriptionTierEnum.ENTERPRISE.value: {
                'max_generations_per_month': -1,  # Unlimited
                'max_frames_per_generation': 100,
                'max_custom_urls': -1,  # Unlimited
                'random_mode_enabled': True,
                'custom_colors_enabled': True,
                'custom_fonts_enabled': True,
                'api_access_enabled': True,
                'monthly_cost_usd': 299
            }
        }
    
    def validate_subscription_tier_access_intent(
        self,
        user_id: str,
        user_tier: str,
        requested_operation: str,
        operation_parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        CRITICAL: Validate subscription tier allows requested operation
        
        Args:
            user_id: Authenticated user ID
            user_tier: User's subscription tier
            requested_operation: Operation being requested
            operation_parameters: Parameters of the operation
        
        Returns:
            Validation result with access decision
        """
        validation_timestamp = datetime.now().isoformat()
        
        if user_tier not in self.tier_limits_definition_registry:
            return {
                'access_granted': False,
                'rejection_reason': 'INVALID_SUBSCRIPTION_TIER',
                'tier': user_tier,
                'timestamp': validation_timestamp
            }
        
        tier_limits = self.tier_limits_definition_registry[user_tier]
        
        if requested_operation == 'generate_marketing_gif':
            validation_result = self._validate_generation_request(
                user_id=user_id,
                tier_limits=tier_limits,
                operation_parameters=operation_parameters
            )
        elif requested_operation == 'api_access':
            validation_result = self._validate_api_access_request(
                tier_limits=tier_limits
            )
        else:
            validation_result = {
                'access_granted': False,
                'rejection_reason': 'UNKNOWN_OPERATION',
                'tier': user_tier
            }
        
        if not validation_result['access_granted']:
            self._log_tier_violation(
                user_id=user_id,
                tier=user_tier,
                operation=requested_operation,
                rejection_reason=validation_result['rejection_reason'],
                timestamp=validation_timestamp
            )
        
        validation_result['timestamp'] = validation_timestamp
        return validation_result
    
    def _validate_generation_request(
        self,
        user_id: str,
        tier_limits: Dict[str, Any],
        operation_parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate GIF generation request against tier limits
        
        Args:
            user_id: User requesting generation
            tier_limits: Limits for user's tier
            operation_parameters: Generation parameters
        
        Returns:
            Validation result
        """
        current_period_usage = self._get_current_period_usage(user_id)
        
        max_generations = tier_limits['max_generations_per_month']
        if max_generations != -1:  # -1 = unlimited
            if current_period_usage >= max_generations:
                return {
                    'access_granted': False,
                    'rejection_reason': 'MONTHLY_GENERATION_LIMIT_EXCEEDED',
                    'usage_current': current_period_usage,
                    'usage_limit': max_generations,
                    'usage_remaining': 0
                }
        
        requested_frame_count = operation_parameters.get('count', 3)
        max_frames = tier_limits['max_frames_per_generation']
        if requested_frame_count > max_frames:
            return {
                'access_granted': False,
                'rejection_reason': 'FRAME_COUNT_EXCEEDS_TIER_LIMIT',
                'requested_frames': requested_frame_count,
                'max_frames_allowed': max_frames
            }
        
        if operation_parameters.get('random') and not tier_limits['random_mode_enabled']:
            return {
                'access_granted': False,
                'rejection_reason': 'RANDOM_MODE_NOT_AVAILABLE_IN_TIER'
            }
        
        if operation_parameters.get('bg') and not tier_limits['custom_colors_enabled']:
            return {
                'access_granted': False,
                'rejection_reason': 'CUSTOM_COLORS_NOT_AVAILABLE_IN_TIER'
            }
        
        self._increment_usage_counter(user_id)
        
        usage_remaining = max_generations - (current_period_usage + 1) if max_generations != -1 else -1
        
        return {
            'access_granted': True,
            'rejection_reason': None,
            'usage_current': current_period_usage + 1,
            'usage_limit': max_generations,
            'usage_remaining': usage_remaining
        }
    
    def _validate_api_access_request(
        self,
        tier_limits: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate API access request
        
        Args:
            tier_limits: Limits for user's tier
        
        Returns:
            Validation result
        """
        if not tier_limits['api_access_enabled']:
            return {
                'access_granted': False,
                'rejection_reason': 'API_ACCESS_NOT_AVAILABLE_IN_TIER'
            }
        
        return {
            'access_granted': True,
            'rejection_reason': None
        }
    
    def _get_current_period_usage(self, user_id: str) -> int:
        """
        Get user's usage count for current billing period
        
        Args:
            user_id: User to check
        
        Returns:
            Usage count
        """
        if user_id not in self.user_usage_tracking_registry:
            self._initialize_user_usage_tracking(user_id)
        
        user_tracking = self.user_usage_tracking_registry[user_id]
        
        current_period_start = self._get_current_billing_period_start()
        
        if user_tracking['period_start'] != current_period_start:
            self._reset_user_usage_for_new_period(user_id, current_period_start)
            return 0
        
        return user_tracking['usage_count']
    
    def _increment_usage_counter(self, user_id: str) -> None:
        """
        Increment user's usage counter
        
        Args:
            user_id: User whose usage to increment
        """
        if user_id not in self.user_usage_tracking_registry:
            self._initialize_user_usage_tracking(user_id)
        
        self.user_usage_tracking_registry[user_id]['usage_count'] += 1
        self.user_usage_tracking_registry[user_id]['last_usage_timestamp'] = datetime.now().isoformat()
    
    def _initialize_user_usage_tracking(self, user_id: str) -> None:
        """
        Initialize usage tracking for new user
        
        Args:
            user_id: User to initialize
        """
        self.user_usage_tracking_registry[user_id] = {
            'period_start': self._get_current_billing_period_start(),
            'usage_count': 0,
            'last_usage_timestamp': None
        }
    
    def _reset_user_usage_for_new_period(
        self,
        user_id: str,
        new_period_start: str
    ) -> None:
        """
        Reset usage counter for new billing period
        
        Args:
            user_id: User to reset
            new_period_start: New period start date
        """
        self.user_usage_tracking_registry[user_id] = {
            'period_start': new_period_start,
            'usage_count': 0,
            'last_usage_timestamp': None
        }
    
    def _get_current_billing_period_start(self) -> str:
        """
        Get start date of current billing period
        Periods start on 1st of each month
        
        Returns:
            Period start date (YYYY-MM-01)
        """
        now = datetime.now()
        return f"{now.year}-{now.month:02d}-01"
    
    def _log_tier_violation(
        self,
        user_id: str,
        tier: str,
        operation: str,
        rejection_reason: str,
        timestamp: str
    ) -> None:
        """
        Log tier violation attempt
        
        Args:
            user_id: User who violated
            tier: User's tier
            operation: Operation attempted
            rejection_reason: Why rejected
            timestamp: Violation timestamp
        """
        self.tier_violations_log.append({
            'timestamp': timestamp,
            'user_id': user_id,
            'tier': tier,
            'operation': operation,
            'rejection_reason': rejection_reason
        })
    
    def get_tier_limits_for_tier(self, tier: str) -> Dict[str, Any]:
        """
        Get limits definition for a tier
        
        Args:
            tier: Tier name
        
        Returns:
            Tier limits or empty dict
        """
        return self.tier_limits_definition_registry.get(tier, {})
    
    def export_subscription_metrics_as_json(self) -> Dict[str, Any]:
        """
        Export subscription metrics for monitoring
        
        Returns:
            Subscription statistics
        """
        return {
            'total_users_tracked': len(self.user_usage_tracking_registry),
            'tier_violations_total': len(self.tier_violations_log),
            'tier_violations_recent': self.tier_violations_log[-10:],
            'tier_definitions': self.tier_limits_definition_registry
        }


subscription_validator_intent_firewall_singleton = SubscriptionValidatorIntentFirewall()


def get_subscription_validator_intent_firewall() -> SubscriptionValidatorIntentFirewall:
    """
    Accessor for subscription validator
    Ensures single source of truth for subscription validation
    """
    return subscription_validator_intent_firewall_singleton
