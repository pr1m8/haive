"""
A simple example
================

This is a simple example to test Sphinx Gallery.
"""

# %%
# Plotting a simple graph
# -----------------------
# Let's create a simple plot to test the gallery.

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.title("Simple Sine Wave")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.grid(True)
plt.show()

# %%
# Simple calculation
# ------------------
# Let's do a simple calculation.

result = 2 + 2
print(f"2 + 2 = {result}")

print("Gallery example completed!")
