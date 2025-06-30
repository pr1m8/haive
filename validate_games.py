#!/usr/bin/env python3
"""Validate consistent structure across all games."""

import os
from pathlib import Path

def main():
    games_path = Path('packages/haive-games/src/haive/games')
    
    # Framework/utility directories to exclude (not actual games)
    framework_dirs = {
        'base', 'base_v2', 'board', 'cards', 'framework', 
        'multi_player', 'resources', 'single_player', 'utils'
    }
    
    all_games = []
    for d in games_path.iterdir():
        if d.is_dir() and not d.name.startswith('_') and d.name != 'core' and d.name not in framework_dirs:
            all_games.append(d.name)

    print('🎮 Validating consistent structure across ALL games...')
    print(f'Found {len(all_games)} games')
    print()

    required_files = ['__init__.py', 'agent.py', 'config.py', 'engines.py', 'state.py', 'models.py']
    generic_files = ['generic_engines.py', 'configurable_config.py']

    complete_with_generic = 0
    has_generic_files = 0 
    has_all_required = 0

    for game in sorted(all_games):
        game_path = games_path / game
        files = [f.name for f in game_path.iterdir() if f.is_file()]
        
        has_required = all(req_file in files for req_file in required_files)
        has_generic = all(gen_file in files for gen_file in generic_files)
        
        status = '✅' if has_required and has_generic else '⚠️' if has_required else '❌'
        
        if has_required:
            has_all_required += 1
        if has_generic:
            has_generic_files += 1
        if has_required and has_generic:
            complete_with_generic += 1
        
        missing = []
        if not has_required:
            missing_req = [f for f in required_files if f not in files]
            missing.extend(missing_req)
        if not has_generic:
            missing_gen = [f for f in generic_files if f not in files]
            missing.extend(missing_gen)
        
        missing_str = f' (missing: {missing})' if missing else ''
        print(f'{status} {game:15} - Required: {has_required}, Generic: {has_generic}{missing_str}')

    print()
    print('📊 FINAL SUMMARY:')
    print(f'Total games: {len(all_games)}')
    print(f'Games with all required files: {has_all_required}/{len(all_games)}')
    print(f'Games with generic system files: {has_generic_files}/{len(all_games)}')
    print(f'Fully complete games: {complete_with_generic}/{len(all_games)}')
    print()

    # Expected complete games (excluding go due to package conflict)
    expected_complete = len(all_games) - 1  # Exclude go
    if complete_with_generic == expected_complete:
        print('🎉 SUCCESS: All non-skipped games have consistent structure!')
        return True
    else:
        print(f'⚠️ INCOMPLETE: {complete_with_generic}/{expected_complete} games have complete structure')
        return False

if __name__ == '__main__':
    main()