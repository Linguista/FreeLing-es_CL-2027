# FreeLing es-CL 2027

[![release](https://img.shields.io/github/v/release/Linguista/FreeLing-es_CL-2027?label=release&color=1f6feb)](https://github.com/Linguista/FreeLing-es_CL-2027/releases)
[![package build](https://github.com/Linguista/FreeLing-es_CL-2027/actions/workflows/packages.yml/badge.svg)](https://github.com/Linguista/FreeLing-es_CL-2027/actions/workflows/packages.yml)
![license](https://img.shields.io/badge/license-AGPL--3.0-2ea44f)
![FreeLing](https://img.shields.io/badge/FreeLing-4.2%2C%20bundled-8250df)
![packages](https://img.shields.io/badge/packages-Fedora%2043%20%7C%2044%20%7C%20Debian%2013%20%7C%20Ubuntu%2024.04%20%7C%2026.04-8250df)
![macOS](https://img.shields.io/badge/macOS-15%2C%20Apple%20silicon%20%7C%20Intel-8250df)
![Windows](https://img.shields.io/badge/Windows-10%20%7C%2011%2C%20x86--64-8250df)
![processors](https://img.shields.io/badge/processors-x86--64%20%7C%20arm64%20(macOS)-1f6feb)
![data](https://img.shields.io/badge/data-UTF--8%20NFC-d29922)
![languages](https://img.shields.io/badge/languages-Spanish%20only-d29922)
![dictionaries](https://img.shields.io/badge/dictionaries-2027%20%7C%2019th%20century%20%7C%20Old%20Spanish-1f6feb)

This is the Chilean Spanish version of FreeLing 4.2. It contains Chilean versions of the dictionaries, probabilities, multiword expressions, tagset, name recognizer rules, currencies and units, as well as a name recognizer and classifier that tags every Chilean locality as a place (section 8). It is self-contained, meaning it requires nothing from the original FreeLing project. The releases section holds binaries or installers for most common platforms, including the brutally difficult to compile Windows version.

Why this new version? The short of it is as follows: The 2016 version of FreeLing for Chilean Spanish was incorporated into the master version of FreeLing, but it excluded the custom tags for _voseo_ paradigm verbs ("V" in the last verb tag slot, which was unused except for marking gender in participles, which _voseo_ forms don't have). This made them indistinguishable from _tuteo_ forms, thereby closing a whole avenue of potential linguistic inquiry. Furthermore, since FreeLing rebuilds its dictionary and various other files from scratch each time you run it, it ended up clobbering a good deal of Chileanization work that I had done (that was on me, for not thoroughly understanding FreeLing's architecture). At the same time, nasty Spainisms crept in everywhere, from proper names to units, leading to many tagging errors. In addition, this new version gave me a chance to iterate it over the [COSCACH](https://corpora.pro) corpus several times and add many new lemmas that aren't in the 2016 version. Finally, I took the opportunity to create three different versions of FreeLing 4.2 for Chilean Spanish, depending on the era of the texts to be tagged (see below). 

*So consider the 2016 version, which is the same as the one in FreeLing's Chilean Spanish version today, to be thoroughly deprecated.*

**Three varieties of Chilean Spanish, chosen by the config you name** (section 2):

| Config | What it reads | For |
|---|---|---|
| `es-cl.cfg` | FreeLing es-CL 2027: contemporary Chilean Spanish, with modern voseo. The default. | contemporary texts |
| `es-cl-19th-century.cfg` | FreeLing es-CL 19th Century: everything in 2027 plus **wordforms written with the various alternative orthographies used in Chile from the mid-19th century to 1927: Andrés Bello's orthography of 1844 (jente, jeneral, mui, hoi, rei, i, esplicar), Sarmiento's (little-used) proposal (ombre, bino, sapato, sielo, Enrrique) and the Chilean neographers' _ortografía rrazional_ (qasa, kasa, soziedad, elektrizidad)**, each with the lemma and tags of the modern word; the pre-1952 accents (fué, dió, á, ménos, ántes, órden); and the vosotros readings. | historical corpora |
| `es-old.cfg` | FreeLing Old: FreeLing's own Old Spanish, exactly as FreeLing ships it (dixo, muger, fermosa). One day I hope to Chileanize this, but that will take time.| medieval and Golden Age texts |

The packages install Spanish only: FreeLing's English and Portuguese data, the configs of its other languages and its Argentine variant are not built or installed.

## What is new: the linguistic innovations

Each point gives the section where it is described in full.

### FreeLing es-CL 2027

**Voseo**

- By some estimates, over half of all Spanish speakers, from Argentina and Uruguay to El Salvador and large swathes of Colombia, use _vos_ instead of _tú_. However, the thoroughly colonized mindset present in so much of Hispanic linguistics, education and related fields, pointlessly and unsuccessfully drills the _vosotros_ fossil forms, used by perhaps 8% of the world's Spanish speakers, into schoolchildren's heads, while typically ignoring the _voseo_ forms that they use everyday. This communicates the idea that _voseo_ forms are ignorant, uneducated and unworthy. When it comes to Spanish taggers, retaining _vosotros_ can do nothing but lead to errors in contemporary non-Spain texts, with the exception of the odd Biblical quote. It does have its place, to some degree or another, in 19th century non-Spain texts, as it had acquired a deeply ironic hypercorrect status among some speakers by then. Those working with non-Chilean _voseante_ varieties can use the Argentinian (es-AR) version of FreeLing (for its verbs, at least), but the Chilean _voseo_ is almost completely different, and thus requires its own tagger (e.g. hablás = _hablái_, hablabas = _hablabai_, has comido = _hai comido_, comés = _comís_, etc.).
- **Voseo tags.** The Chilean tagset adds a voseo value to the last position of the verb tag and of the personal-pronoun tag: cantái is VMIP2SV, "verb, main, indicative, present, 2nd person, singular, voseo", and vos is PP2CS0V. Voseo forms can be told apart from tuteo forms in any search or count, which the version of these data in FreeLing itself cannot do. The forms of tú (tú, te, ti, contigo) never have the voseo value (section 4).
- **The full Chilean voseo paradigm for every verb**: cantái, comís, vivís, cantabai, cantaríai, cantarái, cantís (subjunctive), and the irregulars (erís and soi of ser, hai of haber, estái, vai, tenís), for every verb of the dictionary and every verb added, each tagged voseo (sections 5 and 6.1).
- **vos, voh and vo** are voseo pronouns. In 2027, vos is voseo only, never the reverential version, and the -ís forms that are both voseo and vosotros forms of the same verb and tense (salís, vivís: 497 forms) are voseo only, as they are in Chilean speech (section 2).
- **The spellings of voseo in actual writing.** The voseo forms are almost exclusively _spoken_, so speakers write it every which way: estái as estai, estay or estáy, tenís as tenis, tenih, teníh or tení. Eight rules add these spellings to every voseo form, 88,916 new forms in all, each with exactly the readings of its canonical form, never with a vosotros reading (section 7).
- **Deliberate overgeneration** of what Chileans actually say and write: the raised e of -ear verbs (golpiái beside golpeái), the dropped i of -iar verbs (envís), dái beside dai as vái beside vai (section 5).
- **Wrong voseo readings removed**: vais, dais, veis and deis are vosotros only (the voseo forms are vai, dai, veís, deís); the voseo forms of erar, which absolutely nobody uses and which collided with ser, are gone (erai and erís are ser only); regular forms wrongly generated for 30 irregular verbs (ponerái, convertierai) have been eliminated (section 5).

**Vosotros**

- **The whole vosotros paradigm for every verb that has one, except where these forms clash with the voseo forms** (8,255 verbs): -áis, -éis, -abais, -íais, -ríais, the -ad, -ed, -id imperatives, and os, vosotros, vuestro, sois, so Spanish texts are read correctly too (section 2). For the forms in which a vosotros and a vos interpretation are both possible, the vosotros interpretation has been eliminated, ensuring the vos version wins every time.

**Correctly interpreting bad spelling**

These measures vastly improve tagging accuracy on both transcriptions and texts extracted from social media, forums, etc.

- **Words written without their accents** are read as the word: comeriamos as comeríamos, colaboracion as colaboración, pinguino as pingüino. Every correctly spelled accented or diaeresized form gives its unaccented twin (140,895 forms), except where the twin is already a correctly spelled word (seria, esta and mas keep their own readings) or could come from more than one word (vacio, from vació and vacío: 516 left out) (section 6.4).
- **Misspellings found in transcriptions** are read as the word they misspell (6,555 forms): a misspelt form that slips past a corpus's spelling step is still tagged and lemmatized correctly (section 6.4).
- **Non-standard forms kept as they are** get the readings of the standard form: haiga as haya, vaiga as vaya, volao as volado (section 6.3).
- **Non-standard verb forms** of known verbs get the tags of the regular pattern where they have them: ponido, ponieron, descubrido (section 6.1).
- **The pre-1952 accents** fué, fuí, dió, vió, á, é, ó, ú, still common in writing, are read as fue, fui, dio, vio, a, e, o, u (section 2.1).

**The lexicon**

- **About 6,000 additional Chilean lemas[1] (compared to the 2016 version)** decided one by one in the spelling review of a large corpus of spoken Chilean Spanish, each with its lemma and word class, nouns with both numbers, adjectives with all their forms (section 6.1).
- **170 new verbs with their whole paradigm**, voseo included (hackear, reprogramar, sobreexigir), each conjugated like the known verb it is made from or like the verbs that share its ending, so a regular verb never gets a stem change (section 6.1).
- **Chilean imperatives with attached pronouns**: háceme, díceselo, pónete, etc., which compete with the canonical imperatives hazme, díselo and ponte (section 6.1).
- **Evaluative and superlative values**: a diminutive or augmentative whose lemma is the base word carries the evaluative value (cantitos, lemma canto; calladita, lemma callado), a superlative the superlative value (relajadísimo); a lexicalized diminutive (burrito) does not (section 6.1).
- **Words and expressions from the FreeLing es-AR dictionary** that are used in Chile (e.g. desprolijo, bue, holis), along with multiwords (de a poco, dulce de leche, ponerse las pilas).
- **Modern Chilean words and spelling variants not found in most lexical resources** such as CESFAM, SAR, COSAM, minipimer, chupafusiles, tatú and tatoo (section 6.5b).
- **Standardized lemmas**: one lemma for multiple spellings of a word (sánguche and sandwich, ranking and ránking, marketing and márketing), so every spelling of a word is counted under one lemma (section 6.5).
- **Lemma preferences** for forms two verbs share, to increase overall tagging accuracy: hacer over hacendar, ser over erar, vender over vendar, poder over podar (section 9).
- **Errors of the earlier Chilean lists corrected**: the empty-stem forms of ir (a, o, e given as forms of ir), lost forms of ser restored (erih, eríh), capitalized keys that FreeLing could never find, malformed tags (section 5).

[1] We invite you to join our campaign to not say "lemmata".

**Interjections and multiwords**

- **326 Chilean interjections and discourse markers** with their lemma (po and poh, lemma poh), and 103 multiword ones (ya po and ya poh as ya_poh). Rare ones keep their interjection reading but are seldom chosen (section 6.2).
- **Interjections from Spain removed**: the interjection readings of he, ha, fuera, hombre, vaya and 230 more are gone (their other readings stay), and 53 Spanish forms that were only interjections (agur, caray, olé) are no longer in the dictionary (section 6.2).
- **FreeLing's general Spanish multiwords merged with the Chilean ones** (o sea, por ejemplo, a pesar de: 1,563 added). FreeLing reads one multiword file, and the Chilean one used to hold only the Chilean multiwords, so every general multiword was split into its words. Duplicate and broken multiword lines are repaired (section 9).

**Names**

- **Every Chilean locality is a place**: the 343 _comunas_, countries, capitals of Latin America and 66 regions, provinces and localities all have a fixed class, and the name classifier's lists are replaced by Chilean ones. On a corpus of spoken Chilean Spanish, Chilean place names went from 75.6% tagged as places to 99.6%; España, Concepción, Antofagasta and Perú are places every time (sections 8.3, 8.4 and 8.6).
- **Names that are also surnames or words are weighed, not fixed**: Molina leans toward the place, Pinto is a surname, Asunción and Sucre are mostly places and sometimes persons, and Quito or Tomé at the start of a written sentence are the verb with a 10% chance of being the place (section 8.4).
- **Speech and writing are told apart**: in transcribed speech a line rarely starts with a capital unless its first word is a name, so a separate name recognizer (`np-speech.dat`) reads a capital at the start of a line as a name (section 8.4).
- **Spelled-out letters are never names** (S H) (section 8.4).
- **A change to FreeLing's code** makes all of this possible: fixed classes, the dictionary's class kept for a capitalized word, rules for the start of a sentence, and shares between a name's classes (section 8.5).

**Currencies and units**

- **Chilean currencies**: peso alone and the sign $ are the Chilean peso (CLP), not the Cuban peso and the US dollar (how did the Cuban peso ever become the default, anyway?); unidad de fomento (UF) and unidad tributaria mensual (UTM) are added; the euro is EUR and not the deprecated abbreviation previously included (section 10).
- **56 unit names removed** when they turned ordinary words, letters and false starts into spurious measures: mi (the possessive, not the mile), tr, s, d, cd, pk (porque in chat writing, not the peck), and the imperial units nobody writes in Chile (section 10). (That said, I can't help but love the fact that the peck was included until now.).

**Voseo tagged as tuteo, if so desired**

- **A tuteo-tagged copy of the default dictionary**, in which voseo verb forms carry the tuteo tags and vos is tagged like te and ti (section 11). This option does nothing but throw large amounts of information away, making _tuteo_ and _voseo_ verb form tags indistinguishable, but there's no accounting for taste. (There _is_ a hidden pitfall in using the _voseo_ tags that I had to find and fix for them to fully work - since they deviate from EAGLES tags by one letter, there's a FreeLing module that doesn't recognize them; that module has been fixed, so the voseo tags always work for everything).

### FreeLing es-CL 19th Century

Everything in 2027, plus:

- **The old Chilean orthographies**: every form of the 2027 dictionary but the proper nouns, in the spellings of Andrés Bello and Juan García del Río (1823), Domingo Faustino Sarmiento (1843), the Chilean orthography of 1844 and the Chilean neographers' ortografía rrazional (1890s to the early 1900s), in every combination a writer could use: jente, jeneral, mui, hoi, rei, i, esplicar, ecsamen, Méjico, qerer, kasa, soziedad, sapato, gerra, ombre, bino, rrazional. 1,203,611 spellings, each with the lemma and tags of the modern word (section 2.1).
- **No false words**: a spelling that is already a word is added only when one of the rules the 1844 orthography adopted gives it (g as j, vowel y as i, x before a consonant as s), and its old reading is nearly impossible on its own, so the word keeps its own reading unless the context demands the old one. Casa never gets the readings of caza, nor echo those of hecho (section 2.1).
- **Accents are never dropped**, as the neographers did (unifikazion): an unaccented twin of every accented word would read más as mas and está as esta (section 2.1).
- **Words decided one by one**: i is the conjunction y 99% of the time; rei is rey, lei is ley, hai is hay and soi is soy only; testo is texto 90% and testar 10% (section 2.1).
- **5,333 attested spellings** with an extra or a moved accent (tíempo, ráices, cáida, zodiáco), from historical texts, read as the modern word (section 2.1).
- **Vos and vosotros of the 19th century**: vos keeps its polite reading and is read as polite; a form that is both voseo and vosotros (salís, vivís) is read as vosotros (section 2.1).
- **6,539 multiwords in the old spellings** (hoi_día, hoi_en_día) (section 2.1).
- **Compound analysis off**, so FreeLing can load a dictionary of 2.1 million forms at all (section 2.1).

### FreeLing Old

- **FreeLing's own Old Spanish** (dixo, muger, fermosa), installed exactly as FreeLing ships it, beside the two Chilean dictionaries and chosen by its own config, so medieval and Golden Age texts are read with the dictionary made for them (section 2.2).
- **It reads FreeLing's general Spanish multiwords merged with the Chilean ones**, through a link to the Chilean multiword file (sections 2.2 and 9).

## Builds

### Fedora

Each release has an RPM for Fedora 44 and one for Fedora 43, both for x86-64 processors (`freeling-es-cl-4.2.0-YYMMDD.fc44.x86_64.rpm`, `freeling-es-cl-4.2.0-YYMMDD.fc43.x86_64.rpm`): FreeLing 4.2 with every change of this release, built by GitHub in a container of that distribution (so it links to that distribution's own Boost and ICU), then installed on a fresh container of the same distribution and checked there (`packaging/test-freeling.sh`); only packages that pass are attached to a release. It installs into `/usr/local`: the programs in `/usr/local/bin`, the library in `/usr/local/lib` (registered through `/etc/ld.so.conf.d/freeling-es-cl.conf`), the data and the three configs in `/usr/local/share/freeling`. Each package is about 560 MB. It cannot be installed beside another package named `freeling`. dnf installs what it needs from Fedora with it, including `glibc-langpack-en` (FreeLing runs in the en_US.UTF-8 locale).

Files of release 261113 (each newer release, with its own date in the file names, is on the [Releases page](https://github.com/Linguista/FreeLing-es_CL-2027/releases)):

- [`freeling-es-cl-4.2.0-261113.fc44.x86_64.rpm`](https://github.com/Linguista/FreeLing-es_CL-2027/releases/download/261113/freeling-es-cl-4.2.0-261113.fc44.x86_64.rpm)
- [`freeling-es-cl-4.2.0-261113.fc43.x86_64.rpm`](https://github.com/Linguista/FreeLing-es_CL-2027/releases/download/261113/freeling-es-cl-4.2.0-261113.fc43.x86_64.rpm)

Download the RPM of your Fedora release, install it with dnf, and try it (Fedora 44 shown; on Fedora 43 use the `fc43` file):

```bash
curl -LO https://github.com/Linguista/FreeLing-es_CL-2027/releases/download/261113/freeling-es-cl-4.2.0-261113.fc44.x86_64.rpm
sudo dnf install ./freeling-es-cl-4.2.0-261113.fc44.x86_64.rpm
echo "Vos tenís que venir." | /usr/local/bin/analyze -f es-cl.cfg --outlv tagged
```

A newer release is installed the same way, over the old one. To remove it: `sudo dnf remove freeling-es-cl`.

### Ubuntu

Each release has a package for Ubuntu 26.04 and one for Ubuntu 24.04, both for x86-64 processors (`freeling-es-cl_4.2.0-YYMMDD.ubuntu26.04_amd64.deb`, `freeling-es-cl_4.2.0-YYMMDD.ubuntu24.04_amd64.deb`): FreeLing 4.2 with every change of this release, built by GitHub in a container of that distribution (so it links to that distribution's own Boost and ICU), then installed on a fresh container of the same distribution and checked there (`packaging/test-freeling.sh`); only packages that pass are attached to a release. It installs into `/usr/local`: the programs in `/usr/local/bin`, the library in `/usr/local/lib` (registered through `/etc/ld.so.conf.d/freeling-es-cl.conf`), the data and the three configs in `/usr/local/share/freeling`. Each package is about 560 MB. It cannot be installed beside another package named `freeling`. apt installs what it needs from Ubuntu with it, including `locales`; when the package is installed it generates the en_US.UTF-8 locale (FreeLing runs in it) with `locale-gen en_US.UTF-8` if it is missing, and leaves every other locale and setting alone.

Files of release 261113 (each newer release, with its own date in the file names, is on the [Releases page](https://github.com/Linguista/FreeLing-es_CL-2027/releases)):

- [`freeling-es-cl_4.2.0-261113.ubuntu26.04_amd64.deb`](https://github.com/Linguista/FreeLing-es_CL-2027/releases/download/261113/freeling-es-cl_4.2.0-261113.ubuntu26.04_amd64.deb)
- [`freeling-es-cl_4.2.0-261113.ubuntu24.04_amd64.deb`](https://github.com/Linguista/FreeLing-es_CL-2027/releases/download/261113/freeling-es-cl_4.2.0-261113.ubuntu24.04_amd64.deb)

Download the package of your Ubuntu release, install it with apt (the `./` tells apt it is a file, not a package name), and try it (Ubuntu 26.04 shown; on 24.04 use the `ubuntu24.04` file):

```bash
curl -LO https://github.com/Linguista/FreeLing-es_CL-2027/releases/download/261113/freeling-es-cl_4.2.0-261113.ubuntu26.04_amd64.deb
sudo apt install ./freeling-es-cl_4.2.0-261113.ubuntu26.04_amd64.deb
echo "Vos tenís que venir." | /usr/local/bin/analyze -f es-cl.cfg --outlv tagged
```

A newer release is installed the same way, over the old one. To remove it: `sudo apt remove freeling-es-cl`.

### Debian

Each release has a package for Debian 13 on x86-64 processors (`freeling-es-cl_4.2.0-YYMMDD.debian13_amd64.deb`): FreeLing 4.2 with every change of this release, built by GitHub in a container of that distribution (so it links to that distribution's own Boost and ICU), then installed on a fresh container of the same distribution and checked there (`packaging/test-freeling.sh`); only packages that pass are attached to a release. It installs into `/usr/local`: the programs in `/usr/local/bin`, the library in `/usr/local/lib` (registered through `/etc/ld.so.conf.d/freeling-es-cl.conf`), the data and the three configs in `/usr/local/share/freeling`. Each package is about 560 MB. It cannot be installed beside another package named `freeling`. apt installs what it needs from Debian with it, including `locales`; when the package is installed it generates the en_US.UTF-8 locale (FreeLing runs in it) by enabling it in `/etc/locale.gen` if it is missing, and leaves every other locale and setting alone.

Files of release 261113 (each newer release, with its own date in the file names, is on the [Releases page](https://github.com/Linguista/FreeLing-es_CL-2027/releases)):

- [`freeling-es-cl_4.2.0-261113.debian13_amd64.deb`](https://github.com/Linguista/FreeLing-es_CL-2027/releases/download/261113/freeling-es-cl_4.2.0-261113.debian13_amd64.deb)

Download it, install it with apt (the `./` tells apt it is a file, not a package name), and try it:

```bash
curl -LO https://github.com/Linguista/FreeLing-es_CL-2027/releases/download/261113/freeling-es-cl_4.2.0-261113.debian13_amd64.deb
sudo apt install ./freeling-es-cl_4.2.0-261113.debian13_amd64.deb
echo "Vos tenís que venir." | /usr/local/bin/analyze -f es-cl.cfg --outlv tagged
```

A newer release is installed the same way, over the old one. To remove it: `sudo apt remove freeling-es-cl`.

### macOS

Each release has a tarball for macOS 15 or later on Apple silicon (`freeling-es-cl-2027-YYMMDD-macos-arm64.tar.gz`) and on Intel (`...-macos-x86_64.tar.gz`): FreeLing 4.2 with every change of this release, built by GitHub on its macOS 15 machines against Homebrew's Boost and ICU, with the Chilean data installed and checked (`packaging/test-freeling.sh`) on the machine that built it. It installs into `/usr/local/freeling-es-cl-2027`.

Files of release 261113 (each newer release, with its own date in the file names, is on the [Releases page](https://github.com/Linguista/FreeLing-es_CL-2027/releases)):

- [`freeling-es-cl-2027-261113-macos-arm64.tar.gz`](https://github.com/Linguista/FreeLing-es_CL-2027/releases/download/261113/freeling-es-cl-2027-261113-macos-arm64.tar.gz)
- [`freeling-es-cl-2027-261113-macos-x86_64.tar.gz`](https://github.com/Linguista/FreeLing-es_CL-2027/releases/download/261113/freeling-es-cl-2027-261113-macos-x86_64.tar.gz)

```bash
brew install boost icu4c
sudo tar -xzf freeling-es-cl-2027-YYMMDD-macos-arm64.tar.gz -C /
echo "Vos tenís que venir." | /usr/local/freeling-es-cl-2027/bin/analyze -f es-cl.cfg --outlv tagged
```

The programs find Homebrew's libraries where Homebrew installs them (`/opt/homebrew` on Apple silicon, `/usr/local` on Intel); a Homebrew upgrade of boost or icu4c to a new major version needs the tarball of a newer release.

### Windows

Each release has a zip for 64-bit Windows 10 and 11 (`freeling-es-cl-2027-YYMMDD-windows-x86_64.zip`): FreeLing 4.2 with every change of this release, built by GitHub on its Windows machines with MSYS2's UCRT64 toolchain (GCC, Boost and ICU), with the Chilean data installed, and with every library it needs in its `bin` folder, so nothing else has to be installed. It is checked where it was built (`packaging/test-freeling.sh`) and again unpacked elsewhere, through `analyze.bat` from Windows' own shell. Unpack it anywhere, for example in `C:\FreeLing`, and run `analyze.bat` from its `bin` folder, in PowerShell.

Files of release 261113 (each newer release, with its own date in the file names, is on the [Releases page](https://github.com/Linguista/FreeLing-es_CL-2027/releases)):

- [`freeling-es-cl-2027-261113-windows-x86_64.zip`](https://github.com/Linguista/FreeLing-es_CL-2027/releases/download/261113/freeling-es-cl-2027-261113-windows-x86_64.zip)

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
"Vos tenís que venir." | C:\FreeLing\freeling-es-cl-2027\bin\analyze.bat -f es-cl.cfg --outlv tagged
```

FreeLing reads and writes UTF-8: the two first lines make PowerShell send and show it as UTF-8. `analyze.bat` finds the configs by name (`es-cl.cfg`, `es-cl-19th-century.cfg`, `es-old.cfg`) in the zip's `share\freeling\config` folder. Six changes to FreeLing's source make it build and run on Windows with GCC (`packaging/patch-freeling.sh`, 9a to 9f); they take effect only there.

## If you really want to try and build this rather than use a package...

This folder is the release. It is rebuilt, never edited by hand:

```text
/home/user/FreeLing_es-CL_2027
```

It is built by `freeling_escl_build.py` and put into use by `freeling_escl_deploy.py`; `freeling_csld_configs.py` then writes the CSLD configs that use it. All three are kept in

```text
/home/user/csld/software/10-Infrastructure/freeling/scripts/
```

A copy of every tool that made this build is in `software/`. A previous build is moved, whole, to `/home/user/software/deprecated/FreeLing_es-CL_2027.DEPRECATED-YYMMDD[letter]`.

### Building FreeLing 4.2 itself

The name-class change (section 8.5) is a change to FreeLing's code, so using this release fully means building FreeLing 4.2 from its source, `FreeLing-src-4.2.tar.gz` from FreeLing's GitHub releases (sha256 `f96afbdb000d7375426644fb2f25baff9a63136dddce6551ea0fd20059bfce3b`). That source dates from 2020, and as published it no longer builds or installs on any current Linux distribution. The packages are built by `packaging/build-freeling.sh`, which applies every fix below (`packaging/patch-freeling.sh`), on each distribution in a container of its own (`.github/workflows/packages.yml`). On 261112 the build was tried on five distributions:

| Distribution | GCC | Boost | ICU |
|---|---|---|---|
| Fedora 44 | 16.2.1 | 1.90.0 | 77.1 |
| Fedora 43 | 15.3.1 | 1.83.0 | 77.1 |
| Ubuntu 26.04 | 15.2.0 | 1.90.0 | 78.2 |
| Debian 13 | 14.2.0 | 1.83.0 | 76.1 |
| Ubuntu 24.04 | 13.3.0 | 1.83.0 | 74.2 |

What fails, where, and the fix for each. The fixes are applied on every distribution, since none of them changes what FreeLing does on a system that did not need it.

1. **CMake 4 refuses the bundled dynet** (CMake 4 and later; Fedora 44 has 4.3.0). `src/libdynet/CMakeLists.txt` declares `cmake_minimum_required(VERSION 2.8 FATAL_ERROR)`, and CMake 4 removed compatibility with versions below 3.5, so configuring stops. Fix: `-DCMAKE_POLICY_VERSION_MINIMUM=3.5`.
2. **Errors inside templates that are never used** (GCC 14 and later). GCC now checks the body of a template even when nothing instantiates it. Two such bodies were always wrong: the bundled Eigen's `Transpositions.h`, line 387, calls `derived()` on a `Transpose`, which has no such member, and treeler's `scores.h`, line 96, assigns to `_s`, which is declared `const`. GCC 15 and 16 (Fedora 43 and 44, Ubuntu 26.04) report them under `-Wtemplate-body`, which `-Wno-template-body` silences. GCC 14 (Debian 13) has no such option and stops: "assignment of read-only member 'treeler::ConstantScores<X, R>::_s'". GCC 13 (Ubuntu 24.04) does not check. Fix: the flag, and both lines corrected in the source: Eigen's as Eigen 3.4.1 corrected it (`trt` instead of `trt.derived()`), and `_s` no longer `const` (only its constructor and `set_score` write it).
3. **libfoma is K&R C** (GCC 15 and later, whose default is C23: Fedora 43 and 44, Ubuntu 26.04). In C23 an empty `()` in a declaration means no arguments, so `fsm_state_close` and its kin conflict with their own definitions: "conflicting types", "too many arguments to function". Fix: `-DCMAKE_C_FLAGS="-std=gnu17"`.
4. **ICU's headers need C++17** (ICU 77 and later: Fedora 43 and 44, Ubuntu 26.04), and FreeLing's `CMakeLists.txt` sets C++11 with a plain `set(CMAKE_CXX_STANDARD 11)`, which overrides anything given on the command line: hundreds of errors such as "'enable_if_t' in namespace 'std' does not name a template type". Fix: that line edited to 17.
5. **Math functions without `<cmath>`**. Older standard libraries brought `<cmath>` in through other headers; current ones do not, and which files fail depends on the version. `csr_kb.cc`, `relaxcor_fex_dep.cc`, `summarizer.cc` and `numbers_cs.cc` fail with GCC 16 ("'fabs' was not declared in this scope"); `smoothingLD.h` fails with GCC 13 (Ubuntu 24.04): "there are no arguments to 'log' that depend on a template parameter, so a declaration of 'log' must be available". Fix: `#include <cmath>` in all five.
6. **The install builds two Catalan variants whose data is not in the source tarball** (everywhere). `CMakeLists.txt` lists `ca/balear` and `ca/valencia` among the variants, so `make install` stops after Spanish: "file .../data/ca/balear/dictionary/header not found". Fix (and FreeLing es-CL 2027 is Spanish only, decided 261112): the language list limited to `es` and the variant list to `es/es-old` and `es/es-cl`; the English and Portuguese data the source tarball carries, the Argentine variant `es/es-ar` and the configs of every other language deleted from the source tree, so nothing of them is built or installed.
7. **The install needs the en_US.UTF-8 locale** (every machine without it; the distributions' containers have only C.UTF-8). FreeLing's "default" locale is hard-coded as en_US.UTF-8 (`DEFAULT_LOCALE` in `src/libfreeling/util.cc`), and `make install` uses it to build the phonetic dictionaries: "Locale name 'en_US.UTF-8' is unknown or not installed", then "creating phonetic dictionary failed with error: 1". Fix: the locale generated before the install (`localedef -i en_US -f UTF-8 en_US.UTF-8`). FreeLing needs it at run time too, so the packages depend on `glibc-langpack-en` (Fedora) or `locales` (Debian, Ubuntu). On Debian and Ubuntu, `locales` does not generate en_US.UTF-8 by itself, so the package generates it when it is installed, if it is missing (on Ubuntu with `locale-gen en_US.UTF-8`, on Debian by enabling it in `/etc/locale.gen`), and leaves every other locale and setting alone.
8. **A bug that aborts word-sense annotation** (wherever the standard library checks its assertions, as Fedora's does). `csr_kb.cc` reserves room in four vectors and then indexes them, although their size is still zero: "Assertion '__n < this->size()' failed", the first time UKB is used. Fix: `reserve` changed to `resize`.

With these fixes FreeLing 4.2 builds, installs and passes the package checks on all five distributions. The packages are built with `-DCMAKE_BUILD_TYPE=Release` (optimized); a build configured without a build type gets no optimization at all.

This README describes grammatical categories in words. The data files use FreeLing's tags, which FreeLing requires; `CHANGELOG.tsv` and `VARIANTS.tsv` give every tag in words beside it.

## License

FreeLing es-CL 2027 is based on FreeLing 4.2's own data files, and is under the same license as FreeLing: the GNU Affero General Public License, version 3 or (at your option) any later version. The license is in `LICENSE`. FreeLing was created by the TALP Research Center of the Universitat Politècnica de Catalunya, without whom this software would not exist.

In this release, the paths in the README and in the copies of the tools are those of the machine that built it, written in a public form (`/home/user/...`); every tool takes its paths (which will be your actual paths) as options.

## 1. Contents

| File | What it is |
|---|---|
| `README.md` | this file |
| `LICENSE` | the GNU Affero General Public License 3.0, FreeLing's license |
| `BUILD-REPORT.md` | the counts of this build and the sha256 of every input |
| `CHANGELOG.tsv` | every line-level change, one per row: list, change, rule, form, lemma, tag, the tag in words, detail |
| `DECISIONS.tsv` | every spelling and name decision read, one per row: decision file, form, what was decided, what the build did, detail |
| `NAME-CLASSES.tsv` | every name with a rule of its own: the fixed classes, the readings at the start of a sentence and the class shares, each with its form as FreeLing writes it, class, tag, share, files and source (section 8.4) |
| `NAME-WEIGHTS.tsv` | every decided name that is also an adjective, an adverb or an interjection, with the weight it got (section 6.6) |
| `VARIANTS.tsv` | every spelling variant: rule, variant, standard form, analyses copied (in words), new form or joined to an existing one |
| `SHA256SUMS` | the sha256 of every file here; the deploy script refuses a release that does not match it |
| `data/es/es-cl/dicc.src` | the default dictionary: contemporary Chilean Spanish (section 2) |
| `data/es/es-cl/historical/dicc.src` | the 19th-century dictionary: 2027 plus the 19th-century spellings, the pre-1952 accents and the vosotros readings, for historical corpora only (section 2) |
| `data/es/es-cl/historical/probabilitats.dat`, `historical/locucions.dat` | its probabilities and multiword expressions (section 2) |
| `data/config/es-cl.cfg` | the config of FreeLing es-CL 2027 (FreeLing's es-cl config with the Chilean tagset and currencies) |
| `data/config/es-cl-19th-century.cfg` | the config of the 19th-century dictionary (the same, with the 19th-century files and no compound analysis) |
| `data/es/es-cl/probabilitats.dat` | the lexical probabilities |
| `data/es/es-cl/locucions.dat` | the multiword expressions: FreeLing's general Spanish set and the full Chilean set (section 9) |
| `data/es/es-cl/locucions-MINIMAL.dat` | the minimal set (20), for those who prefer it (section 9) |
| `data/es/es-cl/tagset.dat` | the Chilean tagset (section 4) |
| `data/es/es-cl/np.dat` | the name recognizer's rules for written texts (CODICACH): every single letter is never a name; the fixed and dictionary name classes, inside a sentence; the readings of six names at the start of a sentence (section 8.4) |
| `data/es/es-cl/np-speech.dat` | the same for transcribed speech (COSCACH): the name classes apply at the start of a line too; the readings of four names there |
| `data/es/nerc/nec/nec-ab-poor1.dat` | the name classifier's file: FreeLing's, with the class shares of five names (section 8.4) |
| `data/common/nec/cities.dat` | the name classifier's city list: FreeLing's two city lists merged, with every place name of the Chilean data (section 8.3) |
| `data/es/nerc/data/gazLOC-c.dat` | the classifier's list of whole place names: FreeLing's, with every place name of the Chilean data |
| `data/es/nerc/data/gazPER-c.dat` | the classifier's list of whole person names: FreeLing's, without the seven places it held |
| `data/es/nerc/data/gazPER-p.dat` | the classifier's list of person-name parts: the Chilean list (3,018 names) |
| `data/es/es-cl/quantities.dat` | currencies and measures, with the Chilean currencies, and without 56 unit names that were false joins or are not used in Chile (section 10) |
| `data/es/es-cl/dictionary/header`, `dictionary/entries/CL.*` | the Chilean entries of the default dictionary, one analysis per line: what FreeLing's own build reads |
| `data/es/es-cl/remove/CL.removed` | the Spanish readings the default dictionary drops: FreeLing's own build reads it |
| `data/es/es-cl/historical/dictionary/entries/CL.historical`, `CL.19th-century-spellings`, `CL.19th-century-attested`, `historical/remove/CL.removed`, `historical/CL.removed-from-chilean-entries` | the same for the 19th-century dictionary (section 2) |
| `tuteo-tagged-dictionary/dicc-0-tags.zip` | the default dictionary with voseo tagged like tuteo, zipped, with its own README (section 11) |
| `grammatical-lists/freeling-cl/CL.*.GRAM.txt` | the corrected grammatical lists, tab-separated, in the layout of the CSLD lists they replace |
| `software/` | the tools that made this build, their READMEs, this README, and the six `explode-*-4-FreeLing.pl` scripts with `explode-VERBS-4-FreeLing_README.md` |
| `sources/escl-sources/` | every decision file this build read, with its README: the release can be rebuilt from itself (section 6) |
| `packaging/` | the packaging of FreeLing 4.2 with this release for Fedora 43 and 44, Debian 13 and Ubuntu 24.04 and 26.04, the macOS tarballs and the Windows zip: the scripts that patch, build, package and check it, each with its README (section "If you really want to try and build this rather than use a package...") |
| `.github/workflows/packages.yml` | the GitHub workflow that builds the packages on each distribution, installs each on a fresh one, checks it (and builds and checks the macOS tarballs on macOS 15, Apple silicon and Intel, and the Windows zip), and attaches it to a release tagged with a date (YYMMDD, an optional letter for a second release that day) |
| `software/patches/` | the change to FreeLing's name recognizer and classifier: `freeling-4.2-np-classes.patch`, its README, and the three source files it changes, as changed (section 8.5) |

The entries files:

| File | Lines | Content |
|---|---|---|
| `CL.adj` | 4,873 | adjectives (DUECh) |
| `CL.adv` | 107 | adverbs |
| `CL.demonyms` | 2,920 | demonyms (most from BDCUT-CL) |
| `CL.int` | 149 | interjections of the list (section 6.2 removed the others) |
| `CL.nom` | 16,637 | nouns |
| `CL.tanc` | 30 | closed-class words: vos, voh, vo, pa, toa, ke, naa, nadien ... |
| `CL.vaux` | 38 | the voseo forms of ser, estar and haber |
| `CL.verb` | 122,292 | the voseo paradigm of every Spanish verb, and the DUECh verbs |
| `CL.variants` | 97,183 | the spelling variants of the voseo forms (section 7) |
| `CL.names` | 21,563 | person, place and organization names of the lists, and arica, barbados, chanco and pirque as places only (section 8) |
| `CL.additions` | 21,015 | the decided words, with their paradigms (section 6.1) |
| `CL.nonstandard` | 193 | forms kept in the text, read as a standard form (section 6.3) |
| `CL.common-misspellings` | 163,652 | common misspellings, read as the word they misspell: the misspelt forms of the transcriptions and every accented word written without its accents (section 6.4) |
| `CL.old-accents` | 14 | fué, fuí, dió, vió, á, é, ó, ú, read as fue, fui, dio, vio, a, e, o, u (section 2) |
| `CL.standard-lemmas` | 10 | Spanish readings given their standard lemma (section 6.5) |

## 2. The three dictionaries

Decided 261109 and 261113: the default is contemporary Chilean Spanish, with modern voseo and everything associated with it; the 19th century and Old Spanish are asked for by naming their config.

| | FreeLing es-CL 2027, `dicc.src` | FreeLing es-CL 19th Century, `historical/dicc.src` | FreeLing Old, `es/es-old/dicc.src` |
|---|---|---|---|
| config | `es-cl.cfg` (the default) | `es-cl-19th-century.cfg` | `es-old.cfg` |
| for | contemporary corpora | historical corpora | medieval and Golden Age texts |
| vos | voseo only | voseo and polite; read as polite | as FreeLing ships it |
| -is forms with a voseo and a vosotros reading of the same verb and tense (salís, vivís) | voseo only (497 forms) | both; read as vosotros | as FreeLing ships it |
| 19th-century spellings | no | yes (below) | not added |
| pre-1952 accents fué, fuí, dió, vió, á, é, ó, ú | yes | yes | as FreeLing ships it |
| common misspellings (section 6.4) | yes | yes | not added |
| forms | 937,701 | 2,146,645 | 59,730 (its own dictionary only) |

Every other vosotros form (-áis, -éis, -abais, -íais, -ríais, the -ad, -ed, -id imperatives, os, vosotros, vuestro, sois) is in all three: every verb with a vosotros paradigm has all of it (8,255 verbs; the eight others are defective: llover, neviscar, ventisquear, abolir, garantir, embaír, soler, peder). The CSLD configs choose the dictionary (`freeling_csld_configs.py`, section 12), and `freeling_tag_corpus.py` refuses a historical corpus without `--historical` and refuses `--historical` for any other corpus.

### 2.1. The 19th-century dictionary

**It holds the old Chilean orthographies.** Every form of the 2027 dictionary but the proper nouns is also written in the spellings of Andrés Bello and Juan García del Río (1823), Domingo Faustino Sarmiento (1843), the Chilean orthography of 1844 and the Chilean neographers of the 1890s to the early 1900s (Carlos Cabezón, Carlos Newman and others, whose ortografía rrazional was printed in books, articles and translations), and each spelling gets the lemma and tags of the modern form it comes from. A writer could use any combination of them, so every combination is generated; a rule changes every place it applies in a word:

| Rule | Example | Used by |
|---|---|---|
| g before e or i written j | jente, jeneral, lijero | Bello, the 1844 orthography, Sarmiento, the neographers |
| x for the j sound written j (México, Texas, Oaxaca, Ximénez, Quixote, Xalapa) | Méjico, Tejas | Bello |
| y as a vowel written i | rei, mui, hoi, estoi, i | Bello, the 1844 orthography, Sarmiento, the neographers |
| x before a consonant written s | esplicar, estranjero, testo | the 1844 orthography |
| x before a vowel written cs | ecsamen | Sarmiento |
| qu written q, or k | qerer, qeso, keso | Bello, Sarmiento, the neographers |
| c for the k sound written k, or q | kasa, qasa, elektrizidad, qomerziantes | Bello, the neographers |
| c before e or i written s, or z | sielo, sienzia, soziedad, zientífica | Sarmiento, the neographers |
| z written s | sapato | Sarmiento, the neographers |
| the silent u of gue, gui dropped | gerra, giso | Bello, the neographers |
| silent h dropped (before a vowel) | ombre, umano | Bello, Sarmiento, the neographers |
| v written b | bino, abiso, Balparaíso | Sarmiento, the neographers |
| the trill written rr at the start and after n, l, s | rrazional, Enrrique | Sarmiento, the neographers |

Accents are never dropped (decided 261112): the neographers wrote unifikazion and fonetika, but an unaccented twin of every accented word (más and mas, está and esta) would read the 2027 words wrongly.

**A spelling that is already a word.** Only the rules the Chilean orthography of 1844 adopted (g before e or i as j, vowel y as i, x before a consonant as s) may give a spelling that is already a word, and the reading they add is nearly impossible on its own in `historical/probabilitats.dat`, so the word keeps its own readings unless the context demands the old one; where both readings have the same word class, the word's own lemma wins (lemma preferences). A spelling of another rule that is already a word is not added: casa never gets the readings of caza, nor echo those of hecho, nor a those of ha. Five such words are decided one by one (decided 261113):

| Form | In the 19th-century dictionary | Probability |
|---|---|---|
| i | the conjunction y, and the letter i | y 99%, the letter 1% |
| rei | rey only (not the name Rei) | |
| lei | ley only (not the plural of leu) | |
| hai | hay only, whatever its use | |
| soi | soy only (never voseo) | |
| testo | texto and testar | texto 90%, testar 10% |

In the 2027 dictionary these keep their own readings (i the letter, rei the name, lei the plural of leu, hai and soi voseo, testo testar).

**Attested spellings.** 5,333 spellings attested in historical texts (the CSLD's Historic-Word-List, and the pre-reform spellings taken out of its contemporary word list on 260811), with an accent where the modern word has none or in another place (tíempo, búsca, ráices, cáida, zodiáco), get the readings of the one modern word with the same letters. A spelling that matches several modern words, or that lacks an accent the modern word has, is not added. Source: `sources/escl-sources/historical-attested-spellings--261113.tsv`.

**The pre-1952 accents.** fué, fuí, dió, vió and the accented one-letter words á, é, ó, ú are in both the 2027 and the 19th-century dictionaries, with every reading of fue, fui, dio, vio, a, e, o, u (`CL.old-accents`).

**Vosotros.** A form with a voseo and a vosotros reading of the same verb and tense is read as vosotros, and vos as the polite pronoun (decided 261113). Both readings of such a form have the same short tag, and FreeLing's probabilities and tagger work on short tags, so a share (such as 90% to 10%) cannot be given: the tag preferences of `historical/probabilitats.dat` (PosPreferences) decide between them, always for vosotros.

**Multiwords.** Every multiword is also written in the 19th-century spellings (hoi_día, hoi_en_día): 6,539 keys, in `historical/locucions.dat`.

**Compound analysis is off** in the 19th-century config. FreeLing builds its compound analyzer from every form of the dictionary with foma, whose stack holds 2,097,152 entries, fewer than the 2.1 million forms of this dictionary: with it on, FreeLing stops at once with "Stack full!".

Loading it takes about 930 MB of memory, against about 780 MB for 2027.

**What FreeLing makes of it**, tagged with `es-cl-19th-century.cfg`: "La jente del jeneral esplicó que mui pronto llegaría el rei á Balparaíso i la lei fué clara. Ménos ántes que la soziedad zientífica. Hoi testo el qeso." gives gente, general, explicar, muy, rey, a, y, ley, ser, menos, antes, sociedad, científico, hoy, texto, queso. Balparaíso is taken as a name, since names get no 19th-century spellings.

**FreeLing's build-dict.** The 19th-century dictionary drops four readings that come from the Chilean lists (rei as a name, the voseo readings of hai and soi). FreeLing's build-dict applies a remove folder to the Spanish entries only, so these are listed apart, in `historical/CL.removed-from-chilean-entries`; the build checks that the 19th-century dictionary is FreeLing's Spanish entries, minus `historical/remove/CL.removed`, plus the Chilean entries minus those four, plus the 19th-century entries.

### 2.2. FreeLing Old

FreeLing's own Old Spanish (`es/es-old/`: its dictionary, probabilities, tagger and affix rules) is installed exactly as FreeLing ships it (decided 261113). Its config also reads a few shared files of the Spanish folder (the tagset, the sentence splitter, the currencies); its multiword file, `es/locucions.dat`, is a link to the Chilean one, which has FreeLing's general multiwords merged in (section 9), so its config is unchanged.

## 3. How the dictionaries are made

The Spanish dictionary is rebuilt from FreeLing 4.2's own source files, `/home/user/build/FreeLing-4.2/data/es/dictionary/header` and `entries/MM.*`, exactly as FreeLing's build does it, and the build refuses unless the result is FreeLing's Spanish dictionary byte for byte. Each source file is checked against FreeLing 4.2's sha256. No installed FreeLing file and no archived file is read.

Each dictionary is then the Spanish entries, minus the Spanish readings it drops, plus the Chilean entries: joined, sorted byte-wise (C locale), duplicates dropped, the analyses of each form joined onto one line, under the header. FreeLing's own build does the same with the entries and remove folders of this release (`build-dict`, as FreeLing's install runs it for a variant), and the build checks that it would give both dictionaries byte for byte.

Two facts of FreeLing's own code govern several fixes below. FreeLing lowercases a word before looking it up in the dictionary and before matching it against the multiword expressions, but stores both files' keys exactly as written, so a key written with a capital letter is never found. And when a multiword expression appears on two lines, FreeLing keeps only the first.

## 4. The tagset

The Chilean tagset is FreeLing's Spanish tagset with one value added in two places (decided 261109): voseo on the last position of a verb tag (gender) and of a personal pronoun tag (politeness). So cantái is "verb, main, indicative, present, 2nd person, singular, voseo", and vos is "pronoun, personal, 2nd person, common gender, singular, voseo". The forms of tú (tú, te, ti, contigo) never carry the voseo value. On nouns and adjectives the last position means evaluative (diminutive and the like), as in the Spanish tagset.

The build refuses a tagset that is not the approved one (sha256 `4f8def5440de2ffe6b73b11fc309ac8c6817b0f785ddb8ad41f8e5c875f137e8`) or not FreeLing's Spanish tagset plus exactly those two values, and refuses a file with a tag the tagset cannot decode. `probabilitats.dat` and `locucions.dat` name the Chilean tagset beside them (`./tagset.dat`; FreeLing's es-cl files named the Spanish one). Eight unknown-word tags of FreeLing's es-cl probabilities that no tagset decodes (adjective degrees such as AQCCN00, AQDFS00) are removed.

## 5. Corrections to the Chilean lists

The base is the CSLD grammatical lists (`linguistic-derived/grammatical-lists/individual/contemporary/freeling-cl/`); the corrected lists are in `grammatical-lists/` and deployed back.

| Change | Why |
|---|---|
| ir: 53 lines with an empty stem removed (a, o, e, an, ái, ís given as forms of ir), the 50 real forms restored | the explode script removed "ir" from "ir" (section 13) |
| vais, dais, veis, deis lose their voseo reading; dai, veís, deís added as voseo | vais, dais, veis and deis are vosotros only |
| erih and eríh restored as voseo present indicative of ser | lost from the newest list; confirmed correct |
| habís gains the auxiliary reading | habís alternates with hai, which has both |
| chorrocientos gains the indefinite-pronoun reading | the feminine had it |
| vos, voh, vo: tagged as voseo pronouns | the voseo pronoun tag |
| narcotraficante: a malformed tag corrected | lowercase letter inside the tag |
| capitalized keys lowercased (ABC, AFP, GCU, NEM, NN, PIB, UES) | never found (section 3) |
| U as a noun removed | its lowercase u is the conjunction |
| nguillatún, nguillatun and nguillatunes: the lemma guillatun corrected to nguillatún | the correct lemma (decided 261112) |
| every voseo form of erar removed, with its spelling variants | erar is practically never used, and its voseo forms collided with ser: erai and erís are ser only (decided 261101) |
| regular forms of irregular verbs removed (ponerái, convertierai, de, do, alenta, mova ...): every Chilean verb line of a verb the Spanish dictionary knows is checked against the Spanish dictionary's own forms | 30 verbs had been conjugated as regular |

The deliberate overgeneration is kept: the raised e of -ear verbs (golpiái), the dropped i of -iar verbs (envís), dái beside dai like vái beside vai. Not touched, because the Chilean paradigm is right: garuar, taimar, apernar.

## 6. The spelling decisions

The COSCACH spelling review (rounds 1 to 9) is read whole, with the name decisions of 261110d (section 8); later rounds win. `DECISIONS.tsv` gives each row's outcome.

Since 261112 the files the build reads have one copy, in the FreeLing tree: `/home/user/csld/software/10-Infrastructure/freeling/escl-sources/`, linked from the COSCACH decisions folder (`/home/user/corpora/050-Spelling-normalized/COSCACH/_processing-records/spelling-review/decisions/`), so the spelling step reads the same files (they were in `working/coscach-spelling--261101/decisions/` until 261111). The build refuses while a link is missing or a file of these kinds is an ordinary file in the COSCACH folder. A copy of every file read is in `sources/escl-sources/`, with its README. They are lists of words and names; the files that quote the interviews stay in COSCACH.

### 6.1. The decided words (CL.additions)

From `dictionary-additions-all-rounds-standardized--*.tsv` (6,328 rows, standard lemmas applied) and `verb-form-readings--*.tsv` (25 rows):

- Names keep their class: person, place, organization, other. A name whose lowercase form is also a common noun or a verb gets no proper-noun reading (decided 261110b): FreeLing's name recognizer tags it when it is capitalized. 401 names are exempted this way (chile, concepción, general, rosa, victoria, consejo ...). A name whose other readings are adjectives, adverbs or interjections keeps both readings (41 names; section 6.6).
- Nouns get their other number, and the lemma with its plural when the form is its plural or its feminine and the lemma is not yet a word (cosmetóloga gives cosmetólogo, cosmetólogos). A feminine form of a masculine lemma is tagged feminine (exalumnas).
- Adjectives get all their forms (masculine, feminine, singular, plural, or two when they do not vary for gender).
- A diminutive or augmentative whose lemma is the base word gets the evaluative value: cantitos, lemma canto, is noun, masculine, plural, evaluative (decided 261110: the diminutive of cantos); calladita, lemma callado, is an evaluative adjective. A superlative gets the superlative value (relajadísimo, lemma relajado). A lexicalized diminutive whose lemma has the suffix itself (burritos, lemma burrito) is not evaluative.
- New verbs get their whole paradigm, voseo included (168 verbs, 12,623 lines): a verb made of a prefix and a known verb is conjugated like it (sobreexigir like exigir, reprogramar like programar); any other like the known verbs that share its longest ending (hackear like the 797 regular verbs in -ear), taking the pattern at least three of them share, so a regular verb never gets a stem change. Their spelling variants follow (section 7).
- A verb form with attached pronouns (desestresarme, empréstame, tránsate: transar plus te, decided 261110) is analyzed by FreeLing's affix rules once the verb is known. A non-standard form of a known verb gets the tags of the regular pattern where it has them (ponido, ponieron, descubrido, coce).
- The verb forms no pattern could tag were decided one by one (decided 261110b, `verb-form-readings--261110b.tsv`): querímos and dicimos are present indicative, 1st person plural; sirvimos also preterite; haguís and estéi are present subjunctive, voseo; regatiái is present indicative, voseo; promesar is an infinitive of prometer, procastinar of procrastinar, parodear of parodiar, afiatear of afiatar, whatsappiar of whatsappear; and so on. A form with attached pronouns gets its reading on the form it is made from: hace, dice and pone are Chilean imperatives (háceme, hácela, díceselo, pónete), llevamos is the imperative of llevámonos, and rootiar is the infinitive of rootiarlos. The four imperatives are nearly impossible on their own in `probabilitats.dat`, so hace alone stays "verb, main, indicative, present, 3rd person, singular", while FreeLing's affix rules analyze háceme, hácele or díceselo from it. Four more forms are read through another decision (haguemos, vaiga, bendicir, intindís). anduvís is not added (section 14).
- Round 9 (261112, the COSCACH words in which Perkins found a syllable without a vowel): nocaut and nocauts, apk and cpu (feminine nouns), nguillatún, glug (interjection), and tsunami and tsunamis as a noun (FreeLing read tsunami as an adjective).
- A generated form that is already another word is not added.

### 6.2. Interjections

- 326 single-word interjections with their decided lemma (e.g. _po_, lemma 'poh'); an interjection reading with another lemma is replaced.
- 103 multiword interjections in `locucions.dat`; ya po and ya poh are ya_poh (section 9).
- RARE (62): the interjection reading stays but is nearly impossible. A single word's interjection count is 0 in `probabilitats.dat`, the other readings share at least 10,000, so FreeLing's smoothing leaves it about 1 in 100,000; a multiword becomes ambiguous (A), so its words can stay apart. mm is treated the same way: millimeter by far the more probable (in COSCACH the text itself, always a hesitation marker, becomes mmm).
- 235 removals (the Spanish interjections he, ha, fuera, hombre, vaya ...): their other readings stay. 53 Spanish forms that were only interjections (agur, caray, olé, ...) are no longer in the dictionaries: FreeLing will treat them as unknown words if it somehow comes across them.

### 6.3. Forms kept in the text (CL.nonstandard)

From `dictionary-variants`: the form stays in the text and gets the readings of its standard form (haiga as haya, vaiga as vaya, volao as volado). hácele, hácelo and hácete (read as hazle, hazlo, hazte) are analyzed by FreeLing's affix rules from the imperative hace (section 6.1). 11 are not added: the standard form is several words (el rubius) or not in the dictionary (jólidei).

### 6.4. Common misspellings (CL.common-misspellings)

Every misspelling FreeLing reads as the word it misspells is in one file, `CL.common-misspellings`, which the build merges into the dictionary like every other entries file; the build checks that every line of it is in `dicc.src` and in `historical/dicc.src`, with exactly its readings, and writes nothing if one is not (decided 261112). It holds two kinds.

**Every accented word written without its accents** (decided 261112): every correctly spelled form with a written accent or a diaeresis gives the same form without them, read as that form (comeriamos as comeríamos, colaboracion as colaboración, pinguino as pingüino), when the result is not already a word (seria, esta and mas are not added) and comes from that one form only (vacio, from both vació and vacío, is not added): 140,895 forms; 516 left out. The sources are correctly spelled forms only, never the misspelt forms below.

**The misspelt forms of the transcriptions.** Decided 261110: the text is corrected (the spelling step), and any misspelt form that slips through is read as its correction. 6,555 misspelt forms get their correction's readings, or the lemma and category of `correction-lemmas` where the user gave one (cosejo is the organization Consejo); a corrected word not yet in the dictionary is added with that lemma and category (zeppelin, trocadero). Not added: a misspelt form that is itself a word (it is corrected in the text only), a split or a join, and a correction FreeLing does not know (numbers such as dieciséis, which FreeLing recognizes by rule). Adverbs in -mente are read as adverbs. The corrections óscar to oscar and bachelte to bachellet are withdrawn (`text-correction-removals--261110.tsv`): oscar and óscar are both lemma óscar. So is ses to sea (`text-correction-removals--261110c.tsv`): every occurrence of ses is ruled one by one in the text, so ses is not read as sea.

### 6.5. Standard lemmas

`lemma-standardization` maps each lemma to its standard lemma; its two sheets are chained (aylen to aylén to ailén). A lemma is changed only on entries of the word class it was decided for: the name Ala becomes alá, the noun ala (wing) is untouched. Changed: 259 names of the lists (agustin becomes agustín, jose becomes josé), 6 Chilean nouns (sanguche becomes sánguche, clóset becomes closet) and 10 Spanish readings (vídeo becomes video, fríjol becomes frijol, ranking becomes ránking, márketing becomes marketing).

### 6.5b. Dictionary words and hand edits (decided 261112, 261113)

Two more sources of words, read at every build:

- `sources/escl-sources/dictionary-words--*.tsv`: form, lemma, category, tag, notes. With a tag, the form gets exactly that reading; without one, it gets the category's readings, as a decided word does (the other number and gender of a noun or an adjective, the whole paradigm of a new verb). Every round is read; a later round wins for the same form and lemma. The round of 261113 holds the Argentine and Rioplatense words decided for the CSLD (birome, subte, delivery, pibe, concheto, desprolijo, bue, holis ...; culiao and culiá, adjective and noun, lemma culeado), and the verbs pajear and serruchar; their multiword expressions (de a poco, dulce de leche, ponerse las pilas, hacer dedo ...) are in `locutions--261113.tsv`.
- `sources/escl-sources/dictionary-hand-edits.tsv`: exact dictionary lines, form, lemma and tag, edited in place; its comment lines say what goes in it. It holds cesfam, sar (masculine) and cosam (feminine), minipimer and chupafusiles, all with the same plural, and tatú and tatoo, lemma tatuaje.

### 6.6. The decided names in probabilitats.dat

A decided name that is also a common noun or a verb has no proper-noun reading (section 6.1), and its line in `probabilitats.dat` is FreeLing's own Spanish line, or none when FreeLing has none (decided 261110b).

Decided 261110. A decided name whose other readings are adjectives, adverbs or interjections (41: florida, allende, camilo, pacífico, roma ...) keeps both readings, and its line in `probabilitats.dat` gives the proper noun:

- 80% of the word's lexical probability for a place: the user's Chilean toponyms, much higher than the ordinary readings;
- 30% for a person, an organization or another name: moderate.

The ordinary readings share the rest in the proportions FreeLing already gives them. FreeLing's tagger divides each lexical probability by the tag's overall frequency, and a proper noun is about 3 times rarer than a common noun in its training corpus, so these shares weigh 3 times more against a common noun in context. FreeLing's name recognizer still runs.

`NAME-WEIGHTS.tsv` lists every weighted name, its ordinary readings and how often the word occurs in FreeLing's Spanish training corpus (about 418,000 words), and marks "common word: review" from 20 occurrences up. Marked in this build: florida.

The lines of the decided names are computed from FreeLing's own Spanish lines, never from the deployed file, which may hold the lines an earlier build wrote for them; every line the build manages is written in one block, sorted, at the end of the FormTagFreq section.

## 7. Spelling variants (CL.variants)

The Chilean voseo is almost exclusively spoken, so speakers rarely know how it's written (e.g. "estái" is more often seen as "estai", "estay" or even "estáy"). In order to handle this, the lists overgenerate on purpose, and this release adds the common misspellings of every voseo form. A variant gets exactly the verb readings of its standard form, and not the vosotros reading of an -is form that also has a voseo reading of the same verb and tense.

| Rule | From | To | Example | New forms | Joined to an existing form |
|---|---|---|---|---|---|
| R1 | -ái | -ai | estái > estai, cantarái > cantarai | 9,512 | 7,631 |
| R2 | -ís | -is | cantís > cantis | 9,050 | 0 |
| R3 | -íai | -iai | comíai > comiai | 9,553 | 0 |
| R4 | -ís | -íh | cantís > cantíh | 9,127 | 0 |
| R5 | -ís | -ih | cantís > cantih | 9,127 | 0 |
| R6 | -ái | -ay | cantái > cantay | 17,143 | 5 |
| R7 | -ái | -áy | cantái > cantáy | 17,150 | 0 |
| R8 | -ís | -í | tenís > tení | 8,254 | 0 |

R1 joins an existing form only if every reading it has is voseo (the unaccented future meeting the -ra imperfect subjunctive: cantarai; section 9 gives the future 20%). R2 to R5 and R8 add only new forms. R6 and R7 join existing forms, by the user's rule that -ay is -ái, except day and muday. No rule adds a reading to a function word.

## 8. Names

Decided 261110d: every Chilean locality (Santiago, Valdivia, Concepción, Castro, Arica ...) is read as a place, and the data FreeLing uses for names is the Chilean data, under the names FreeLing gives its own files, so that FreeLing reads it in their place. Decided 261110e: the Latin American capitals are places too; Molina is left to the classifier and Pinto is a surname; Barbados, Chanco and Pirque are places only; Catar, Irán, Tomé and Quito, at the start of a written sentence, are the verb with a 10% chance of being the place; Asunción, San José, San Juan and Sucre are mostly places, sometimes persons. Decided 261110f: Pinto, at the start of a sentence, can also be the verb pintar; Molina gets class shares like Asunción's, with the person slightly more probable. Decided 261110g: molina comes off FreeLing's list of whole person names; in transcribed speech, Pinto at the start of a line is the surname only (a speaker's pinto is written in lower case).

### 8.1. How FreeLing finds and classifies names

FreeLing decides in two steps whether a word is a proper name, and which kind:

1. **The name recognizer** (`np`, configured by `np.dat`) decides which words are a name. Inside a sentence, a capitalized word becomes a new name, "proper noun, unclassified", and every reading the dictionary gave it is dropped, a place reading included. At the start of a sentence a word becomes a name only if the dictionary also knows it as a common noun or an adjective, and keeps its dictionary readings beside the name reading; a word whose only readings are verbs (arica, molina) is not a name there at all.
2. **The name classifier** (`nec`) gives every unclassified name a class: person, place, organization or other. It weighs features, among them whether the name or its neighbors are on its word lists: whole names and name parts of each class (`es/nerc/data/gaz*.dat`) and a city list (`common/nec/cities.dat`).

Until 261110 the classifier read FreeLing's own lists: a world city list without most Chilean _comunas_, as well as **person** lists that held España, Lima and other places, and the Chilean surnames that are also communes (Castro, Molina, Pinto, Freire). In the COSCACH, a quarter of the place names came out as persons or organizations according to FreeLing (section 8.6).

### 8.2. The names in the dictionary (CL.names)

| List | Class (decided 261101) |
|---|---|
| `CL.peoplenames.GRAM.txt`, first names and surnames | person |
| `CL.cities.GRAM.txt`, places | place |
| `CL.orgnames.GRAM.txt`, organizations | organization, with the gender and number of the list |

21,559 entries in all, lowercased with lowercased lemmas. A list name whose lowercase form is already a word is left to the name recognizer, which tags it when capitalized (decided 261101): 1,162 people, 988 places, 4 organizations. Multiword places (agua_dulce) are not added.

**Place only** (`place-only-forms--261110d.tsv`, `place-only-forms--261110e.tsv`): arica, barbados, chanco and pirque are places and nothing else. Their readings as forms of a verb (aricar, barbar, chancar, pircar, all unheard of in Chile) are removed from the dictionaries; each gets the place reading, and any lemma preference (arica over aricar) or probability line of its own is dropped. They are then places at the start of a sentence too, in written texts and in speech.

### 8.3. The classifier's lists, replaced by Chilean ones

The release holds the classifier's lists under FreeLing's own names, and `freeling_escl_deploy.py --target system` installs them over FreeLing's:

| File (as FreeLing names it) | FreeLing 4.2 | FreeLing es-CL 2027 |
|---|---|---|
| `common/nec/cities.dat` | the world city list (2,211 names, in 4,683 lines: FreeLing's file repeats many) | FreeLing's city list and its Chilean version `cities-CL.dat` merged, with every place name of the Chilean data: 3,427 names (1,216 added) |
| `es/nerc/data/gazLOC-c.dat` | whole place names (1,782) | FreeLing's, with every place name of the Chilean data: 4,881 names (3,099 added) |
| `es/nerc/data/gazPER-c.dat` | whole person names (4,446) | FreeLing's, without seven places: españa, concepción, la_reina, maría_elena, santa_bárbara, lima (`person-name-removals--261110d.tsv`), molina (`person-name-removals--261110g.tsv`): 4,439 |
| `es/nerc/data/gazPER-p.dat` | person-name parts (1,012 lines) | the Chilean list of 291026, `linguistic-derived/people-names-list/gazPER-p.dat`: 3,018 |
| `es/nerc/nec/nec-ab-poor1.dat` | the classifier's file: its model, word list and classes | FreeLing's, with the section `<ClassShares>` (section 8.4); only FreeLing with the change of section 8.5 reads it |

FreeLing 4.2 ships `common/nec/cities-CL.dat`, its city list with 381 Chilean communes, provinces and regions added, but nothing reads it: the classifier's feature file names `cities.dat` only. It is merged into `cities.dat`, and the deploy retires it, with FreeLing's own name parts `es/nerc/data/gazPER-p.dat.upstream` (kept there on 291026), into a `deprecated/` folder beside them, compressed and unreadable.

**The place names of the Chilean data** (3,465) are those of the Chilean place list (`CL.cities.GRAM.txt`), the Chilean places of `cities-CL.dat`, and every place reading of the default dictionary and of the multiword expressions. All of them go into `gazLOC-c.dat` and `cities.dat`, except a single word that is also an ordinary word of the dictionary (a common noun, a verb ...) and not a fixed place (section 8.4): such a word on a place list would make the classifier see a place wherever it is capitalized. So castro is added to `gazLOC-c.dat` (it is a fixed place) and navidad is not (it is on `cities.dat` only because FreeLing's `cities-CL.dat` has it). The fixed places that are not place names of the Chilean data (most countries, and Quito) are not added: their fixed class decides, and the classifier never sees them alone. Every addition and removal is a row of `CHANGELOG.tsv` (lists `cities`, `gazLOC-c`, `gazPER-c`).

The classifier's other lists (organizations, other names, the place-name parts) and its model are FreeLing's: there is no Chilean version of them (this may well change in the future, however). FreeLing's own lists are kept whole, so a name decided not to be a place can still be on them: pinto is on FreeLing's `gazLOC-c.dat` and on its `cities-CL.dat`. The lists are features, not rules, so a list alone cannot fix a class; the fixed classes (section 8.4) do.

### 8.4. The recognizer's rules and the classifier's shares

`np.dat` and `np-speech.dat` are both FreeLing 4.2's Spanish `np.dat`, with:

- every single letter (a to z, and ñ) on its Ignore list as "ignore always", so a spelled-out letter (S H) is never a name (decided 261101). The cost: an initial inside a name (Juan A. Pérez) is no longer joined to the name;
- four sections that only FreeLing with the change of section 8.5 reads (FreeLing without it skips them):

| Section | Content |
|---|---|
| `<DictionaryClasses>` | place, person, organization, other (`NP00G00 NP00SP0 NP00O00 NP00V00`): a one-word name the dictionary knows as a proper noun of one of these classes keeps that class and the dictionary's lemma; the classifier is not asked |
| `<FixedClasses>` | 688 lines, `form tag`: the 668 names whose class is fixed, written as FreeLing writes a name (lower case, the words joined by _), those holding del or al also with de_el or a_el, as FreeLing writes them inside a name (viña_del_mar and viña_de_el_mar) |
| `<ClassesAtSentenceStart>` | `no` in `np.dat`, `yes` in `np-speech.dat` |
| `<SentenceStartClasses>` | the reading of a few names at the start of a sentence (below): 6 lines in `np.dat`, 4 in `np-speech.dat` |

The classifier's file, `es/nerc/nec/nec-ab-poor1.dat`, is FreeLing's with one section only the changed FreeLing reads (FreeLing without the change stops on it, so the deploy installs it only after the library):

| Section | Content |
|---|---|
| `<ClassShares>` | the classes of five names and their shares (below) |

**The fixed names** (`NAME-CLASSES.tsv` lists each one and where it comes from):

| Names | Class | Source |
|---|---|---|
| the 343 communes of Chile, all but Navidad, Molina and Pinto | place | `fixed-name-classes--261110d.tsv`, from the list of the communes of Chile, https://en.wikipedia.org/wiki/Communes_of_Chile (346 communes) |
| 197 countries and 15 continents and regions of the world (Chile, Perú, España, Estados Unidos, Europa, Latinoamérica ...) | place | `fixed-name-classes--261110d.tsv` (user, 261110: places, not organizations) |
| the capitals of Latin America, 18 names: Buenos Aires, La Paz, Brasilia and Brasília, Bogotá, La Habana and Habana, Quito, San Salvador, Ciudad de Guatemala, Puerto Príncipe, Tegucigalpa, Ciudad de México, Managua, Ciudad de Panamá, Lima, Montevideo, Caracas | place | `fixed-name-classes--261110e.tsv` (user, 261110: Lima is treated as all other Latin American capitals); Santiago and Santo Domingo are communes of Chile; Asunción, San José and Sucre have shares instead (below) |
| 66 Chilean regions, provinces and localities of FreeLing's `cities-CL.dat` that are not communes (Atacama, Chiloé, Ñuble, Región Metropolitana ...) | place | derived by the build: the names `cities-CL.dat` adds to `cities.dat` |
| 24 places of the Chilean list in neither of FreeLing's city lists: Chilean short forms (Antofa, Conce, Valpo, Ohiggins) and some foreign cities written without their apostrophe | place | derived by the build from `CL.cities.GRAM.txt` |
| Pinto | person | `fixed-name-classes--261110e.tsv` (user, 261110: Pinto is not a place, María Pinto is; a surname) |
| SES | organization | `fixed-name-classes--261110d.tsv` (round 8) |
| JUDEJUT | other | the same |
| Dr. House, Dr. Simi | person | the same |

Not fixed, and left to the classifier (class none): Navidad (a commune, but mostly the holiday), Mauricio and Israel (countries, and common given names in Chile) (`fixed-name-classes--261110d.tsv`); Molina (a commune, and a common surname: not invariably a place, user, 261110; `fixed-name-classes--261110e.tsv`), weighted toward the place by its class shares (below). OE and PH are left to the classifier too (user, 261110).

**The two files.** A capital at the start of a sentence says nothing in a written text. In the COSCACH transcriptions a line is an utterance, and it rarely begins with a capital unless its first word is a name: of the 21,366 probe lines (section 8.6), 2,434 begin with a capital, nearly all of them with a name (España, Perú, Santiago, Temuco), about a hundred with another word (Y, En):

| | `np.dat`: written texts (CODICACH) | `np-speech.dat`: transcribed speech (COSCACH) |
|---|---|---|
| inside a sentence | the fixed and dictionary classes | the same |
| at the start of a sentence (a line) | the readings of `<SentenceStartClasses>` (below); otherwise FreeLing's own treatment for a word that is also a common noun or an adjective (Castro, the noun castro; Lima, the noun lima) | the readings of `<SentenceStartClasses>`; otherwise the fixed and dictionary classes: Castro, Lima, Concepción, Tomé are places |

At the start of a sentence in a written text, then, FreeLing's own treatment decides for 100 of the 459 one-word fixed places, those that are also a common noun or an adjective (decided 261110d: the rule applies inside a sentence only, in written texts): algarrobo, antártica, argentina, brasil, cabildo, caldera, canela, castro, chile, china, colina, concepción, constitución, cordillera, cuba, florida, freire, granada, independencia, india, japón, laja, lima, linares, lota, malta, nacimiento, natales, nogales, olivar, parral, penco, pica, porvenir, primavera, providencia, recoleta, retiro, rusia, victoria, vicuña, zapallar and others. FreeLing keeps the name reading beside the dictionary's, and its tagger chooses.

**At the start of a sentence** (`sentence-start-classes--261110e.tsv`, `--261110f.tsv` and `--261110g.tsv`; the section `<SentenceStartClasses>`):

| Name | Files | Reading there | Why |
|---|---|---|---|
| Catar, Irán, Tomé | `np.dat` | the verb (catar; ir; tomar), with a 10% chance of the place: the verb readings kept beside the place, the tagger chooses | user, 261110: verbs at the start of a sentence, with a chance of being places, 10% |
| Quito | `np.dat` | the same: the verb quitar, with a 10% chance of the place; its rare adjective reading (quito, exempt) is not kept there | user, 261110: Quito gets the rule of Tomé |
| Molina | both | a name, the classifier decides (a place or a surname); never the verb molinar | user, 261110 |
| Pinto | `np.dat` | the surname, with a 30% chance, beside the verb pintar: the tagger chooses | user, 261110: Pinto is not a place, and it can also be a verb (`sentence-start-classes--261110g.tsv`, as 261110f had it for both files) |
| Pinto | `np-speech.dat` | the surname only | user, 261110: a COSCACH line starts with a lower-case letter unless its first word is a name, so a speaker's pinto is written in lower case and stays the verb (`sentence-start-classes--261110g.tsv`) |
| Asunción, Sucre | `np-speech.dat` | a name, the classifier decides with the shares (below); never the noun asunción or the currency sucre | a capital at the start of a COSCACH line is a name |

The 10% is the place's share among the readings the word has at the start of a sentence, set by its line in `probabilitats.dat` (section 9). It was chosen on 15 test sentences (Catar es un país pequeño, Catar el vino requiere práctica, Tomé tiene playas, Tomé un café, Quito es la capital, Quito la tapa ...): 2% got 13 right, 5% 14, 10%, 20% and 30% all 15, 50% 14 (`software/patches/freeling-4.2-np-classes_README.md`, section 3.4). 10% is the lowest share that gets every test sentence right. In speech the four are places at the start of a line, as every fixed place is.

Pinto's 30% was chosen the same way, on 16 test sentences, eight with the verb (Pinto la casa todos los años, Pinto cuadros al óleo, Pinto paisajes, Pinto y dibujo ...) and eight with the surname (Pinto dijo que no vendría, Pinto la vio ayer, Pinto no vino ...):

| Share of the person | Right | Wrong |
|---|---|---|
| 5% | 15 of 16 | Pinto la vio ayer (the verb) |
| 10% | 14 of 16 | Pinto la vio ayer (the verb); Pinto y dibujo (the surname) |
| 20%, 30%, 50% | 15 of 16 | Pinto y dibujo (the surname) |
| 70% | 12 of 16 | Pinto cuadros al óleo, Pinto con acuarelas, Pinto paisajes, Pinto y dibujo (the surname) |

"Pinto y dibujo" reads like "Pinto y Molina" up to its last word. 30% is the middle of the shares that tested best. In transcribed speech the share does not apply: a capitalized Pinto at the start of a COSCACH line is the surname (decided 261110g). In the probe, "Y" starts a line 13 times against "y" 1,861 times, "En" 11 against "en" 1,526, "No" 5 against "no" 1,051, and the one verb reading of Pinto there ("Pinto el", before "Sergio Navarro", in a list of footballers) was wrong.

**The class shares** (`name-class-shares--261110e.tsv`; the classifier's `<ClassShares>`):

| Name | Place | Person |
|---|---|---|
| Asunción | 80% | 20% |
| Molina | 75% | 25% |
| San José | 80% | 20% |
| San Juan | 80% | 20% |
| Sucre | 95% | 5% |

When the classifier classifies one of these names, it takes the place or the person, whichever has the higher score: the classifier's own weight plus half the log odds of the share. "Viajamos a Asunción en enero" was a person and is a place; "La señora Asunción vive al lado" stays a person. The share weighs the classes, it does not detect the person: where the classifier sees little evidence for one (Mi tío San José, El general Sucre), the place stays. Molina (decided 261110f: as Asunción, with the person slightly more probable) worked the other way round while FreeLing's list of whole person names had molina: the classifier's own weight for the person was strong, and the share turned only some places around ("Allá en Molina hace calor" became a place, "Vivo en Molina" stayed a person). With molina off that list (decided 261110g), "Vivo en Molina" is a place too; at the start of a sentence the classifier can still call it a person ("Molina queda cerca de Talca"), section 8.6.

### 8.5. The change to FreeLing's code

FreeLing 4.2 cannot fix a name's class, it drops a place reading to which the dictionary gives a capitalized word inside a sentence, it has no rule of its own for a word at the start of a sentence, and cannot weigh a name's classes. The change, `software/patches/freeling-4.2-np-classes.patch` (decided 261110d and 261110e), adds the four sections of section 8.4 to FreeLing's name recognizer (`src/libfreeling/np.cc` and `src/include/freeling/morfo/np.h`) and `<ClassShares>` to its classifier (`src/libfreeling/nec.cc`). A rule file without the recognizer's sections works exactly as before, and FreeLing without the change skips them; a classifier file with `<ClassShares>` stops FreeLing without the change. Its README, `software/patches/freeling-4.2-np-classes_README.md`, describes the change in the code, how to apply, build and install it, and how to check that the installed library has it:

```bash
strings -e L /usr/local/lib/libfreeling.so | grep -c -x -E "DictionaryClasses|FixedClasses|ClassesAtSentenceStart|SentenceStartClasses|ClassShares|keep:"
```

(6 with the change; 5 with its first state, which drops the verb readings of Quito at the start of a sentence; 0 without.) Only the library is rebuilt and installed; `make install` must not be run, because it also reinstalls FreeLing's own data over this release's (deploy again after it if it ever is). `freeling_escl_deploy.py --target system` refuses to install this release, and `freeling_tag_corpus.py` to tag COSCACH or CODICACH, with a library without the change.

### 8.6. The measured effect

The probe of 261110 took every line of COSCACH stage 050 holding a place name of the Chilean data: 21,366 lines, 24,408 occurrences, 22,422 of them a token of exactly the name (the others are part of a longer name, such as Hospital de Puerto Montt). It is in `/home/user/csld/working/freeling/probe-261110j/` (`in/` the lines, `lists/targets.txt` the names, `tagged/` FreeLing's output before the change). The class each exact token got:

| FreeLing | Place | Person | Organization | Other | Not a name |
|---|---|---|---|---|---|
| 4.2 with FreeLing es-CL 2027 as of 261110 (before) | 16,940 (75.6%) | 3,666 (16.4%) | 1,573 (7.0%) | 162 (0.7%) | 81 (0.4%) |
| the same, with the Chilean lists of section 8.3 only | 21,641 (96.5%) | 71 | 600 | 29 | 81 |
| this release, with the change: `np-speech.dat` | 22,304 of 22,394 (99.6%) | 17 | 46 | 14 | 13 |
| this release, with the change: `np.dat` | 22,302 (99.5%) | 16 | 49 | 15 | 40 |

(Before 261110g: 22,289 (99.5%) with `np-speech.dat` and 22,287 (99.4%) with `np.dat`, 31 persons each. The release of 261110f, installed on this machine and run by `freeling_tag_corpus.py`, gave the same tags as the test copy, token for token. 261110g changed 16 of the 220,734 tokens in speech, 15 Molina and one Pinto, and 15 in written texts, all Molina.)

Before: España a person 459 times, Concepción 322, Antofagasta 193; Perú an organization 231 times. After: each a place every time. Of the 2,306 other names in the same lines, 459 changed class, most of them for the better: 255 countries from organization to place, 71 given names from organization to person, 37 from person to place (San Martín, Viña); 27 went from place to person (Florencia, Errázuriz).

What is left:

- Molina, left to the classifier with its shares and off FreeLing's list of whole person names (decided 261110g), is a place 31 times of its 32 occurrences as a single word; the one person is Enrique Molina, a school named after a person. With molina on that list it was a person 16 times (de Molina a Curicó, eh cerca de Molina), and with neither the removal nor the shares 25 times;
- Pinto, a surname by decision, is a person 4 times in speech (feria Pinto, al Pinto, and "Pinto el" at the start of a line, which in written mode is the verb);
- a whole name that holds a place ("con Santiago Pérez" is one name, and the classifier calls it a place); two capitalized words in a row are one name (Caracas Venezuela at the start of a line);
- the place names that are also given names and not fixed (Navidad, Mauricio, Israel), as decided;
- Florencia, the Italian city, is a person: the dictionary has the given name only;
- the fixed places at the start of a sentence in written texts (Castro 14 times the noun at the start of a line, section 8.4).

## 9. Probabilities and multiword expressions

`probabilitats.dat` is the deployed Chilean file, with:

| Lines | What |
|---|---|
| 6 lemma preferences | hacer over hacendar, ser over erar, aburrir over aburrar, vender over vendar, mío over miar, poder over podar (arica over aricar until 261110d: arica is a place only, section 8.2) |
| hm | the interjection more probable than hectómetro |
| the unaccented future against the -ra imperfect subjunctive | cantarai is future 1 time in 5 |
| poder over podar where their categories differ | podís, podis ... (1,000 to 1) |
| the decided names | section 6.6 |
| the RARE interjections and mm | section 6.2 |
| hace, dice, pone, llevamos | the imperative reading nearly impossible on its own (section 6.1) |
| pinto | the person 30% against the verb at the start of a written sentence (section 8.4): `pinto NP-VMI NP 429 VMI 1000`; in speech the line has no effect there, as the person is the only reading |
| catar, irán, quito, tomé | the place 10% against the verb at the start of a written sentence (section 8.4): `tomé NP-VMI NP 111 VMI 1000`; `quito AQ-NP-VMI AQ 47040 NP 112 VMI 1008`, where the place is counted against the verb only (the adjective is not kept at the start of a sentence), and elsewhere the adjective and the verb keep FreeLing's proportions |

`locucions.dat` is the deployed full set, with the repairs of every build (duplicate lines merged, lemmas written as patterns repaired, capitalized keys lowercased, a comma as its own token, three tags corrected, jeans_day and jean_day), and the interjection decisions (section 6.2). The key `ya_<po>` named a lemma po that no form has, so it never matched; it is `ya_<poh>`, lemma ya_poh (decided 261109).

Since 261112 it also holds FreeLing's general Spanish multiwords (o sea, por ejemplo, por lo menos, a pesar de ...). FreeLing reads a single multiword file, and the Chilean file used to hold only the Chilean multiwords, so every general one was split into its words. The 1,563 general entries the Chilean file did not have are merged in; for a key in both, the Chilean entry wins (ni fu ni fa stays an adjective). FreeLing's general file tags tal y cual as a punctuation mark; it is an indefinite pronoun here (PI0CS00). Multiwords decided for the CSLD come from `sources/escl-sources/locutions--*.tsv` and are removed by `locution-removals--*.tsv`. A multiword is written as FreeLing matches it: al and del are split before matching, so al final is `a_el_final`.

`locucions-MINIMAL.dat` is the minimal set of the 2026 release, built into the build script, with the same repairs and the interjection decisions on the expressions it has: a multiword lemma hides its words from searches ("a" does not find "a_través_de"). To use it, install it as `locucions.dat`.

## 10. Currencies (quantities.dat)

FreeLing 4.2's Spanish file, Chileanized (decided 261109):

| Change | Was |
|---|---|
| peso alone is the Chilean peso, CLP | the Cuban peso |
| the sign $ is the Chilean peso | the US dollar (US$ is not affected) |
| the euro's code is EUR | ECU |
| added: unidad de fomento and uf, code UF; unidad tributaria mensual and utm, code UTM | |

**56 unit names removed** (decided 261112). FreeLing's quantities module joins a number and the unit name after it into one token, comparing the word in lower case and accepting "number de unit". In COSCACH a number followed by an abbreviation that is also a letter, a word or a false start became a quantity: "uno tr ..." was 1 unit of weight (tr), "uno de mi ..." 1 mile (41 tokens with mi), "uno s ..." 1 second, "sesenta D" 60 days, "los tres cd" 3 candelas. Removed from `<MeasureNames>`:

| Removed | Why |
|---|---|
| tr | the letters of a false start, never a unit |
| mi | the possessive mi, not the mile |
| s, d | the letters, and false starts, not the second and the day |
| cd | CD, the compact disc, not the candela |
| cl, bu | false starts, not the centiliter and the bushel |
| pk | the chat spelling of porque, not the peck |
| in | the English word in, not the inch |
| pt | punto, points, not the pint |
| ft, gal, lb, oz, ac, yd, qt, with their compound forms (ft2, ft3, ft/s, gal/h, lb/ft3, floz, ac-ft, yd2 ...) and those of in and mi (in2, inHg, mi2, mi/h ...) | not written so in Chile |

The unit codes in `<Measure>` stay, so the full words keep working (dos días, `TM_d:2`; milla, pie, galón, libra, onza, pulgada are kept), except the code of tr, `WG tr`, which no name uses once tr is removed. Kept, as real units in Chilean writing: g, h, m, l, ml, w, km, kg, cm, mm, mg, min, tm, cal, mb, gb, kb and the rest. Every removal is a row of `CHANGELOG.tsv` (list `quantities`, change `removed`), with its reason. A false start before an ellipsis that FreeLing reads as meters or liters ("dos m ...", "uno l ...", about ten in COSCACH) is still joined: the file cannot tell it from the unit.

## 11. The tuteo-tagged dictionary

`tuteo-tagged-dictionary/dicc-0-tags.zip` holds the default dictionary with voseo tagged like tuteo: a voseo verb form carries the tuteo tag, and vos is tagged like te and ti, with no voseo value. It is not used by the CSLD; its README says how to use it.

## 12. The CSLD configs

`freeling_csld_configs.py` (1.2.0) writes, in `/home/user/csld/software/10-Infrastructure/freeling/`:

| Config | Corpus | Dictionary | Name recognizer |
|---|---|---|---|
| `coscach/csld-es-cl--coscach.cfg` | COSCACH, transcribed speech | default | `es-cl/np-speech.dat` |
| `codicach/csld-es-cl--codicach.cfg` | CODICACH, written texts | default | `es-cl/np.dat` |
| `historical/csld-es-cl--historical.cfg` | historical corpora | 19th century, with its probabilities and multiwords; compound analysis off (section 2.1) | FreeLing's statistical recognizer, as in the base config |

All three use the Chilean tagset and currencies; COSCACH and CODICACH each have the stand-in user map beside their config (`usermap--coscach.dat`, `usermap--codicach.dat`). The config COSCACH and CODICACH shared until 261110, `coscach-codicach/csld-es-cl--coscach-codicach.cfg`, is retired to `coscach-codicach/deprecated/` with its user map. The separate COSCACH/CODICACH copy of the dictionary was retired earlier: the installed default is that dictionary. The place and person lists of section 8.3 are also features of FreeLing's statistical recognizer, so the historical config reads them too (all but `cities.dat`); the fixed and dictionary classes are read only by COSCACH's and CODICACH's.

## 13. The explode scripts

The lists were generated with `/home/user/MyScripts/linguistics/explode-*-4-FreeLing.pl`. The current `explode-VERBS-4-FreeLing.pl` fixes the three faults that produced errors here: the empty stem of "ir", the -uir branch that dropped the u, and -guir/-quir verbs sent to the -uir branch.

## 14. Open points

- The spelling step of COSCACH (stage 050) corrects the text; veis written for voseo must become veís there, since veis is vosotros only.
- FreeLing's Spanish dictionary itself has garua (for garúa) and taíma (for taima). This release does not change it.
- anduvís (lemma andar) is not added: which form it stands for is still to be decided.
- FreeLing's classifier calls Año Nuevo a person; it is not on any list.

## 15. Rebuilding and installing

The data:

```bash
freeling_escl_build.py --dry-run
freeling_escl_build.py
freeling_escl_deploy.py --target user --dry-run
freeling_escl_deploy.py --target user
sudo /home/user/csld/software/10-Infrastructure/freeling/scripts/freeling_escl_deploy.py --target system --dry-run
sudo /home/user/csld/software/10-Infrastructure/freeling/scripts/freeling_escl_deploy.py --target system
freeling_csld_configs.py
```

The user deployment replaces the CSLD grammatical lists and the build tree's Chilean files in `/home/user/build/FreeLing-4.2/data/es/es-cl/`. The build tree's other FreeLing files (the city lists, the classifier's lists) stay FreeLing's own, because the build reads them and checks them against FreeLing 4.2. The system deployment replaces, in `/usr/local/share/freeling/`:

```text
es/es-cl/dicc.src, es/es-cl/historical/dicc.src,
es/es-cl/historical/probabilitats.dat, es/es-cl/historical/locucions.dat,
es/es-cl/probabilitats.dat, es/es-cl/locucions.dat, es/es-cl/tagset.dat,
es/es-cl/np.dat, es/es-cl/np-speech.dat, es/es-cl/quantities.dat,
common/nec/cities.dat, es/nerc/data/gazLOC-c.dat, es/nerc/data/gazPER-c.dat,
es/nerc/data/gazPER-p.dat, es/nerc/nec/nec-ab-poor1.dat
```

retires `common/nec/cities-CL.dat`, `es/nerc/data/gazPER-p.dat.upstream`, `config/es-cl.cfg` and `config/es-cl-19th-century.cfg` (the CSLD tags with its own configs, made from these files, so no other es-cl config is kept where it could be used by mistake), and makes `es/locucions.dat` (FreeLing Old's multiword file) a link to `es-cl/locucions.dat`. The user deployment also retires the build tree's `dictionary/entries/CL.misspellings`, now `CL.common-misspellings`. Each replaced or retired file is first moved to a `deprecated/` folder beside it; in the installed data it is also compressed and made unreadable. The build is reproducible: run again on its own deployed output, or on an earlier build's, it gives the same files, byte for byte.

The library, once, and before the system deployment, which refuses to run without it (section 8.5 and `software/patches/freeling-4.2-np-classes_README.md`, section 7): the change applied to `/home/user/build/FreeLing-4.2/src`; the build folder configured with the options of the first build (`cmake -S /home/user/build/FreeLing-4.2 -B /home/user/build/FreeLing-4.2/build -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DCMAKE_CXX_FLAGS="-Wno-template-body" -DCMAKE_C_FLAGS="-std=gnu17"`), which also rebuilds a build folder that was emptied; the library alone built (`make -C /home/user/build/FreeLing-4.2/build -j16 freeling`); the library installed by its own folder's install script (`sudo cmake -P /home/user/build/FreeLing-4.2/build/src/libfreeling/cmake_install.cmake`) and the header copied; never `make install`.

The release is public. The build writes every file of it that is not data (this README, the build report, the software, the sources) with the private paths of `freeling-release-privacy.tsv` replaced by public ones, and writes nothing if any private term of that file is left in any file of the release, data included. The privacy file is in `software/10-Infrastructure/freeling/` of the project and is never copied into the release.

## 16. Changelog

- 2027 (rebuilt 261113, freeling_escl_build.py 2.8.1): a zip for 64-bit Windows (section "Windows"), built with MSYS2's UCRT64 toolchain and the six Windows fixes of `packaging/patch-freeling.sh` 1.2.0; no change to the data or the configs.

- 2027 (rebuilt 261113, freeling_escl_build.py 2.8.1): no change to the data or the configs; the build carries FreeLing 4.2's `es-cl.cfg` instead of reading it. This README gains the list of linguistic innovations.

- 2027 (rebuilt 261113, freeling_escl_build.py 2.8.0): three Spanishes, chosen by config (section 2): the 19th-century dictionary now holds the 19th-century Chilean spellings (Bello, the 1844 orthography, Sarmiento, the neographers; 1,203,611 spellings), 5,333 attested old-accent spellings, the multiwords in those spellings, its own probabilities (the Bello readings of existing words nearly impossible; i, rei, lei, hai, soi and testo decided one by one; vosotros over voseo) and its own config, `es-cl-19th-century.cfg`; FreeLing Old installed as FreeLing ships it, its multiword file the Chilean one; fué, fuí, dió, vió, á, é, ó, ú in both Chilean dictionaries; common misspellings: 140,895 unaccented forms, with the misspelt forms of the transcriptions, in `CL.common-misspellings` (formerly `CL.misspellings`); the Argentine and Rioplatense words decided for the CSLD, and cesfam, sar, cosam, minipimer, chupafusiles, tatú and tatoo; `es-cl.cfg` with the Chilean tagset and currencies; the packages Spanish only, with no Argentine variant. This README says "historical corpora" for the corpora the 19th-century dictionary is for.

- 2027 (rebuilt 261112, freeling_escl_build.py 2.7.0): FreeLing's general Spanish multiwords merged into `locucions.dat` (1,563 added; section 9), which every corpus tagged with the earlier releases lacked; tal y cual an indefinite pronoun; decided multiwords from `locutions` files; every decision file read per expression across all its rounds. The other data are unchanged. Badges added to this README.

- 2027 (rebuilt 261112, freeling_escl_build.py 2.6.0): packages of FreeLing 4.2 with this release for Fedora 43 and 44, Debian 13 and Ubuntu 24.04 and 26.04, built and checked by GitHub (`packaging/`, `.github/workflows/packages.yml`); how FreeLing 4.2 fails to build on each, and the fixes (the section "If you really want to try and build this rather than use a package..."); why this new version. The data are unchanged; one class in `NAME-CLASSES.tsv` reads `organization` for `organisation`.

- 2027 (rebuilt 261112, freeling_escl_build.py 2.5.1): the release is public (decided 261112): no private path in any file (section 15), and FreeLing's license, the GNU AGPL 3.0, in `LICENSE`. The data are unchanged.

- 2027 (rebuilt 261112, freeling_escl_build.py 2.4.3): the unit code of tr removed from `quantities.dat`; nguillatún, nguillatun and nguillatunes have the lemma nguillatún (the Chilean noun list gave guillatun; decided 261112), corrected in the noun list itself (section 5) and in the dictionaries.

- 2027 (rebuilt 261112, freeling_escl_build.py 2.4.1): 56 unit names removed from `quantities.dat` (section 10): tr, mi, s, d, cd, cl, bu, pk, in and pt, and ft, gal, lb, oz, ac, yd and qt with their compound forms and those of in and mi. The decision files read from `escl-sources/` in the FreeLing tree, linked from COSCACH, and copied into `sources/escl-sources/` (freeling_escl_build.py 2.4.0); round 9 of the spelling review: nocaut, nocauts, apk, cpu, nguillatún, glug, tsunami and tsunamis.

- 2027 (rebuilt 261110, freeling_escl_build.py 2.3.0): decided 261110g. molina off the classifier's list of whole person names (`gazPER-c.dat`: 4,439, seven places removed); in transcribed speech (`np-speech.dat`) Pinto at the start of a line is the surname only, while written texts (`np.dat`) keep the verb beside it at 30%. Place names in the COSCACH probe read as places: 99.6% with `np-speech.dat` (Molina 31 of 32).

- 2027 (rebuilt 261110, freeling_escl_build.py 2.2.0): the names (decided 261110d, 261110e and 261110f, section 8). The classifier's lists replaced by Chilean ones: `cities.dat` (FreeLing's two city lists merged, 1,216 names added), `gazLOC-c.dat` (3,099 added), `gazPER-c.dat` (six places removed), `gazPER-p.dat` (the Chilean list); `cities-CL.dat` and `gazPER-p.dat.upstream` retired. The change to FreeLing's name recognizer and classifier (`software/patches/`), and its sections in `np.dat` (written texts), the new `np-speech.dat` (transcribed speech) and the classifier's `nec-ab-poor1.dat`: 668 names with a fixed class (663 places: the communes of Chile, the countries and continents, the capitals of Latin America, the Chilean regions, provinces and localities; Pinto, SES, JUDEJUT, Dr. House, Dr. Simi), and the dictionary's proper-noun classes kept; the readings of Catar, Irán, Tomé, Quito, Molina and Pinto at the start of a sentence; the class shares of Asunción, Molina, San José, San Juan and Sucre. arica, barbados, chanco and pirque places only. ses no longer read as sea. Place names in COSCACH read as places: 75.6% before, 99.5% after. Default dicc.src: 796,408 forms.

- 2027 (rebuilt 261110, freeling_escl_build.py 2.1.0): a decided name that is also a common noun or a verb has no proper-noun reading (401 names); the verb forms decided one by one, with the Chilean imperatives hace, dice and pone, and llevamos; the decided names' probability lines from FreeLing's own Spanish lines. Default dicc.src: 796,409 forms.

- 2027 (261110, freeling_escl_build.py 2.0.0): two dictionaries, default (contemporary) and historical (for historical corpora); the spelling decisions of rounds 1 to 7 (decided words with paradigms, interjections, forms kept in the text, misspellings, standard lemmas, decided names weighted); ya_poh; the Chilean tagset checked; the Chilean currencies; the Spanish base from FreeLing's own source files; FreeLing's entries and remove files for both dictionaries; the tuteo-tagged dictionary zipped in its own folder. Default dicc.src: 796,382 forms.

- 2027 (rebuilt 261101, freeling_escl_build.py 1.1.0): the voseo forms of erar removed, with their variants and probability lines; np.dat added. dicc.src: 770,683 forms.

- 2027 (built 261101, freeling_escl_build.py 1.0.0): first release.
