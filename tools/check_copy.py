#!/usr/bin/env python3
"""Check that every sentence of COPY.md appears verbatim on the matching built page,
and that each page's <title> and meta description match COPY.md exactly."""
import html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = {"1": "", "2": "experience/", "3": "projects/", "4": "education/", "5": "about/", "6": "contact/"}


def norm(t):
    t = html.unescape(t)
    t = t.replace("“", '"').replace("”", '"').replace("’", "'")
    return re.sub(r"\s+", " ", t).strip()


def page_text(path):
    s = open(path, encoding="utf-8").read()
    title = re.search(r"<title>(.*?)</title>", s, re.S).group(1)
    desc = re.search(r'<meta name="description" content="(.*?)">', s, re.S).group(1)
    body = re.sub(r"(?s)<(script|style|title)\b.*?</\1>", " ", s)
    body = re.sub(r"(?s)<head>.*?</head>", " ", body)
    body = re.sub(r"</?(strong|em|span|a|abbr|b|i)\b[^>]*>", "", body)
    body = re.sub(r"<[^>]+>", " ", body)
    return norm(title), norm(desc), norm(body)


def strip_md(line):
    m = re.search(r"\(H2: \*?([^)*]+)\*?\)", line)
    if m:  # an annotated label line: the heading text is what appears on the page
        return m.group(1)
    line = re.sub(r"^\*\*(Closing call to action|Apelo final|Next step|Próximo passo)\*\*.*", "", line)
    line = re.sub(r"\[([^\]]+)\]\((https?://|mailto:)[^)]+\)", r"\1", line)        # md links
    line = re.sub(r"\[(Button|Botão|Link|Links|Expander|Expansor)[^\]]*\]", " ", line)  # directives
    line = re.sub(r"\*\((photo|foto)[^)]*\)\*", " ", line)
    line = re.sub(r"\((H2|H3|pull quote|tradução do original em inglês)[^)]*\):?", " ", line)
    line = line.replace("**", "").replace("`", "")
    line = re.sub(r"(?<!\w)\*(?!\s)|(?<!\s)\*(?!\w)", "", line)
    line = re.sub(r"^\s*(>|-|\d+\.)\s*", "", line)
    line = re.sub(r"^#+\s*", "", line)
    line = re.sub(r"^(H1|H2|Opening|Abertura|Subheading|Subtítulo|Location line|Localização|Summary|Resumo):\s*", "", line)
    return line


def pieces(line):
    # split into sentence-ish chunks; check each chunk that is long enough to matter
    parts = re.split(r"(?<=[.!?:;»”\"])\s+| · |→", line)
    return [p.strip(" ·→") for p in parts if len(p.strip(" ·→")) >= 12]


def main():
    copy = open(os.path.join(ROOT, "COPY.md"), encoding="utf-8").read()
    sections = re.split(r"\n## (\d)\. ", copy)
    failures = 0
    for i in range(1, len(sections), 2):
        num, sec = sections[i], sections[i + 1]
        for lang, block in re.findall(r"### (EN|PT)\n(.*?)(?=\n### |\n---|\Z)", sec, re.S):
            path = os.path.join(ROOT, ("pt/" if lang == "PT" else "") + SLUG[num], "index.html")
            title, desc, body = page_text(path)
            for line in block.splitlines():
                if not line.strip():
                    continue
                m = re.match(r"- \*\*Title tag:\*\* (.*)", line)
                if m:
                    if norm(m.group(1)) != title:
                        failures += 1; print(f"[{lang} {num}] TITLE mismatch: {title!r}")
                    continue
                m = re.match(r"- \*\*Meta description:\*\* (.*)", line)
                if m:
                    if norm(m.group(1)) != desc:
                        failures += 1; print(f"[{lang} {num}] DESC mismatch")
                    continue
                if line.startswith("[Link") or line.startswith("[Links"):
                    continue
                for p in pieces(norm(strip_md(line))):
                    if p not in body:
                        failures += 1; print(f"[{lang} {num}] missing: {p}")
    print("OK: all COPY.md text found" if not failures else f"{failures} problem(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
