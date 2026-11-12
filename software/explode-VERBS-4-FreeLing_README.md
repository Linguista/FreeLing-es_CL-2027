# explode-VERBS-4-FreeLing_README.md

Documents `explode-VERBS-4-FreeLing.pl` 1.2.

Real files (identical copies):

- `/home/user/MyScripts/linguistics/explode-VERBS-4-FreeLing.pl`
- `/home/user/ProgData/System-Install-Script/linguistics/explode-VERBS-4-FreeLing.pl`

## Purpose

Takes a file with one infinitive per line and writes every form of each verb,
with its lemma and FreeLing tag, one per line, ready for a FreeLing
dictionary entries file. Besides the standard paradigm it writes the seven
Chilean voseo forms, tagged as voseo: conditional cantaríai, future
cantarái, imperfect cantabai, present indicative cantái, preterite
cantastes, imperfect subjunctive cantarai, present subjunctive cantís; and,
on purpose, common misspellings for -ear and -iar verbs
(golpiái beside golpeái, envís beside enviís). It produced the verb lists of
the Chilean FreeLing data (FreeLing es-CL 2027).

## Usage

```bash
perl /home/user/MyScripts/linguistics/explode-VERBS-4-FreeLing.pl /path/to/verbs.txt
```

The input must be UTF-8, one infinitive per line. The output is written next to the input as
`verbs.txt.verbs.EXPLODED`. Messages go to the terminal:

| Message | Meaning |
|---|---|
| `SKIPPED, NO STEM (enter this verb by hand): ir` | nothing is left of the entry once its ending is removed; nothing is written for it |
| `NOTE, -guir/-quir verb: check stem changes by hand (seguir: sigo): seguir` | the forms are written, with g/c before a and o, but stem changes are not known to the script |
| `UNRECOGNIZED VERB: x` | the entry does not end in -ar, -er or -ir |

## Limits

The script knows the spelling changes of the endings (-zar, -car, -gar,
-cer, -cir, -gir, -uir, -guar, -uar, -iar, -ear), not irregular stems:
poner, dar, andar, mover, servir and the like come out regular and must be
corrected by hand. `freeling_escl_build.py` checks every verb the Spanish
FreeLing dictionary knows against that dictionary's paradigm and removes such
forms (FreeLing es-CL 2027, README section 4.2).

## Changelog

- 1.2 (261101):
  - The "blank entry" of the old KNOWN ISSUE note, which wrote 72 bare endings
    after "intrusear", was the verb "ir": removing "ir" from "ir" left an
    empty stem. Entries with nothing left after their ending are now skipped
    with a message.
  - The -uir branch dropped the u of the stem (constriríai, constryo for
    construir); the stem now keeps it (construiríai, construyo).
  - -guir and -quir verbs (distinguir, delinquir, seguir) no longer go to
    the -uir branch (distinguyo); they go to the -ir branch, with g and c
    before a and o (distingo, distinga, delinco, delinca).
  - A carriage return at the end of an input line is removed.
- 1.1: the version before; voseo forms with V tags.

## Platform

Perl 5.12 or later, Linux and Windows.
