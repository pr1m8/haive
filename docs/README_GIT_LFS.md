# Documentation Version Control with Git LFS

This document explains how we version control the built documentation using Git LFS.

## Overview

We use Git LFS (Large File Storage) to track built documentation while keeping the main repository size manageable. This allows us to:

- Version control the built documentation
- Share documentation builds across the team
- Keep a history of documentation changes
- Deploy specific documentation versions

## Setup

### 1. Install Git LFS

```bash
# macOS
brew install git-lfs

# Ubuntu/Debian
apt-get install git-lfs

# Windows
# Download from https://git-lfs.github.com/
```

### 2. Initialize Git LFS in the repository

```bash
git lfs install
```

## Directory Structure

```
docs/
├── source/          # Documentation source files (in git)
├── build/           # Local build output (in .gitignore)
├── published/       # Published docs tracked with Git LFS
│   ├── current/     # Symlink to latest version
│   └── README.md    # Published docs info
└── versions/        # All documentation versions
    ├── v1.0.0/      # Tagged releases
    ├── v1.1.0/
    └── dev-abc123/  # Development builds
```

## Publishing Documentation

We provide a script to automate the documentation publishing process:

```bash
# Run the publish script
./scripts/maintenance/docs/publish_docs.sh
```

This script will:

1. Build the documentation using `nox -s docs`
2. Create a version identifier (git tag or commit-based)
3. Copy built docs to `docs/versions/<version>`
4. Update the `current` symlink
5. Stage files for Git LFS
6. Create a commit

## Manual Publishing

If you prefer to publish manually:

```bash
# 1. Build documentation
nox -s docs

# 2. Create version directory
VERSION="v1.0.0"  # or "dev-$(git rev-parse --short HEAD)"
mkdir -p docs/versions/$VERSION

# 3. Copy built docs
cp -r docs/build/html/* docs/versions/$VERSION/

# 4. Update current symlink
rm -f docs/published/current
ln -s ../versions/$VERSION docs/published/current

# 5. Add to Git LFS
git add docs/published/
git add docs/versions/$VERSION

# 6. Commit
git commit -m "docs: Publish documentation $VERSION"

# 7. Push (including LFS objects)
git push origin main
git lfs push --all origin
```

## Viewing Documentation

### Local Development

```bash
# View current published version
python -m http.server 8003 --directory docs/published/current/

# View specific version
python -m http.server 8003 --directory docs/versions/v1.0.0/

# View latest build (not version controlled)
python -m http.server 8003 --directory docs/build/html/
```

### Deployed Documentation

The `docs/published/current` directory can be deployed to any static hosting service.

## Best Practices

1. **Tag Releases**: When releasing, create a git tag first so the documentation version matches:

   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   ./scripts/maintenance/docs/publish_docs.sh
   ```

2. **Development Builds**: For development, the script automatically creates versions like `dev-abc123-20231215-143022`

3. **Storage Considerations**: Git LFS stores files on a remote server. Make sure your Git LFS storage quota is sufficient.

4. **CI/CD Integration**: The publish script can be integrated into CI/CD pipelines for automatic documentation publishing.

## Troubleshooting

### LFS Not Initialized

```bash
git lfs install
git lfs track "docs/published/**"
git lfs track "docs/versions/**"
```

### Large File Warnings

If you get warnings about large files:

```bash
git lfs migrate import --include="docs/published/**,docs/versions/**"
```

### Viewing LFS Status

```bash
git lfs status
git lfs ls-files
```

## Configuration Files

### .gitattributes

Defines which files are tracked by Git LFS:

```
docs/published/**/*.html filter=lfs diff=lfs merge=lfs -text
docs/versions/**/*.html filter=lfs diff=lfs merge=lfs -text
# ... and other file types
```

### .gitignore

The `docs/build/` directory remains in `.gitignore` since it's for local builds only.

## Summary

Using Git LFS for documentation allows us to:

- ✅ Version control built documentation
- ✅ Keep main repository size small
- ✅ Share documentation across team
- ✅ Deploy specific versions
- ✅ Track documentation history

The `publish_docs.sh` script automates the entire process, making it easy to publish new documentation versions.
