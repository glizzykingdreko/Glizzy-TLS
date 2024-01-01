# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

## [0.1.5] - 2023-06-11
### Improved
- Client hello loading and selection
- Added `Session.get_all_client_profiles()` to get a list of all the available client hello

## [0.1.3] - 2023-06-11
### Fixed
- Fixed an installation bug with directories not being reset properly.

## [0.1.2] - 2023-06-11
### Changed
- Renamed the `body` parameter to `data` in `request()` and `Session.request()` to match the `requests` library.

## [0.1.1] - 2023-06-11
### Fixed
- Removed `build_go.py` from `MANIFEST.in` to fix installation issues.
- Redisigned the installation process to make it more reliable.

## [0.1.0] - 2023-06-11
### Added
- Initial release of Glizzy TLS.
- `TLSSession` class to handle TLS connections.
- `setup.py` for package installation.
- `build_go.py` for building Go source code during installation.

### Changed
- Updated documentation and README.md
