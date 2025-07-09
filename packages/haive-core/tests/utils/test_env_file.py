# tests/utils/test_env_utils.py

import os

import pytest

from haive.core.utils.env_utils import (
    get_env_var,
    is_development,
    is_production,
    is_test,
    is_testing,
    load_env_file,
    load_project_env_files,
)


@pytest.fixture
def test_env_file(tmp_path):
    """Create a temporary .env file for testing."""
    env_file = tmp_path / ".env"
    with open(env_file, "w") as f:
        f.write("TEST_VAR=test_value\n")
        f.write("TEST_INT=42\n")
        f.write("TEST_FLOAT=3.14\n")
        f.write("TEST_BOOL=true\n")
        f.write("# This is a comment\n")
        f.write("TEST_EMPTY=\n")
    return env_file


def test_load_env_file(test_env_file):
    """Test loading environment variables from a file."""
    # Save original environment
    original_env = os.environ.copy()

    try:
        # Clear test variables
        for key in list(os.environ.keys()):
            if key.startswith("TEST_"):
                del os.environ[key]

        # Load test env file
        loaded_vars = load_env_file(test_env_file)

        # Check if variables were loaded
        assert "TEST_VAR" in os.environ
        assert os.environ["TEST_VAR"] == "test_value"
        assert "TEST_INT" in os.environ
        assert os.environ["TEST_INT"] == "42"
        assert "TEST_BOOL" in os.environ
        assert os.environ["TEST_BOOL"] == "true"

        # Check returned dict
        assert "TEST_VAR" in loaded_vars
        assert loaded_vars["TEST_VAR"] == "test_value"

    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)


def test_get_env_var(test_env_file):
    """Test getting environment variables with type casting."""
    # Save original environment
    original_env = os.environ.copy()

    try:
        # Load test env file
        load_env_file(test_env_file)

        # Test string value
        assert get_env_var("TEST_VAR") == "test_value"

        # Test integer casting
        assert get_env_var("TEST_INT", cast_to=int) == 42

        # Test float casting
        assert get_env_var("TEST_FLOAT", cast_to=float) == 3.14

        # Test boolean casting
        assert get_env_var("TEST_BOOL", cast_to=bool) is True

        # Test default value
        assert get_env_var("NON_EXISTENT", default="default") == "default"

        # Test required parameter
        with pytest.raises(ValueError):
            get_env_var("NON_EXISTENT", required=True)

    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)


def test_load_project_env_files(monkeypatch, tmp_path):
    """Test loading environment from multiple locations."""
    # Create a fake project structure in a temp directory
    project_root = tmp_path / "project"
    packages_dir = project_root / "packages"
    haive.core_dir = packages_dir / "haive-core"
    src_dir = haive.core_dir / "src"
    haive.core_src = src_dir / "haive.core"
    utils_dir = haive.core_src / "utils"

    # Create directories
    utils_dir.mkdir(parents=True)

    # Create .env files
    with open(project_root / ".env", "w") as f:
        f.write("ROOT_VAR=root_value\n")
        f.write("COMMON_VAR=root_value\n")

    with open(haive.core_dir / ".env", "w") as f:
        f.write("PACKAGE_VAR=package_value\n")
        f.write("COMMON_VAR=package_value\n")  # Overrides root

    with open(project_root / ".env.local", "w") as f:
        f.write("LOCAL_VAR=local_value\n")
        f.write("COMMON_VAR=local_value\n")  # Highest priority

    # Mock __file__ path to point to our temp directory
    monkeypatch.setattr(
        "haive.core.utils.env_utils.__file__", str(utils_dir / "env_utils.py")
    )

    # Save original environment
    original_env = os.environ.copy()

    try:
        # Clear test variables
        for key in ["ROOT_VAR", "PACKAGE_VAR", "LOCAL_VAR", "COMMON_VAR"]:
            if key in os.environ:
                del os.environ[key]

        # Load project env files
        loaded_vars = load_project_env_files()

        # Check if variables were loaded in correct priority order
        assert os.environ.get("ROOT_VAR") == "root_value"
        assert os.environ.get("PACKAGE_VAR") == "package_value"
        assert os.environ.get("LOCAL_VAR") == "local_value"
        assert (
            os.environ.get("COMMON_VAR") == "local_value"
        )  # Should be overridden by local

    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)


def test_environment_checks():
    """Test environment check helper functions."""
    # Save original environment
    original_env = os.environ.copy()

    try:
        # Test production check
        os.environ["ENV"] = "production"
        assert is_production() is True
        assert is_development() is False
        assert is_test() is False
        assert is_testing() is False

        # Test development check
        os.environ["ENV"] = "development"
        assert is_production() is False
        assert is_development() is True
        assert is_test() is False
        assert is_testing() is False

        # Test test check
        os.environ["ENV"] = "test"
        assert is_production() is False
        assert is_development() is False
        assert is_test() is True
        assert is_testing() is True

    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)
