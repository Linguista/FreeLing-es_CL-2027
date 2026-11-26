#!/usr/bin/env bash
# VERSION 1.4.0
#
# build-freeling.sh -- builds FreeLing 4.2 with the changes of
# FreeLing es-CL 2027, installs it into /usr/local together with the
# Chilean data of this repository, and copies everything installed into
# pkgroot/ for nfpm to package. FreeLing carries its own copies of the
# ICU and Boost libraries it was built against (bundle-libraries.sh), so an
# upgrade of the system cannot break it.
#
# PREFIX=DIR installs into another prefix than /usr/local (the generic
# Linux tarball: /opt/freeling-es-cl-2027), and RELOCATABLE=yes makes the
# run paths relative to each file ($ORIGIN), so that folder can be moved
# anywhere (bundle-libraries.sh). The packages the libraries come from are
# found with rpm (Fedora, openSUSE, the Red Hat family), dpkg (Debian,
# Ubuntu) or pacman (Arch Linux).
#
# Meant for a fresh, disposable machine or container (the GitHub build):
# it runs FreeLing's own "make install", which writes into /usr/local and
# cannot be redirected (FreeLing's install step builds its dictionaries
# straight into the install prefix). Run it as root, from anywhere:
#
#   packaging/build-freeling.sh FreeLing-src-4.2.tar.gz
#
# It writes, in the repository root:
#   pkgroot/          everything FreeLing's install and the Chilean data
#                     put into /usr/local (moved out of /usr/local, which is
#                     left as it was), plus the documents
#   pkgetc/           freeling-es-cl.conf, for /etc/ld.so.conf.d/
#   pkgdeps.txt       the distribution packages the installed programs and
#                     libraries need, one per line (found from their
#                     shared-library dependencies)

set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(dirname "$here")"
tarball="$(realpath "${1:?FreeLing-src-4.2.tar.gz}")"
jobs="${JOBS:-$(nproc)}"
prefix="${PREFIX:-/usr/local}"
share="$prefix/share/freeling"
work="${WORK:-/tmp/freeling-build}"

# FreeLing-src-4.2.tar.gz from https://github.com/TALP-UPC/FreeLing/releases/tag/4.2
echo "f96afbdb000d7375426644fb2f25baff9a63136dddce6551ea0fd20059bfce3b  $tarball" | sha256sum -c -

rm -rf "$work" "$repo/pkgroot" "$repo/pkgetc" "$repo/pkgdeps.txt"
mkdir -p "$work"
tar -xzf "$tarball" -C "$work"
src="$work/FreeLing-4.2"
[ "${REMOVE_TARBALL:-no}" = yes ] && rm -f "$tarball"

"$here/patch-freeling.sh" "$src" "$repo/software/patches/freeling-4.2-np-classes.patch" \
    "$repo/software/patches/freeling-4.2-known-roots.patch" \
    "$repo/software/patches/freeling-4.2-tag-probabilities.patch" \
    "$repo/software/patches/freeling-4.2-ambiguous-multiwords.patch"

# What is in the prefix before the install: none of it is packaged.
mkdir -p "$prefix"
find "$prefix" -mindepth 1 \( -type f -o -type l \) | sort > "$work/before.txt"

# Build fixes 1 to 3 as flags: CMake 4 refuses the bundled dynet's
# cmake_minimum_required(2.8); GCC 15 and later diagnose errors in the
# bundled Eigen's uninstantiated templates; libfoma is K&R C, which C23
# (GCC 15's default) rejects.
cmake -S "$src" -B "$work/build" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$prefix" \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
    -DCMAKE_CXX_FLAGS="-Wno-template-body" \
    -DCMAKE_C_FLAGS="-std=gnu17"
make -C "$work/build" -j"$jobs"
make -C "$work/build" install
# Disk space: the build and the source are no longer needed.
rm -rf "$work/build" "$src"

# The Chilean data, over FreeLing's own files (the files and places of
# freeling_escl_deploy.py --target system), and the link for FreeLing Old.
"$here/install-data.sh" "$share"

# The library must hold the name-class change.
n=$(strings -e L "$prefix/lib/libfreeling.so" | grep -c -x -E "DictionaryClasses|FixedClasses|ClassesAtSentenceStart|SentenceStartClasses|ClassShares|keep:" || true)
[ "$n" -eq 6 ] || { echo "libfreeling.so lacks the name-class change ($n of 6 marks)" >&2; exit 1; }

# FreeLing's own copies of the ICU and Boost libraries it was built against,
# in /usr/local/lib/freeling-es-cl/, found first by every program and
# library of FreeLing (their run path), so that an upgrade of the system
# cannot break it; the package then needs no ICU or Boost package.
"$here/bundle-libraries.sh" "$prefix"

# The distribution packages that provide the shared libraries the
# programs and libraries need, other than those installed here.
find "$prefix" -mindepth 1 \( -type f -o -type l \) | sort > "$work/after.txt"
comm -13 "$work/before.txt" "$work/after.txt" > "$work/new.txt"
own="$(grep -E '/lib/(freeling-es-cl/)?[^/]*\.so' "$work/new.txt" | xargs -r -n1 basename | sort -u)"
needed="$(grep -v '/share/' "$work/new.txt" | while read -r f; do
        [ -f "$f" ] && [ ! -L "$f" ] && file -b "$f" | grep -q '^ELF' && readelf -d "$f"
    done | sed -n 's/.*(NEEDED).*\[\(.*\)\]/\1/p' | sort -u)"
: > "$repo/pkgdeps.txt"
for lib in $needed; do
    grep -qx "$lib" <<<"$own" && continue
    path="$(ldconfig -p | awk -v l="$lib" '$1 == l {print $NF; exit}')"
    [ -n "$path" ] || { echo "no system library for $lib" >&2; exit 1; }
    path="$(realpath "$path")"
    if command -v pacman >/dev/null 2>&1; then
        pacman -Qoq "$path"
    elif command -v rpm >/dev/null 2>&1 && rpm -qf "$path" >/dev/null 2>&1; then
        rpm -qf --qf '%{NAME}\n' "$path"
    else
        dpkg -S "$path" 2>/dev/null | head -1 | cut -d: -f1
    fi
done | sort -u >> "$repo/pkgdeps.txt"
echo "dependencies:"
sed 's/^/  /' "$repo/pkgdeps.txt"
[ -s "$repo/pkgdeps.txt" ] || { echo "no dependencies found" >&2; exit 1; }

# Everything the install added, moved into pkgroot/.
mkdir -p "$repo/pkgroot" "$repo/pkgetc"
tar -cf - -T "$work/new.txt" --remove-files | tar -xf - -C "$repo/pkgroot"
echo "$prefix/lib" > "$repo/pkgetc/freeling-es-cl.conf"
docs="$repo/pkgroot$prefix/share/doc/freeling-es-cl"
mkdir -p "$docs"
cp "$repo/README.md" "$repo/LICENSE" "$repo/BUILD-REPORT.md" "$repo/CHANGELOG.tsv" "$docs/"
echo "packaged: $(wc -l < "$work/new.txt") files, $(du -sh "$repo/pkgroot" | cut -f1)"
