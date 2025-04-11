from src.haive.dataflow.db.supabase import (
    get_supabase_client,
    fetch_all_schemas_and_tables,
    fetch_foreign_key_relations,
    fetch_table_columns,
    fetch_primary_keys
)

def main():
    client = get_supabase_client()

    print("📄 Tables by Schema:\n")
    for row in fetch_all_schemas_and_tables(client):
        print(f"{row['table_schema']}.{row['table_name']} ({row['table_type']})")

    print("\n🔗 Foreign Key Relationships:\n")
    for fk in fetch_foreign_key_relations(client):
        print(
            f"{fk['table_schema']}.{fk['table_name']}.{fk['column_name']} -> "
            f"{fk['foreign_table_schema']}.{fk['foreign_table_name']}.{fk['foreign_column_name']}"
        )

    print("\n🔑 Primary Keys:\n")
    for pk in fetch_primary_keys(client):
        print(f"{pk['table_schema']}.{pk['table_name']}.{pk['column_name']} (PK)")

    print("\n🧬 Column Definitions:\n")
    for col in fetch_table_columns(client):
        print(
            f"{col['table_schema']}.{col['table_name']}.{col['column_name']} "
            f"({col['data_type']}, {'NULLABLE' if col['is_nullable'] == 'YES' else 'NOT NULL'}) "
            f"default={col['column_default']}"
        )

if __name__ == "__main__":
    main()
