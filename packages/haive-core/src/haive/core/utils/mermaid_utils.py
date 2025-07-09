"""
Mermaid diagram utilities for Haive.

This module provides utilities for generating and displaying Mermaid diagrams
in different environments, with fallback mechanisms.
"""

import os
import subprocess
import tempfile
from enum import Enum
from typing import Optional


class Environment(str, Enum):
    """Execution environment types."""

    JUPYTER_NOTEBOOK = "jupyter_notebook"
    JUPYTER_LAB = "jupyter_lab"
    VSCODE_NOTEBOOK = "vscode_notebook"
    COLAB = "colab"
    TERMINAL = "terminal"
    UNKNOWN = "unknown"


def detect_environment() -> Environment:
    """
    Detect the current execution environment.

    Returns:
        Environment enum indicating the detected environment
    """
    try:
        # Check if running in IPython
        import IPython

        # Test if we're in a notebook environment at all
        shell = IPython.get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":  # Jupyter environment
            try:
                # Check for Colab
                import google.colab

                return Environment.COLAB
            except ImportError:
                # Check for VSCode
                if "VSCODE_PID" in os.environ:
                    return Environment.VSCODE_NOTEBOOK

                # Try to determine if we're in JupyterLab or classic notebook
                try:
                    # In Jupyter Lab, we can check the IPython config
                    app_name = (
                        IPython.get_ipython()
                        .config.get("IPKernelApp", {})
                        .get("connection_file", "")
                    )
                    if "jupyter-lab" in app_name or "jpserver" in app_name:
                        return Environment.JUPYTER_LAB
                    return Environment.JUPYTER_NOTEBOOK
                except:
                    # Fallback to classic notebook
                    return Environment.JUPYTER_NOTEBOOK
        else:
            # Terminal IPython or script
            return Environment.TERMINAL
    except (ImportError, AttributeError, NameError):
        # Not running in IPython
        return Environment.UNKNOWN


def mermaid_to_png(
    mermaid_code: str, output_path: Optional[str] = None
) -> Optional[str]:
    """
    Convert Mermaid diagram code to a PNG file.

    Args:
        mermaid_code: Mermaid diagram code as string
        output_path: Path to save the PNG file (auto-generated if not provided)

    Returns:
        Path to the generated PNG file, or None if conversion failed
    """
    # Create a temporary file for the mermaid code
    with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False) as mmd_file:
        mmd_file.write(mermaid_code)
        mmd_path = mmd_file.name

    try:
        # Generate default output path if not provided
        if not output_path:
            output_dir = os.path.join(os.getcwd(), "graph_images")
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(
                output_dir, f"diagram_{os.path.basename(mmd_path)}.png"
            )

        # Try using mmdc (Mermaid CLI) if available
        try:
            subprocess.run(
                ["mmdc", "-i", mmd_path, "-o", output_path, "-b", "transparent"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return output_path
        except (subprocess.SubprocessError, FileNotFoundError):
            # Fallback to puppeteer if available
            try:
                subprocess.run(
                    [
                        "npx",
                        "@mermaid-js/mermaid-cli",
                        "-i",
                        mmd_path,
                        "-o",
                        output_path,
                    ],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                return output_path
            except (subprocess.SubprocessError, FileNotFoundError):
                # If both fail, use a web-based approach with base64 encoding
                print(
                    "Warning: Mermaid CLI not found. Using online rendering fallback."
                )

                # Create an HTML file with the diagram embedded
                with open(output_path.replace(".png", ".html"), "w") as f:
                    f.write(
                        f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <title>Mermaid Diagram</title>
                        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
                    </head>
                    <body>
                        <div class="mermaid">{mermaid_code}</div>
                        <script>
                            mermaid.initialize({{startOnLoad:true}});
                        </script>
                    </body>
                    </html>
                    """
                    )

                print(f"HTML diagram saved as: {output_path.replace('.png', '.html')}")
                return None
    finally:
        # Clean up the temporary file
        try:
            os.unlink(mmd_path)
        except:
            pass


def display_mermaid(
    mermaid_code: str,
    output_path: Optional[str] = None,
    save_png: bool = False,
    width: str = "100%",
) -> None:
    """
    Display a Mermaid diagram in the current environment.

    This function detects the current environment and uses the appropriate
    method to display the diagram, with fallbacks for each environment.

    Args:
        mermaid_code: Mermaid diagram code
        output_path: Optional path to save the diagram
        save_png: Whether to save the diagram as PNG
        width: Width of the displayed diagram
    """
    # Detect the current environment
    env = detect_environment()

    # Try multiple approaches based on the environment
    if env in [
        Environment.JUPYTER_NOTEBOOK,
        Environment.JUPYTER_LAB,
        Environment.VSCODE_NOTEBOOK,
        Environment.COLAB,
    ]:
        # We're in a notebook environment
        try:
            from IPython.display import HTML, Image, Markdown, display

            # First approach: Try direct Mermaid rendering via Markdown
            # This works in JupyterLab with the mermaid extension
            try:
                display(Markdown(f"```mermaid\n{mermaid_code}\n```"))
                return
            except:
                pass

            # Second approach: Use HTML with CDN
            # This works in most environments if JavaScript is allowed
            try:
                html = f"""
                <div class="mermaid" style="width: {width};">
                {mermaid_code}
                </div>
                <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
                <script>
                    mermaid.initialize({{startOnLoad:true}});
                </script>
                """
                display(HTML(html))
                return
            except:
                pass

            # Third approach: Use require.js if available (JupyterLab)
            try:
                html = f"""
                <div id="mermaid-{id(mermaid_code)}" class="mermaid" style="width: {width};">
                {mermaid_code}
                </div>
                <script>
                require.config({{
                    paths: {{
                        mermaid: 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min'
                    }}
                }});
                require(['mermaid'], function(mermaid) {{
                    mermaid.initialize({{startOnLoad:true}});
                    mermaid.init(undefined, '.mermaid');
                }});
                </script>
                """
                display(HTML(html))
                return
            except:
                pass

            # Fourth approach: Save to PNG and display the image
            if save_png or output_path:
                png_path = mermaid_to_png(mermaid_code, output_path)
                if png_path and os.path.exists(png_path):
                    display(Image(png_path, width=width))
                    print(f"Diagram saved as: {png_path}")
                    return

            # Final approach: Just show the Mermaid code
            print("Unable to render Mermaid diagram. Displaying code:")
            print(f"```mermaid\n{mermaid_code}\n```")

        except ImportError:
            # If IPython is not available, fall back to terminal mode
            print("Mermaid diagram code:")
            print(f"```mermaid\n{mermaid_code}\n```")

    else:
        # Terminal or unknown environment
        print("Mermaid diagram code:")
        print(f"```mermaid\n{mermaid_code}\n```")

        # Save to PNG if requested
        if save_png or output_path:
            png_path = mermaid_to_png(mermaid_code, output_path)
            if png_path:
                print(f"Diagram saved as: {png_path}")
