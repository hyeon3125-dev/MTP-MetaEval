# How to put this on arXiv

## Short answer to "can you just push it from here?"

**No — arXiv has no `git push` / no submit API for individuals.** Submission is a
web upload tied to *your* arXiv account, and (for a first submission in a category)
it needs an **endorsement**. I can't create the account, pass the endorsement, or
click submit for you. What I *have* done is make the manual step as small as
possible: a self-contained manuscript that compiles with zero local setup.

There is an arXiv API, but it is **read-only** (search/metadata). Bulk deposit
(SWORD) exists only for institutional/conference partners, not individuals.

## The whole thing is ~10 minutes. Two paths.

### Path A — Overleaf (no local LaTeX; easiest)
1. Zip the `paper/` folder (`main.tex`, `refs.bib`, `figs/`).
2. Overleaf → *New Project* → *Upload Project* → drop the zip.
3. It compiles as-is (`main.tex` embeds its own bibliography — no bibtex pass
   needed). Download the PDF to eyeball it.
4. Overleaf → *Submit* → *arXiv*, **or** download the source `.zip` and use Path B.

### Path B — arXiv directly
1. Make an account at \<https://arxiv.org\> and, if this is your first submission
   in **cs.LG** (or **stat.ME**), get an **endorsement** (arxiv.org/help/endorsement
   — usually a colleague who has posted in that category; many are auto-endorsed
   after affiliation verification).
2. \<https://arxiv.org/submit\> → *Start New Submission*.
3. Upload the **source**, not a PDF: a `.zip`/`.tar.gz` of `main.tex` + `figs/`
   (include `refs.bib` too; harmless). arXiv runs LaTeX on its own TeX Live, so
   the PDF is regenerated — source upload is preferred and required for most cats.
4. Primary category **cs.LG**; cross-list **stat.ME**, **cs.AI**. (The LLM section
   makes cs.LG the natural primary.)
5. Title/abstract are in `main.tex`; paste the abstract into the metadata box.
6. License: pick CC BY 4.0 or arXiv's default non-exclusive — your call.
7. Preview the arXiv-built PDF, then *Submit*. It lands on the next announcement
   cycle (~1 business day).

## Before you submit (honest checklist)
- The manuscript is a **research report / preprint**, positioned as cross-domain
  synthesis + protocol, **not** new single-domain theory (see §9 Related work).
  That framing is deliberate; don't let a reader expect a new theorem.
- Author/affiliation: set your name and (if any) affiliation on the title page.
  No affiliation is fine for arXiv but slightly slows endorsement.
- Numbers are reproducible from the repo; the LLM Elo figures are real and cited
  to openlm.ai/chatbot-arena (June 2026) — keep the access date if a reviewer asks.
- If you'd rather not deal with endorsement, the same PDF works as-is for a
  personal site, OSF, Zenodo (gets a DOI), or a workshop submission.

## Files in this folder
- `main.tex` — self-contained manuscript (compiles alone).
- `refs.bib` — optional BibTeX (not needed; `main.tex` embeds its bibliography).
- `figs/` — the two figures referenced by the manuscript.
