#!/usr/bin/env python3
"""Check available user IDs from auth.users table."""
from __future__ import annotations

import os
from urllib.parse import urlparse

import psycopg
from dotenv import load_dotenv
from langmem import LangMem

# Load environment variables from .env file
load_dotenv()


def get_database_connection():
    """Get database connection from environment variables."""
    # Use POSTGRES_CONNECTION_STRING specifically
    connection_url = os.getenv("POSTGRES_CONNECTION_STRING")

    if connection_url:
        # Handle if it includes {} format placeholder
        if "{}" in connection_url:
            connection_url = connection_url.format("postgres")
        return connection_url

    # Fallback to other options
    fallback_urls = [
        os.getenv("DATABASE_URL"),
        os.getenv("SUPABASE_DATABASE_URL"),
    ]

    for url in fallback_urls:
        if url:
            # Handle Supabase format with {}
            if "{}" in url:
                url = url.format("postgres")
            return url

    # Last resort - local
    return "postgresql://postgres:postgres@localhost:5432/postgres"


def main():
    """Check auth.users table for available user IDs."""

    try:
        # Get connection string
        conn_string = get_database_connection()

        # Connect to database
        with psycopg.connect(conn_string) as conn, conn.cursor() as cursor:
            print("✅ Connected successfully!")

            # Check if auth.users table exists
            cursor.execute(
                """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_schema = 'auth'
                        AND table_name = 'users'
                    )
                """
            )
            auth_users_exists = cursor.fetchone()[0]

            if not auth_users_exists:
                print("❌ auth.users table does not exist")

                # Check for users in public schema
                cursor.execute(
                    """
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables
                            WHERE table_schema = 'public'
                            AND table_name = 'users'
                        )
                    """
                )
                public_users_exists = cursor.fetchone()[0]

                if public_users_exists:
                    print("✅ Found public.users table instead")
                    cursor.execute("SELECT id, email FROM public.users LIMIT 10")
                    users = cursor.fetchall()

                    print(
                        f"\n📋 Available users in public.users ({len(users)} shown):"
                    )
                    for user in users:
                        print(f"  - ID: {user[0]}")
                        print(f"    Email: {user[1] if user[1] else 'No email'}")
                        print()
                else:
                    print("❌ No users table found in public schema either")

                    # Check what tables exist
                    cursor.execute(
                        """
                            SELECT table_schema, table_name
                            FROM information_schema.tables
                            WHERE table_schema IN ('auth', 'public')
                            ORDER BY table_schema, table_name
                        """
                    )
                    tables = cursor.fetchall()

                    print("\n📋 Available tables:")
                    for schema, table in tables:
                        print(f"  - {schema}.{table}")
            else:
                print("✅ auth.users table exists")

                # Get users from auth.users
                cursor.execute("SELECT id, email FROM auth.users LIMIT 10")
                users = cursor.fetchall()

                print(f"\n📋 Available users in auth.users ({len(users)} shown):")
                for user in users:
                    print(f"  - ID: {user[0]}")
                    print(f"    Email: {user[1] if user[1] else 'No email'}")
                    print()

            # Also check threads table structure
            print("\n🔍 Checking threads table structure...")
            cursor.execute(
                """
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns
                    WHERE table_schema = 'public' AND table_name = 'threads'
                    ORDER BY ordinal_position
                """
            )
            columns = cursor.fetchall()

            if columns:
                print("📋 Threads table structure:")
                for col in columns:
                    nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                    default = f" DEFAULT {col[3]}" if col[3] else ""
                    print(f"  - {col[0]} ({col[1]}) {nullable}{default}")

                # Check constraints
                cursor.execute(
                    """
                        SELECT constraint_name, constraint_type
                        FROM information_schema.table_constraints
                        WHERE table_schema = 'public' AND table_name = 'threads'
                    """
                )
                constraints = cursor.fetchall()

                if constraints:
                    print("\n🔗 Threads table constraints:")
                    for constraint in constraints:
                        print(f"  - {constraint[0]} ({constraint[1]})")
            else:
                print("❌ Threads table does not exist")")

    except Exception as e:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
