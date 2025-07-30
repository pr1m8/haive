"""Data models for Labs Agent."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from haive.agents.memory.search.base import SearchResponse


class AssetType(str, Enum):
    """Types of assets that can be created."""

    CHART = "chart"
    IMAGE = "image"
    CSV = "csv"
    CODE = "code"
    DASHBOARD = "dashboard"
    REPORT = "report"
    APP = "app"
    DATASET = "dataset"


class ProjectAsset(BaseModel):
    """Model for project assets created during workflow."""

    asset_id: str = Field(..., description="Unique asset identifier")
    name: str = Field(..., description="Asset name")
    type: AssetType = Field(..., description="Asset type")
    description: str = Field(..., description="Asset description")
    file_path: str | None = Field(default=None, description="File path if saved")
    content: str | None = Field(default=None, description="Asset content or code")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Asset metadata")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    size_bytes: int = Field(default=0, description="Asset size in bytes")
    downloadable: bool = Field(
        default=True, description="Whether asset can be downloaded"
    )


class WorkflowStep(BaseModel):
    """Model for individual workflow steps."""

    step_id: str = Field(..., description="Step identifier")
    name: str = Field(..., description="Step name")
    description: str = Field(..., description="Step description")
    tool_used: str | None = Field(default=None, description="Tool used for this step")
    input_data: dict[str, Any] = Field(
        default_factory=dict, description="Input data for step"
    )
    output_data: dict[str, Any] = Field(
        default_factory=dict, description="Output data from step"
    )
    duration_seconds: float = Field(default=0.0, description="Step execution time")
    success: bool = Field(default=True, description="Whether step succeeded")
    error_message: str | None = Field(
        default=None, description="Error message if failed"
    )


class InteractiveApp(BaseModel):
    """Model for interactive applications created in Labs."""

    app_id: str = Field(..., description="App identifier")
    name: str = Field(..., description="App name")
    description: str = Field(..., description="App description")
    app_type: str = Field(
        ..., description="Type of app (dashboard, slideshow, website)"
    )
    html_content: str = Field(..., description="HTML content of the app")
    css_styles: str | None = Field(default=None, description="CSS styles")
    javascript_code: str | None = Field(default=None, description="JavaScript code")
    data_sources: list[str] = Field(
        default_factory=list, description="Data sources used"
    )
    interactive_elements: list[str] = Field(
        default_factory=list, description="Interactive elements"
    )
    deployment_url: str | None = Field(
        default=None, description="Deployment URL if deployed"
    )


class LabsResponse(SearchResponse):
    """Response model for Labs operations.

    Extends the base SearchResponse with Labs-specific fields.
    """

    search_type: str = Field(default="Labs", description="Type of search performed")
    project_name: str = Field(default="", description="Name of the project")
    workflow_steps: list[WorkflowStep] = Field(
        default_factory=list, description="Workflow steps executed"
    )
    assets_created: list[ProjectAsset] = Field(
        default_factory=list, description="Assets created"
    )
    interactive_apps: list[InteractiveApp] = Field(
        default_factory=list, description="Interactive apps created"
    )
    total_work_time: float = Field(
        default=0.0, description="Total work time in seconds"
    )
    tools_used: list[str] = Field(
        default_factory=list, description="Tools used in workflow"
    )
    code_execution_results: list[dict[str, Any]] = Field(
        default_factory=list, description="Code execution results"
    )
    data_analysis_results: dict[str, Any] = Field(
        default_factory=dict, description="Data analysis results"
    )
    visualizations_created: int = Field(
        default=0, description="Number of visualizations created"
    )
    project_summary: str = Field(default="", description="Summary of project work")
    next_steps: list[str] = Field(
        default_factory=list, description="Suggested next steps"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "query": "Create a dashboard analyzing customer satisfaction survey data",
                "response": "# Customer Satisfaction Dashboard Project\n\nI've created a comprehensive dashboard analyzing your customer satisfaction survey data...",
                "sources": ["survey_data.csv", "customer_feedback.json"],
                "confidence": 0.9,
                "search_type": "Labs",
                "processing_time": 180.5,
                "project_name": "Customer Satisfaction Analysis",
                "workflow_steps": [
                    {
                        "step_id": "data_load",
                        "name": "Load Survey Data",
                        "description": "Load and validate customer survey data",
                        "tool_used": "pandas",
                        "input_data": {"file": "survey_data.csv"},
                        "output_data": {"rows": 1250, "columns": 15},
                        "duration_seconds": 2.3,
                        "success": True,
                    }
                ],
                "assets_created": [
                    {
                        "asset_id": "dashboard_001",
                        "name": "Customer Satisfaction Dashboard",
                        "type": "dashboard",
                        "description": "Interactive dashboard showing satisfaction metrics",
                        "file_path": "/assets/customer_dashboard.html",
                        "content": "<html>...</html>",
                        "metadata": {"chart_count": 5, "data_points": 1250},
                        "created_at": "2025-01-15T10:30:00",
                        "size_bytes": 45000,
                        "downloadable": True,
                    }
                ],
                "interactive_apps": [
                    {
                        "app_id": "satisfaction_app",
                        "name": "Satisfaction Analyzer",
                        "description": "Interactive app for exploring satisfaction data",
                        "app_type": "dashboard",
                        "html_content": "<html>...</html>",
                        "css_styles": "body { font-family: Arial; }",
                        "javascript_code": "function updateChart() { ... }",
                        "data_sources": ["survey_data.csv"],
                        "interactive_elements": ["filters", "dropdowns", "charts"],
                    }
                ],
                "total_work_time": 180.5,
                "tools_used": ["pandas", "matplotlib", "d3.js", "html"],
                "code_execution_results": [
                    {
                        "code": "df.describe()",
                        "output": "Statistical summary of survey data",
                        "success": True,
                    }
                ],
                "data_analysis_results": {
                    "total_responses": 1250,
                    "average_satisfaction": 3.8,
                    "top_concerns": ["price", "delivery", "support"],
                },
                "visualizations_created": 5,
                "project_summary": "Created an interactive dashboard with 5 visualizations analyzing customer satisfaction survey data from 1,250 responses.",
                "next_steps": [
                    "Add real-time data updates",
                    "Include predictive analytics",
                    "Deploy to production environment",
                ],
                "metadata": {},
            }
        }


class LabsRequest(BaseModel):
    """Request model for Labs operations."""

    query: str = Field(
        ..., min_length=1, max_length=2000, description="Project description or request"
    )
    project_type: str = Field(
        default="analysis", description="Type of project (analysis, dashboard, app)"
    )
    data_sources: list[str] = Field(
        default_factory=list, description="Data sources to use"
    )
    required_tools: list[str] = Field(
        default_factory=list, description="Required tools"
    )
    output_format: str = Field(
        default="interactive", description="Desired output format"
    )
    enable_code_execution: bool = Field(
        default=True, description="Enable code execution"
    )
    create_interactive_app: bool = Field(
        default=True, description="Create interactive app"
    )
    max_work_time: int = Field(default=600, description="Maximum work time in seconds")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "query": "Analyze sales data and create interactive charts showing trends",
                "project_type": "dashboard",
                "data_sources": ["sales_data.csv", "product_info.json"],
                "required_tools": ["pandas", "matplotlib", "plotly"],
                "output_format": "interactive",
                "enable_code_execution": True,
                "create_interactive_app": True,
                "max_work_time": 600,
            }
        }
