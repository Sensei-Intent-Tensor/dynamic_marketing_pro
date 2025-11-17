#!/usr/bin/env python3
"""
4.0.c_fileGIFCompositorOutputEngine.py

GIF COMPOSITOR OUTPUT ENGINE
Converts SVG frames to PNG, composes animated GIF
Handles rendering, optimization, and file output

PRINCIPLE: SVG → PNG → GIF Pipeline
Clean raster conversion with quality preservation
Optimized output for web delivery
"""

from typing import Dict, Any, List
from pathlib import Path
import tempfile
import os


class GIFCompositorOutputEngine:
    """
    GIF composition engine
    Converts SVG frames to animated GIF
    """
    
    def __init__(self):
        self.temp_directory_path = tempfile.gettempdir()
        self.total_gifs_composed_count = 0
    
    def compose_gif_from_frames_intent(
        self,
        frames: List[Dict[str, Any]],
        output_format: str = 'gif',
        frame_duration_ms: int = 1000
    ) -> Dict[str, Any]:
        """
        CRITICAL: Compose animated GIF from SVG frames
        Pipeline: SVG → PNG → GIF
        
        Args:
            frames: List of frame specifications with SVG
            output_format: Output format (currently only 'gif')
            frame_duration_ms: Duration per frame in milliseconds
        
        Returns:
            Composition result with output file path
        """
        from datetime import datetime
        
        composition_timestamp = datetime.now().isoformat()
        
        if not frames or len(frames) == 0:
            return {
                'success': False,
                'error': 'NO_FRAMES_PROVIDED',
                'timestamp': composition_timestamp
            }
        
        temp_png_files = []
        
        try:
            for frame_index, frame in enumerate(frames):
                svg_content = frame['svg_document']
                
                png_file_path = self._convert_svg_to_png_intent(
                    svg_content=svg_content,
                    frame_index=frame_index
                )
                
                temp_png_files.append(png_file_path)
            
            gif_output_path = self._compose_png_frames_to_gif_intent(
                png_files=temp_png_files,
                frame_duration_ms=frame_duration_ms
            )
            
            self.total_gifs_composed_count += 1
            
            return {
                'success': True,
                'output_file_path': gif_output_path,
                'frame_count': len(frames),
                'frame_duration_ms': frame_duration_ms,
                'composition_timestamp': composition_timestamp,
                'total_gifs_composed': self.total_gifs_composed_count
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': composition_timestamp
            }
        
        finally:
            self._cleanup_temporary_files(temp_png_files)
    
    def _convert_svg_to_png_intent(
        self,
        svg_content: str,
        frame_index: int
    ) -> str:
        """
        Convert SVG content to PNG file
        
        Args:
            svg_content: SVG as string
            frame_index: Frame number for temp file naming
        
        Returns:
            Path to generated PNG file
        """
        import cairosvg
        from datetime import datetime
        
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_png_path = os.path.join(
            self.temp_directory_path,
            f"frame_{timestamp_str}_{frame_index}.png"
        )
        
        cairosvg.svg2png(
            bytestring=svg_content.encode('utf-8'),
            write_to=temp_png_path,
            output_width=400,
            output_height=480
        )
        
        return temp_png_path
    
    def _compose_png_frames_to_gif_intent(
        self,
        png_files: List[str],
        frame_duration_ms: int
    ) -> str:
        """
        Compose PNG frames into animated GIF
        
        Args:
            png_files: List of PNG file paths
            frame_duration_ms: Duration per frame
        
        Returns:
            Path to generated GIF file
        """
        from PIL import Image
        from datetime import datetime
        
        timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_gif_path = os.path.join(
            self.temp_directory_path,
            f"marketing_gif_{timestamp_str}.gif"
        )
        
        images = []
        for png_file in png_files:
            img = Image.open(png_file)
            images.append(img.convert('RGB'))
        
        images[0].save(
            output_gif_path,
            save_all=True,
            append_images=images[1:],
            duration=frame_duration_ms,
            loop=0,
            optimize=True
        )
        
        return output_gif_path
    
    def _cleanup_temporary_files(self, file_paths: List[str]) -> None:
        """
        Clean up temporary PNG files
        
        Args:
            file_paths: List of file paths to delete
        """
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                pass
    
    def compose_single_frame_png_intent(
        self,
        frame: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compose single PNG from frame (no animation)
        
        Args:
            frame: Frame specification with SVG
        
        Returns:
            Composition result with PNG path
        """
        from datetime import datetime
        
        composition_timestamp = datetime.now().isoformat()
        
        try:
            svg_content = frame['svg_document']
            
            png_file_path = self._convert_svg_to_png_intent(
                svg_content=svg_content,
                frame_index=0
            )
            
            return {
                'success': True,
                'output_file_path': png_file_path,
                'composition_timestamp': composition_timestamp
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': composition_timestamp
            }
    
    def get_compositor_statistics_intent(self) -> Dict[str, Any]:
        """
        Get compositor statistics
        
        Returns:
            Statistics about GIF composition
        """
        return {
            'total_gifs_composed': self.total_gifs_composed_count,
            'temp_directory_path': self.temp_directory_path
        }


gif_compositor_output_engine_singleton = GIFCompositorOutputEngine()


def get_gif_compositor_output_engine() -> GIFCompositorOutputEngine:
    """
    Accessor for GIF compositor engine
    Ensures single source of truth for GIF composition
    """
    return gif_compositor_output_engine_singleton
