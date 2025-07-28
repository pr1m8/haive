#!/usr/bin/env python3
"""List users from Supabase auth.users table to get user IDs for HAIVE_USER_ID."""

import asyncio
import os
import sys
from datetime import datetime

import asyncpg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def list_supabase_users():
    """List all users from auth.users table."""

    # Get database URL
    database_url = (
        os.getenv("DATABASE_URL")
        or os.getenv("SUPABASE_DATABASE_URL")
        or os.getenv("SUPABASE_DATABASE_URI")
        or os.getenv("SUPABASE_DATABASE_URI_SSL")
        or os.getenv("POSTGRES_URL")
    )

    if not database_url:
        print("❌ No database URL found in environment variables")
        print(
            "   Please set one of: DATABASE_URL, SUPABASE_DATABASE_URL, SUPABASE_DATABASE_URI"
        )
        return

    try:
        print("🔍 Connecting to Supabase...")
        conn = await asyncpg.connect(database_url)

        # Query auth.users table
        print("\n📋 Users in auth.users table:\n")

        users = await conn.fetch(
            """
            SELECT 
                id,
                email,
                created_at,
                last_sign_in_at,
                raw_user_meta_data->>'full_name' as full_name
            FROM auth.users
            ORDER BY created_at
        """
        )

        if not users:
            print("No users found in auth.users table")
            return

        print(f"Found {len(users)} user(s):\n")

        for i, user in enumerate(users, 1):
            print(f"{i}. User ID: {user['id']}")
            print(f"   Email: {user['email']}")
            if user["full_name"]:
                print(f"   Name: {user['full_name']}")
            print(f"   Created: {user['created_at'].strftime('%Y-%m-%d %H:%M:%S')}")
            if user["last_sign_in_at"]:
                print(
                    f"   Last login: {user['last_sign_in_at'].strftime('%Y-%m-%d %H:%M:%S')}"
                )
            print()

        print("\n💡 To use one of these IDs, add to your .env file:")
        print(f"   HAIVE_USER_ID={users[0]['id']}")

        # Also check if there are any threads
        thread_count = await conn.fetchval("SELECT COUNT(*) FROM public.threads")
        if thread_count:
            print(f"\n📊 Found {thread_count} thread(s) in public.threads table")

            # Show thread distribution by user
            user_threads = await conn.fetch(
                """
                SELECT 
                    t.user_id,
                    u.email,
                    COUNT(*) as thread_count
                FROM public.threads t
                LEFT JOIN auth.users u ON t.user_id = u.id
                GROUP BY t.user_id, u.email
                ORDER BY thread_count DESC
            """
            )

            if user_threads:
                print("\n🧵 Threads per user:")
                for ut in user_threads:
                    email = ut["email"] or "Unknown"
                    print(f"   {email}: {ut['thread_count']} threads")

        await conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure your database URL is correct")
        print("2. Ensure you have permission to read auth.users")
        print("3. Check if you're using the service role key (not anon key)")


async def main():
    """Main function."""
    print("🚀 Supabase User ID Finder")
    print("=" * 50)

    await list_supabase_users()


if __name__ == "__main__":
    asyncio.run(main())
