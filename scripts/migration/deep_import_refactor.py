# scripts/migration/deep_import_refactor.py
#!/usr/bin/env python3
# Advanced import refactoring script

import ast
import sys
import os
from pathlib import Path
import astor

class ImportTransformer(ast.NodeTransformer):
    def __init__(self, import_map):
        self.import_map = import_map
        self.changes = 0
    
    def visit_Import(self, node):
        new_names = []
        for name in node.names:
            for old_path, new_path in self.import_map.items():
                if name.name == old_path or name.name.startswith(old_path + '.'):
                    suffix = name.name[len(old_path):] if name.name.startswith(old_path + '.') else ''
                    new_name = new_path + suffix
                    new_names.append(ast.alias(name=new_name, asname=name.asname))
                    self.changes += 1
                    break
            else:
                new_names.append(name)
        
        node.names = new_names
        return node
    
    def visit_ImportFrom(self, node):
        if node.module:
            for old_path, new_path in self.import_map.items():
                if node.module == old_path or node.module.startswith(old_path + '.'):
                    suffix = node.module[len(old_path):] if node.module.startswith(old_path + '.') else ''
                    node.module = new_path + suffix
                    self.changes += 1
                    break
        return node

def refactor_file(file_path, import_map):
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        
        tree = ast.parse(source)
        transformer = ImportTransformer(import_map)
        tree = transformer.visit(tree)
        
        if transformer.changes > 0:
            print(f"Made {transformer.changes} import changes in {file_path}")
            with open(file_path, 'w') as f:
                f.write(astor.to_source(tree))
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python deep_import_refactor.py <directory_or_file> [package_map.txt]")
        sys.exit(1)
    
    path = sys.argv[1]
    
    # Default import mappings
    import_map = {
        'src.haive.core': 'haive_core',
        'src.haive.agents': 'haive_agents',
        'src.haive.games': 'haive_games',
        'src.haive.tak': 'haive_tools',
        'src.haive.prebuilt': 'haive_prebuilt',
        'src.haive.dataflow': 'haive_dataflow'
    }
    
    # Load custom mapping if provided
    if len(sys.argv) > 2:
        map_file = sys.argv[2]
        with open(map_file, 'r') as f:
            for line in f:
                if ':' in line:
                    old, new = line.strip().split(':', 1)
                    import_map[old.strip()] = new.strip()
    
    # Process files
    if os.path.isfile(path):
        refactor_file(path, import_map)
    else:
        for file_path in Path(path).rglob('*.py'):
            refactor_file(file_path, import_map)

if __name__ == "__main__":
    main()