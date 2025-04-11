from pathlib import Path

def clear_env_values(env_path: str = ".env.example") -> None:
    path = Path(env_path)
    if not path.exists():
        print(f"File not found: {env_path}")
        return

    cleaned_lines = []
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            cleaned_lines.append(line)
        else:
            key = stripped.split("=", 1)[0]
            cleaned_lines.append(f"{key}=")

    path.write_text("\n".join(cleaned_lines) + "\n")
    print(f"Values cleared from {env_path}")

if __name__ == "__main__":
    clear_env_values()
