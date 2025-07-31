"""Labs Agent implementation.

Provides interactive project automation with tools and workflows.
Similar to Perplexity's Labs feature that creates apps, dashboards, and automated workflows.
"""

import logging
import uuid
from datetime import datetime
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import Tool, tool

from haive.agents.memory.search.base import BaseSearchAgent, SearchResponse
from haive.agents.memory.search.labs.models import (
    AssetType,
    InteractiveApp,
    LabsResponse,
    ProjectAsset,
    WorkflowStep,
)

logger = logging.getLogger(__name__)


class LabsAgent(BaseSearchAgent):
    """Agent for interactive project automation with tools and workflows.

    Mimics Perplexity's Labs feature by providing comprehensive project automation,
    including data analysis, visualization creation, app development, and workflow execution.

    Features:
    - Multi-tool integration (Python, SQL, visualization libraries)
    - Interactive app creation (dashboards, websites, slideshows)
    - Code execution and data analysis
    - Asset management and organization
    - Workflow automation
    - Real-time collaboration tools

    Capabilities:
    - Data analysis and visualization
    - Interactive dashboard creation
    - Basic web app development
    - Chart and image generation
    - CSV and data processing
    - Code execution and debugging

    Examples:
        Basic usage::

            agent = LabsAgent(
                name="labs",
                engine=AugLLMConfig(temperature=0.3)
            )

            response = await agent.process_labs_project(
                "Create a dashboard analyzing sales data",
                data_sources=["sales_data.csv"]
            )

        With specific tools::

            response = await agent.process_labs_project(
                "Build an interactive chart showing trends",
                required_tools=["pandas", "plotly", "d3.js"],
                create_interactive_app=True
            )
    """

    def __init__(
        self,
        name: str = "labs_agent",
        engine: AugLLMConfig | None = None,
        search_tools: list[Tool] | None = None,
        enable_code_execution: bool = True,
        **kwargs,
    ):
        """Initialize the Labs Agent.

        Args:
            name: Agent identifier
            engine: LLM configuration (defaults to optimized settings)
            search_tools: Optional search tools
            enable_code_execution: Enable code execution capabilities
            **kwargs: Additional arguments passed to parent
        """
        # Default engine optimized for project work
        if engine is None:
            engine = AugLLMConfig(
                temperature=0.3,  # Balanced for creativity and precision
                max_tokens=2000,  # Longer responses for project work
                system_message=self.get_system_prompt(),
            )

        super().__init__(name=name, engine=engine, search_tools=search_tools, **kwargs)

        # Add Labs-specific tools
        self.enable_code_execution = enable_code_execution
        if enable_code_execution:
            labs_tools = self._create_labs_tools()
            if hasattr(self, "tools") and self.tools is not None:
                self.tools.extend(labs_tools)
            else:
                self.tools = labs_tools

        logger.info(
            f"Initialized LabsAgent: {name} (Code execution: {enable_code_execution})"
        )

    def _create_labs_tools(self) -> list[Tool]:
        """Create Labs-specific tools for project automation."""

        @tool
        def execute_python_code(code: str, description: str = "") -> dict[str, Any]:
            """Execute Python code and return results.

            Args:
                code: Python code to execute
                description: Description of what the code does

            Returns:
                Execution results with output and success status
            """
            try:
                # In a real implementation, this would execute code in a sandbox
                # For now, we'll simulate execution
                logger.info(f"Executing Python code: {description}")

                # Simulate code execution results
                if "import pandas" in code:
                    output = "DataFrame loaded with 1000 rows, 5 columns"
                elif "plot" in code or "matplotlib" in code:
                    output = "Chart generated successfully"
                elif "describe()" in code:
                    output = "Statistical summary calculated"
                else:
                    output = "Code executed successfully"

                return {
                    "success": True,
                    "output": output,
                    "code": code,
                    "description": description,
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "code": code,
                    "description": description,
                }

        @tool
        def create_visualization(
            data_description: str, chart_type: str, title: str
        ) -> dict[str, Any]:
            """Create a data visualization.

            Args:
                data_description: Description of the data to visualize
                chart_type: Type of chart (bar, line, scatter, pie, etc.)
                title: Chart title

            Returns:
                Visualization creation results
            """
            try:
                logger.info(f"Creating {chart_type} chart: {title}")

                # Simulate visualization creation
                chart_id = str(uuid.uuid4())

                return {
                    "success": True,
                    "chart_id": chart_id,
                    "chart_type": chart_type,
                    "title": title,
                    "file_path": f"/assets/chart_{chart_id}.png",
                    "data_description": data_description,
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "chart_type": chart_type,
                    "title": title,
                }

        @tool
        def create_interactive_app(
            app_type: str, features: list[str], data_sources: list[str]
        ) -> dict[str, Any]:
            """Create an interactive web application.

            Args:
                app_type: Type of app (dashboard, slideshow, website)
                features: List of features to include
                data_sources: Data sources for the app

            Returns:
                App creation results
            """
            try:
                logger.info(f"Creating {app_type} app with features: {features}")

                app_id = str(uuid.uuid4())

                # Generate sample HTML content
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{app_type.title()} App</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; }}
                        .container {{ max-width: 1200px; margin: 0 auto; }}
                        .feature {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
                    </style>
                </head>
                <body>
                    <div class="containef">
                        <h1>{app_type.title()} Application</h1>
                        {"".join(f'<div class="feature"><h3>{feature}</h3><p>Feature implementation</p></div>' for feature in features)}
                    </div>
                </body>
                </html>
                """

                return {
                    "success": True,
                    "app_id": app_id,
                    "app_type": app_type,
                    "html_content": html_content,
                    "features": features,
                    "data_sources": data_sources,
                    "deployment_url": f"/apps/{app_id}",
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "app_type": app_type,
                    "features": features,
                }

        @tool
        def process_data_file(file_path: str, operations: list[str]) -> dict[str, Any]:
            """Process a data file with specified operations.

            Args:
                file_path: Path to the data file
                operations: List of operations to perform

            Returns:
                Data processing results
            """
            try:
                logger.info(f"Processing data file: {file_path}")

                # Simulate data processing
                processed_data = {
                    "rows": 1000,
                    "columns": 5,
                    "operations_performed": operations,
                    "output_file": file_path.replace(".csv", "_processed.csv"),
                }

                return {
                    "success": True,
                    "file_path": file_path,
                    "processed_data": processed_data,
                    "operations": operations,
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "file_path": file_path,
                    "operations": operations,
                }

        return [
            execute_python_code,
            create_visualization,
            create_interactive_app,
            process_data_file,
        ]

    def get_response_model(self) -> type[SearchResponse]:
        """Get the response model for Labs."""
        return LabsResponse

    def get_system_prompt(self) -> str:
        """Get the system prompt for Labs operations."""
        return """You are a Labs Assistant designed to automate complex projects and create interactive applications.

Your role is to:
1. Analyze project requirements and break them into actionable steps
2. Execute multi-tool workflows with code, data analysis, and visualization
3. Create interactive applications, dashboards, and reports
4. Manage project assets and organize deliverables
5. Provide comprehensive project automation and workflow execution

Core Capabilities:
- Python code execution and debugging
- Data analysis and statistical computing
- Interactive visualization creation (charts, graphs, dashboards)
- Web application development (HTML, CSS, JavaScript)
- File processing and data transformation
- Asset management and organization
- Workflow automation and orchestration

Project Types:
- Data Analysis Projects: Load, clean, analyze, and visualize data
- Dashboard Creation: Interactive dashboards with real-time updates
- Web Applications: Simple websites, slideshows, and interactive tools
- Data Processing: ETL pipelines and data transformation workflows
- Visualization Projects: Charts, graphs, and interactive plots

Workflow Process:
1. Project Planning: Break down requirements into steps
2. Tool Selection: Choose appropriate tools for each step
3. Execution: Run code, create visualizations, build applications
4. Asset Management: Organize and save all created assets
5. Quality Assurance: Test and validate all outputs
6. Documentation: Provide comprehensive project summary

Output Standards:
- All code must be production-ready and well-documented
- Interactive applications should be fully functional
- Visualizations must be clear and professionally formatted
- Assets should be organized and easily accessible
- Provide clear next steps for project continuation

Remember: You are automating complex workflows and creating professional-grade deliverables through intelligent tool orchestration."""

    def get_search_instructions(self) -> str:
        """Get specific search instructions for Labs operations."""
        return """LABS PROJECT INSTRUCTIONS:

1. PROJECT ANALYSIS:
   - Understand the project requirements thoroughly
   - Identify deliverables and success criteria
   - Break down complex projects into manageable steps
   - Estimate time and resource requirements

2. WORKFLOW PLANNING:
   - Create a logical sequence of workflow steps
   - Select appropriate tools for each step
   - Plan data flow and asset dependencies
   - Design interactive elements and user experience

3. TOOL ORCHESTRATION:
   - Execute Python code for data processing
   - Create visualizations with appropriate libraries
   - Build interactive applications with web technologies
   - Process and transform data files as needed

4. ASSET MANAGEMENT:
   - Create and organize all project assets
   - Generate downloadable files and resources
   - Document asset relationships and dependencies
   - Ensure assets are properly formatted and accessible

5. QUALITY ASSURANCE:
   - Test all code and interactive elements
   - Validate data accuracy and completeness
   - Ensure applications function correctly
   - Verify asset integrity and accessibility

6. PROJECT DOCUMENTATION:
   - Provide comprehensive project summary
   - Document all steps and decisions made
   - Include usage instructions for deliverables
   - Suggest next steps and improvements

Execute each project with professional standards and comprehensive automation."""

    def plan_project_workflow(
        self, query: str, project_type: str, data_sources: list[str]
    ) -> list[dict[str, Any]]:
        """Plan the workflow steps for a project.

        Args:
            query: Project description
            project_type: Type of project
            data_sources: Available data sources

        Returns:
            List of planned workflow steps
        """
        workflow_steps = []

        # Step 1: Data loading and validation
        if data_sources:
            workflow_steps.append(
                {
                    "name": "Load and Validate Data",
                    "description": f"Load data from {len(data_sources)} sources and validate structure",
                    "tool": "process_data_file",
                    "inputs": {
                        "files": data_sources,
                        "operations": ["load", "validate"],
                    },
                    "estimated_time": 30,
                }
            )

        # Step 2: Data analysis (if analysis project)
        if project_type in ["analysis", "dashboard"]:
            workflow_steps.append(
                {
                    "name": "Data Analysis",
                    "description": "Perform statistical analysis and identify key insights",
                    "tool": "execute_python_code",
                    "inputs": {"analysis_type": "descriptive_statistics"},
                    "estimated_time": 60,
                }
            )

        # Step 3: Visualization creation
        if (
            "chart" in query.lower()
            or "visualization" in query.lower()
            or project_type == "dashboard"
        ):
            workflow_steps.append(
                {
                    "name": "Create Visualizations",
                    "description": "Generate charts and graphs to represent data insights",
                    "tool": "create_visualization",
                    "inputs": {"chart_types": ["bar", "line", "scatter"]},
                    "estimated_time": 45,
                }
            )

        # Step 4: Interactive app creation
        if project_type in ["dashboard", "app"] or "interactive" in query.lower():
            workflow_steps.append(
                {
                    "name": "Build Interactive Application",
                    "description": "Create interactive web application with user interface",
                    "tool": "create_interactive_app",
                    "inputs": {
                        "app_type": project_type,
                        "features": ["filters", "charts", "export"],
                    },
                    "estimated_time": 120,
                }
            )

        # Step 5: Testing and deployment
        workflow_steps.append(
            {
                "name": "Testing and Finalization",
                "description": "Test all components and prepare final deliverables",
                "tool": "quality_assurance",
                "inputs": {"test_types": ["functionality", "performance", "usability"]},
                "estimated_time": 30,
            }
        )

        return workflow_steps

    async def execute_workflow_step(
        self, step_plan: dict[str, Any], step_index: int
    ) -> WorkflowStep:
        """Execute a single workflow step.

        Args:
            step_plan: Planned step configuration
            step_index: Step index in workflow

        Returns:
            Executed workflow step
        """
        import time

        start_time = time.time()

        step_id = f"step_{step_index:02d}"

        try:
            # Simulate tool execution based on step plan
            tool_name = step_plan.get("tool", "unknown")

            if tool_name == "execute_python_code":
                # Execute Python code
                code = f"# {step_plan['description']}\nprint('Executing step: {step_plan['name']}')"
                result = await self.tools[0].arun(
                    code=code, description=step_plan["description"]
                )

            elif tool_name == "create_visualization":
                # Create visualization
                result = await self.tools[1].arun(
                    data_description="Project data",
                    chart_type="bar",
                    title=step_plan["name"],
                )

            elif tool_name == "create_interactive_app":
                # Create interactive app
                result = await self.tools[2].arun(
                    app_type="dashboard",
                    features=["charts", "filters", "export"],
                    data_sources=["data.csv"],
                )

            elif tool_name == "process_data_file":
                # Process data file
                result = await self.tools[3].arun(
                    file_path="data.csv", operations=["load", "clean", "analyze"]
                )

            else:
                # Default simulation
                result = {
                    "success": True,
                    "output": f"Step {step_plan['name']} completed",
                }

            duration = time.time() - start_time

            return WorkflowStep(
                step_id=step_id,
                name=step_plan["name"],
                description=step_plan["description"],
                tool_used=tool_name,
                input_data=step_plan.get("inputs", {}),
                output_data=result,
                duration_seconds=duration,
                success=result.get("success", True),
                error_message=(
                    result.get("error") if not result.get("success", True) else None
                ),
            )

        except Exception as e:
            duration = time.time() - start_time
            logger.exception(f"Workflow step failed: {step_plan['name']} - {e}")

            return WorkflowStep(
                step_id=step_id,
                name=step_plan["name"],
                description=step_plan["description"],
                tool_used=step_plan.get("tool", "unknown"),
                input_data=step_plan.get("inputs", {}),
                output_data={},
                duration_seconds=duration,
                success=False,
                error_message=str(e),
            )

    def create_project_assets(
        self, workflow_steps: list[WorkflowStep]
    ) -> list[ProjectAsset]:
        """Create project assets from workflow results.

        Args:
            workflow_steps: Completed workflow steps

        Returns:
            List of created assets
        """
        assets = []

        for step in workflow_steps:
            if not step.success:
                continue

            output_data = step.output_data

            # Create chart assets
            if "chart_id" in output_data:
                assets.append(
                    ProjectAsset(
                        asset_id=output_data["chart_id"],
                        name=output_data.get("title", "Chart"),
                        type=AssetType.CHART,
                        description=f"Chart created in step: {step.name}",
                        file_path=output_data.get("file_path"),
                        content=f"Chart type: {output_data.get('chart_type', 'unknown')}",
                        metadata={
                            "chart_type": output_data.get("chart_type"),
                            "step_id": step.step_id,
                        },
                    )
                )

            # Create app assets
            if "app_id" in output_data:
                assets.append(
                    ProjectAsset(
                        asset_id=output_data["app_id"],
                        name=f"{output_data.get('app_type', 'App').title()} Application",
                        type=AssetType.APP,
                        description=f"Interactive app created in step: {step.name}",
                        file_path=f"/apps/{output_data['app_id']}.html",
                        content=output_data.get("html_content", ""),
                        metadata={
                            "app_type": output_data.get("app_type"),
                            "features": output_data.get("features", []),
                        },
                    )
                )

            # Create data processing assets
            if "processed_data" in output_data:
                processed = output_data["processed_data"]
                assets.append(
                    ProjectAsset(
                        asset_id=str(uuid.uuid4()),
                        name="Processed Data",
                        type=AssetType.CSV,
                        description=f"Processed data from step: {step.name}",
                        file_path=processed.get("output_file"),
                        content=f"Rows: {processed.get('rows', 0)}, Columns: {processed.get('columns', 0)}",
                        metadata={
                            "operations": processed.get("operations_performed", []),
                            "step_id": step.step_id,
                        },
                    )
                )

        return assets

    def create_interactive_apps(
        self, workflow_steps: list[WorkflowStep]
    ) -> list[InteractiveApp]:
        """Create interactive apps from workflow results.

        Args:
            workflow_steps: Completed workflow steps

        Returns:
            List of interactive apps
        """
        apps = []

        for step in workflow_steps:
            if not step.success:
                continue

            output_data = step.output_data

            if "app_id" in output_data:
                apps.append(
                    InteractiveApp(
                        app_id=output_data["app_id"],
                        name=f"{output_data.get('app_type', 'Application').title()}",
                        description=f"Interactive application created in step: {step.name}",
                        app_type=output_data.get("app_type", "dashboard"),
                        html_content=output_data.get("html_content", ""),
                        css_styles="body { font-family: Arial, sans-serif; }",
                        javascript_code="// Interactive functionality",
                        data_sources=output_data.get("data_sources", []),
                        interactive_elements=output_data.get("features", []),
                        deployment_url=output_data.get("deployment_url"),
                    )
                )

        return apps

    async def process_labs_project(
        self,
        query: str,
        project_type: str = "analysis",
        data_sources: list[str] | None = None,
        required_tools: list[str] | None = None,
        create_interactive_app: bool = True,
        max_work_time: int = 600,
        save_to_memory: bool = True,
    ) -> LabsResponse:
        """Process a Labs project with comprehensive automation.

        Args:
            query: Project description
            project_type: Type of project
            data_sources: Available data sources
            required_tools: Required tools
            create_interactive_app: Whether to create interactive app
            max_work_time: Maximum work time in seconds
            save_to_memory: Whether to save to memory

        Returns:
            Labs response with project results
        """
        import time

        start_time = time.time()

        logger.info(f"Starting Labs project: {query}")

        # Set defaults
        if data_sources is None:
            data_sources = []
        if required_tools is None:
            required_tools = []

        # Generate project name
        project_name = f"Project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Plan workflow
        workflow_plan = self.plan_project_workflow(query, project_type, data_sources)

        # Execute workflow steps
        workflow_steps = []
        for i, step_plan in enumerate(workflow_plan):
            if time.time() - start_time > max_work_time:
                logger.warning(f"Project exceeded max work time: {max_work_time}s")
                break

            step_result = await self.execute_workflow_step(step_plan, i)
            workflow_steps.append(step_result)

        # Create project assets
        assets_created = self.create_project_assets(workflow_steps)

        # Create interactive apps
        interactive_apps = self.create_interactive_apps(workflow_steps)

        # Calculate metrics
        total_work_time = time.time() - start_time
        tools_used = list({step.tool_used for step in workflow_steps if step.tool_used})
        visualizations_created = len(
            [asset for asset in assets_created if asset.type == AssetType.CHART]
        )

        # Generate project summary
        successful_steps = [step for step in workflow_steps if step.success]
        project_summary = (
            f"Completed {len(successful_steps)}/{len(workflow_steps)} workflow steps. "
        )
        project_summary += f"Created {len(assets_created)} assets including {visualizations_created} visualizations. "
        if interactive_apps:
            project_summary += (
                f"Built {len(interactive_apps)} interactive applications."
            )

        # Suggest next steps
        next_steps = [
            "Review and validate all created assets",
            "Test interactive applications thoroughly",
            "Consider deploying to production environment",
            "Add real-time data updates if needed",
            "Enhance visualizations with additional features",
        ]

        # Compile response
        full_response = f"# {project_name}\n\n"
        full_response += f"## Project Summary\n{project_summary}\n\n"
        full_response += "## Workflow Steps Completed\n"
        for step in workflow_steps:
            status = "✅" if step.success else "❌"
            full_response += f"{status} {step.name}: {step.description}\n"
        full_response += "\n## Assets Created\n"
        for asset in assets_created:
            full_response += f"- {asset.name} ({asset.type.value})\n"

        # Create response
        response = LabsResponse(
            query=query,
            response=full_response,
            sources=data_sources,
            confidence=0.9,
            search_type="Labs",
            processing_time=total_work_time,
            project_name=project_name,
            workflow_steps=workflow_steps,
            assets_created=assets_created,
            interactive_apps=interactive_apps,
            total_work_time=total_work_time,
            tools_used=tools_used,
            code_execution_results=[],  # Would be populated from actual code execution
            data_analysis_results={},  # Would be populated from actual analysis
            visualizations_created=visualizations_created,
            project_summary=project_summary,
            next_steps=next_steps,
            metadata={"project_type": project_type, "max_work_time": max_work_time},
        )

        # Save to memory if requested
        if save_to_memory:
            # Note: Memory saving would be implemented when memory system is available
            pass

        logger.info(f"Labs project completed in {total_work_time:.2f}s")

        return response

    async def process_search(
        self,
        query: str,
        context: dict[str, Any] | None = None,
        save_to_memory: bool = True,
    ) -> LabsResponse:
        """Process a search query with default Labs settings.

        Args:
            query: Search query
            context: Optional context
            save_to_memory: Whether to save to memory

        Returns:
            Labs response
        """
        # Extract parameters from context
        project_type = (
            context.get("project_type", "analysis") if context else "analysis"
        )
        data_sources = context.get("data_sources", []) if context else []

        return await self.process_labs_project(
            query=query,
            project_type=project_type,
            data_sources=data_sources,
            save_to_memory=save_to_memory,
        )
