# The tuteo-tagged dictionary (dicc-0-tags)

`dicc-0-tags.zip` holds `dicc-0-tags.src`: the default (contemporary)
FreeLing es-CL 2027 dictionary with voseo tagged like tuteo. A voseo verb
form carries the tuteo tag (cantai is tagged as cantas, verb, main,
indicative, present, 2nd person, singular), and vos is tagged like te and
ti (pronoun, personal, 2nd person, common gender, singular, no voseo
value). Voseo and tuteo are then told apart only by their spelling.

It is not used by the CSLD. It exists for anyone who needs FreeLing's
Spanish tags unchanged, for example a tool that rejects the voseo value.

To use it:

1. Unzip it: `unzip dicc-0-tags.zip`
2. Install `dicc-0-tags.src` as `dicc.src` in a FreeLing data folder of its
   own, never over the default dictionary, and point a config at it with
   `DictionaryFile=`.
3. Keep `TagsetFile=` pointing at the Chilean tagset: it decodes both tag
   sets.

It is rebuilt with every release by `freeling_escl_build.py`; the copy here
always matches the release it came with.
