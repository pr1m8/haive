"""Dynamic Choice Model Builder with Protocol-based Generic Options Support.

Uses Protocol to ensure options have extractable names, making it flexible for
strings, dicts, BaseModels, or any custom class with a name attribute.
"""

import logging
from enum import Enum
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
    runtime_checkable,
)

from pydantic import (
    BaseModel,
    Field,
    PrivateAttr,
    create_model,
    field_validator,
    model_validator,
)
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from haive.core.common.types.protocols.general_protocols import Nameable

console = Console()
logger = logging.getLogger(__name__)


# Generic type that can be string, dict with name key, or any object with name attribute
OptionItem = TypeVar("OptionItem", str, dict[str, Any], Nameable)


class DynamicChoiceModel(BaseModel, Generic[OptionItem]):
    """Dynamic choice model builder that is itself a BaseModel.
    Can be called to generate new choice models with current options.
    Supports strings, dicts with name keys, or any object with name attribute.
    """

    # Core configuration
    options: list[OptionItem] = Field(
        default_factory=list, description="Current options list"
    )
    name_field: str = Field(
        default="name", description="Field/attribute to extract names from"
    )
    include_end: bool = Field(default=True, description="Always include END option")
    model_name: str = Field(
        default="DynamicChoice", description="Base name for generated models"
    )

    # Private attributes (Pydantic v2 style)
    _current_model: type[BaseModel] | None = PrivateAttr(default=None)
    _option_names: list[str] = PrivateAttr(default_factory=list)
    _model_counter: int = PrivateAttr(default=0)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self._regenerate_model()
        self._debug_print_initial()

    def _extract_name_from_option(self, option: OptionItem) -> str:
        """Extract name from an option regardless of its type."""
        if isinstance(option, str):
            return option
        if isinstance(option, dict):
            name = option.get(self.name_field)
            if name is None:
                raise ValueError(
                    f"Dict option missing '{self.name_field}' key: {option}"
                )
            return str(name)
        if hasattr(option, self.name_field):
            # Works for BaseModel, dataclass, or any object with name attribute
            return str(getattr(option, self.name_field))
        # Fallback to string representation
        return str(option)

    def _extract_option_names(self) -> list[str]:
        """Extract all option names."""
        names = []

        for option in self.options:
            try:
                name = self._extract_name_from_option(option)
                names.append(name)
            except Exception as e:
                logger.warning(f"Failed to extract name from option {option}: {e}")
                names.append(str(option))

        # Always include END if specified
        if self.include_end and "END" not in names:
            names.append("END")

        return names

    def _regenerate_model(self) -> None:
        """Generate new choice model with current options."""
        self._option_names = self._extract_option_names()
        self._model_counter += 1

        # Capture current options for validator closure
        valid_options = self._option_names.copy()

        def validate_choice_field(cls, v: str) -> str:
            if v not in valid_options:
                raise ValueError(f"Choice '{v}' must be one of: {valid_options}")
            return v

        # Create unique model name
        model_name = f"{self.model_name}_{self._model_counter}"

        # Create the model with field validator
        self._current_model = create_model(
            model_name,
            choice=(
                str,
                Field(..., description=f"Must be one of: {', '.join(valid_options)}"),
            ),
            __validators__={
                "validate_choice": field_validator("choice", mode="after")(
                    validate_choice_field
                )
            },
        )

        logger.debug(f"Generated model {model_name} with options: {valid_options}")

    def __call__(self) -> type[BaseModel]:
        """Make the builder callable to return current choice model."""
        if self._current_model is None:
            self._regenerate_model()
        return self._current_model

    @property
    def current_model(self) -> type[BaseModel]:
        """Get current choice model."""
        return self()

    @property
    def option_names(self) -> list[str]:
        """Get current option names."""
        return self._option_names.copy()

    def add_option(self, option: OptionItem) -> None:
        """Add a new option and regenerate model."""
        if option not in self.options:
            self.options.append(option)
            self._regenerate_model()
            name = self._extract_name_from_option(option)
            console.print(f"[green]➕ Added option:[/green] {name}")
            self._debug_print_change("ADD", name)
        else:
            name = self._extract_name_from_option(option)
            console.print(f"[yellow]Option '{name}' already exists[/yellow]")

    def remove_option(self, option: OptionItem) -> bool:
        """Remove an option and regenerate model."""
        name = self._extract_name_from_option(option)

        if name == "END" and self.include_end:
            console.print("[red]Cannot remove END option when include_end=True[/red]")
            return False

        # Find and remove the option
        for i, existing_option in enumerate(self.options):
            existing_name = self._extract_name_from_option(existing_option)
            if existing_name == name:
                self.options.pop(i)
                self._regenerate_model()
                console.print(f"[red]➖ Removed option:[/red] {name}")
                self._debug_print_change("REMOVE", name)
                return True

        console.print(f"[yellow]Option '{name}' not found[/yellow]")
        return False

    def remove_option_by_name(self, name: str) -> bool:
        """Remove option by name string."""
        if name == "END" and self.include_end:
            console.print("[red]Cannot remove END option when include_end=True[/red]")
            return False

        for i, option in enumerate(self.options):
            option_name = self._extract_name_from_option(option)
            if option_name == name:
                self.options.pop(i)
                self._regenerate_model()
                console.print(f"[red]➖ Removed option:[/red] {name}")
                self._debug_print_change("REMOVE", name)
                return True

        console.print(f"[yellow]Option '{name}' not found[/yellow]")
        return False

    def validate_choice(self, choice: str) -> bool:
        """Test if a choice would be valid."""
        return choice in self._option_names

    def test_model(self, test_choice: str) -> BaseModel | None:
        """Test the model with a choice and return instance if valid."""
        console.print(f"\n[blue]🧪 Testing choice: '{test_choice}'[/blue]")

        try:
            model_class = self.current_model
            instance = model_class(choice=test_choice)
            console.print(f"[green]✅ Valid! Created: {instance}[/green]")
            console.print(f"[dim]   Model: {model_class.__name__}[/dim]")
            console.print(f"[dim]   Choice: {instance.choice}[/dim]")
            return instance
        except Exception as e:
            console.print(f"[red]❌ Invalid! Error: {e}[/red]")
            return None

    def _debug_print_initial(self) -> None:
        """Print initial state."""
        panel_content = f"""
[bold]Options:[/bold] {', '.join(self._option_names)}
[bold]Include END:[/bold] {self.include_end}
[bold]Name Field:[/bold] {self.name_field}
[bold]Model Name:[/bold] {self._current_model.__name__ if self._current_model else 'None'}
"""
        console.print(
            Panel(
                panel_content, title="🚀 Dynamic Choice Model Initialized", style="blue"
            )
        )

    def _debug_print_change(self, action: str, option_name: str) -> None:
        """Print state after change."""
        action_color = "green" if action == "ADD" else "red"
        action_emoji = "➕" if action == "ADD" else "➖"

        tree = Tree(
            f"{action_emoji} [bold {action_color}]{action} Operation[/bold {action_color}]"
        )

        # Operation details
        op_branch = tree.add("📋 Operation Details")
        op_branch.add(f"Action: {action}")
        op_branch.add(f"Option: {option_name}")

        # Current state
        state_branch = tree.add("🔄 Current State")
        state_branch.add(f"Total Options: {len(self._option_names)}")
        state_branch.add(f"Model: {self._current_model.__name__}")

        options_branch = state_branch.add("Options List")
        for opt in self._option_names:
            if opt == "END":
                options_branch.add(f"🔚 [red]{opt}[/red]")
            else:
                options_branch.add(f"🎯 [green]{opt}[/green]")

        console.print(Panel(tree, title="State Change", expand=False))

    def print_full_state(self) -> None:
        """Print comprehensive state information."""
        table = Table(title="🔍 Dynamic Choice Model State")
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        table.add_row("Current Options", ", ".join(self._option_names))
        table.add_row("Option Count", str(len(self._option_names)))
        table.add_row("Raw Options Count", str(len(self.options)))
        table.add_row("Include END", str(self.include_end))
        table.add_row("Name Field", self.name_field)
        table.add_row("Model Counter", str(self._model_counter))

        if self._current_model:
            table.add_row("Current Model", self._current_model.__name__)
            table.add_row(
                "Model Fields", str(list(self._current_model.model_fields.keys()))
            )

            # Field details
            choice_field = self._current_model.model_fields.get("choice")
            if choice_field:
                table.add_row("Field Type", str(choice_field.annotation))
                table.add_row("Field Description", str(choice_field.description))

        console.print(table)

    def interactive_demo(self) -> None:
        """Interactive demo mode."""
        console.print("\n[bold blue]🎮 Interactive Demo Mode[/bold blue]")
        console.print("Commands:")
        console.print("  add <option>     - Add string option")
        console.print("  remove <option>  - Remove option by name")
        console.print("  test <choice>    - Test a choice")
        console.print("  state           - Show current state")
        console.print("  quit            - Exit demo")

        while True:
            self.print_full_state()

            try:
                cmd = console.input("\n[bold cyan]Enter command:[/bold cyan] ").strip()

                if cmd.lower() == "quit":
                    break
                if cmd.lower() == "state":
                    continue  # Will print state at top of loop
                if cmd.startswith("add "):
                    option = cmd[4:].strip()
                    self.add_option(option)  # Add as string
                elif cmd.startswith("remove "):
                    option = cmd[7:].strip()
                    self.remove_option_by_name(option)
                elif cmd.startswith("test "):
                    choice = cmd[5:].strip()
                    self.test_model(choice)
                else:
                    console.print(
                        "[yellow]Unknown command. Use: add <option>, remove <option>, test <choice>, state, quit[/yellow]"
                    )

            except KeyboardInterrupt:
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

        console.print("[blue]Demo ended[/blue]")
