#!/usr/bin/env python3
"""
4.0.a_fileFlaskServerIntentRouter.py

FLASK SERVER INTENT ROUTER
Main HTTP server orchestrating all generation engines
Routes requests through authentication → validation → generation → output

PRINCIPLE: Single entry point for all requests
Complete orchestration of entire pipeline
Every request logged and traced
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from typing import Dict, Any
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime


class FlaskServerIntentRouter:
    """
    Main Flask server with complete request routing
    Orchestrates all generation engines
    """
    
    def __init__(
        self,
        auth_gatekeeper,
        subscription_validator,
        parameter_validator,
        parameter_parser,
        frame_generator,
        color_resolver,
        text_engine,
        shape_engine,
        layer_orchestrator,
        library_indexer,
        asset_resolver,
        gif_compositor
    ):
        self.auth_gatekeeper = auth_gatekeeper
        self.subscription_validator = subscription_validator
        self.parameter_validator = parameter_validator
        self.parameter_parser = parameter_parser
        self.frame_generator = frame_generator
        self.color_resolver = color_resolver
        self.text_engine = text_engine
        self.shape_engine = shape_engine
        self.layer_orchestrator = layer_orchestrator
        self.library_indexer = library_indexer
        self.asset_resolver = asset_resolver
        self.gif_compositor = gif_compositor
        
        self.app = Flask(__name__)
        CORS(self.app)
        
        self.request_count_total = 0
        self.successful_generations_count = 0
        self.failed_generations_count = 0
        
        self._register_routes_intent()
    
    def _register_routes_intent(self) -> None:
        """
        Register all HTTP routes
        Maps endpoints to handler functions
        """
        self.app.route('/health', methods=['GET'])(self.health_check_intent)
        self.app.route('/generate', methods=['GET'])(self.generate_marketing_gif_intent)
        self.app.route('/assets/list', methods=['GET'])(self.list_available_assets_intent)
        self.app.route('/stats', methods=['GET'])(self.get_server_statistics_intent)
    
    def health_check_intent(self) -> Dict[str, Any]:
        """
        Health check endpoint
        Verifies server is running
        """
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0_diamond_standard'
        })
    
    def generate_marketing_gif_intent(self) -> Any:
        """
        CRITICAL: Main generation endpoint
        Complete pipeline: Auth → Validate → Generate → Compose → Output
        """
        self.request_count_total += 1
        request_timestamp = datetime.now().isoformat()
        
        request_metadata = {
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'request_path': request.path
        }
        
        auth_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        auth_result = self.auth_gatekeeper.validate_authentication_token_intent(
            auth_token=auth_token,
            request_metadata=request_metadata
        )
        
        if not auth_result['authenticated']:
            return jsonify({
                'error': 'AUTHENTICATION_FAILED',
                'message': auth_result['rejection_reason'],
                'timestamp': request_timestamp
            }), 401
        
        user_object = auth_result['user_object']
        user_id = user_object['user_id']
        user_tier = user_object.get('subscription_tier', 'free')
        
        raw_parameters = dict(request.args)
        
        validation_result = self.parameter_validator.validate_parameters_as_writable_for_generation_intent(
            raw_parameters=raw_parameters,
            user_id=user_id
        )
        
        if not validation_result['all_parameters_writable']:
            return jsonify({
                'error': 'PARAMETER_VALIDATION_FAILED',
                'validation_log': validation_result['validation_log'],
                'timestamp': request_timestamp
            }), 400
        
        writable_parameters = validation_result['writable_parameters']
        
        frame_count = writable_parameters.get('count', 3)
        
        subscription_check = self.subscription_validator.validate_subscription_tier_access_intent(
            user_id=user_id,
            user_tier=user_tier,
            requested_operation='generate_marketing_gif',
            operation_parameters={'count': frame_count}
        )
        
        if not subscription_check['access_granted']:
            return jsonify({
                'error': 'SUBSCRIPTION_LIMIT_EXCEEDED',
                'rejection_reason': subscription_check['rejection_reason'],
                'tier': user_tier,
                'timestamp': request_timestamp
            }), 403
        
        parsed_parameters = self.parameter_parser.parse_parameters_for_generation_intent(
            writable_parameters=writable_parameters
        )
        
        try:
            generated_frames = []
            
            for frame_index in range(frame_count):
                frame_seed = parsed_parameters['base_seed'] + frame_index
                
                frame_spec = self.frame_generator.generate_frame_from_seed_and_parameters_intent(
                    frame_seed=frame_seed,
                    user_parameters=parsed_parameters,
                    authenticated_user_id=user_id
                )
                
                color_scheme = self.color_resolver.resolve_color_scheme_with_precedence_intent(
                    resolved_parameters=frame_spec['resolved_parameters']
                )
                
                text_layout = self.text_engine.calculate_text_layout_with_boundaries_intent(
                    company_name=parsed_parameters.get('company', 'Your Company'),
                    services_list=parsed_parameters.get('services', []),
                    canvas_dimensions=frame_spec['base_structure'],
                    font_style=frame_spec['resolved_parameters'].get('font_style', 'bold')
                )
                
                shape_composition = self.shape_engine.compose_shapes_in_safe_zones_intent(
                    text_layout=text_layout,
                    canvas_dimensions=frame_spec['base_structure'],
                    geometry_style=frame_spec['resolved_parameters'].get('geometry', 'sharp'),
                    seed=frame_seed
                )
                
                complete_frame = self.layer_orchestrator.orchestrate_complete_frame_generation_intent(
                    frame_specification=frame_spec,
                    color_scheme=color_scheme,
                    text_layout=text_layout,
                    shape_composition=shape_composition
                )
                
                generated_frames.append(complete_frame)
            
            gif_output = self.gif_compositor.compose_gif_from_frames_intent(
                frames=generated_frames,
                output_format='gif',
                frame_duration_ms=1000
            )
            
            self.successful_generations_count += 1
            
            return send_file(
                gif_output['output_file_path'],
                mimetype='image/gif',
                as_attachment=True,
                download_name=f"marketing_{user_id}_{request_timestamp.replace(':', '-')}.gif"
            )
        
        except Exception as e:
            self.failed_generations_count += 1
            
            return jsonify({
                'error': 'GENERATION_FAILED',
                'message': str(e),
                'timestamp': request_timestamp
            }), 500
    
    def list_available_assets_intent(self) -> Dict[str, Any]:
        """
        List all available assets in libraries
        Allows clients to discover available options
        """
        indexing_stats = self.library_indexer.get_indexing_statistics_intent()
        
        available_fonts = self.library_indexer.list_all_assets_in_category_intent('fonts')
        available_icons = self.library_indexer.list_all_assets_in_category_intent('icons')
        available_decorations = self.library_indexer.list_all_assets_in_category_intent('decorations')
        available_backgrounds = self.library_indexer.list_all_assets_in_category_intent('backgrounds')
        
        return jsonify({
            'assets': {
                'fonts': available_fonts,
                'icons': available_icons,
                'decorations': available_decorations,
                'backgrounds': available_backgrounds
            },
            'statistics': indexing_stats,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_server_statistics_intent(self) -> Dict[str, Any]:
        """
        Get server statistics
        Request counts, generation metrics, uptime
        """
        return jsonify({
            'requests': {
                'total': self.request_count_total,
                'successful_generations': self.successful_generations_count,
                'failed_generations': self.failed_generations_count
            },
            'timestamp': datetime.now().isoformat()
        })
    
    def run_server_intent(self, host: str = '0.0.0.0', port: int = 5000, debug: bool = False) -> None:
        """
        Start Flask server
        
        Args:
            host: Host to bind to
            port: Port to listen on
            debug: Debug mode
        """
        print(f"[SERVER] Starting Dynamic Marketing GIF Server on {host}:{port}")
        print(f"[SERVER] Diamond Standard Architecture v1.0.0")
        print(f"[SERVER] Indexing library assets...")
        
        index_result = self.library_indexer.index_all_library_assets_intent()
        print(f"[SERVER] Indexed {index_result['total_assets_indexed']} assets")
        
        print(f"[SERVER] Server ready. Listening for requests...")
        
        self.app.run(host=host, port=port, debug=debug)


def create_flask_server_intent_router(
    auth_gatekeeper,
    subscription_validator,
    parameter_validator,
    parameter_parser,
    frame_generator,
    color_resolver,
    text_engine,
    shape_engine,
    layer_orchestrator,
    library_indexer,
    asset_resolver,
    gif_compositor
) -> FlaskServerIntentRouter:
    """
    Factory function to create Flask server
    Wires up all engines
    
    Returns:
        Configured Flask server
    """
    return FlaskServerIntentRouter(
        auth_gatekeeper=auth_gatekeeper,
        subscription_validator=subscription_validator,
        parameter_validator=parameter_validator,
        parameter_parser=parameter_parser,
        frame_generator=frame_generator,
        color_resolver=color_resolver,
        text_engine=text_engine,
        shape_engine=shape_engine,
        layer_orchestrator=layer_orchestrator,
        library_indexer=library_indexer,
        asset_resolver=asset_resolver,
        gif_compositor=gif_compositor
    )
