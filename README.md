# Ingresses-CLI

An offline terminal tool that prints current tropical zodiac positions for
the ascendant, Sun, Moon, planets, true node, Ceres, and Chiron. Fire signs are
red, water signs purple, air signs yellow, and earth signs green.

## Install and run

Requires Python 3.11 or newer on Linux or macOS.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python ingresses.py --latitude 51.4779 --longitude 0
```

The example uses Greenwich. Both coordinates must be supplied explicitly;
there is no stored or assumed location. Latitude ranges from -90 to 90 and
longitude from -180 to 180, with east positive and west negative. Only the
ascendant depends on the location; the other positions are geocentric.

A compiler may be needed if `pysweph` has no wheel for your Python version and
platform. Normal calculations need no network connection after installation.

## Options

```sh
.venv/bin/python ingresses.py \
  --latitude 51.4779 --longitude 0 \
  --at 2000-01-01T12:00Z --no-color
```

`--at` accepts an ISO 8601 timestamp. Times without an offset are interpreted
as UTC. With no `--at`, the current instant is used. `--no-color` or the
`NO_COLOR` environment variable disables ANSI colors.

The command prints positions and exits. Despite the project name, it does not
predict future ingress times. Degrees within a sign are truncated to an
integer. Equal houses are used to obtain the ascendant, including at polar
latitudes.

## Ephemeris data

Planets use Swiss Ephemeris's built-in Moshier model. Ceres and Chiron use the
included `ephe/seas_18.se1` file, covering 1800-2399 CE. Keep the `ephe` directory
beside the script. See [ephe/README.md](ephe/README.md) for the upstream source
and checksum.

## Tests

```sh
.venv/bin/python -m unittest -v
```

## License

Copyright (C) 2026 akrabu. Licensed under GNU AGPL version 3 only, without
warranty. Required upstream notices for Swiss Ephemeris, its Python binding,
and the included data are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
and [licenses/Swiss-Ephemeris.txt](licenses/Swiss-Ephemeris.txt).
The full application license is [LICENSE](LICENSE).
