#!/usr/bin/env python3
"""
server_main.py

MAIN SERVER ENTRY POINT
Diamond Standard Architecture Production Server
WITH GOD MODE: AUTO (seed-based) & MANUAL (explicit asset selection)
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
            'god_auto': '/god?count=3&company=Test&services=AI,Cloud (seed-based)',
            'god_manual': '/god?mode=manual&count=3&company=Test&icon=sun_nature_icon&decoration=elegant_corner_decoration'
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
    GOD MODE - DUAL PATH
    
    AUTO MODE (default): Seed-based asset selection
    MANUAL MODE: Explicit asset selection
    
    AUTO Usage:
    /god?count=5&company=Test&services=AI,Cloud&seed=12345
    
    MANUAL Usage:
    /god?mode=manual&count=3&company=Test&icon=sun_nature_icon&decoration=elegant_corner_decoration&background_gradient=diagonal_gradient_background
    
    Available Assets:
    Icons: sun_nature_icon, tree_nature_icon, leaf_nature_icon, 
           rocket_tech_icon, cpu_tech_icon, cloud_tech_icon,
           chart_business_icon, briefcase_business_icon, handshake_business_icon
    
    Decorations: elegant_corner_decoration, tech_corner_decoration,
                 grid_pattern_decoration, wave_pattern_decoration
    
    Gradients: diagonal_gradient_background, radial_gradient_background, 
               vertical_gradient_background
    """
    from datetime import datetime
    import random
    
    print(f"[GOD MODE] Request from {request.remote_addr}")
    
    try:
        raw_params = dict(request.args)
        
        # FORK POINT: Auto or Manual mode
        mode = raw_params.get('mode', 'auto').lower()
        
        count = int(raw_params.get('count', 3))
        company = raw_params.get('company', 'Your Company')
        services_raw = raw_params.get('services', '')
        services = [s.strip() for s in services_raw.split(',') if s.strip()] if services_raw else []
        
        seed = int(raw_params.get('seed', random.randint(0, 3145728)))
        
        bg_color = raw_params.get('bg')
        text_color = raw_params.get('text')
        accent_color = raw_params.get('accent')
        
        font_style = raw_params.get('font')
        geometry = raw_params.get('geometry')
        
        # MANUAL MODE PARAMETERS
        manual_icon = raw_params.get('icon')
        manual_decoration = raw_params.get('decoration')
        manual_gradient = raw_params.get('background_gradient')
        
        if mode == 'manual':
            print(f"[GOD MODE - MANUAL] Drawing from scratch")
            print(f"[GOD MODE - MANUAL] Icon: {manual_icon}")
            print(f"[GOD MODE - MANUAL] Decoration: {manual_decoration}")
            print(f"[GOD MODE - MANUAL] Gradient: {manual_gradient}")
            
            # Validate manual assets exist
            if manual_icon or manual_decoration or manual_gradient:
                print(f"[GOD MODE - MANUAL] User-specified assets will override seed selection")
        else:
            print(f"[GOD MODE - AUTO] Seed: {seed} | Frames: {count} | Company: {company}")
        
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
            'random_mode': False,
            'mode': mode,
            'manual_icon': manual_icon,
            'manual_decoration': manual_decoration,
            'manual_gradient': manual_gradient
        }
        
        frames = []
        
        for i in range(count):
            frame_seed = seed + i
            
            print(f"[GOD MODE] Frame {i+1}/{count} | Seed: {frame_seed} | Mode: {mode.upper()}")
            
            frame_spec = engines['frame_generator'].generate_frame_from_seed_and_parameters_intent(
                frame_seed=frame_seed,
                user_parameters=parsed,
                authenticated_user_id='GOD_MODE_ADMIN'
            )
            
            # MANUAL MODE: Override asset selections
            if mode == 'manual':
                if manual_icon:
                    frame_spec['resolved_parameters']['icon_selection'] = manual_icon
                    print(f"[MANUAL OVERRIDE] Icon: {manual_icon}")
                
                if manual_decoration:
                    frame_spec['resolved_parameters']['decoration_selection'] = manual_decoration
                    print(f"[MANUAL OVERRIDE] Decoration: {manual_decoration}")
                
                if manual_gradient:
                    frame_spec['resolved_parameters']['gradient_selection'] = manual_gradient
                    print(f"[MANUAL OVERRIDE] Gradient: {manual_gradient}")
            
            colors = engines['color_resolver'].resolve_color_scheme_with_precedence_intent(
                resolved_parameters=frame_spec['resolved_parameters']
            )
            
            text = engines['text_engine'].calculate_text_layout_with_boundaries_intent(
                company_name=company,
                services_list=services,
                canvas_dimensions=frame_spec['base_structure'],
                font_style=frame_spec['resolved_parameters'].get('font_style', 'bold')
            )
            
            shapes = engines['shape_engine'].compose_shapes_in_safe_zones_intent(
                text_layout=text,
                canvas_dimensions=frame_spec['base_structure'],
                geometry_style=frame_spec['resolved_parameters'].get('geometry', 'sharp'),
                seed=frame_seed
            )
            
            complete = engines['layer_orchestrator'].orchestrate_complete_frame_generation_intent(
                frame_specification=frame_spec,
                color_scheme=colors,
                text_layout=text,
                shape_composition=shapes
            )
            
            frames.append(complete)
            print(f"[GOD MODE] Frame {i+1} complete")
        
        print(f"[GOD MODE] Composing GIF...")
        
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
        
        mode_suffix = "manual" if mode == "manual" else "auto"
        filename = f"godmode_{mode_suffix}_{company}_{count}frames_{seed}.gif"
        
        print(f"[GOD MODE] Success! File: {filename}")
        
        return send_file(
            gif['output_file_path'],
            mimetype='image/gif',
            as_attachment=True,
            download_name=filename
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
