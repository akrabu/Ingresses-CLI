# Third-party notices

Application source code is Copyright (C) 2026 akrabu and licensed under
GNU AGPL version 3 only. See LICENSE.

## Swiss Ephemeris and pysweph

This application uses pysweph 2.10.3.6, which provides Python bindings to
Swiss Ephemeris 2.10.03. The Python binding and its compiled library are
installed separately from PyPI; they are not vendored in this repository.

Upstream software, source code, and license information:

- Swiss Ephemeris: <https://github.com/aloistr/swisseph>
- pysweph: <https://github.com/sailorfe/pysweph>
- Pinned release and source distribution:
  <https://pypi.org/project/pysweph/2.10.3.6/#files>
- Swiss Ephemeris licensing:
  <https://www.astro.com/swisseph/swephinfo_e.htm>

This project uses the GNU AGPL licensing option. The upstream Swiss Ephemeris
copyright and license notice is reproduced verbatim in
[licenses/Swiss-Ephemeris.txt](licenses/Swiss-Ephemeris.txt).

## Included ephemeris data

ephe/seas_18.se1 is an unmodified upstream Swiss Ephemeris data file for
1800-2399 CE, distributed under the same GNU AGPL option and upstream notice.
Its origin and SHA-256 are documented in [ephe/README.md](ephe/README.md).
