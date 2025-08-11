#! /usr/bin/env python3

##########
# to run:
#   python remove_abandoned_files.py
# more at:
#   https://github.com/approvals/ApprovalTests.CommonScripts/blob/main/docs/how_to/run.md
##########

from enum import Enum
from pathlib import Path
from typing import Callable, List

SCRIPT_DIR = Path(__file__).parent


class Mode(Enum):
    DELETE_WITHOUT_PROMPTING = 1
    PROMPT = 2
    DRY_RUN = 3


def delete_file(path: Path) -> None:
    path.unlink(missing_ok=True)


def load_touched_files() -> List[str]:
    return (SCRIPT_DIR / ".approved_files.log").read_text().splitlines()


def get_all_approved_files() -> List[str]:
    return list(map(str, SCRIPT_DIR.parent.rglob("*.approved.*")))


def remove_abandoned_files(
    *,
    mode: Mode,
    load_touched_files: Callable[[], List[str]] = load_touched_files,
    get_all_approved_files: Callable[[], List[str]] = get_all_approved_files,
    delete: Callable[[Path], None] = delete_file,
    system_out: Callable[[str], None] = print,
    get_input: Callable[[], str] = input,
) -> None:
    touched_files = [Path(file).as_posix() for file in load_touched_files()]
    all_approved_files = [Path(file).as_posix() for file in get_all_approved_files()]

    stray_files = [
        Path(file) for file in all_approved_files if file not in touched_files
    ]
    report_dry_run(system_out, stray_files)

    if len(stray_files) and should_delete(mode, system_out, get_input):
        for stray_file in stray_files:
            delete(stray_file)
        report_final_status(system_out, stray_files)
    else:
        system_out("No files were deleted.")


def should_delete(
    mode: Mode, system_out: Callable[[str], None], get_input: Callable[[], str] = input
) -> bool:
    if mode == Mode.PROMPT:
        system_out("Delete? [Y/n]")
        response = get_input()
        return response in ["Y", "y", ""]
    elif mode == Mode.DELETE_WITHOUT_PROMPTING:
        return True
    elif mode == Mode.DRY_RUN:
        return False

    return False


def report_dry_run(system_out: Callable[[str], None], stray_files: List[Path]) -> None:
    if not len(stray_files):
        system_out("No unused `.approved.` files found.\n")
        return

    system_out("Unused `.approved.` files found.\n")

    for stray_file in stray_files:
        system_out(f" - {stray_file.name} (in {stray_file.parent.as_posix()}/)")


def report_final_status(
    system_out: Callable[[str], None], stray_files: List[Path]
) -> None:
    system_out("")
    system_out(f"Deleted {len(stray_files)} files.")


if __name__ == "__main__":
    remove_abandoned_files(mode=Mode.PROMPT)
