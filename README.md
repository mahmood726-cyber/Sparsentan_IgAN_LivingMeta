# Sparsentan_IgAN_LivingMeta

A single-file, offline HTML living meta-analysis dashboard for **sparsentan in
IgA nephropathy (IgAN)**, built on the RapidMeta engine.

- Open `index.html` (it redirects to `SPARSENTAN_IGAN_REVIEW.html`).
- Runs entirely in the browser — no server or build step required.
- Statistics: random-effects pooling (DerSimonian-Laird, with a REML / Q-profile
  sensitivity card), heterogeneity (I², τ², Q-profile CI), GRADE, PRISMA flow,
  funnel/Egger, and optional WebR-based R validation.

Curated trial data and evidence cards live inline in the dashboard; the topic
config is in `configs/sparsentan_igan.json`. See `UPGRADE.md` for the engine
transplant history.

`test_smoke.py` checks the shipped HTML parses, that script tags are balanced,
that no template tokens are left unfilled, and that the config JSON is valid
(`pytest -q` or `python test_smoke.py`).
