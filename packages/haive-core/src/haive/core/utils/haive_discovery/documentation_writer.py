"""
Documentation writer for saving discovered components.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from haive.core.utils.haive_discovery.component_info import ComponentInfo

logger = logging.getLogger(__name__)


class DocumentationWriter:
    """Handles writing documentation for discovered components."""

    def save_to_project_docs(
        self,
        components: List[ComponentInfo],
        project_root: Optional[str] = None,
        subfolder: str = "component_discovery",
    ) -> Dict[str, str]:
        """Save components to timestamped project documentation with separate files for each type."""
        if project_root is None:
            project_root = self._find_project_root()

        docs_dir = Path(project_root) / "project_docs" / subfolder
        docs_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_files = {}

        # Group components by type
        by_type = {}
        for comp in components:
            comp_type = comp.component_type
            if comp_type not in by_type:
                by_type[comp_type] = []
            by_type[comp_type].append(comp)

        # Save each component type separately
        for comp_type, type_components in by_type.items():
            type_dir = docs_dir / comp_type
            type_dir.mkdir(exist_ok=True)

            # Save JSON
            self._save_type_json(
                type_dir, comp_type, type_components, timestamp, saved_files
            )

            # Save Markdown
            self._save_type_markdown(
                type_dir, comp_type, type_components, timestamp, saved_files
            )

        # Save tools separately
        self._save_generated_tools(docs_dir, components, timestamp, saved_files)

        # Save engine configs
        self._save_engine_configs(docs_dir, components, timestamp, saved_files)

        # Save overall summary
        self._save_summary(docs_dir, components, by_type, timestamp, saved_files)

        # Log summary
        logger.info(f"Saved {len(components)} components to {docs_dir}")
        logger.info(f"Created {len(saved_files)} documentation files")

        self._print_file_locations(docs_dir, by_type, timestamp)

        return saved_files

    def _save_type_json(
        self,
        type_dir: Path,
        comp_type: str,
        components: List[ComponentInfo],
        timestamp: str,
        saved_files: Dict[str, str],
    ):
        """Save JSON file for a component type."""
        json_file = type_dir / f"{comp_type}_{timestamp}.json"
        try:
            component_dicts = []
            for comp in components:
                try:
                    comp_dict = comp.to_dict()
                    component_dicts.append(comp_dict)
                except Exception as e:
                    logger.warning(f"Could not serialize {comp_type} {comp.name}: {e}")
                    component_dicts.append(
                        {
                            "name": comp.name,
                            "component_type": comp.component_type,
                            "error": f"Serialization failed: {str(e)}",
                        }
                    )

            with open(json_file, "w") as f:
                json.dump(component_dicts, f, indent=2, default=str)
            saved_files[f"{comp_type}_json"] = str(json_file)
        except Exception as e:
            logger.error(f"Failed to save {comp_type} JSON file: {e}")

    def _save_type_markdown(
        self,
        type_dir: Path,
        comp_type: str,
        components: List[ComponentInfo],
        timestamp: str,
        saved_files: Dict[str, str],
    ):
        """Save Markdown file for a component type."""
        md_file = type_dir / f"{comp_type}_{timestamp}.md"
        try:
            with open(md_file, "w") as f:
                f.write(f"# {comp_type.title()} Discovery Report\n")
                f.write(f"**Generated:** {datetime.now().isoformat()}\n")
                f.write(f"**Total {comp_type.title()}s:** {len(components)}\n\n")

                # Add type-specific summary
                self._write_type_summary(f, comp_type, components)

                # Write component details
                for comp in components:
                    try:
                        f.write(comp.to_document_content())
                        f.write("\n---\n\n")
                    except Exception as e:
                        f.write(f"### {comp.name}\n")
                        f.write(f"Error generating content: {e}\n")
                        f.write("\n---\n\n")

            saved_files[f"{comp_type}_md"] = str(md_file)
        except Exception as e:
            logger.error(f"Failed to save {comp_type} markdown file: {e}")

    def _write_type_summary(
        self, file, comp_type: str, components: List[ComponentInfo]
    ):
        """Write type-specific summary information."""
        if comp_type == "tool":
            tools_with_schema = sum(
                1 for c in components if c.tool_instance is not None
            )
            file.write(f"**Successfully converted to tools:** {tools_with_schema}\n\n")
        elif comp_type in ["retriever", "vector_store"]:
            with_engine = sum(1 for c in components if c.engine_config is not None)
            file.write(f"**With engine configs:** {with_engine}\n\n")
        elif comp_type == "document_loader":
            as_tools = sum(1 for c in components if c.tool_instance is not None)
            file.write(f"**Converted to tools:** {as_tools}\n\n")

    def _save_generated_tools(
        self,
        docs_dir: Path,
        components: List[ComponentInfo],
        timestamp: str,
        saved_files: Dict[str, str],
    ):
        """Save generated tools information."""
        # Group tools by source type
        tools_by_source = {}
        for comp in components:
            if comp.tool_instance:
                source_type = f"{comp.component_type}_tools"
                if source_type not in tools_by_source:
                    tools_by_source[source_type] = []
                tools_by_source[source_type].append(comp)

        if not tools_by_source:
            return

        tools_dir = docs_dir / "generated_tools"
        tools_dir.mkdir(exist_ok=True)

        for source_type, tool_components in tools_by_source.items():
            tools_file = tools_dir / f"{source_type}_{timestamp}.json"
            try:
                tool_data = []
                for comp in tool_components:
                    if comp.tool_instance:
                        try:
                            tool = comp.tool_instance
                            tool_dict = {
                                "name": getattr(tool, "name", "unknown"),
                                "description": getattr(tool, "description", ""),
                                "source_component": comp.name,
                                "source_type": comp.component_type,
                                "source_module": comp.module_path,
                            }

                            # Try to get schema
                            try:
                                if hasattr(tool, "args_schema") and hasattr(
                                    tool.args_schema, "model_json_schema"
                                ):
                                    tool_dict["schema"] = (
                                        tool.args_schema.model_json_schema()
                                    )
                                else:
                                    tool_dict["schema"] = {
                                        "note": "Schema not available"
                                    }
                            except Exception as e:
                                tool_dict["schema"] = {"error": str(e)}

                            tool_data.append(tool_dict)
                        except Exception as e:
                            logger.warning(
                                f"Could not serialize tool from {comp.name}: {e}"
                            )

                with open(tools_file, "w") as f:
                    json.dump(tool_data, f, indent=2, default=str)
                saved_files[source_type] = str(tools_file)
            except Exception as e:
                logger.error(f"Failed to save {source_type} file: {e}")

    def _save_engine_configs(
        self,
        docs_dir: Path,
        components: List[ComponentInfo],
        timestamp: str,
        saved_files: Dict[str, str],
    ):
        """Save engine configuration files."""
        # Group by engine type
        engines_by_type = {}
        for comp in components:
            if comp.engine_config:
                engine_type = comp.engine_config.get("engine_type", comp.component_type)
                if engine_type not in engines_by_type:
                    engines_by_type[engine_type] = []
                engines_by_type[engine_type].append(comp.engine_config)

        if not engines_by_type:
            return

        engines_dir = docs_dir / "engine_configs"
        engines_dir.mkdir(exist_ok=True)

        for engine_type, configs in engines_by_type.items():
            engine_file = engines_dir / f"{engine_type}_engines_{timestamp}.json"
            try:
                with open(engine_file, "w") as f:
                    json.dump(configs, f, indent=2, default=str)
                saved_files[f"{engine_type}_engines"] = str(engine_file)
            except Exception as e:
                logger.error(f"Failed to save {engine_type} engine configs: {e}")

    def _save_summary(
        self,
        docs_dir: Path,
        components: List[ComponentInfo],
        by_type: Dict[str, List[ComponentInfo]],
        timestamp: str,
        saved_files: Dict[str, str],
    ):
        """Save overall summary file."""
        summary_file = docs_dir / f"discovery_summary_{timestamp}.md"
        try:
            with open(summary_file, "w") as f:
                f.write("# Component Discovery Summary\n")
                f.write(f"**Generated:** {datetime.now().isoformat()}\n")
                f.write(f"**Total Components:** {len(components)}\n\n")

                f.write("## Components by Type\n")
                for comp_type, type_components in by_type.items():
                    f.write(f"- **{comp_type.title()}s:** {len(type_components)}\n")

                f.write("\n## Generated Artifacts\n")
                tools_count = sum(1 for c in components if c.tool_instance)
                engine_count = sum(1 for c in components if c.engine_config)
                f.write(f"- **Tools Created:** {tools_count}\n")
                f.write(f"- **Engine Configs:** {engine_count}\n")

                f.write("\n## File Locations\n")
                for file_type, file_path in saved_files.items():
                    f.write(f"- **{file_type}:** `{Path(file_path).name}`\n")

            saved_files["summary"] = str(summary_file)
        except Exception as e:
            logger.error(f"Failed to save summary: {e}")

    def _print_file_locations(
        self, docs_dir: Path, by_type: Dict[str, List[ComponentInfo]], timestamp: str
    ):
        """Print file locations to console."""
        print(f"\n📁 Documentation saved to: {docs_dir}")
        print("\n📄 Generated files:")
        for comp_type in by_type.keys():
            type_dir = docs_dir / comp_type
            if type_dir.exists():
                print(f"  📂 {comp_type}/")
                for file in type_dir.glob(f"*{timestamp}*"):
                    print(f"    • {file.name}")

    def _find_project_root(self) -> str:
        """Find project root by looking for common markers."""
        current = Path.cwd()
        markers = ["pyproject.toml", ".git", "setup.py", "requirements.txt"]

        while current != current.parent:
            for marker in markers:
                if (current / marker).exists():
                    return str(current)
            current = current.parent

        return str(Path.cwd())
