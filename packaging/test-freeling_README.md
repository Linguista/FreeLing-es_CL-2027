# test-freeling_README.md

Documents `test-freeling.sh` 1.0.0.

## Purpose

Checks an installed FreeLing es-CL 2027 package: `libfreeling.so` has the name-class change, the 13 Chilean data files are this release's (their sha256 as in `SHA256SUMS`), `cities-CL.dat` is gone, and FreeLing analyzes "Vos tenís que venir a Arica." with the Chilean dictionary (tenís is a voseo form of tener, `VMIP2SV`). It prints FreeLing's output.

## Usage

From the repository root, on a machine where the package is installed:

```bash
packaging/test-freeling.sh
```

## Exit codes

0 every check passed (it prints ALL CHECKS PASSED); 1 a check failed (it prints FAIL and what failed).

## Platform

Linux. bash, binutils (strings), sha256sum.
