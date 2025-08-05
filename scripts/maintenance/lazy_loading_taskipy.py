#!/usr/bin/env python3
"""Taskipy-friendly wrapper for lazy loading deployment.

This script provides simple commands that work well with taskipy and
provide excellent user experience with clear feedback and dry-run
capabilities.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from safe_lazy_loading_deployment import SafeLazyLoadingDeployment

# Add the scripts directory to the path
sys.path.insert(0, str(Path(__file__).parent))


def show_banner():
    """Show a nice banner for lazy loading operations."""
    print('🦥' * 20)
    print('🦥  HAIVE LAZY LOADING MANAGER  🦥')
    print('🦥' * 20)


def lazy_loading_dry_run():
    """Run lazy loading in dry-run mode (for taskipy)."""
    show_banner()
    print('🔍 DRY RUN MODE - No files will be modified')
    print('=' * 50)

    deployer = SafeLazyLoadingDeployment(dry_run=True)

    # Find files to process
    base = Path('/home/will/Projects/haive/backend/haive/packages')
    files = [
        base / 'haive-core/src/haive/core/models/__init__.py',
        base / 'haive-core/src/haive/core/tools/__init__.py',
        base / 'haive-agents/src/haive/agents/__init__.py',
    ]
    # Filter to existing files
    files = [f for f in files if f.exists()]

    print(f"📁 Would process {len(files)} files:")
    for f in files:
        print(f"   - {f.relative_to(Path.cwd())}")

    print('\n🧪 Running pre-deployment tests...')
    if deployer.test_imports_before_deployment(files):
        print('✅ All tests passed - deployment would be safe!')
        print('\n💡 To actually deploy, run: poetry run task lazy-loading-deploy')
        return True
    print('❌ Tests failed - deployment not recommended')
    return False


def lazy_loading_test_only():
    """Test imports without deploying (for taskipy)."""
    show_banner()
    print('🧪 TEST ONLY MODE - Checking if deployment would be safe')
    print('=' * 50)

    deployer = SafeLazyLoadingDeployment(dry_run=False)

    # Find files to process
    base = Path('/home/will/Projects/haive/backend/haive/packages')
    files = [
        base / 'haive-core/src/haive/core/models/__init__.py',
        base / 'haive-core/src/haive/core/tools/__init__.py',
        base / 'haive-agents/src/haive/agents/__init__.py',
    ]
    files = [f for f in files if f.exists()]

    print(f"📁 Testing {len(files)} files:")
    for f in files:
        print(f"   - {f.relative_to(Path.cwd())}")

    success = deployer.test_imports_before_deployment(files)

    if success:
        print('\n🎉 All import tests passed!')
        print('✅ Lazy loading deployment would be safe')
        print("💡 Run 'poetry run task lazy-loading-deploy' to deploy")
    else:
        print('\n❌ Import tests failed')
        print('⚠️  Lazy loading deployment not recommended')

    return success


def lazy_loading_deploy():
    """Deploy lazy loading with full safety checks (for taskipy)."""
    show_banner()
    print('🚀 DEPLOYMENT MODE - Applying lazy loading with full safety')
    print('=' * 50)

    # Check if running in dry-run mode via environment
    env_dry_run = os.getenv('DRY_RUN', '').lower() in ('1', 'true', 'yes')
    if env_dry_run:
        print('🔍 DRY_RUN environment variable detected')
        return lazy_loading_dry_run()

    deployer = SafeLazyLoadingDeployment(dry_run=False)

    # Find files to process
    base = Path('/home/will/Projects/haive/backend/haive/packages')
    files = [
        base / 'haive-core/src/haive/core/models/__init__.py',
        base / 'haive-core/src/haive/core/tools/__init__.py',
        base / 'haive-agents/src/haive/agents/__init__.py',
    ]
    files = [f for f in files if f.exists()]

    print(f"📁 Deploying to {len(files)} files:")
    for f in files:
        print(f"   - {f.relative_to(Path.cwd())}")

    try:
        # Create safety backups
        deployer.create_git_checkpoint()
        backups = deployer.create_file_backups(files)

        # Pre-deployment testing
        if not deployer.test_imports_before_deployment(files):
            raise Exception('Pre-deployment tests failed')

        # Deploy files
        deployment_success = deployer.deploy_incremental(files, test_after_each=True)

        if not deployment_success:
            raise Exception('Deployment failed')

        # Post-deployment testing
        if not deployer.test_imports_after_deployment(files):
            raise Exception('Post-deployment tests failed')

        print('\n🎉 Deployment successful!')
        print(f"📋 Deployment ID: {deployer.deployment_id}")
        print(f"💾 Backups saved in: {deployer.backup_dir}")
        print(
            '🧪 Run Sphinx to test: poetry run sphinx-build -b html docs/source docs/build/html',
        )

        return True

    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        print('🔄 Initiating automatic rollback...')

        # Attempt rollback
        rollback_success = deployer.rollback_from_backups(backups)

        if rollback_success:
            print('✅ Automatic rollback successful')
        else:
            print('⚠️  Rollback failed - manual recovery may be needed')
            print(f"💾 Backups available in: {deployer.backup_dir}")

        return False

    finally:
        deployer.save_deployment_log()


def lazy_loading_rollback():
    """Show available backups and rollback options (for taskipy)."""
    show_banner()
    print('🔄 ROLLBACK MODE - Showing available backups')
    print('=' * 50)

    deployer = SafeLazyLoadingDeployment()

    # List available backups
    if deployer.backup_dir.exists():
        manifests = list(deployer.backup_dir.glob('manifest_*.json'))
        if manifests:
            print(f"📦 Available backups in {deployer.backup_dir}:")
            import json

            for manifest in sorted(manifests, reverse=True)[:10]:  # Show last 10
                with open(manifest) as f:
                    data = json.load(f)
                print(
                    f"   🗂️  {data['deployment_id']} - {data['timestamp'][:19]} ({len(data['backups'])} files)",
                )

            print('\n💡 To rollback:')
            print(
                '   poetry run python scripts/maintenance/safe_lazy_loading_deployment.py --rollback DEPLOYMENT_ID',
            )
        else:
            print('📭 No backups found')
    else:
        print("📂 Backup directory doesn't exist yet")


if __name__ == '__main__':
    # Simple command dispatcher
    command = sys.argv[1] if len(sys.argv) > 1 else 'help'

    if command == 'dry':
        sys.exit(0 if lazy_loading_dry_run() else 1)
    elif command == 'test':
        sys.exit(0 if lazy_loading_test_only() else 1)
    elif command == 'deploy':
        sys.exit(0 if lazy_loading_deploy() else 1)
    elif command == 'rollback':
        lazy_loading_rollback()
        sys.exit(0)
    else:
        print('Usage: python lazy_loading_taskipy.py {dry|test|deploy|rollback}')
        sys.exit(1)
