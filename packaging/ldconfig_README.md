# ldconfig_README.md

Documents `ldconfig.sh` 1.0.0.

## Purpose

Runs `ldconfig` after the Fedora package is installed and after any of the packages is removed, so that the libraries in `/usr/local/lib` (listed in `/etc/ld.so.conf.d/freeling-es-cl.conf`) are found, or forgotten.

## Usage

Not run by hand: the package runs it.

## Platform

Linux. POSIX sh.
