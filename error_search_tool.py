#!/usr/bin/env python3
"""Interactive tool to search and query the error database."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


class ErrorSearchTool:

    def __init__(self, db_path="error_analysis/error_database.json"):
        self.db_path = Path(db_path)
        self.load_database()

    def load_database(self):
        """Load the error database."""
        if not self.db_path.exists():
            print(f"Error database not found at {self.db_path}")
            print("Please run analyze_all_errors.py first")
            sys.exit(1)

        with open(self.db_path) as f:
            self.db = json.load(f)

        self.errors = self.db["errors"]
        self.indexes = self.db["indexes"]
        self.stats = self.db["metadata"]["stats"]

        print(f"Loaded {len(self.errors)} errors from database")

    def search(self, query, field=None):
        """Search errors by query string."""
        results = []
        query_lower = query.lower()

        for error in self.errors:
            if field:
                # Search specific field
                if field in error and query_lower in str(error[field]).lower():
                    results.append(error)
            else:
                # Search all text fields
                text_fields = ["message", "file", "type", "module", "traceback"]
                for f in text_fields:
                    if f in error and query_lower in str(error[f]).lower():
                        results.append(error)
                        break

        return results

    def get_by_type(self, error_type):
        """Get all errors of a specific type."""
        error_ids = self.indexes["by_type"].get(error_type, [])
        return [e for e in self.errors if e["id"] in error_ids]

    def get_by_file(self, filepath):
        """Get all errors in a specific file."""
        error_ids = self.indexes["by_file"].get(filepath, [])
        return [e for e in self.errors if e["id"] in error_ids]

    def get_by_package(self, package):
        """Get all errors in a specific package."""
        error_ids = self.indexes["by_package"].get(package, [])
        return [e for e in self.errors if e["id"] in error_ids]

    def get_by_category(self, category):
        """Get all errors in a specific category."""
        error_ids = self.indexes["by_category"].get(category, [])
        return [e for e in self.errors if e["id"] in error_ids]

    def get_by_id(self, error_id):
        """Get specific error by ID."""
        for error in self.errors:
            if error["id"] == error_id:
                return error
        return None

    def get_related_errors(self, error_id):
        """Find errors related to a specific error."""
        error = self.get_by_id(error_id)
        if not error:
            return []

        related = []

        # Find errors in same file
        file_errors = self.get_by_file(error["file"])
        related.extend([e for e in file_errors if e["id"] != error_id])

        # Find errors with same type
        type_errors = self.get_by_type(error["type"])
        related.extend(
            [e for e in type_errors if e["id"] != error_id and e not in related],
        )

        return related[:20]  # Limit to 20

    def get_error_chains(self):
        """Find chains of related errors."""
        chains = defaultdict(list)

        # Group import errors by what they're trying to import
        for error in self.errors:
            if error["type"] in ["ModuleNotFoundError", "ImportError"]:
                if "message" in error:
                    # Extract module name from message
                    msg = error["message"]
                    if "'" in msg:
                        parts = msg.split("'")
                        if len(parts) >= 2:
                            module = parts[1]
                            chains[f"Missing: {module}"].append(error)

        return chains

    def print_error(self, error, verbose=False):
        """Print an error in readable format."""
        print(f"\n{'=' * 80}")
        print(f"Error ID: {error['id']}")
        print(f"Type: {error['type']}")
        print(f"Category: {error['category']}")
        print(f"File: {error['file']}:{error['line']}")
        print(f"Package: {error['package']}")
        print(f"Message: {error['message']}")

        if verbose:
            if error.get("code_context"):
                print("\nCode Context:")
                print(error["code_context"])

            if "traceback" in error:
                print("\nTraceback:")
                print(error["traceback"][:500])

    def print_summary(self, errors):
        """Print summary of error list."""
        if not errors:
            print("No errors found")
            return

        print(f"\nFound {len(errors)} errors:")

        # Group by type
        by_type = defaultdict(int)
        by_package = defaultdict(int)

        for error in errors:
            by_type[error["type"]] += 1
            by_package[error["package"]] += 1

        print("\nBy Type:")
        for err_type, count in sorted(
            by_type.items(),
            key=lambda x: x[1],
            reverse=True,
        ):
            print(f"  {err_type}: {count}")

        print("\nBy Package:")
        for package, count in sorted(by_package.items()):
            print(f"  {package}: {count}")

    def interactive_mode(self):
        """Run interactive search mode."""
        print("\nError Search Tool - Interactive Mode")
        print(
            "Commands: search <query>, type <error_type>, file <path>, package <name>, id <id>, chains, quit",
        )

        while True:
            try:
                cmd = input("\n> ").strip()

                if not cmd:
                    continue

                parts = cmd.split(None, 1)
                command = parts[0].lower()

                if command == "quit" or command == "exit":
                    break

                if command == "search" and len(parts) > 1:
                    results = self.search(parts[1])
                    self.print_summary(results)
                    if results and len(results) <= 5:
                        for error in results:
                            self.print_error(error)

                elif command == "type" and len(parts) > 1:
                    results = self.get_by_type(parts[1])
                    self.print_summary(results)

                elif command == "file" and len(parts) > 1:
                    results = self.get_by_file(parts[1])
                    self.print_summary(results)

                elif command == "package" and len(parts) > 1:
                    results = self.get_by_package(parts[1])
                    self.print_summary(results)

                elif command == "id" and len(parts) > 1:
                    error = self.get_by_id(parts[1])
                    if error:
                        self.print_error(error, verbose=True)

                        # Show related
                        related = self.get_related_errors(parts[1])
                        if related:
                            print(f"\nRelated errors: {len(related)}")
                            for e in related[:5]:
                                print(
                                    f"  - {e['id']}: {e['type']} in {e['file']}:{e['line']}",
                                )
                    else:
                        print("Error not found")

                elif command == "chains":
                    chains = self.get_error_chains()
                    print(f"\nFound {len(chains)} error chains:")
                    for chain_name, errors in sorted(
                        chains.items(),
                        key=lambda x: len(x[1]),
                        reverse=True,
                    )[:10]:
                        print(f"  {chain_name}: {len(errors)} errors")

                elif command == "help":
                    print("Commands:")
                    print("  search <query> - Search all fields")
                    print("  type <error_type> - Get errors by type")
                    print("  file <path> - Get errors in file")
                    print("  package <name> - Get errors in package")
                    print("  id <error_id> - Get specific error")
                    print("  chains - Show error chains")
                    print("  quit - Exit")

                else:
                    print("Unknown command. Type 'help' for commands.")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Search error database")
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument(
        "--db",
        default="error_analysis/error_database.json",
        help="Path to error database",
    )

    args = parser.parse_args()

    tool = ErrorSearchTool(args.db)

    if args.command:
        if args.command == "search" and args.query:
            results = tool.search(args.query)
            tool.print_summary(results)
            for error in results[:10]:
                tool.print_error(error)
        elif args.command == "type" and args.query:
            results = tool.get_by_type(args.query)
            tool.print_summary(results)
        elif args.command == "chains":
            chains = tool.get_error_chains()
            for chain_name, errors in sorted(
                chains.items(),
                key=lambda x: len(x[1]),
                reverse=True,
            )[:20]:
                print(f"{chain_name}: {len(errors)} errors")
        else:
            print(f"Unknown command: {args.command}")
    else:
        # Interactive mode
        tool.interactive_mode()


if __name__ == "__main__":
    main()
