#!/usr/bin/env python
"""Run the Among Us game with the new enhanced features."""

from haive.games.among_us.demo import run_among_us_demo


def main():
    """Run the Among Us game demo."""
    # Run the game with default settings
    run_among_us_demo(
        player_count=6,
        impostor_count=1,
        map_name="skeld",
        interactive=True,
        max_rounds=15,
        speed=1.0,
    )


if __name__ == "__main__":
    main()
