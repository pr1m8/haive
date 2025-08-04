#!/usr/bin/env python3
"""Haive Namespace Migration Script.

This script migrates the Haive framework from package-style imports (haive.core)
to namespace package imports (haive.core). It handles both directory structure
reorganization and import statement updates across multiple submodules.

Features:
- Migrates directory structure from src/haive_* to src/haive/*
- Updates import statements throughout the codebase
- Handles centralization of logs, resources, and other common directories
- Updates package configuration in pyproject.toml files
- Works with git submodules
- Provides detailed logging and error handling
- Includes dry-run mode to preview changes

Usage:
    python namespace_migration.py [options]

Options:
    --dry-run       Show what would be done without making changes
    --submodule=X   Only process the specified submodule (e.g., haive-core)
    --no-central    Skip centralizing common directories
    --no-imports    Skip updating import statements
    --no-structure  Skip migrating directory structure
    --no-pyproject  Skip updating pyproject.toml files
    --no-commit     Skip committing changes to git
"""
from __future__ import annotations

import argparse
import logging
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import tomli
import tomli_w

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('namespace_migration.log')
    ],
)
logger = logging.getLogger('migration')

# Mapping of old to new module paths
MODULE_MAPPING = {
    'haive.core': 'haive.core',
    'haive_agents': 'haive.agents',
    'haive_games': 'haive.games',
    'haive_dataflow': 'haive.dataflow',
    'haive_prebuilt': 'haive.prebuilt',
    'haive_tools': 'haive.tools',
}

# Common directories to centralize
COMMON_DIRS = {
    'logs': 'logs',
    'resources': 'resources',
    'graphs': 'resources/graphs',
    'test_output': 'test_outputs',
    'test_outputs': 'test_outputs',
    'allure-results': 'test_outputs/allure-results',
}


class GitStatus:
    """Helper class to track git status and operations."""

    def __init__(self, repo_path, dry_run=False):
        self.repo_path = Path(repo_path)
        self.dry_run = dry_run

    def run_git(self, cmd, silent=False):
        """Run a git command."""
        full_cmd = f"git -C {self.repo_path} {cmd}"
        if self.dry_run and not silent:
            logger.info(f"[DRY RUN] Would execute: {full_cmd}")
            return ''

        try:
            result = subprocess.run(
                full_cmd,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                text=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            if not silent:
                logger.exception(f"Git command failed: {full_cmd}")
                logger.exception(f"Error: {e.stderr}")
            return None

    def is_submodule(self):
        """Check if the path is a git submodule."""
        # If it has its own .git directory or file, it's a repo
        return bool((self.repo_path / '.git').exists())

    def get_current_branch(self):
        """Get the current branch name."""
        return self.run_git('rev-parse --abbrev-ref HEAD', silent=True)

    def create_branch(self, branch_name):
        """Create a new branch."""
        # Check if branch exists
        branches = self.run_git('branch --list', silent=True)
        if branches and branch_name in branches:
            logger.info(f"Branch {branch_name} already exists")
            # Switch to branch
            self.run_git(f"checkout {branch_name}")
            return True

        # Create and switch to the branch
        result = self.run_git(f"checkout -b {branch_name}")
        return result is not None

    def stage_changes(self, paths=None):
        """Stage changes for commit."""
        if paths:
            for path in paths:
                self.run_git(f"add {path}")
        else:
            self.run_git('add .')

    def commit_changes(self, message):
        """Commit staged changes."""
        return self.run_git(f'commit -m "{message}"')

    def has_changes(self):
        """Check if there are uncommitted changes."""
        return self.run_git('status --porcelain', silent=True) != ''


class PackageMigrator:
    """Handles migration of a single package."""

    def __init__(self, package_path, root_path=None, dry_run=False):
        self.package_path = Path(package_path)
        self.package_name = self.package_path.name
        self.root_path = Path(
            root_path) if root_path else self.package_path.parent.parent
        self.dry_run = dry_run
        self.git = GitStatus(self.package_path, dry_run)
        self.old_module_name = self._get_old_module_name()
        self.new_module_name = MODULE_MAPPING.get(
            self.old_module_name,
            f"haive.{self.old_module_name.replace('haive_', '')}",
        )

        # Make paths absolute
        self.src_path = self.package_path / 'src'
        self.old_module_path = self.src_path / self.old_module_name
        self.new_base_path = self.src_path / 'haive'
        self.new_module_path = self.src_path / self.new_module_name.replace(
            '.', '/')

        # Track what we've done
        self.structure_migrated = False
        self.imports_updated = False
        self.pyproject_updated = False

    def _get_old_module_name(self):
        """Determine the old module name based on directory structure."""
        # Check for existing module directories
        src_path = self.package_path / 'src'
        if not src_path.exists():
            logger.warning(f"No src directory found in {self.package_path}")
            # Try to guess based on package name
            package_part = self.package_name.replace('haive-', '')
            return f"haive_{package_part}"

        # Look for haive_* directories
        for item in src_path.iterdir():
            if item.is_dir() and item.name.startswith('haive_'):
                return item.name

        # Maybe already migrated? Look for haive/package directories
        haive_dir = src_path / 'haive'
        if haive_dir.exists() and haive_dir.is_dir():
            for item in haive_dir.iterdir():
                if item.is_dir():
                    # Get the root package name
                    package_part = self.package_name.replace('haive-', '')
                    if item.name == package_part:
                        logger.info(
                            f"Found already migrated directory: haive/{item.name}",
                        )
                        return f"haive_{item.name}"

        # Fallback to guessing based on package name
        package_part = self.package_name.replace('haive-', '')
        return f"haive_{package_part}"

    def migrate_structure(self):
        """Migrate directory structure from haive_* to haive/package."""
        if not self.old_module_path.exists():
            logger.warning(
                f"Old module path does not exist: {self.old_module_path}")

            # Check if already migrated
            if self.new_module_path.exists():
                logger.info(
                    f"Directory already migrated: {self.new_module_path}")
                self.structure_migrated = True
                return True

            return False

        logger.info(
            f"Migrating {self.old_module_path} to {self.new_module_path}")

        # Create new module path
        if not self.dry_run:
            self.new_module_path.parent.mkdir(parents=True, exist_ok=True)

            # Create empty __init__.py in haive directory for namespace packages
            with open(self.new_base_path / '__init__.py', 'w') as f:
                f.write('# Namespace package\n')

            # Move files
            if self.old_module_path.exists(
            ) and not self.new_module_path.exists():
                try:
                    shutil.move(str(self.old_module_path),
                                str(self.new_module_path))
                    logger.info(
                        f"Moved {self.old_module_path} to {self.new_module_path}",
                    )
                except (OSError, shutil.Error) as e:
                    logger.exception(f"Error moving directory: {e}")
                    return False

            # Remove old module path if empty
            if self.old_module_path.exists() and not any(
                    self.old_module_path.iterdir(), ):
                try:
                    self.old_module_path.rmdir()
                    logger.info(
                        f"Removed empty directory: {self.old_module_path}")
                except OSError as e:
                    logger.warning(f"Could not remove old directory: {e}")

        self.structure_migrated = True
        return True

    def update_imports(self):
        """Update import statements throughout the package."""
        if not self.new_module_path.exists():
            logger.warning(
                f"New module path does not exist: {self.new_module_path}")
            return False

        logger.info(f"Updating imports in {self.new_module_path}")

        # Patterns to search for and their replacements
        patterns = []
        for old_mod, new_mod in MODULE_MAPPING.items():
            patterns.extend([
                (rf"from\s+{old_mod}(\s+|\.)(?!_)", f"from {new_mod}\\1"),
                (rf"import\s+{old_mod}(\s+|$|\.)", f"import {new_mod}\\1"),
            ], )

        # Walk through all Python files
        files_updated = 0
        for py_file in self.new_module_path.glob('**/*.py'):
            try:
                with open(py_file, encoding='utf-8') as f:
                    content = f.read()

                # Apply all replacements
                new_content = content
                for pattern, replacement in patterns:
                    new_content = re.sub(pattern, replacement, new_content)

                # Write back if changed
                if new_content != content:
                    if not self.dry_run:
                        with open(py_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                    files_updated += 1
                    logger.debug(f"Updated imports in {py_file}")
            except Exception as e:
                logger.exception(f"Error updating imports in {py_file}: {e}")

        logger.info(f"Updated imports in {files_updated} files")
        self.imports_updated = files_updated > 0
        return True

    def update_pyproject(self):
        """Update the pyproject.toml file for namespace packages."""
        pyproject_path = self.package_path / 'pyproject.toml'
        if not pyproject_path.exists():
            logger.warning(f"No pyproject.toml found in {self.package_path}")
            return False

        logger.info(f"Updating {pyproject_path}")

        try:
            # Read the pyproject.toml file
            with open(pyproject_path, 'rb') as f:
                pyproject = tomli.load(f)

            # Check if using poetry
            is_poetry = 'tool' in pyproject and 'poetry' in pyproject['tool']

            # Update package configuration
            if is_poetry:
                # Poetry configuration
                if 'packages' not in pyproject['tool']['poetry']:
                    pyproject['tool']['poetry']['packages'] = [
                        {
                            'include': 'haive',
                            'from': 'src'
                        },
                    ]
                else:
                    # Update existing packages entry if needed
                    needs_update = True
                    for _i, pkg in enumerate(
                            pyproject['tool']['poetry']['packages']):
                        if pkg.get('include') == 'haive' and pkg.get(
                                'from') == 'src':
                            needs_update = False
                            break

                    if needs_update:
                        pyproject['tool']['poetry']['packages'].append(
                            {
                                'include': 'haive',
                                'from': 'src'
                            }, )
            else:
                # Setuptools configuration
                if 'tool' not in pyproject:
                    pyproject['tool'] = {}

                if 'setuptools' not in pyproject['tool']:
                    pyproject['tool']['setuptools'] = {}

                pyproject['tool']['setuptools']['packages'] = ['haive']
                pyproject['tool']['setuptools']['package-dir'] = {'': 'src'}

            # Write back the updated pyproject.toml
            if not self.dry_run:
                with open(pyproject_path, 'wb') as f:
                    tomli_w.dump(pyproject, f)
                logger.info(f"Updated {pyproject_path}")

            self.pyproject_updated = True
            return True

        except Exception as e:
            logger.exception(f"Error updating pyproject.toml: {e}")
            return False

    def centralize_common_dirs(self, central_root):
        """Move common directories to a central location."""
        central_root = Path(central_root)

        for dir_name, central_path in COMMON_DIRS.items():
            src_dir = self.package_path / dir_name
            if not src_dir.exists() or not src_dir.is_dir():
                continue

            logger.info(f"Centralizing {dir_name} from {self.package_name}")

            # Setup destination (package-specific subfolder in central directory)
            dest_dir = central_root / central_path / self.package_name
            if not self.dry_run:
                dest_dir.parent.mkdir(parents=True, exist_ok=True)
                dest_dir.mkdir(exist_ok=True)

            # Move content
            try:
                for item in src_dir.iterdir():
                    dest_item = dest_dir / item.name
                    logger.debug(f"Moving {item} to {dest_item}")

                    if not self.dry_run:
                        if item.is_file():
                            shutil.copy2(item, dest_item)
                            os.remove(item)
                        elif item.is_dir():
                            shutil.copytree(item,
                                            dest_item,
                                            dirs_exist_ok=True)
                            shutil.rmtree(item)

                # Remove original directory if empty
                if not self.dry_run and src_dir.exists() and not any(
                        src_dir.iterdir()):
                    src_dir.rmdir()
                    logger.debug(f"Removed empty directory: {src_dir}")

                # Create symlink if requested
                symlink_path = src_dir
                if not self.dry_run and not symlink_path.exists():
                    # Create relative symlink
                    rel_path = os.path.relpath(str(dest_dir),
                                               str(symlink_path.parent))
                    os.symlink(rel_path,
                               str(symlink_path),
                               target_is_directory=True)
                    logger.debug(
                        f"Created symlink: {symlink_path} -> {rel_path}")

            except Exception as e:
                logger.exception(f"Error centralizing {dir_name}: {e}")

    def commit_changes(self):
        """Commit changes to git if there are any."""
        if self.dry_run:
            logger.info('[DRY RUN] Would commit changes')
            return True

        if not self.git.has_changes():
            logger.info('No changes to commit')
            return True

        logger.info('Committing changes to git')

        # Stage all changes
        self.git.stage_changes()

        # Build commit message based on what we've done
        message_parts = []
        if self.structure_migrated:
            message_parts.append('directory structure')
        if self.imports_updated:
            message_parts.append('imports')
        if self.pyproject_updated:
            message_parts.append('pyproject.toml')

        message = 'Migrate to namespace package: ' + ', '.join(message_parts)
        return self.git.commit_changes(message) is not None

    def migrate(
        self,
        central_root=None,
        skip_structure=False,
        skip_imports=False,
        skip_pyproject=False,
        skip_central=False,
        skip_commit=False,
    ):
        """Perform the complete migration process."""
        logger.info(f"Migrating package: {self.package_name}")

        # Create migration branch
        if not self.git.create_branch('namespace-migration'):
            logger.error(
                f"Failed to create or switch to migration branch for {
                    self.package_name}", )
            return False

        # Steps to perform
        success = True

        # 1. Directory structure migration
        if not skip_structure and not self.migrate_structure():
            logger.warning(
                f"Structure migration failed for {self.package_name}")
            success = False

        # 2. Import statement updates
        if not skip_imports and not self.update_imports():
            logger.warning(f"Import updates failed for {self.package_name}")
            # Non-critical failure

        # 3. Pyproject.toml updates
        if not skip_pyproject and not self.update_pyproject():
            logger.warning(
                f"pyproject.toml update failed for {self.package_name}")
            # Non-critical failure

        # 4. Centralize common directories
        if not skip_central and central_root:
            self.centralize_common_dirs(central_root)

        # 5. Commit changes
        if success and not skip_commit and not self.commit_changes():
            logger.warning(f"Failed to commit changes for {self.package_name}")
            # Non-critical failure

        return success


class RootPackageMigrator:
    """Handles migration of the root package."""

    def __init__(self, root_path, dry_run=False):
        self.root_path = Path(root_path)
        self.dry_run = dry_run
        self.git = GitStatus(self.root_path, dry_run)

    def create_central_dirs(self):
        """Create central directories for common resources."""
        logger.info('Creating central directories')

        for central_dir in set(COMMON_DIRS.values()):
            central_path = self.root_path / central_dir
            if not central_path.exists():
                logger.info(f"Creating directory: {central_path}")
                if not self.dry_run:
                    central_path.mkdir(parents=True, exist_ok=True)

    def create_root_package(self):
        """Create or update the root package."""
        logger.info('Setting up root package')

        # Create directory structure
        src_dir = self.root_path / 'src'
        haive_dir = src_dir / 'haive'

        if not self.dry_run:
            src_dir.mkdir(exist_ok=True)
            haive_dir.mkdir(exist_ok=True)

        # Create root __init__.py
        init_path = haive_dir / '__init__.py'
        init_content = """\"\"\"Haive - Agent Framework and Ecosystem.\"\"\"

__version__ = "0.1.0"

# Import from submodules
try:
    from haive.core import *
except ImportError:
    pass

try:
    from haive.agents import *
except ImportError:
    pass

try:
    from haive.games import *
except ImportError:
    pass

try:
    from haive.dataflow import *
except ImportError:
    pass

try:
    from haive.prebuilt import *
except ImportError:
    pass

try:
    from haive.tools import *
except ImportError:
    pass
"""

        if not self.dry_run:
            with open(init_path, 'w') as f:
                f.write(init_content)
            logger.info(f"Created {init_path}")

        # Create or update pyproject.toml
        pyproject_path = self.root_path / 'pyproject.toml'

        if pyproject_path.exists():
            # Update existing file
            try:
                with open(pyproject_path, 'rb') as f:
                    pyproject = tomli.load(f)

                # Check if using poetry
                is_poetry = 'tool' in pyproject and 'poetry' in pyproject[
                    'tool']

                if is_poetry:
                    # Update poetry configuration
                    if 'packages' not in pyproject['tool']['poetry']:
                        pyproject['tool']['poetry']['packages'] = [
                            {
                                'include': 'haive',
                                'from': 'src'
                            },
                        ]
                else:
                    # Update setuptools configuration
                    if 'tool' not in pyproject:
                        pyproject['tool'] = {}

                    if 'setuptools' not in pyproject['tool']:
                        pyproject['tool']['setuptools'] = {}

                    pyproject['tool']['setuptools']['packages'] = ['haive']
                    pyproject['tool']['setuptools']['package-dir'] = {
                        '': 'src'
                    }

                # Update dependencies
                if 'project' in pyproject and 'dependencies' in pyproject[
                        'project']:
                    # Add optional dependencies for sub-packages
                    if 'optional-dependencies' not in pyproject['project']:
                        pyproject['project']['optional-dependencies'] = {}

                    optional_deps = pyproject['project'][
                        'optional-dependencies']

                    for package in [
                            'agents', 'games', 'dataflow', 'tools', 'prebuilt'
                    ]:
                        if package not in optional_deps:
                            optional_deps[package] = [f"haive-{package}"]

                    if 'all' not in optional_deps:
                        optional_deps['all'] = [
                            'haive-agents',
                            'haive-games',
                            'haive-dataflow',
                            'haive-tools',
                            'haive-prebuilt',
                        ]

                # Write back
                if not self.dry_run:
                    with open(pyproject_path, 'wb') as f:
                        tomli_w.dump(pyproject, f)
                    logger.info(f"Updated {pyproject_path}")

            except Exception as e:
                logger.exception(f"Error updating pyproject.toml: {e}")

        else:
            # Create new file
            pyproject_content = {
                'build-system': {
                    'requires': ['setuptools>=61.0', 'wheel'],
                    'build-backend': 'setuptools.build_meta',
                },
                'project': {
                    'name': 'haive',
                    'version': '0.1.0',
                    'description': 'Haive - Agent Framework and Ecosystem',
                    'dependencies': ['haive-core'],
                    'optional-dependencies': {
                        'agents': ['haive-agents'],
                        'games': ['haive-games'],
                        'dataflow': ['haive-dataflow'],
                        'tools': ['haive-tools'],
                        'prebuilt': ['haive-prebuilt'],
                        'all': [
                            'haive-agents',
                            'haive-games',
                            'haive-dataflow',
                            'haive-tools',
                            'haive-prebuilt',
                        ],
                    },
                },
                'tool': {
                    'setuptools': {
                        'packages': ['haive'],
                        'package-dir': {
                            '': 'src'
                        }
                    },
                },
            }

            if not self.dry_run:
                with open(pyproject_path, 'wb') as f:
                    tomli_w.dump(pyproject_content, f)
                logger.info(f"Created {pyproject_path}")

    def commit_changes(self):
        """Commit root package changes."""
        if self.dry_run:
            logger.info('[DRY RUN] Would commit root package changes')
            return True

        if not self.git.has_changes():
            logger.info('No changes to commit in root package')
            return True

        logger.info('Committing root package changes')

        # Stage changes
        self.git.stage_changes()

        # Commit
        return self.git.commit_changes(
            'Set up root namespace package') is not None


def get_submodule_paths(root_path):
    """Get all submodule paths."""
    root_path = Path(root_path)
    packages_dir = root_path / 'packages'

    if not packages_dir.exists():
        logger.error(f"Packages directory not found: {packages_dir}")
        return []

    # Get all directories that look like Haive packages
    return [
        d for d in packages_dir.iterdir()
        if d.is_dir() and d.name.startswith('haive-')
    ]


def main():
    parser = argparse.ArgumentParser(
        description='Migrate Haive framework to namespace package structure', )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes',
    )
    parser.add_argument(
        '--submodule',
        help='Only process the specified submodule (e.g., haive-core)',
    )
    parser.add_argument(
        '--no-central',
        action='store_true',
        help='Skip centralizing common directories',
    )
    parser.add_argument(
        '--no-imports',
        action='store_true',
        help='Skip updating import statements',
    )
    parser.add_argument(
        '--no-structure',
        action='store_true',
        help='Skip migrating directory structure',
    )
    parser.add_argument(
        '--no-pyproject',
        action='store_true',
        help='Skip updating pyproject.toml files',
    )
    parser.add_argument(
        '--no-commit',
        action='store_true',
        help='Skip committing changes to git',
    )
    parser.add_argument(
        '--no-root',
        action='store_true',
        help='Skip setting up root package',
    )
    parser.add_argument(
        '--root',
        help='Path to root directory (defaults to current directory)',
    )
    args = parser.parse_args()

    # Set root path
    root_path = Path(args.root) if args.root else Path.cwd()
    logger.info(f"Using root path: {root_path}")

    # Create migration branch in root repository
    root_git = GitStatus(root_path, args.dry_run)
    if not args.dry_run and not root_git.create_branch('namespace-migration'):
        logger.error('Failed to create migration branch in root repository')
        return 1

    # Setup root migrator
    root_migrator = RootPackageMigrator(root_path, args.dry_run)

    # Create central directories
    if not args.no_central:
        root_migrator.create_central_dirs()

    # Get all submodule paths
    if args.submodule:
        submodule_path = root_path / 'packages' / args.submodule
        if not submodule_path.exists():
            logger.error(f"Submodule not found: {submodule_path}")
            return 1
        submodule_paths = [submodule_path]
    else:
        submodule_paths = get_submodule_paths(root_path)

    # Migrate each submodule
    for submodule_path in submodule_paths:
        migrator = PackageMigrator(submodule_path, root_path, args.dry_run)
        migrator.migrate(
            central_root=root_path,
            skip_structure=args.no_structure,
            skip_imports=args.no_imports,
            skip_pyproject=args.no_pyproject,
            skip_central=args.no_central,
            skip_commit=args.no_commit,
        )

    # Setup root package
    if not args.no_root:
        root_migrator.create_root_package()
        if not args.no_commit:
            root_migrator.commit_changes()

    logger.info('Migration complete!')
    return 0


if __name__ == '__main__':
    sys.exit(main())
