import os

# Optionally display the image (for local viewing, using PIL)
# Function to render and display the graph
from haive.core.config.constants import GRAPH_IMAGES_DIR


def render_and_display_graph(
    compiled_graph,
    output_dir=GRAPH_IMAGES_DIR,
    output_name="graph.png",
):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Generate the Mermaid diagram PNG
        png_data = compiled_graph.get_graph(xray=True).draw_mermaid_png()
        output_path = os.path.join(output_dir, output_name)
        # Save the PNG data to a file

        with open(output_path, "wb") as f:
            f.write(png_data)

    except Exception:
        pass


# Assuming `graph` is your graphviz graph object
