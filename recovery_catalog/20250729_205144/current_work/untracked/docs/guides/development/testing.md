# Documentation Testing Tools

This directory contains comprehensive testing tools for validating the Haive documentation build, CSS alignment, game demos, and visual appearance.

## Quick Start

Run all basic tests (CSS and game demo validation):

```bash
poetry run python docs/run_all_doc_tests.py
```

Run all tests including screenshots:

```bash
poetry run python docs/run_all_doc_tests.py --all
```

## Available Test Scripts

### 1. Master Test Runner (`run_all_doc_tests.py`)

Runs all documentation tests and generates a comprehensive report.

```bash
# Basic validation only
poetry run python docs/run_all_doc_tests.py

# Include screenshot tests
poetry run python docs/run_all_doc_tests.py --screenshots

# Include visual browser check
poetry run python docs/run_all_doc_tests.py --visual

# Run everything
poetry run python docs/run_all_doc_tests.py --all
```

### 2. Screenshot Testing (`test_documentation_screenshots.py`)

Takes screenshots of all major pages at different viewport sizes and validates content.

```bash
poetry run python docs/test_documentation_screenshots.py
```

Features:

- Tests at 4 viewport sizes (desktop, laptop, tablet, mobile)
- Captures screenshots of all major pages
- Checks for CSS alignment issues
- Validates navigation and content presence
- Verifies game streaming content
- Generates detailed report with screenshots

Output:

- Screenshots: `docs/test_screenshots/`
- Report: `docs/documentation_test_report.md`

### 3. CSS Validation (`validate_css_fixes.py`)

Validates that CSS fixes for alignment and game content are properly applied.

```bash
poetry run python docs/validate_css_fixes.py
```

Checks:

- Container max-width and alignment
- Text alignment fixes
- Navigation styles
- Game demo CSS classes
- Responsive styles
- Code block alignment

### 4. Game Demo Validation (`validate_game_demos.py`)

Validates game demo pages have proper streaming content and structure.

```bash
poetry run python docs/validate_game_demos.py
```

Validates:

- RST source files have streaming directives
- HTML output contains game-demo classes
- Asciinema or streaming players present
- Proper game demo structure

### 5. Quick Visual Check (`quick_visual_check.py`)

Opens documentation pages in browser for manual visual inspection.

```bash
poetry run python docs/quick_visual_check.py
```

Features:

- Builds documentation
- Starts local server
- Opens key pages in browser
- Provides visual checklist

## Test Scenarios

### Scenario 1: Quick Validation

```bash
# Just validate CSS and structure
poetry run python docs/validate_css_fixes.py
poetry run python docs/validate_game_demos.py
```

### Scenario 2: Full Automated Testing

```bash
# Run all tests with screenshots
poetry run python docs/run_all_doc_tests.py --screenshots
```

### Scenario 3: Manual Visual Review

```bash
# Build and open in browser
poetry run python docs/quick_visual_check.py
```

### Scenario 4: Comprehensive Testing

```bash
# Everything including visual check
poetry run python docs/run_all_doc_tests.py --all
```

## Understanding Test Results

### CSS Validation Results

✅ **Pass**: All CSS alignment fixes are in place
❌ **Fail**: Missing required CSS rules

Common issues:

- Container not properly aligned
- Missing game-demo classes
- No responsive styles

### Game Demo Validation Results

✅ **Pass**: All game demos have streaming content
❌ **Fail**: Missing streaming directives or classes

Common issues:

- No `.. class:: game-demo streaming-content` directive
- Missing asciinema embed code
- No raw HTML blocks for streaming

### Screenshot Test Results

The screenshot report shows:

- Screenshots at 4 viewport sizes
- CSS alignment issues (elements overflowing)
- Console errors
- Missing content or navigation

## Fixing Common Issues

### 1. CSS Alignment Problems

Edit `docs/source/_static/haive-minimal.css` and ensure:

```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.body,
[role="main"] {
  text-align: left;
}
```

### 2. Missing Game Streaming Content

Edit `docs/source/games/demos/{game}-demo.rst`:

```rst
.. class:: game-demo streaming-content

   .. raw:: html

      <div id="player-{game}"></div>
      <script src="https://asciinema.org/a/{cast_id}.js"
              id="asciicast-{cast_id}"
              async>
      </script>
```

### 3. Build Errors

```bash
# Clean build
rm -rf docs/build
poetry run sphinx-build -b html docs/source docs/build/html
```

## Requirements

- Python 3.8+
- Poetry
- Sphinx
- For screenshots: Playwright (`poetry add --group dev playwright`)
- For visual check: Web browser

## Troubleshooting

### Playwright Not Installed

```bash
poetry add --group dev playwright
poetry run playwright install chromium
```

### Server Already Running

```bash
# Kill existing server on port 8003
lsof -ti:8003 | xargs kill -9
```

### Documentation Won't Build

```bash
# Check for errors
poetry run sphinx-build -b html docs/source docs/build/html -v
```

## Contributing

When updating documentation:

1. Run CSS validation after style changes
2. Run game demo validation after adding demos
3. Run screenshot tests before releasing
4. Use visual check for final review
