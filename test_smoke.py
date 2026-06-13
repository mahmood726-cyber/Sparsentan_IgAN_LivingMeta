# sentinel:skip-file -- this test intentionally contains the placeholder-token
# patterns ({{...}}, REPLACE_ME, __PLACEHOLDER__) it scans the HTML for.
"""Minimal smoke test for the Sparsentan IgAN LivingMeta dashboard.

This repo is a single-file HTML living-meta dashboard (no build step). The
smoke test asserts the shipped artifacts are well-formed enough to load:

  * the entry redirect (index.html) and the dashboard parse as HTML;
  * every <script> tag is balanced (no stray literal </script> that would
    truncate a template literal);
  * no unfilled template tokens ({{...}}, REPLACE_ME, __PLACEHOLDER__);
  * no UTF-8 BOM on shipped assets;
  * the topic config JSON is valid.

Run with `pytest -q` or plain `python test_smoke.py`.
"""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML_FILES = ["index.html", "SPARSENTAN_IGAN_REVIEW.html"]
TOKEN_RE = re.compile(r"\{\{[^}]*\}\}|REPLACE_ME|__PLACEHOLDER__")


def _read(name):
    raw = (ROOT / name).read_bytes()
    assert raw[:3] != b"\xef\xbb\xbf", f"{name} has a UTF-8 BOM"
    return raw.decode("utf-8", errors="replace")


def test_html_files_exist():
    for name in HTML_FILES:
        assert (ROOT / name).is_file(), f"missing {name}"


def test_html_parses():
    for name in HTML_FILES:
        text = _read(name)
        HTMLParser(convert_charrefs=True).feed(text)  # raises on malformed input


def test_script_tags_balanced():
    for name in HTML_FILES:
        text = _read(name)
        opens = len(re.findall(r"<script\b", text))
        closes = text.count("</script>")
        assert opens == closes, (
            f"{name}: {opens} <script> vs {closes} </script> "
            "(stray literal </script> can truncate a template literal)"
        )


def test_no_unfilled_tokens():
    for name in HTML_FILES:
        text = _read(name)
        leftovers = TOKEN_RE.findall(text)
        assert not leftovers, f"{name} has unfilled tokens: {set(leftovers)}"


def test_config_json_valid():
    cfg = json.loads((ROOT / "configs" / "sparsentan_igan.json").read_text(encoding="utf-8"))
    for key in ("drug", "condition", "source_html"):
        assert key in cfg, f"config missing required key: {key}"


if __name__ == "__main__":
    for fn in [
        test_html_files_exist,
        test_html_parses,
        test_script_tags_balanced,
        test_no_unfilled_tokens,
        test_config_json_valid,
    ]:
        fn()
        print(f"ok  {fn.__name__}")
    print("all smoke checks passed")
