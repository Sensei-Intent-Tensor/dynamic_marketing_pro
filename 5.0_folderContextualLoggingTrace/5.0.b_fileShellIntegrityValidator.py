#!/usr/bin/env python3
"""
5.0.b_fileShellIntegrityValidator.py

SHELL INTEGRITY VALIDATOR
Validates codebase integrity against Diamond Standard
Detects ghost code, ambiguous naming, and malicious patterns

PRINCIPLE: Ghost code screams
Any deviation from ghostless naming is immediately detected
Malicious code cannot hide in this architecture
"""

from typing import Dict, Any, List, Tuple, Set
from pathlib import Path
import re
import ast


class ShellIntegrityValidator:
    """
    Shell integrity validator
    Enforces Diamond Standard compliance
    Detects ghost code and naming violations
    """
    
    def __init__(self):
        self.validation_results_history = []
        self.ghost_code_patterns_detected = []
        
        self.ghostless_naming_patterns = [
            r'.*_intent$',
            r'.*Intent$',
            r'.*_engine$',
            r'.*Engine$',
            r'.*_validator$',
            r'.*Validator$',
            r'.*_resolver$',
            r'.*Resolver$',
            r'.*_compositor$',
            r'.*Compositor$',
            r'.*_orchestrator$',
            r'.*Orchestrator$',
            r'.*_indexer$',
            r'.*Indexer$',
            r'.*_logger$',
            r'.*Logger$',
            r'.*_gatekeeper$',
            r'.*Gatekeeper$',
            r'.*_firewall$',
            r'.*Firewall$'
        ]
        
        self.ghost_code_warning_patterns = [
            'def process(',
            'def handle(',
            'def do_',
            'def execute(',
            'def run(',
            'def perform(',
            'def manage(',
            'def update(',
            'def get(',
            'def set(',
            'data =',
            'result =',
            'temp =',
            'value =',
            'item =',
            'obj ='
        ]
    
    def validate_codebase_integrity_against_diamond_standard_intent(
        self,
        codebase_path: str
    ) -> Dict[str, Any]:
        """
        CRITICAL: Validate entire codebase against Diamond Standard
        Scans all Python files for ghostless compliance
        
        Args:
            codebase_path: Root path of codebase to validate
        
        Returns:
            Complete validation report
        """
        from datetime import datetime
        
        validation_timestamp = datetime.now().isoformat()
        
        codebase_path_obj = Path(codebase_path)
        
        if not codebase_path_obj.exists():
            return {
                'validation_success': False,
                'error': 'CODEBASE_PATH_NOT_FOUND',
                'timestamp': validation_timestamp
            }
        
        python_files = list(codebase_path_obj.rglob('*.py'))
        
        validation_results = {
            'total_files_scanned': len(python_files),
            'compliant_files': [],
            'non_compliant_files': [],
            'ghost_code_detections': [],
            'ambiguous_naming_detections': [],
            'validation_timestamp': validation_timestamp
        }
        
        for python_file in python_files:
            file_validation = self._validate_file_integrity_intent(python_file)
            
            if file_validation['compliant']:
                validation_results['compliant_files'].append(str(python_file))
            else:
                validation_results['non_compliant_files'].append({
                    'file_path': str(python_file),
                    'violations': file_validation['violations']
                })
            
            validation_results['ghost_code_detections'].extend(
                file_validation.get('ghost_code_patterns', [])
            )
            
            validation_results['ambiguous_naming_detections'].extend(
                file_validation.get('ambiguous_names', [])
            )
        
        compliance_percentage = (
            len(validation_results['compliant_files']) / 
            validation_results['total_files_scanned'] * 100
        ) if validation_results['total_files_scanned'] > 0 else 0
        
        validation_results['compliance_percentage'] = compliance_percentage
        validation_results['diamond_standard_achieved'] = compliance_percentage >= 95
        
        self.validation_results_history.append(validation_results)
        
        return validation_results
    
    def _validate_file_integrity_intent(
        self,
        file_path: Path
    ) -> Dict[str, Any]:
        """
        Validate single file for Diamond Standard compliance
        
        Args:
            file_path: Path to Python file
        
        Returns:
            File validation result
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
        except Exception as e:
            return {
                'compliant': False,
                'violations': [f'FILE_READ_ERROR: {str(e)}'],
                'ghost_code_patterns': [],
                'ambiguous_names': []
            }
        
        violations = []
        ghost_code_patterns = []
        ambiguous_names = []
        
        try:
            tree = ast.parse(file_content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_name = node.name
                    
                    if function_name.startswith('_') and not function_name.startswith('__'):
                        continue
                    
                    if not self._is_ghostless_name(function_name):
                        ambiguous_names.append({
                            'type': 'FUNCTION',
                            'name': function_name,
                            'line': node.lineno,
                            'reason': 'DOES_NOT_FOLLOW_GHOSTLESS_PATTERN'
                        })
                        violations.append(f"Function '{function_name}' at line {node.lineno} violates ghostless naming")
                
                elif isinstance(node, ast.ClassDef):
                    class_name = node.name
                    
                    if not self._is_ghostless_name(class_name):
                        ambiguous_names.append({
                            'type': 'CLASS',
                            'name': class_name,
                            'line': node.lineno,
                            'reason': 'DOES_NOT_FOLLOW_GHOSTLESS_PATTERN'
                        })
                        violations.append(f"Class '{class_name}' at line {node.lineno} violates ghostless naming")
        
        except SyntaxError as e:
            violations.append(f'SYNTAX_ERROR: {str(e)}')
        
        for pattern in self.ghost_code_warning_patterns:
            if pattern in file_content:
                ghost_code_patterns.append({
                    'pattern': pattern,
                    'file': str(file_path),
                    'occurrences': file_content.count(pattern)
                })
        
        is_compliant = len(violations) == 0 and len(ghost_code_patterns) == 0
        
        return {
            'compliant': is_compliant,
            'violations': violations,
            'ghost_code_patterns': ghost_code_patterns,
            'ambiguous_names': ambiguous_names
        }
    
    def _is_ghostless_name(self, name: str) -> bool:
        """
        Check if name follows ghostless naming patterns
        
        Args:
            name: Function or class name to check
        
        Returns:
            True if name is ghostless compliant
        """
        for pattern in self.ghostless_naming_patterns:
            if re.match(pattern, name):
                return True
        
        return False
    
    def detect_malicious_code_patterns_intent(
        self,
        codebase_path: str
    ) -> Dict[str, Any]:
        """
        Scan for malicious code patterns
        Detects common attack vectors
        
        Args:
            codebase_path: Root path to scan
        
        Returns:
            Malicious pattern detection report
        """
        from datetime import datetime
        
        scan_timestamp = datetime.now().isoformat()
        
        malicious_patterns = [
            (r'eval\(', 'DANGEROUS_EVAL'),
            (r'exec\(', 'DANGEROUS_EXEC'),
            (r'__import__\(', 'DYNAMIC_IMPORT'),
            (r'os\.system\(', 'SYSTEM_COMMAND_EXECUTION'),
            (r'subprocess\.', 'SUBPROCESS_USAGE'),
            (r'open\(.*(\'w\'|"w")', 'FILE_WRITE_OPERATION'),
            (r'pickle\.loads', 'PICKLE_DESERIALIZATION'),
            (r'requests\.get\(', 'HTTP_REQUEST'),
            (r'socket\.', 'SOCKET_USAGE')
        ]
        
        codebase_path_obj = Path(codebase_path)
        python_files = list(codebase_path_obj.rglob('*.py'))
        
        detections = []
        
        for python_file in python_files:
            try:
                with open(python_file, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                for pattern, threat_type in malicious_patterns:
                    matches = re.finditer(pattern, file_content)
                    for match in matches:
                        line_number = file_content[:match.start()].count('\n') + 1
                        
                        detections.append({
                            'file': str(python_file),
                            'line': line_number,
                            'threat_type': threat_type,
                            'pattern_matched': pattern,
                            'context': file_content[max(0, match.start()-50):match.end()+50]
                        })
            
            except Exception:
                pass
        
        return {
            'scan_timestamp': scan_timestamp,
            'total_files_scanned': len(python_files),
            'detections_count': len(detections),
            'detections': detections,
            'threat_level': 'HIGH' if len(detections) > 0 else 'LOW'
        }
    
    def validate_function_naming_consistency_intent(
        self,
        codebase_path: str
    ) -> Dict[str, Any]:
        """
        Validate that function names are consistent and descriptive
        Ensures all functions follow intent-based naming
        
        Args:
            codebase_path: Root path to validate
        
        Returns:
            Function naming validation report
        """
        codebase_path_obj = Path(codebase_path)
        python_files = list(codebase_path_obj.rglob('*.py'))
        
        all_functions = []
        
        for python_file in python_files:
            try:
                with open(python_file, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                tree = ast.parse(file_content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        all_functions.append({
                            'name': node.name,
                            'file': str(python_file),
                            'line': node.lineno,
                            'is_ghostless': self._is_ghostless_name(node.name)
                        })
            
            except Exception:
                pass
        
        ghostless_functions = [f for f in all_functions if f['is_ghostless']]
        ghost_functions = [f for f in all_functions if not f['is_ghostless']]
        
        compliance_rate = (
            len(ghostless_functions) / len(all_functions) * 100
        ) if len(all_functions) > 0 else 0
        
        return {
            'total_functions': len(all_functions),
            'ghostless_functions': len(ghostless_functions),
            'ghost_functions': len(ghost_functions),
            'compliance_rate': compliance_rate,
            'ghost_function_details': ghost_functions[:20]
        }
    
    def get_validation_history_intent(
        self,
        count: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get validation history
        
        Args:
            count: Number of historical validations to retrieve
        
        Returns:
            List of validation results
        """
        return self.validation_results_history[-count:]


shell_integrity_validator_singleton = ShellIntegrityValidator()


def get_shell_integrity_validator() -> ShellIntegrityValidator:
    """
    Accessor for shell integrity validator
    Ensures single source of truth for integrity validation
    """
    return shell_integrity_validator_singleton
