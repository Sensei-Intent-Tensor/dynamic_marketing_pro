#!/usr/bin/env python3
"""
3.0.c_fileLibraryHotReloadWatcher.py

LIBRARY HOT RELOAD WATCHER
Watches library folders for changes and triggers re-indexing
Development-time feature for rapid asset iteration

PRINCIPLE: Add files → Auto-detected → Immediately available
No server restart needed during development
Production can disable this for performance
"""

from typing import Dict, Any, Callable, Optional
from pathlib import Path
from datetime import datetime
import time
import threading


class LibraryHotReloadWatcher:
    """
    Hot reload watcher for library assets
    Monitors file system for changes and triggers re-indexing
    """
    
    def __init__(
        self,
        library_indexer,
        libraries_base_path: str = 'libraries',
        enabled: bool = False
    ):
        self.library_indexer = library_indexer
        self.libraries_base_path = Path(libraries_base_path)
        self.enabled = enabled
        self.watcher_thread = None
        self.watcher_running = False
        self.file_modification_times_cache = {}
        self.reload_events_log = []
        self.check_interval_seconds = 5
    
    def start_hot_reload_watcher_intent(self) -> Dict[str, Any]:
        """
        Start hot reload watcher thread
        Monitors file system for changes
        
        Returns:
            Watcher start status
        """
        if not self.enabled:
            return {
                'watcher_started': False,
                'reason': 'HOT_RELOAD_DISABLED',
                'message': 'Hot reload is disabled. Enable in configuration to use this feature.'
            }
        
        if self.watcher_running:
            return {
                'watcher_started': False,
                'reason': 'ALREADY_RUNNING',
                'message': 'Hot reload watcher is already running.'
            }
        
        self.watcher_running = True
        
        self.watcher_thread = threading.Thread(
            target=self._watch_library_files_loop,
            daemon=True
        )
        self.watcher_thread.start()
        
        return {
            'watcher_started': True,
            'reason': None,
            'message': 'Hot reload watcher started successfully.',
            'check_interval_seconds': self.check_interval_seconds,
            'monitoring_path': str(self.libraries_base_path)
        }
    
    def stop_hot_reload_watcher_intent(self) -> Dict[str, Any]:
        """
        Stop hot reload watcher thread
        
        Returns:
            Watcher stop status
        """
        if not self.watcher_running:
            return {
                'watcher_stopped': False,
                'reason': 'NOT_RUNNING',
                'message': 'Hot reload watcher is not running.'
            }
        
        self.watcher_running = False
        
        if self.watcher_thread:
            self.watcher_thread.join(timeout=10)
        
        return {
            'watcher_stopped': True,
            'reason': None,
            'message': 'Hot reload watcher stopped successfully.'
        }
    
    def _watch_library_files_loop(self) -> None:
        """
        Main watcher loop
        Runs in separate thread, checks for file changes
        """
        self._initialize_file_modification_cache()
        
        while self.watcher_running:
            try:
                changes_detected = self._check_for_file_changes()
                
                if changes_detected:
                    self._trigger_library_reindex()
                
                time.sleep(self.check_interval_seconds)
            
            except Exception as e:
                self._log_watcher_error(str(e))
                time.sleep(self.check_interval_seconds)
    
    def _initialize_file_modification_cache(self) -> None:
        """
        Initialize cache of file modification times
        Baseline for detecting changes
        """
        self.file_modification_times_cache = {}
        
        if not self.libraries_base_path.exists():
            return
        
        for file_path in self.libraries_base_path.rglob('*'):
            if file_path.is_file():
                try:
                    mod_time = file_path.stat().st_mtime
                    self.file_modification_times_cache[str(file_path)] = mod_time
                except Exception:
                    pass
    
    def _check_for_file_changes(self) -> bool:
        """
        Check if any files have been added, modified, or deleted
        
        Returns:
            True if changes detected, False otherwise
        """
        if not self.libraries_base_path.exists():
            return False
        
        current_files = {}
        for file_path in self.libraries_base_path.rglob('*'):
            if file_path.is_file():
                try:
                    mod_time = file_path.stat().st_mtime
                    current_files[str(file_path)] = mod_time
                except Exception:
                    pass
        
        cached_files = set(self.file_modification_times_cache.keys())
        current_files_set = set(current_files.keys())
        
        added_files = current_files_set - cached_files
        deleted_files = cached_files - current_files_set
        
        modified_files = []
        for file_path in cached_files & current_files_set:
            if self.file_modification_times_cache[file_path] != current_files[file_path]:
                modified_files.append(file_path)
        
        changes_detected = len(added_files) > 0 or len(deleted_files) > 0 or len(modified_files) > 0
        
        if changes_detected:
            self._log_detected_changes(
                added=list(added_files),
                deleted=list(deleted_files),
                modified=modified_files
            )
            
            self.file_modification_times_cache = current_files
        
        return changes_detected
    
    def _trigger_library_reindex(self) -> None:
        """
        Trigger complete library re-indexing
        Called when changes are detected
        """
        reindex_timestamp = datetime.now().isoformat()
        
        try:
            reindex_result = self.library_indexer.index_all_library_assets_intent()
            
            self._log_reload_event(
                timestamp=reindex_timestamp,
                success=True,
                assets_indexed=reindex_result['total_assets_indexed']
            )
        
        except Exception as e:
            self._log_reload_event(
                timestamp=reindex_timestamp,
                success=False,
                error=str(e)
            )
    
    def _log_detected_changes(
        self,
        added: List[str],
        deleted: List[str],
        modified: List[str]
    ) -> None:
        """
        Log detected file changes
        
        Args:
            added: List of added file paths
            deleted: List of deleted file paths
            modified: List of modified file paths
        """
        print(f"[HOT_RELOAD] Changes detected:")
        if added:
            print(f"  Added: {len(added)} files")
        if deleted:
            print(f"  Deleted: {len(deleted)} files")
        if modified:
            print(f"  Modified: {len(modified)} files")
    
    def _log_reload_event(
        self,
        timestamp: str,
        success: bool,
        assets_indexed: Optional[int] = None,
        error: Optional[str] = None
    ) -> None:
        """
        Log reload event
        
        Args:
            timestamp: Event timestamp
            success: Whether reload succeeded
            assets_indexed: Number of assets indexed (if successful)
            error: Error message (if failed)
        """
        event = {
            'timestamp': timestamp,
            'success': success,
            'assets_indexed': assets_indexed,
            'error': error
        }
        
        self.reload_events_log.append(event)
        
        if len(self.reload_events_log) > 100:
            self.reload_events_log = self.reload_events_log[-100:]
        
        if success:
            print(f"[HOT_RELOAD] Library re-indexed successfully. Total assets: {assets_indexed}")
        else:
            print(f"[HOT_RELOAD] Re-indexing failed: {error}")
    
    def _log_watcher_error(self, error_message: str) -> None:
        """
        Log watcher error
        
        Args:
            error_message: Error description
        """
        print(f"[HOT_RELOAD] Watcher error: {error_message}")
    
    def get_watcher_status_intent(self) -> Dict[str, Any]:
        """
        Get current watcher status
        
        Returns:
            Watcher status information
        """
        return {
            'enabled': self.enabled,
            'running': self.watcher_running,
            'check_interval_seconds': self.check_interval_seconds,
            'monitored_path': str(self.libraries_base_path),
            'files_tracked': len(self.file_modification_times_cache),
            'reload_events_count': len(self.reload_events_log),
            'recent_reload_events': self.reload_events_log[-5:]
        }
    
    def get_reload_history_intent(self) -> List[Dict[str, Any]]:
        """
        Get reload event history
        
        Returns:
            List of reload events
        """
        return self.reload_events_log


def create_library_hot_reload_watcher(
    library_indexer,
    libraries_base_path: str = 'libraries',
    enabled: bool = False
) -> LibraryHotReloadWatcher:
    """
    Factory function to create hot reload watcher
    
    Args:
        library_indexer: Initialized library indexer instance
        libraries_base_path: Base path to library folders
        enabled: Whether hot reload is enabled
    
    Returns:
        Configured hot reload watcher
    """
    return LibraryHotReloadWatcher(
        library_indexer=library_indexer,
        libraries_base_path=libraries_base_path,
        enabled=enabled
    )
