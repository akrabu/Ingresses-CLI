#!/usr/bin/env python3
# Copyright (C) 2026 akrabu
# SPDX-License-Identifier: AGPL-3.0-only
# See LICENSE for the full license text.
"""Print the current tropical zodiac positions, one per line."""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone
from pathlib import Path

try:
    import swisseph as swe
except ImportError as error:
    raise SystemExit(
        "Missing dependency. Install it with:\n"
        "  python3 -m venv .venv\n"
        "  .venv/bin/python -m pip install -r requirements.txt"
    ) from error


UTC = timezone.utc
EPHEMERIS_DIR = Path(__file__).with_name("ephe")

SIGNS = (
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
)
ELEMENTS = (
    "fire",
    "earth",
    "air",
    "water",
    "fire",
    "earth",
    "air",
    "water",
    "fire",
    "earth",
    "air",
    "water",
)
COLORS = {
    "fire": "\033[31m",
    "water": "\033[35m",
    "air": "\033[33m",
    "earth": "\033[32m",
}
RESET = "\033[0m"

BODIES = (
    ("Sun", swe.SUN),
    ("Moon", swe.MOON),
    ("Mercury", swe.MERCURY),
    ("Venus", swe.VENUS),
    ("Mars", swe.MARS),
    ("Jupiter", swe.JUPITER),
    ("Saturn", swe.SATURN),
    ("Uranus", swe.URANUS),
    ("Neptune", swe.NEPTUNE),
    ("Pluto", swe.PLUTO),
    ("True Node", swe.TRUE_NODE),
    ("Ceres", swe.CERES),
    ("Chiron", swe.CHIRON),
)
ASTEROIDS = {swe.CERES, swe.CHIRON}

# Ceres and Chiron use ephe/seas_18.se1. Everything else explicitly uses the
# small built-in Moshier ephemeris, so normal runs are entirely offline.
swe.set_ephe_path(str(EPHEMERIS_DIR))


def julian_day(moment: datetime) -> float:
    moment = moment.astimezone(UTC)
    hour = (
        moment.hour
        + moment.minute / 60.0
        + moment.second / 3600.0
        + moment.microsecond / 3_600_000_000.0
    )
    return swe.julday(moment.year, moment.month, moment.day, hour)


def longitude(body: int, jd: float) -> float:
    flags = swe.FLG_SWIEPH if body in ASTEROIDS else swe.FLG_MOSEPH
    return swe.calc_ut(jd, body, flags)[0][0] % 360.0


def format_position(name: str, position: float, color: bool) -> str:
    sign_index = int(position // 30.0)
    line = f"{name} {int(position % 30.0)}° {SIGNS[sign_index]}"
    if not color:
        return line
    return f"{COLORS[ELEMENTS[sign_index]]}{line}{RESET}"


def report(
    moment: datetime,
    latitude: float,
    longitude_degrees: float,
    color: bool = True,
) -> str:
    jd = julian_day(moment)
    # The ascendant is identical across house systems. Equal houses also works
    # in polar regions, where Placidus is undefined.
    ascendant = swe.houses(jd, latitude, longitude_degrees, b"E")[1][0]
    positions = [("Ascendant", ascendant)]
    positions.extend((name, longitude(body, jd)) for name, body in BODIES)
    return "\n".join(
        format_position(name, position, color) for name, position in positions
    )


def parse_time(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "use ISO 8601, for example 2000-01-01T12:00Z"
        ) from error
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def latitude(value: str) -> float:
    number = float(value)
    if not -90.0 <= number <= 90.0:
        raise argparse.ArgumentTypeError("latitude must be between -90 and 90")
    return number


def longitude_argument(value: str) -> float:
    number = float(value)
    if not -180.0 <= number <= 180.0:
        raise argparse.ArgumentTypeError("longitude must be between -180 and 180")
    return number


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--at",
        type=parse_time,
        help="ISO 8601 time; a time without an offset is UTC",
    )
    parser.add_argument(
        "--latitude",
        type=latitude,
        required=True,
        help="observer latitude in degrees, between -90 and 90",
    )
    parser.add_argument(
        "--longitude",
        type=longitude_argument,
        required=True,
        help="observer longitude in degrees, east positive, between -180 and 180",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="disable ANSI element colors",
    )
    args = parser.parse_args()
    use_color = not args.no_color and "NO_COLOR" not in os.environ
    print(
        report(
            args.at or datetime.now(UTC),
            args.latitude,
            args.longitude,
            use_color,
        )
    )


if __name__ == "__main__":
    main()
