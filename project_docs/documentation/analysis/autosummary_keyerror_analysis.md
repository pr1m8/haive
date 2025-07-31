# Autosummary KeyError Analysis Report

## Root Cause Identified

The KeyError `'containers_tilebag'` is caused by a problematic filename in the haive-games package:

**Problem File**: `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/containers/containers_tilebag (1).py`

### Issues with this file:

1. Contains spaces in the filename
2. Contains parentheses in the filename
3. Invalid Python module name (cannot be imported normally)

When Sphinx's autosummary/autoapi tries to process this file, it fails because:

- Python module names cannot contain spaces or parentheses
- The autosummary system tries to import it as a module
- This causes a KeyError when looking up the module

## Additional Issues Found

### 1. Missing imports in container.py

The file `/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/containers/container.py` has:

- Missing import for `uuid`
- Missing import for `random`
- Missing import for `Callable` from typing
- Missing import for `TypeVar` to define generic `T`
- Missing imports for `Card`, `Tile`, `PlayingCard`, `Position`, `Board`

### 2. Duplicate Code

The problematic file `containers_tilebag (1).py` appears to be a duplicate of the `TileBag` class already defined in `container.py`

## Recommended Fixes

### 1. Remove the problematic file

```bash
rm "/home/will/Projects/haive/backend/haive/packages/haive-games/src/haive/games/core/game/containers/containers_tilebag (1).py"
```

### 2. Fix imports in container.py

Add the following imports at the top of the file:

```python
import uuid
import random
from typing import Generic, TypeVar, Callable
from ..pieces import Card, Tile, PlayingCard
from ..board import Position, Board

T = TypeVar('T')
```

### 3. Clean up any other files with problematic names

Search for and rename/remove any other files with spaces, parentheses, or special characters in their names.

## Impact

- This is preventing the documentation from building successfully
- The autosummary extension cannot process modules with invalid names
- This affects the entire documentation generation process

## Verification

After fixing, verify with:

```bash
poetry run sphinx-build -b html docs/source docs/build
```

The KeyError should be resolved once the problematic file is removed.
