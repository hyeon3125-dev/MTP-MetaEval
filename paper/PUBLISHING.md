# Publishing this preprint (the arXiv endorsement bottleneck, and the way around it)

## The bottleneck

arXiv requires a **new submitter** to be **endorsed** in the target category
(e.g. cs.LG) before a first submission. Endorsement normally comes from someone
who has already posted several papers in that category. With no academic affiliation
or endorser, the first arXiv submission is blocked. **Do not fake an arXiv badge —
there is no arXiv ID yet, so claiming one is dishonest and self-defeating.**

Good news: arXiv is *not* required to have a real, citable, DOI'd public preprint.

## Recommended: Zenodo (CERN-backed, no gatekeeper, mints a DOI)

Zenodo gives a permanent DOI with no endorsement and no moderation gate. A DOI is a
legitimate, citable identifier — the badge you *can* honestly display.

1. Compile the PDF: open `paper/` in Overleaf (Upload Project → drop the folder);
   it compiles as-is (self-contained `main.tex`). Download `main.pdf`.
2. Go to <https://zenodo.org>, log in (ORCID or email), *New upload*.
3. Upload `main.pdf` (and optionally the `paper/` source zip). Set:
   - Upload type: *Publication → Preprint* (or *Report*).
   - Title, authors (Seung-hyun Lee), description (paste the abstract).
   - Keywords: computational verification, optimal stopping, decision theory, …
   - License: CC BY 4.0 (recommended) or your choice.
4. *Publish* → you get a DOI like `10.5281/zenodo.XXXXXXX` immediately.
5. Put the DOI into `CITATION.cff` (uncomment the `doi:` line) and, if you want a
   badge, use Zenodo's DOI badge — that one is real.

### Even cleaner: GitHub release → Zenodo (automatic archive + DOI)
Enable the repo in Zenodo's GitHub integration, then cut a GitHub *release* (tag
`v0.1`). Zenodo auto-archives the repo and mints a DOI tied to the release. The
repo and the preprint then share one citable artifact.

## Other no-endorsement venues
- **OSF Preprints** (<https://osf.io/preprints>) — free, DOI, reputable.
- **preprints.org** (MDPI) — DOI, light moderation.
- **TechRxiv** (IEEE) — engineering preprints; check current eligibility.
- Avoid viXra (no credibility).

## If you specifically want arXiv later (parallel track)
- Get endorsed: email an author who has published in cs.LG/stat.ME asking for an
  endorsement (arXiv generates an endorsement code/link for you to share), or
  co-author with someone already endorsed. Many researchers endorse on a brief,
  polite request with the draft attached.
- Affiliation verification (a university/company email) can auto-grant endorsement
  in some categories.
- Once endorsed, follow the standard upload (source tarball, primary cs.LG,
  cross-list stat.ME/cs.AI). The Zenodo DOI can coexist; arXiv allows a DOI link.

## Zero-effort fallback
The repo is already citable: `CITATION.cff` gives GitHub a **"Cite this
repository"** button today, with no upload at all. The Zenodo DOI just upgrades
that to a permanent, venue-independent identifier.
