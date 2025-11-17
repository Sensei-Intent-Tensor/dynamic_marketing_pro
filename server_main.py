# # Create the file (content above)
# git add server_main.py
# git commit -m "Add server main entry point for Render deployment"
# git push
# ```

# ### **2. Update requirements if using Gunicorn**
# Add to `0.0.a_requirements_intent_manifest.txt`:
# ```
# gunicorn==21.2.0
# ```

# ### **3. Create Render Web Service**
# - Go to https://render.com
# - New > Web Service
# - Connect your GitHub repo: `Sensei-Intent-Tensor/dynamic_marketing_pro`

# ### **4. Configure Service**
# ```
# Name: dynamic-marketing-pro
# Environment: Python 3
# Region: (Choose closest to your users)
# Branch: main

#!/usr/bin/env python3
"""
server_main.py

MAIN SERVER ENTRY POINT
Initializes all engines and starts Flask server
This is the file Render will execute
"""

import os
import sys

# Ensure all modules are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all singletons from each level
from 0.0_folderCoreShellRuntime.0.0.d_fileAuthenticationIntentGatekeeper import get_authentication_intent_gatekeeper
from 0.0_folderCoreShellRuntime.0.0.e_fileSubscriptionValidatorIntentFirewall import get_subscription_validator_intent_firewall

from 2.0_folderGenerationEngineCore.2.0.a_fileFrameGeneratorIntentEngine import get_frame_generator_intent_engine
from 2.0_folderGenerationEngineCore.2.0.b_fileColorResolverPrecedenceEngine import get_color_resolver_precedence_engine
from 2.0_folderGenerationEngineCore.2.0.c_fileTextBoundaryAutoFitEngine import get_text_boundary_autofit_engine
from 2.0_folderGenerationEngineCore.2.0.d_fileShapeCompositorSafeZoneEngine import get_shape_compositor_safe_zone_engine
from 2.0_folderGenerationEngineCore.2.0.e_fileLayerOrchestratorIntentPipeline import get_layer_orchestrator_intent_pipeline
from 2.0_folderGenerationEngineCore.2.0.f_fileParameterWritableValidatorIntentGate import get_parameter_writable_validator_intent_gate

from 3.0_folderDynamicLibraryLoader.3.0.a_fileDynamicLibraryIndexer import get_dynamic_library_indexer
from 3.0_folderDynamicLibraryLoader.3.0.b_fileAssetPathResolver import create_asset_path_resolver

from 4.0_folderServerIntentDispatcher.4.0.a_fileFlaskServerIntentRouter import create_flask_server_intent_router
from 4.0_folderServerIntentDispatcher.4.0.b_fileParameterParserIntentResolver import get_parameter_parser_intent_resolver
from 4.0_folderServerIntentDispatcher.4.0.c_fileGIFCompositorOutputEngine import get_gif_compositor_output_engine


def initialize_server_with_all_engines():
    """
    Initialize all engines and create Flask server
    This is called when server starts
    """
    # Get all singletons
    auth_gatekeeper = get_authentication_intent_gatekeeper()
    subscription_validator = get_subscription_validator_intent_firewall()
    parameter_validator = get_parameter_writable_validator_intent_gate()
    parameter_parser = get_parameter_parser_intent_resolver()
    
    frame_generator = get_frame_generator_intent_engine()
    color_resolver = get_color_resolver_precedence_engine()
    text_engine = get_text_boundary_autofit_engine()
    shape_engine = get_shape_compositor_safe_zone_engine()
    layer_orchestrator = get_layer_orchestrator_intent_pipeline()
    
    library_indexer = get_dynamic_library_indexer()
    asset_resolver = create_asset_path_resolver(library_indexer)
    
    gif_compositor = get_gif_compositor_output_engine()
    
    # Create Flask server with all engines wired
    server = create_flask_server_intent_router(
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
    
    return server


if __name__ == '__main__':
    # Initialize server
    server = initialize_server_with_all_engines()
    
    # Get port from environment (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    
    # Run server
    server.run_server_intent(
        host='0.0.0.0',
        port=port,
        debug=False  # Never debug=True in production
    )


# For Gunicorn
app = initialize_server_with_all_engines().app
