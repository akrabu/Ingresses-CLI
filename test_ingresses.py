# Copyright (C) 2026 akrabu
# SPDX-License-Identifier: AGPL-3.0-only
# See LICENSE for the full license text.

import argparse
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

import ingresses


REFERENCE_TIME = datetime(2026, 7, 25, 19, 27, tzinfo=timezone.utc)
REFERENCE_LOCATION = {"latitude": 51.4779, "longitude_degrees": 0.0}


class IngressesTests(unittest.TestCase):
    def test_reference_positions_and_order(self):
        self.assertEqual(
            ingresses.report(REFERENCE_TIME, **REFERENCE_LOCATION, color=False),
            "\n".join(
                (
                    "Ascendant 24° Capricorn",
                    "Sun 2° Leo",
                    "Moon 20° Sagittarius",
                    "Mercury 16° Cancer",
                    "Venus 17° Virgo",
                    "Mars 18° Gemini",
                    "Jupiter 5° Leo",
                    "Saturn 14° Aries",
                    "Uranus 4° Gemini",
                    "Neptune 4° Aries",
                    "Pluto 4° Aquarius",
                    "True Node 0° Pisces",
                    "Ceres 23° Gemini",
                    "Chiron 0° Taurus",
                )
            ),
        )

    def test_element_colors(self):
        self.assertEqual(ingresses.COLORS["water"], "\033[35m")
        report = ingresses.report(REFERENCE_TIME, **REFERENCE_LOCATION)
        self.assertIn(
            f"{ingresses.COLORS['fire']}Sun 2° Leo{ingresses.RESET}", report
        )
        self.assertIn(
            f"{ingresses.COLORS['water']}True Node 0° Pisces"
            f"{ingresses.RESET}",
            report,
        )
        self.assertIn(
            f"{ingresses.COLORS['air']}Mars 18° Gemini"
            f"{ingresses.RESET}",
            report,
        )
        self.assertIn(
            f"{ingresses.COLORS['earth']}Chiron 0° Taurus"
            f"{ingresses.RESET}",
            report,
        )

    def test_naive_time_is_utc(self):
        self.assertEqual(
            ingresses.parse_time("2026-07-25T19:27"),
            REFERENCE_TIME,
        )

    def test_location_only_changes_ascendant(self):
        first = ingresses.report(REFERENCE_TIME, **REFERENCE_LOCATION, color=False).splitlines()
        second = ingresses.report(
            REFERENCE_TIME,
            latitude=0,
            longitude_degrees=0,
            color=False,
        ).splitlines()
        self.assertNotEqual(first[0], second[0])
        self.assertEqual(first[1:], second[1:])

    def test_coordinates_are_required(self):
        result = subprocess.run(
            [sys.executable, str(Path(ingresses.__file__).resolve())],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--latitude", result.stderr)
        self.assertIn("--longitude", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_invalid_coordinates_are_rejected(self):
        for invalid in ("91", "-91", "nan", "inf"):
            with self.subTest(latitude=invalid):
                with self.assertRaises(argparse.ArgumentTypeError):
                    ingresses.latitude(invalid)
        for invalid in ("181", "-181", "nan", "inf"):
            with self.subTest(longitude=invalid):
                with self.assertRaises(argparse.ArgumentTypeError):
                    ingresses.longitude_argument(invalid)

    def test_explicit_offset_is_respected(self):
        self.assertEqual(
            ingresses.parse_time("2000-01-01T14:00+02:00"),
            datetime(2000, 1, 1, 12, 0, tzinfo=timezone.utc),
        )


if __name__ == "__main__":
    unittest.main()
