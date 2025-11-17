#!/usr/bin/env python3
"""
server_main.py

MAIN SERVER ENTRY POINT
Diamond Standard Architecture Production Server
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


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    from datetime import datetime
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/generate', methods=['GET'])
def generate():
    """Main generation endpoint"""
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
