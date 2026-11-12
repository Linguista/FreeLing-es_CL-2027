# postinstall-deb_README.md

Documents `postinstall-deb.sh` 1.0.0.

## Purpose

Runs after the Debian and Ubuntu package is installed: refreshes the shared-library cache and makes sure the en_US.UTF-8 locale exists. FreeLing runs in that locale (its "default"), and stops without it, and the `locales` package does not generate it by itself. If it is missing, it is added the way each distribution adds a locale, so it stays when the locales are regenerated later: on Ubuntu with `locale-gen en_US.UTF-8`, on Debian by enabling it in `/etc/locale.gen` and running `locale-gen`. No other locale and no system setting (`LANG` and the rest) is touched.

## Usage

Not run by hand: the package runs it.

## Platform

Debian and Ubuntu. POSIX sh.
