#!/bin/sh
# VERSION 1.0.0
#
# postinstall-deb.sh -- runs after the Debian and Ubuntu package is
# installed: refreshes the shared-library cache, and makes sure the
# en_US.UTF-8 locale exists, because FreeLing runs in it (its "default"
# locale) and stops without it. The locale is added the way each
# distribution adds one, so that it stays when the locales are regenerated
# later: on Ubuntu with locale-gen en_US.UTF-8, on Debian by enabling it in
# /etc/locale.gen and running locale-gen. No other locale, and no system
# setting (LANG and the rest), is touched.
set -e
ldconfig
if locale -a 2>/dev/null | grep -qix 'en_US\.utf-\?8'; then
    exit 0
fi
if grep -qi '^ID=ubuntu' /etc/os-release 2>/dev/null; then
    locale-gen en_US.UTF-8
else
    if grep -q '^# *en_US\.UTF-8 UTF-8' /etc/locale.gen 2>/dev/null; then
        sed -i 's/^# *\(en_US\.UTF-8 UTF-8\)/\1/' /etc/locale.gen
    elif ! grep -q '^en_US\.UTF-8 UTF-8' /etc/locale.gen 2>/dev/null; then
        echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen
    fi
    locale-gen
fi
