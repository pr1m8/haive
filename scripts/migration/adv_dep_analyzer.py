# scripts/migration/advanced_dependency_analyzer.py

import logging
from collections import defaultdict
from pathlib import Path
import toml
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("dependency-analyzer")

# Root project directory (2 levels up from this script)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Packages to analyze
PACKAGES = [
    'haive-core',
    'haive-agents',
    'haive-games',
    'haive-tools',
    'haive-prebuilt',
    'haive-dataflow'
]

# Toolkit mapping
TOOLKIT_MAPPING = {
    'gmail_toolkit': 'haive-tools',
    'github_toolkit': 'haive-tools',
    'weather_toolkit': 'haive-tools',
    'reddit_toolkit': 'haive-tools',
    'stack_exchange_toolkit': 'haive-tools',
    'wolframalpha_toolkit': 'haive-tools',
    'semantic_scholar_toolkit': 'haive-tools',
    'steam_toolkit': 'haive-tools',
    'arxiv_toolkit': 'haive-tools',
    'office365_toolkit': 'haive-tools',
    'powerbi_toolkit': 'haive-tools',
    'ask_news_toolkit': 'haive-tools',
    'google_tools': 'haive-tools',
    'gradio_toolkit': 'haive-tools',
    'amadues_toolkit': 'haive-tools',
    'jira_toolkit': 'haive-tools',
    'slack_toolkit': 'haive-tools',
    'asknews_retriever': 'haive-tools',
    'google_toolkit': 'haive-tools',
    'document_loaders': 'haive-tools',
    'chat_models': 'haive-agents',
    'elevenlabs_tool': 'haive-tools',
    'gitlab_toolkit': 'haive-tools',
    'scenexplain_tool': 'haive-tools',
    'azure_ai_services_toolkit': 'haive-tools',
    'dalle_image_generator_tool': 'haive-tools',
    'google_toolkits': 'haive-tools',
    'yfinance_tool': 'haive-tools',
    'yt_tools': 'haive-tools',
}


def load_root_pyproject():
    try:
        with open(PROJECT_ROOT / 'pyproject.toml', 'r') as f:
            return toml.load(f)
    except Exception as e:
        logger.error(f"Error loading pyproject.toml: {e}")
        return {}


def extract_packages_from_poetry_groups(pyproject):
    group_packages = {}
    if not pyproject or 'tool' not in pyproject or 'poetry' not in pyproject['tool']:
        return group_packages
    for group_name, group_data in pyproject['tool']['poetry'].get('group', {}).items():
        if 'dependencies' in group_data:
            group_packages[group_name] = group_data['dependencies']
    return group_packages


def extract_sources_from_root(pyproject):
    return pyproject.get("tool", {}).get("poetry", {}).get("source", [])


def distribute_toolkits_to_packages(group_packages):
    package_toolkits = defaultdict(dict)
    for group_name, dependencies in group_packages.items():
        if group_name in TOOLKIT_MAPPING:
            target_package = TOOLKIT_MAPPING[group_name]
            package_toolkits[target_package][group_name] = dependencies
    return package_toolkits


def generate_package_pyproject(package_name, toolkits, root_deps, sources):
    pyproject = {
        "tool": {
            "poetry": {
                "name": package_name,
                "version": "0.1.0",
                "description": f"{package_name.split('-')[1].title()} components for the Haive framework",
                "authors": ["0rac130fD31phi <william.astley@algebraicwealth.com>"],
                "license": "MIT",
                "readme": "README.md",
                "packages": [{"include": package_name.replace('-', '_'), "from": "src"}],
                "dependencies": {"python": ">=3.12,<3.13"},
                "extras": {},
                "group": {
                    "dev": {
                        "dependencies": {
                            "pytest": "^8.3.5",
                            "black": "^25.1.0",
                            "isort": "^6.0.1",
                            "mypy": "^1.15.0"
                        }
                    }
                }
            }
        },
        "build-system": {
            "requires": ["poetry-core>=1.0.0"],
            "build-backend": "poetry.core.masonry.api"
        }
    }

    if sources:
        pyproject["tool"]["poetry"]["source"] = sources

    dependencies = pyproject["tool"]["poetry"]["dependencies"]
    if package_name == "haive-core":
        for dep in ["pydantic", "langchain-core", "langchain", "langgraph"]:
            if dep in root_deps:
                dependencies[dep] = root_deps[dep]
    else:
        dependencies["haive-core"] = {"path": "../haive-core", "develop": True}

    for toolkit_name, toolkit_deps in toolkits.items():
        pyproject["tool"]["poetry"]["group"][toolkit_name] = {
            "dependencies": toolkit_deps.copy()
        }
        short = toolkit_name.split('_')[0]
        pyproject["tool"]["poetry"]["extras"][short] = list(toolkit_deps.keys())

    return toml.dumps(pyproject)


def create_empty_package_structure(package_dir, package_name):
    module_name = package_name.replace('-', '_')
    (package_dir / 'src' / module_name).mkdir(parents=True, exist_ok=True)
    (package_dir / 'tests').mkdir(exist_ok=True)
    init_file = package_dir / 'src' / module_name / '__init__.py'
    if not init_file.exists():
        init_file.write_text(f'"""Haive {package_name.split("-")[1]} package."""\n\n__version__ = "0.1.0"\n')


def merge_with_static_analysis(package_name, toolkit_pyproject, analysis_pyproject):
    toolkit_dict = toml.loads(toolkit_pyproject)
    analysis_dict = toml.loads(analysis_pyproject) if analysis_pyproject else {"tool": {"poetry": {"dependencies": {}}}}

    toolkit_deps = toolkit_dict["tool"]["poetry"]["dependencies"]
    for dep, version in analysis_dict["tool"]["poetry"].get("dependencies", {}).items():
        if dep not in toolkit_deps and dep != "python" and not dep.startswith("haive-"):
            toolkit_deps[dep] = version

    toolkit_dict["tool"]["poetry"]["extras"].update(
        analysis_dict["tool"]["poetry"].get("extras", {})
    )

    for group, group_data in analysis_dict["tool"]["poetry"].get("group", {}).items():
        if group != "dev" and group not in toolkit_dict["tool"]["poetry"]["group"]:
            toolkit_dict["tool"]["poetry"]["group"][group] = group_data

    return toml.dumps(toolkit_dict)


def main():
    logger.info("🔍 Loading root pyproject.toml...")
    root_pyproject = load_root_pyproject()
    if not root_pyproject:
        logger.error("❌ Could not load root pyproject.toml.")
        return

    root_deps = root_pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {})
    group_packages = extract_packages_from_poetry_groups(root_pyproject)
    sources = extract_sources_from_root(root_pyproject)

    logger.info(f"📦 Found {len(group_packages)} dependency groups.")
    package_toolkits = distribute_toolkits_to_packages(group_packages)

    for package in PACKAGES:
        package_dir = PROJECT_ROOT / 'packages' / package
        logger.info(f"\n📁 Processing {package}...")

        if not (package_dir / 'src').exists():
            logger.warning("📂 Structure missing. Creating new package skeleton...")
            create_empty_package_structure(package_dir, package)

        toolkits = package_toolkits.get(package, {})
        toolkit_pyproject = generate_package_pyproject(package, toolkits, root_deps, sources)

        analysis_pyproject = None  # Plug in static analysis logic here if desired
        final_pyproject = merge_with_static_analysis(package, toolkit_pyproject, analysis_pyproject)

        output_path = package_dir / 'pyproject.toml'
        print(f"\n🔧 Generated pyproject.toml for {package}:\n{'='*40}")
        print(final_pyproject)
        print("="*40)

        response = input(f"💾 Write to {output_path}? (y/n/a for all): ").lower().strip()
        write_all = False

        if response == 'a':
            write_all = True
            response = 'y'

        if response == 'y':
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(final_pyproject)
            logger.info(f"✅ Wrote pyproject.toml to {output_path}")

            if write_all:
                input_backup = __builtins__.input
                __builtins__.input = lambda _: 'y'

    logger.info("\n✅ Analysis complete.")
    print("🔁 Next steps:\n  1. Review generated pyproject.toml files\n  2. Update imports\n  3. Run `poetry install`")

if __name__ == "__main__":
    main()
