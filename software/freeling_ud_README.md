# freeling_ud_README.md

Documents `freeling_ud.py` 1.0.0, step 070 of `freeling.py`.

## Purpose

Adds Universal Dependencies (UD v2) part of speech and features to every
token, translated rule by rule from FreeLing's EAGLES tag as the es-cl
tagset defines it. Nothing is tagged again: the two columns say exactly
what FreeLing's tag says, in UD's vocabulary.

## Usage

```bash
freeling.py CORPUS --ud
freeling.py CORPUS --ud --dry-run
```

Reads `060-FreeLing-Tagged`, writes `070-Universal-Dependency-Tagged`: the
same files with two more TAB-separated columns, `UPOS` and `FEATS` (UD
features, `Name=Value`, sorted by name and joined by vertical bars; `_`
when there are none). Every column of 060 is copied byte for byte; each
`NAME.times.tsv` is copied beside its `NAME.conll`, before it. The columns
of 060 are found by name in its `columns.tsv`. A finished document is
skipped (`--redo` rewrites it); a missing sidecar beside one is copied, and
one that differs from 060's is listed.

## The mapping

In the es-cl tagset a final `V` means two things: on a verb and on a
personal pronoun it is voseo; on a noun or an adjective it is evaluative.

| FreeLing | UPOS | Features |
|---|---|---|
| NC, NP | NOUN, PROPN | Gender, Number; Evaluative when the tag marks it |
| AQ, AO | ADJ | Gender, Number; NumType=Ord for AO; Degree=Abs for the superlative; Evaluative |
| AP (mío, tuyo, suyo) | DET | Poss=Yes, PronType=Prs, Person, Number[psor], Gender, Number |
| DA | DET | PronType=Art, Definite=Def |
| DI with lemma uno (un, una) | DET | PronType=Art, Definite=Ind |
| DD, DI, DT, DE | DET | PronType=Dem, Ind, Int, Exc |
| DP (mi, tu, su) | DET | Poss=Yes, PronType=Prs, Person, Number[psor] |
| PP, PD, PI, PR, PT, PE | PRON | PronType; Person, Gender, Number; Case=Nom, Acc, Dat; PrepCase=Pre for mí, ti, sí, conmigo; Polite=Form for usted |
| P0 (se, me, te, nos) | PRON | PronType=Prs, Reflex=Yes |
| VM | VERB (or AUX, below) | VerbForm; Mood (Cnd for the conditional); Tense; Person, Number; Gender on participles |
| VA, VS | AUX | the same |
| RG, RN | ADV | Polarity=Neg for RN |
| SP | ADP | AdpType=Prep |
| CC, CS | CCONJ, SCONJ | |
| I | INTJ | |
| Z | NUM | NumType=Card |
| W (dates) | NOUN | |
| F punctuation | PUNCT | PunctType, PunctSide |
| Fz (other than a stand-in) | SYM | |
| F with letters (etcétera) | ADV | |
| a tag not in the table | X | listed at the end of the run |

**AUX or VERB.** ser is always AUX. haber is AUX when tagged VA or attached
as auxiliary (`v`) to a participle; otherwise VERB (existential hay, hay
que). estar is AUX when tagged VA, attached as `v` to a gerund or
participle, or governing an `atr` (copula); otherwise VERB. Without a parse
(written-old, FreeLing Old), haber and estar are VERB unless tagged VA.

## Project features

UD lets a corpus add features of its own in the same `Name=Value` form.

| Feature | Values | Where |
|---|---|---|
| Voseo | Yes | voseo verb forms (cachái, erís, estái) and vos; with Person=2, Number=Sing |
| Evaluative | Dim, Aug, Pej, Approx, Yes | nouns and adjectives FreeLing marks evaluative |
| MWE | Yes | a FreeLing multiword kept as one token (o_sea, Santiago_de_Chile) |
| Clitic | Yes | a verb still joined to its clitic (reírme) |
| StandIn | Redacted, Unintelligible, NonSpeech, Url, EmailAddr | the stand-in tokens of `stand-ins.tsv`, with UPOS X; a new stand-in XXXNAMEXXX gets StandIn=Name |

**Evaluative.** FreeLing only says "evaluative"; the value comes from the
word's ending, on the form and its possible singulars, longest suffix
first:

| Value | Suffixes |
|---|---|
| Dim | -ito/-ita (and -cito, -ecito, -quito, -guito, -itico, -íto/-íta), -illo/-illa, -ico/-ica, -ín/-ina, -ino, -ete/-eta, -ingo/-inga, -iño/-iña, -uco/-uca |
| Aug | -ón/-ona, -azo/-aza, -azas, -ote/-ota |
| Pej | -ucho/-ucha, -acho/-acha, -aco/-aca, -ajo/-aja, -ejo/-eja, -astro/-astra, -orrio, -orro/-orra, -ute, -uzo/-uza, -ales, -uelo/-uela; the words peliento and upeliento |
| Approx | -uzco/-uzca, -usco/-usca |
| none | any other word in -iento/-ienta: -iento forms adjectives (hambre > hambriento) and gets no Evaluative feature |
| Yes | evaluative, but no listed ending matches |

Sources: Real Academia Española, *Glosario de términos gramaticales*,
"sufijo apreciativo" and "sufijo diminutivo" (citing the *Nueva gramática
de la lengua española*, 9.1 to 9.6); RAE, "Clases de apreciativos. Los
diminutivos" and "Aumentativos y despectivos". -uelo and -zuelo are taken
as pejorative (mujerzuela, ladronzuelo). A multiword is matched part by
part, the first part with an evaluative ending deciding
(autitos_chocadores: Dim), since a Spanish multiword noun has its head
first.

## Records

In the stage's `_processing-records/`: `ud-evaluative--YYMMDD_HHMM.tsv`
(value, form, tag, count of every evaluative token of the run) and, when
something failed, `ud-FAILED--YYMMDD_HHMM.tsv`.

## Exit codes

0 done; 1 a file failed; 2 refused (060 not made, a column missing, a
README or `columns.tsv` that cannot be replaced).

## Platform

Linux and macOS (and anywhere Python runs). Python 3.9 or later, standard
library only.

## Changelog

- 1.0.0 (261119): first version, from the per-corpus UD script of
  261115: the columns found by name in `columns.tsv`; the stand-ins and
  their StandIn values from `stand-ins.tsv`; a text without a parse
  (written-old) is mapped too; a document without a sidecar is no longer a
  failure (only speech has sidecars).
