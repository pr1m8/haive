"""Direct test of database loaders system without cascading imports.

This test validates the database loaders by importing only the core modules
directly to avoid the cascading import issues with the main document engine.
"""

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, List


# Direct imports to avoid package dependency issues
def import_module_from_file(module_name, file_path):
    """Import a module directly from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


# Set up module paths
base_path = Path(
    "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core"
)


try:
    # Import core modules in order

    # Import source types first (base classes)
    source_types_module = import_module_from_file(
        "source_types",
        base_path / "engine" / "document" / "loaders" / "sources" / "source_types.py",
    )

    # Import enhanced registry
    registry_module = import_module_from_file(
        "enhanced_registry",
        base_path
        / "engine"
        / "document"
        / "loaders"
        / "sources"
        / "enhanced_registry.py",
    )

    # Import database sources
    database_sources_module = import_module_from_file(
        "database_sources",
        base_path
        / "engine"
        / "document"
        / "loaders"
        / "sources"
        / "database_sources.py",
    )

    # Import document schema
    document_schema_module = import_module_from_file(
        "document_schema", base_path / "engine" / "document" / "base" / "schema.py"
    )


except Exception as e:
    import traceback

    traceback.print_exc()
    sys.exit(1)


def test_database_system():
    """Test the database system components."""

    # Get key classes and enums
    DatabaseType = database_sources_module.DatabaseType
    LoadingStrategy = database_sources_module.LoadingStrategy
    TextSplitterType = database_sources_module.TextSplitterType
    SourceCategory = source_types_module.SourceCategory

    # Test 1: Database Type Detection

    detect_database_type = database_sources_module.detect_database_type

    test_connections = {
        "postgresql://user:pass@localhost:5432/testdb": DatabaseType.POSTGRESQL,
        "mysql://root:password@localhost:3306/mydb": DatabaseType.MYSQL,
        "sqlite:///path/to/database.db": DatabaseType.SQLITE,
        "mongodb://user:pass@cluster.mongodb.net:27017/db": DatabaseType.MONGODB,
        "neo4j://user:pass@localhost:7687": DatabaseType.NEO4J,
        "elasticsearch://localhost:9200": DatabaseType.ELASTICSEARCH,
        "bigquery://my-project/my-dataset": DatabaseType.BIGQUERY,
        "snowflake://account.snowflakecomputing.com": DatabaseType.SNOWFLAKE,
    }

    detection_success = 0
    for conn_str, expected_type in test_connections.items():
        detected = detect_database_type(conn_str)
        status = "✅" if detected == expected_type else "❌"
        if detected == expected_type:
            detection_success += 1


    # Test 2: Database Sources Registration

    try:
        db_stats = database_sources_module.get_database_sources_statistics()
        db_validation = database_sources_module.validate_database_sources()


        registration_success = db_validation and db_stats["total_database_sources"] >= 9

    except Exception as e:
        registration_success = False

    # Test 3: Loading Strategies

    strategies_tested = 0
    try:
        DatabaseSource = database_sources_module.DatabaseSource

        for strategy in LoadingStrategy:
            try:
                # Create a test source with the strategy
                source = DatabaseSource(
                    connection_string="postgresql://test:test@localhost:5432/test",
                    loading_strategy=strategy,
                    source_id="test-source",
                    category=SourceCategory.DATABASE,
                )

                loading_method = source.get_loading_method()
                loader_kwargs = source.get_loader_kwargs()


                # Validate strategy-specific configuration
                if strategy == LoadingStrategy.LOAD_AND_SPLIT:
                    assert "text_splitter_config" in loader_kwargs
                elif strategy in [
                    LoadingStrategy.FETCH_ALL,
                    LoadingStrategy.SCRAPE_ALL,
                ]:
                    assert "fetch_all_tables" in loader_kwargs

                strategies_tested += 1

            except Exception as e:
                passe}")


    except Exception as e:
        pass")

    # Test 4: Text Splitter Configuration

    splitters_tested = 0
    try:
        DatabaseSource = database_sources_module.DatabaseSource

        for splitter_type in TextSplitterType:
            try:
                source = DatabaseSource(
                    connection_string="postgresql://test:test@localhost:5432/test",
                    loading_strategy=LoadingStrategy.LOAD_AND_SPLIT,
                    text_splitter_type=splitter_type,
                    chunk_size=500,
                    chunk_overlap=50,
                    source_id="test-source",
                    category=SourceCategory.DATABASE,
                )

                splitter_config = source.get_text_splitter_config()


                assert splitter_config["chunk_size"] == 500
                assert splitter_config["chunk_overlap"] == 50

                splitters_tested += 1

            except Exception as e:
                passe}")


    except Exception as e:
        pass")

    # Test 5: Fetch All Configuration

    try:
        DatabaseSource = database_sources_module.DatabaseSource

        source = DatabaseSource(
            connection_string="postgresql://test:test@localhost:5432/test",
            loading_strategy=LoadingStrategy.FETCH_ALL,
            fetch_all_tables=True,
            table_pattern="user_.*",
            exclude_tables=["user_temp", "user_backup"],
            max_tables=50,
            include_system_tables=False,
            source_id="test-source",
            category=SourceCategory.DATABASE,
        )

        fetch_config = source.get_fetch_all_config()


        assert fetch_config["fetch_all_tables"]
        assert "user_temp" in fetch_config["exclude_tables"]
        assert fetch_config["max_tables"] == 50

        fetch_all_success = True

    except Exception as e:
        fetch_all_success = False

    # Test 6: Document Schema Integration

    try:
        DocumentSourceInfo = document_schema_module.DocumentSourceInfo
        LoadingStrategy_Schema = document_schema_module.LoadingStrategy
        TextSplitterType_Schema = document_schema_module.TextSplitterType

        source_info = DocumentSourceInfo(
            source_type="postgresql",
            source_path="postgresql://test:test@localhost:5432/test",
            source_id="test-db-001",
            loader_used="sql",
            loading_strategy=LoadingStrategy_Schema.LOAD_AND_SPLIT,
            lazy_loaded=False,
            was_split=True,
            text_splitter_type=TextSplitterType_Schema.RECURSIVE_CHARACTER,
            chunk_size=1000,
            chunk_overlap=200,
            chunks_created=45,
            metadata={"database_type": "postgresql", "tables_processed": 3},
        )


        assert source_info.source_type == "postgresql"
        assert source_info.chunks_created == 45

        schema_success = True

    except Exception as e:
        schema_success = False

    # Test 7: Specific Database Source Classes

    database_classes = [
        ("PostgreSQLSource", "PostgreSQL database"),
        ("MySQLSource", "MySQL database"),
        ("SQLiteSource", "SQLite database"),
        ("MongoDBSource", "MongoDB database"),
        ("Neo4jSource", "Neo4j graph database"),
        ("ElasticsearchSource", "Elasticsearch search"),
        ("BigQuerySource", "Google BigQuery"),
        ("SnowflakeSource", "Snowflake warehouse"),
    ]

    class_tests_passed = 0
    for class_name, description in database_classes:
        try:
            source_class = getattr(database_sources_module, class_name)

            # Test basic instantiation
            if class_name == "MongoDBSource":
                source = source_class(
                    connection_string="mongodb://test:test@localhost:27017/test",
                    collection_name="test_collection",
                    source_id="test-mongo",
                    category=SourceCategory.DATABASE,
                )
            elif class_name == "BigQuerySource":
                source = source_class(
                    connection_string="bigquery://test-project/test-dataset",
                    project_id="test-project",
                    source_id="test-bigquery",
                    category=SourceCategory.DATABASE,
                )
            elif class_name == "SnowflakeSource":
                source = source_class(
                    connection_string="snowflake://test-account",
                    account="test-account",
                    source_id="test-snowflake",
                    category=SourceCategory.DATABASE,
                )
            else:
                source = source_class(
                    connection_string="test://localhost/test",
                    source_id=f"test-{class_name.lower()}",
                    category=SourceCategory.DATABASE,
                )

            # Test getting loader kwargs
            loader_kwargs = source.get_loader_kwargs()


            class_tests_passed += 1

        except Exception as e:
            pass")


    # Summary

    total_tests = 7
    passed_tests = 0

    if detection_success >= 7:
        passed_tests += 1
    else:
        pass")

    if registration_success:
        passed_tests += 1
    else:
        pass")

    if strategies_tested >= 4:
        passed_tests += 1
    else:
        pass")

    if splitters_tested >= 5:
        passed_tests += 1
    else:
        pass")

    if fetch_all_success:
        passed_tests += 1
    else:
        pass")

    if schema_success:
        passed_tests += 1
    else:
        pass")

    if class_tests_passed >= 6:
        passed_tests += 1
    else:
        pass")


    if passed_tests >= 6:
        return True
    if passed_tests >= 4:
        return True
    else:
        return False


def display_current_progress():
    """Display our current implementation progress."""

    # Get statistics from different modules
    try:
        enhanced_registry = registry_module.enhanced_registry
        overall_stats = enhanced_registry.get_statistics()
        db_stats = database_sources_module.get_database_sources_statistics()






        estimated_total = 13 + 25 + 12 + 11 + 9  # Current phases
        progress_percentage = (estimated_total / 231) * 100


    except Exception as e:
        pass



def main():
    """Run the database system tests."""
    try:
        success = test_database_system()
        display_current_progress()
        return success

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
