#!/usr/bin/env python3
"""
server_main.py

MAIN SERVER ENTRY POINT
Diamond Standard Architecture Production Server
WITH GOD MODE ADMIN ENDPOINT FOR TESTING
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

def get_all_engine_singletons():
    """Get all engine singletons by importing modules"""
    
    exec(open('0.0_folderCoreShellRuntime/0.0.d_fileAuthenticationIntentGatekeeper.py').read(), globals())
    exec(open('0.0_folderCoreShellRuntime/0.0.e_fileSubscriptionValidatorIntentFirewall.py').read(), globals())
    
    exec(open('2.0_folderGenerationEngineCore/2.0.a_fileFrameGeneratorIntentEngine.py').read(), globals())
    exec(open('2.0_folderGenerationEngineCore/2.0.b_fileColorResolverPrecedenceEngine.py').read(), globals())
    exec(open('2.0_folderGenerationEngineCore/2.0.c_fileTextBoundaryAutoFitEngine.py').read(), globals())
    exec(open('2.0_folderGenerationEngineCore/2.0.d_fileShapeCompositorSafeZoneEngine.py').read(), globals())
    exec(open('2.0_folderGenerationEngineCore/2.0.e_fileLayerOrchestratorIntentPipeline.py').read(), globals())
    exec(open('2.0_folderGenerationEngineCore/2.0.f_fileParameterWritableValidatorIntentGate.py').read(), globals())
    
    exec(open('3.0_folderDynamicLibraryLoader/3.0.a_fileDynamicLibraryIndexer.py').read(), globals())
    exec(open('3.0_folderDynamicLibraryLoader/3.0.b_fileAssetPathResolver.py').read(), globals())
    
    exec(open('4.0_folderServerIntentDispatcher/4.0.b_fileParameterParserIntentResolver.py').read(), globals())
    exec(open('4.0_folderServerIntentDispatcher/4.0.c_fileGIFCompositorOutputEngine.py').read(), globals())
    
    return {
        'auth_gatekeeper': get_authentication_intent_gatekeeper(),
        'subscription_validator': get_subscription_validator_intent_firewall(),
        'parameter_validator': get_parameter_writable_validator_intent_gate(),
        'parameter_parser': get_parameter_parser_intent_resolver(),
        'frame_generator': get_frame_generator_intent_engine(),
        'color_resolver': get_color_resolver_precedence_engine(),
        'text_engine': get_text_boundary_autofit_engine(),
        'shape_engine': get_shape_compositor_safe_zone_engine(),
        'layer_orchestrator': get_layer_orchestrator_intent_pipeline(),
        'library_indexer': get_dynamic_library_indexer(),
        'gif_compositor': get_gif_compositor_output_engine()
    }


app = Flask(__name__)
CORS(app)

print("[SERVER] Loading all engines...")
engines = get_all_engine_singletons()

engines['asset_resolver'] = create_asset_path_resolver(engines['library_indexer'])

print("[SERVER] All engines loaded successfully")


@app.route('/', methods=['GET'])
def home():
    """Welcome page"""
    return jsonify({
        'service': 'Dynamic Marketing Pro',
        'version': '1.0.0',
        'status': 'operational',
        'endpoints': {
            'health': '/health',
            'generate': '/generate?count=3&company=YourBrand',
            'god_mode': '/god?count=3&company=Test&services=AI,Cloud'
        },
        'documentation': 'https://github.com/Sensei-Intent-Tensor/dynamic_marketing_pro'
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    from datetime import datetime
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/god', methods=['GET'])
def god_mode_generate():
    """
    GOD MODE - FULL ADMIN ACCESS
    
    NO AUTH REQUIRED
    NO VALIDATION GATES
    NO SUBSCRIPTION LIMITS
    
    Direct access to generation pipeline for testing
    
    Usage:
    /god?count=5&company=Test&services=AI,Cloud,Data&seed=12345&bg=blue&text=white
    
    All parameters optional - uses intelligent defaults
    """
    from datetime import datetime
    import random
    
    print(f"[GOD MODE] Request from {request.remote_addr}")
    
    try:
        # Get ALL parameters - no validation, no gates
        raw_params = dict(request.args)
        
        # Parse with full power
        count = int(raw_params.get('count', 3))
        company = raw_params.get('company', 'Your Company')
        services_raw = raw_params.get('services', '')
        services = [s.strip() for s in services_raw.split(',') if s.strip()] if services_raw else []
        
        seed = int(raw_params.get('seed', random.randint(0, 3145728)))
        
        # Color overrides
        bg_color = raw_params.get('bg')
        text_color = raw_params.get('text')
        accent_color = raw_params.get('accent')
        
        # Style overrides
        font_style = raw_params.get('font')
        geometry = raw_params.get('geometry')
        
        print(f"[GOD MODE] Generating {count} frames | Company: {company} | Seed: {seed}")
        
        # Build parsed parameters
        parsed = {
            'base_seed': seed,
            'count': count,
            'company': company,
            'services': services,
            'color_primary': bg_color,
            'color_text': text_color,
            'color_accent': accent_color,
            'font_style': font_style,
            'geometry': geometry,
            'random_mode': False
        }
        
        # DIRECT GENERATION - NO GATES
        frames = []
        
        for i in range(count):
            frame_seed = seed + i
            
            print(f"[GOD MODE] Generating frame {i+1}/{count} with seed {frame_seed}")
            
            # Generate frame
            frame_spec = engines['frame_generator'].generate_frame_from_seed_and_parameters_intent(
                frame_seed=frame_seed,
                user_parameters=parsed,
                authenticated_user_id='GOD_MODE_ADMIN'
            )
            
            # Resolve colors
            colors = engines['color_resolver'].resolve_color_scheme_with_precedence_intent(
                resolved_parameters=frame_spec['resolved_parameters']
            )
            
            # Calculate text layout
            text = engines['text_engine'].calculate_text_layout_with_boundaries_intent(
                company_name=company,
                services_list=services,
                canvas_dimensions=frame_spec['base_structure'],
                font_style=frame_spec['resolved_parameters'].get('font_style', 'bold')
            )
            
            # Compose shapes
            shapes = engines['shape_engine'].compose_shapes_in_safe_zones_intent(
                text_layout=text,
                canvas_dimensions=frame_spec['base_structure'],
                geometry_style=frame_spec['resolved_parameters'].get('geometry', 'sharp'),
                seed=frame_seed
            )
            
            # Orchestrate complete frame
            complete = engines['layer_orchestrator'].orchestrate_complete_frame_generation_intent(
                frame_specification=frame_spec,
                color_scheme=colors,
                text_layout=text,
                shape_composition=shapes
            )
            
            frames.append(complete)
            print(f"[GOD MODE] Frame {i+1} complete")
        
        print(f"[GOD MODE] All frames generated, composing GIF...")
        
        # Compose GIF
        gif = engines['gif_compositor'].compose_gif_from_frames_intent(
            frames=frames,
            output_format='gif',
            frame_duration_ms=1000
        )
        
        if not gif['success']:
            return jsonify({
                'error': 'GIF_COMPOSITION_FAILED',
                'details': gif
            }), 500
        
        print(f"[GOD MODE] GIF composed successfully at {gif['output_file_path']}")
        
        # Return GIF file
        return send_file(
            gif['output_file_path'],
            mimetype='image/gif',
            as_attachment=True,
            download_name=f"godmode_{company}_{count}frames_{seed}.gif"
        )
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        
        print(f"[GOD MODE ERROR] {str(e)}")
        print(error_trace)
        
        return jsonify({
            'error': 'GOD_MODE_GENERATION_FAILED',
            'message': str(e),
            'traceback': error_trace,
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/generate', methods=['GET'])
def generate():
    """Main generation endpoint - WITH AUTH"""
    from datetime import datetime
    
    auth_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    auth_result = engines['auth_gatekeeper'].validate_authentication_token_intent(
        auth_token=auth_token,
        request_metadata={'ip_address': request.remote_addr}
    )
    
    if not auth_result['authenticated']:
        return jsonify({'error': 'AUTHENTICATION_FAILED'}), 401
    
    raw_params = dict(request.args)
    
    validation = engines['parameter_validator'].validate_parameters_as_writable_for_generation_intent(
        raw_parameters=raw_params,
        user_id='test_user'
    )
    
    if not validation['all_parameters_writable']:
        return jsonify({'error': 'INVALID_PARAMETERS'}), 400
    
    parsed = engines['parameter_parser'].parse_parameters_for_generation_intent(
        writable_parameters=validation['writable_parameters']
    )
    
    frames = []
    count = parsed.get('count', 3)
    
    for i in range(count):
        seed = parsed['base_seed'] + i
        
        frame_spec = engines['frame_generator'].generate_frame_from_seed_and_parameters_intent(
            frame_seed=seed,
            user_parameters=parsed,
            authenticated_user_id='test_user'
        )
        
        colors = engines['color_resolver'].resolve_color_scheme_with_precedence_intent(
            resolved_parameters=frame_spec['resolved_parameters']
        )
        
        text = engines['text_engine'].calculate_text_layout_with_boundaries_intent(
            company_name=parsed.get('company', 'Your Company'),
            services_list=parsed.get('services', []),
            canvas_dimensions=frame_spec['base_structure'],
            font_style='bold'
        )
        
        shapes = engines['shape_engine'].compose_shapes_in_safe_zones_intent(
            text_layout=text,
            canvas_dimensions=frame_spec['base_structure'],
            geometry_style='sharp',
            seed=seed
        )
        
        complete = engines['layer_orchestrator'].orchestrate_complete_frame_generation_intent(
            frame_specification=frame_spec,
            color_scheme=colors,
            text_layout=text,
            shape_composition=shapes
        )
        
        frames.append(complete)
    
    gif = engines['gif_compositor'].compose_gif_from_frames_intent(
        frames=frames,
        output_format='gif',
        frame_duration_ms=1000
    )
    
    return send_file(gif['output_file_path'], mimetype='image/gif')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[SERVER] Starting on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
