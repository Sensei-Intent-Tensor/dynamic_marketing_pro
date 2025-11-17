#!/usr/bin/env python3
"""
2.0.e_fileLayerOrchestratorIntentPipeline.py

LAYER ORCHESTRATOR INTENT PIPELINE
Orchestrates all generation layers into final SVG output
Coordinates: Base → Text → Shapes → Colors → Assembly

PRINCIPLE: Layered composition with strict execution order
Each layer depends on previous layers
No layer conflicts - clean separation of concerns
"""

from typing import Dict, Any, List
from datetime import datetime


class LayerOrchestratorIntentPipeline:
    """
    Complete layer orchestration pipeline
    Coordinates all engines to produce final frame
    """
    
    def __init__(self):
        self.frames_orchestrated_count = 0
    
    def orchestrate_complete_frame_generation_intent(
        self,
        frame_specification: Dict[str, Any],
        color_scheme: Dict[str, Any],
        text_layout: Dict[str, Any],
        shape_composition: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        CRITICAL: Orchestrate all layers into final frame
        Produces complete SVG specification
        
        Args:
            frame_specification: Base frame spec from generator
            color_scheme: Resolved colors from color engine
            text_layout: Text layout from text engine
            shape_composition: Shape composition from shape engine
        
        Returns:
            Complete assembled frame ready for rendering
        """
        orchestration_timestamp = datetime.now().isoformat()
        
        svg_document = self._assemble_svg_document_intent(
            frame_spec=frame_specification,
            colors=color_scheme,
            text=text_layout,
            shapes=shape_composition
        )
        
        self.frames_orchestrated_count += 1
        
        return {
            'frame_id': frame_specification['frame_id'],
            'seed': frame_specification['seed'],
            'orchestration_timestamp': orchestration_timestamp,
            'svg_document': svg_document,
            'layers_composed': {
                'base_structure': True,
                'color_scheme': True,
                'text_layout': True,
                'shape_composition': True
            },
            'metadata': {
                'total_frames_orchestrated': self.frames_orchestrated_count,
                'layer_count': 4,
                'svg_character_count': len(svg_document)
            }
        }
    
    def _assemble_svg_document_intent(
        self,
        frame_spec: Dict[str, Any],
        colors: Dict[str, Any],
        text: Dict[str, Any],
        shapes: Dict[str, Any]
    ) -> str:
        """
        Assemble complete SVG document from all layers
        
        Args:
            frame_spec: Frame specification
            colors: Color scheme
            text: Text layout
            shapes: Shape composition
        
        Returns:
            Complete SVG as string
        """
        canvas = frame_spec['base_structure']
        
        svg_header = f'''<svg xmlns="http://www.w3.org/2000/svg" 
     viewBox="{canvas['viewbox_definition']}" 
     width="{canvas['canvas_width_px']}" 
     height="{canvas['canvas_height_px']}">'''
        
        background_layer = self._generate_background_layer_svg(colors)
        
        shapes_layer = self._generate_shapes_layer_svg(shapes, colors)
        
        text_layer = self._generate_text_layer_svg(text, colors)
        
        svg_footer = '</svg>'
        
        complete_svg = '\n'.join([
            svg_header,
            background_layer,
            shapes_layer,
            text_layer,
            svg_footer
        ])
        
        return complete_svg
    
    def _generate_background_layer_svg(
        self,
        colors: Dict[str, Any]
    ) -> str:
        """
        Generate background layer SVG
        
        Args:
            colors: Color scheme
        
        Returns:
            Background SVG markup
        """
        bg_color = colors['background_primary_hex']
        
        background_svg = f'''
  <!-- Background Layer -->
  <rect x="0" y="0" width="100%" height="100%" 
        fill="{bg_color}" />
'''
        
        return background_svg
    
    def _generate_shapes_layer_svg(
        self,
        shapes: Dict[str, Any],
        colors: Dict[str, Any]
    ) -> str:
        """
        Generate shapes layer SVG
        
        Args:
            shapes: Shape composition
            colors: Color scheme
        
        Returns:
            Shapes SVG markup
        """
        if not shapes['shapes']:
            return '  <!-- Shapes Layer: None -->'
        
        shape_color = colors['accent_color_hex']
        
        shapes_svg = '  <!-- Shapes Layer -->\n  <g id="shapes-layer">\n'
        
        for shape in shapes['shapes']:
            if shape['type'] == 'circle':
                shapes_svg += f'''    <circle cx="{shape['x_position']}" cy="{shape['y_position']}" 
            r="{shape['radius']}" 
            fill="{shape_color}" 
            opacity="{shape['opacity']}" />\n'''
            
            elif shape['type'] == 'rectangle':
                x = shape['x_position'] - (shape['width'] / 2)
                y = shape['y_position'] - (shape['height'] / 2)
                shapes_svg += f'''    <rect x="{x}" y="{y}" 
          width="{shape['width']}" height="{shape['height']}" 
          fill="{shape_color}" 
          opacity="{shape['opacity']}" 
          transform="rotate({shape.get('rotation', 0)} {shape['x_position']} {shape['y_position']})" />\n'''
            
            elif shape['type'] == 'triangle':
                size = shape['size']
                x = shape['x_position']
                y = shape['y_position']
                points = f"{x},{y-size/2} {x-size/2},{y+size/2} {x+size/2},{y+size/2}"
                shapes_svg += f'''    <polygon points="{points}" 
             fill="{shape_color}" 
             opacity="{shape['opacity']}" />\n'''
            
            elif shape['type'] == 'line':
                x1 = shape['x_position'] - shape['length'] / 2
                x2 = shape['x_position'] + shape['length'] / 2
                y = shape['y_position']
                shapes_svg += f'''    <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" 
          stroke="{shape_color}" 
          stroke-width="{shape.get('thickness', 2)}" 
          opacity="{shape['opacity']}" />\n'''
        
        shapes_svg += '  </g>\n'
        
        return shapes_svg
    
    def _generate_text_layer_svg(
        self,
        text: Dict[str, Any],
        colors: Dict[str, Any]
    ) -> str:
        """
        Generate text layer SVG
        
        Args:
            text: Text layout
            colors: Color scheme
        
        Returns:
            Text SVG markup
        """
        text_color = colors['text_color_hex']
        
        text_svg = '  <!-- Text Layer -->\n  <g id="text-layer">\n'
        
        company = text['company_name']
        text_svg += f'''    <text x="{company['x_position']}" y="{company['y_position']}" 
          font-size="{company['font_size']}" 
          font-weight="bold"
          fill="{text_color}" 
          text-anchor="{company['text_anchor']}"
          dominant-baseline="middle">
      {self._escape_xml(company['text'])}
    </text>\n'''
        
        if text['services']['services_list']:
            for service in text['services']['services_list']:
                text_svg += f'''    <text x="{service['x_position']}" y="{service['y_position']}" 
          font-size="{service['font_size']}" 
          fill="{text_color}" 
          text-anchor="{service['text_anchor']}"
          dominant-baseline="middle"
          opacity="0.9">
      {self._escape_xml(service['text'])}
    </text>\n'''
        
        text_svg += '  </g>\n'
        
        return text_svg
    
    def _escape_xml(self, text: str) -> str:
        """
        Escape XML special characters
        
        Args:
            text: Text to escape
        
        Returns:
            XML-safe text
        """
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&apos;')
        return text


layer_orchestrator_intent_pipeline_singleton = LayerOrchestratorIntentPipeline()


def get_layer_orchestrator_intent_pipeline() -> LayerOrchestratorIntentPipeline:
    """
    Accessor for layer orchestrator
    Ensures single source of truth for layer orchestration
    """
    return layer_orchestrator_intent_pipeline_singleton
