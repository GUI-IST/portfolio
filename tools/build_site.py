#!/usr/bin/env python3
"""Build the static portfolio from COPY.md's text and DESIGN.md's components.

Usage:
  python3 tools/build_site.py              # writes the site into the repo root
  python3 tools/build_site.py --artifact DIR  # writes a copy for the claude.ai artifact host

All visible copy below is transcribed verbatim from COPY.md; tools/check_copy.py verifies it.
"""
import html, os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Production address. Change this one line when a custom domain is connected, then rebuild.
SITE = "https://portfolio-guicm.vercel.app"
EMAIL = "gcandeiasmarti@tudelft.nl"
LINKEDIN = "https://www.linkedin.com/in/guilherme-candeias-martins/"
SENTINEL = "https://sentinel-anti-drone.vercel.app/"

PAGES = ["home", "experience", "projects", "education", "about", "contact"]
SLUG = {"home": "", "experience": "experience/", "projects": "projects/", "education": "education/", "about": "about/", "contact": "contact/"}
NAV = {
    "en": {"home": "Home", "experience": "Experience", "projects": "Projects", "education": "Education & Skills", "about": "About", "contact": "Contact"},
    "pt": {"home": "Início", "experience": "Experiência", "projects": "Projetos", "education": "Formação e Competências", "about": "Sobre mim", "contact": "Contacto"},
}
EMAIL_BTN = {"en": "Email me", "pt": "Envie-me um email"}
MENU = {"en": "Menu", "pt": "Menu"}
SKIP = {"en": "Skip to content", "pt": "Saltar para o conteúdo"}
NAV_LABEL = {"en": "Main", "pt": "Principal"}
LANG_LABEL = {"en": "Language", "pt": "Idioma"}

e = html.escape
ARTIFACT = False

ICON_MAIL = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="1.5" y="3.5" width="13" height="9" rx="0"/><path d="M2 4l6 5 6-5"/></svg>'
ICON_EXT = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M4.5 2.5h5v5M9.5 2.5l-7 7"/></svg>'
ICON_ARROW = '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4"/></svg>'
ICON_DOWN = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M8 2v11M4 9l4 4 4-4"/></svg>'
ICON_CHEV = '<svg class="chev" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M3.5 6l4.5 4.5L12.5 6"/></svg>'


# ---------- helpers ----------
def rel(depth):
    return "../" * depth if depth else "./"


def page_path(lang, page):
    return ("pt/" if lang == "pt" else "") + SLUG[page]


def href(from_depth, lang, page):
    target = page_path(lang, page)
    if ARTIFACT:
        target += "index.html"
    out = rel(from_depth) + target
    return out if out != "./" else "./"


def ext(url, text=None):
    text = text if text is not None else url.replace("https://", "").replace("www.", "").rstrip("/")
    return f'<a class="ext" href="{e(url)}" target="_blank" rel="noopener">{e(text)}{ICON_EXT}</a>'


def email_btn(lang, compact=False):
    c = " compact" if compact else ""
    return f'<a class="btn btn-email{c}" href="mailto:{EMAIL}">{ICON_MAIL}{e(EMAIL_BTN[lang])}</a>'


def ghost(url, text, external=True):
    extra = ' target="_blank" rel="noopener"' if external else ""
    return f'<a class="btn btn-ghost" href="{e(url)}"{extra}>{e(text)}</a>'


LOGO_W = {"ist": 23, "it": 24, "aeist": 45, "golp": 90, "silicongate": 72}  # display width at 28px height


def logo(name, alt):
    return f'<span class="logo-tile"><img src="{{A}}img/logo-{name}.webp" alt="{e(alt)}" width="{LOGO_W[name]}" height="28" loading="lazy" decoding="async"></span>'


def page_head(lang, page, h1, opening):
    return f'''<header class="page-head"><div class="wrap">
  <p class="eyebrow label">{e(NAV[lang][page])}</p>
  <h1>{h1}</h1>
  <p class="lead">{opening}</p>
</div></header>'''


def next_block(lang, depth, h2, text, nxt=None):
    link = ""
    if nxt:
        label, page = nxt
        link = f'<a class="next-link label" href="{href(depth, lang, page)}">{e(label)} {ICON_ARROW}</a>'
    return f'''<section class="next reveal" aria-labelledby="next-h"><div class="wrap">
  <hr class="divider">
  <h2 id="next-h">{h2}</h2>
  <p class="lead">{text}</p>
  <div class="row"><div class="actions">{email_btn(lang)}</div>{link}</div>
</div></section>'''


def layout(lang, page, depth, title, desc, body):
    other = "pt" if lang == "en" else "en"
    A = rel(depth) + "assets/"
    nav = "".join(
        f'<a class="label" href="{href(depth, lang, p)}"{" aria-current=\"page\"" if p == page else ""}>{e(NAV[lang][p])}</a>' for p in PAGES)
    menu = "".join(
        f'<li><a href="{href(depth, lang, p)}"{" aria-current=\"page\"" if p == page else ""}>{e(NAV[lang][p])}</a></li>' for p in PAGES)

    def toggle(cls=""):
        en_cur = ' aria-current="true"' if lang == "en" else ""
        pt_cur = ' aria-current="true"' if lang == "pt" else ""
        return (f'<nav class="lang label {cls}" aria-label="{LANG_LABEL[lang]}">'
                f'<a href="{href(depth, "en", page)}" hreflang="en" lang="en"{en_cur}>EN</a><span class="sep" aria-hidden="true"></span>'
                f'<a href="{href(depth, "pt", page)}" hreflang="pt-PT" lang="pt-PT"{pt_cur}>PT</a></nav>')

    footer_line = f'© 2026 Guilherme Candeias Martins'
    def absu(l, pg):
        return SITE + "/" + page_path(l, pg)
    def alt(l, pg):
        return href(depth, l, pg) if ARTIFACT else absu(l, pg)
    og_img = SITE + ("/assets/img/og-pt.jpg" if lang == "pt" else "/assets/img/og-en.jpg")
    og_alt = "Guilherme Candeias Martins · " + ("MSc Electrical Engineering, TU Delft" if lang == "en" else "Mestrado em Engenharia Eletrotécnica, TU Delft")
    jsonld = ""
    if page == "home":
        import json
        jsonld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "Person",
            "name": "Guilherme Candeias Martins", "url": SITE + "/",
            "image": SITE + "/assets/img/profile.webp",
            "jobTitle": "Electrical and Computer Engineer",
            "email": "mailto:" + EMAIL,
            "address": {"@type": "PostalAddress", "addressLocality": "Delft", "addressCountry": "NL"},
            "affiliation": {"@type": "CollegeOrUniversity", "name": "Technische Universiteit Delft"},
            "alumniOf": {"@type": "CollegeOrUniversity", "name": "Instituto Superior Técnico"},
            "knowsLanguage": ["pt", "en", "es"],
            "sameAs": [LINKEDIN],
        }, ensure_ascii=False) + '</script>'
    head_meta = f'''<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{absu(lang, page)}">
<link rel="alternate" hreflang="en" href="{alt("en", page)}">
<link rel="alternate" hreflang="pt-PT" href="{alt("pt", page)}">
<link rel="alternate" hreflang="x-default" href="{alt("en", page)}">
<meta name="theme-color" content="#16100a">
<meta property="og:site_name" content="Guilherme Candeias Martins">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="{"profile" if page == "about" else "website"}">
<meta property="og:url" content="{absu(lang, page)}">
<meta property="og:locale" content="{"en_GB" if lang == "en" else "pt_PT"}">
<meta property="og:locale:alternate" content="{"pt_PT" if lang == "en" else "en_GB"}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="{A}img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{A}img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{A}img/apple-touch-icon.png">
<link rel="preload" href="{A}fonts/fraunces-latin-standard-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{A}fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{A}css/site.css">{jsonld}'''
    content = f'''<a class="skip-link" href="#main">{e(SKIP[lang])}</a>
<header class="site-header"><div class="wrap">
  <a class="wordmark" href="{href(depth, lang, "home")}"><span class="full">Guilherme Candeias Martins</span><span class="short">G. C. Martins</span></a>
  <nav class="nav-links" aria-label="{NAV_LABEL[lang]}">{nav}</nav>
  <div class="header-tools">{toggle()}{email_btn(lang, compact=True)}
    <button class="menu-btn label" type="button" aria-expanded="false" aria-controls="menu-panel">{MENU[lang]}</button>
  </div>
</div></header>
<div class="menu-panel" id="menu-panel" hidden><div class="wrap">
  <nav aria-label="{NAV_LABEL[lang]}"><ul>{menu}</ul></nav>
  <div class="actions">{email_btn(lang)}{toggle()}</div>
</div></div>
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="wrap">
  <div class="footer-grid">
    <span>{footer_line}</span>
    <span class="contacts"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></span>
    {toggle()}
  </div>
</div></footer>
<script src="{A}js/site.js" defer></script>'''
    content = content.replace("{A}", A)
    is_root_artifact = ARTIFACT and lang == "en" and page == "home"
    if is_root_artifact:
        # The artifact host wraps the root page in its own document skeleton.
        return head_meta + "\n" + content + "\n"
    return f'''<!doctype html>
<html lang="{"en" if lang == "en" else "pt-PT"}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head_meta}
</head>
<body>
{content}
</body>
</html>
'''


# ---------- pages ----------
def home(lang, depth):
    if lang == "en":
        title = "Guilherme Candeias Martins | Electrical Engineer, MSc TU Delft"
        desc = "Guilherme Candeias Martins, Electrical and Computer Engineer and MSc student in Microelectronics at TU Delft, with a year of semiconductor test experience. Open to 2027 internships and thesis projects."
        sub = "Electrical and Computer Engineer · MSc Electrical Engineering (Microelectronics, quantum themed), TU Delft"
        loc = "Based in Delft, the Netherlands · from Cascais, Portugal"
        opening = "I'm an electrical engineer doing an MSc in Microelectronics at TU Delft, on a quantum-themed track. Before Delft, I spent a year testing and characterizing power-management chips in a semiconductor lab in Lisbon. I'm interested in where hardware, physics and computation meet."
        h_seek = "What I'm looking for"
        seek = ["An industry internship and MSc thesis from summer 2027", "A part-time or student role alongside my MSc", "Research collaborations with academic groups"]
        h_hl = "Highlights"
        hl = [
            ("A year in semiconductor test.", "About 1,500 hours of hands-on lab work in the Test &amp; Laboratory team at SiliconGate and Celera Semiconductor: validating power-management IP, automating test setups and writing Python instrument drivers.", "See my experience", "experience"),
            ("A quantum-themed MSc at TU Delft.", "MSc in Electrical Engineering on the Microelectronics track, with courses such as Semiconductor Devices and Circuits for Quantum and Superconducting Quantum Sensors for Astronomy.", "See my education", "education"),
            ("Volunteering since 2021.", "Volunteer tutor to about 15 children, and a volunteer with Cascais Jovem at community events, a beach-safety campaign and national elections.", "More about me", "about"),
        ]
        h_cta = "Let's talk"
        cta = "If you have an internship, a thesis project, a student role or a research idea in microelectronics, semiconductor test or quantum hardware, I'd be glad to hear from you."
    else:
        title = "Guilherme Candeias Martins | Engenheiro Eletrotécnico, TU Delft"
        desc = "Guilherme Candeias Martins, engenheiro eletrotécnico e de computadores e estudante de mestrado em Microeletrónica na TU Delft, com um ano de experiência em teste de semicondutores. Disponível para estágios e teses em 2027."
        sub = "Engenheiro Eletrotécnico e de Computadores · Mestrado em Engenharia Eletrotécnica (Microeletrónica, vertente quântica), TU Delft"
        loc = "A viver em Delft, Países Baixos · natural de Cascais, Portugal"
        opening = "Sou engenheiro eletrotécnico e estou a fazer um mestrado em Microeletrónica na TU Delft, numa vertente dedicada à engenharia quântica. Antes de Delft, passei um ano a testar e caracterizar chips de gestão de energia num laboratório de semicondutores em Lisboa. Interessa-me o ponto onde o hardware, a física e a computação se encontram."
        h_seek = "O que procuro"
        seek = ["Um estágio na indústria e uma tese de mestrado a partir do verão de 2027", "Um trabalho a tempo parcial ou de estudante, em paralelo com o mestrado", "Colaborações de investigação com grupos académicos"]
        h_hl = "Destaques"
        hl = [
            ("Um ano em teste de semicondutores.", "Cerca de 1500 horas de trabalho prático em laboratório na equipa de Teste e Laboratório da SiliconGate e da Celera Semiconductor: validação de IP de gestão de energia, automação de montagens de teste e desenvolvimento de drivers de instrumentos em Python.", "Ver experiência", "experience"),
            ("Um mestrado com vertente quântica na TU Delft.", "Mestrado em Engenharia Eletrotécnica, especialização em Microeletrónica, com unidades curriculares como Semiconductor Devices and Circuits for Quantum e Superconducting Quantum Sensors for Astronomy.", "Ver formação", "education"),
            ("Voluntariado desde 2021.", "Explicador voluntário de cerca de 15 crianças e voluntário da Cascais Jovem em eventos comunitários, numa campanha de segurança nas praias e em eleições nacionais.", "Mais sobre mim", "about"),
        ]
        h_cta = "Vamos falar"
        cta = "Se tem um estágio, um tema de tese, uma vaga para estudante ou uma ideia de investigação em microeletrónica, teste de semicondutores ou hardware quântico, gostaria muito de saber."

    A = rel(depth) + "assets/"
    seek_li = "".join(f"<li>{e(s)}</li>" for s in seek)
    hl_li = "".join(
        f'<li><span class="num" aria-hidden="true">{i + 1:02d}</span><h3>{t}</h3><p>{b}</p>'
        f'<a class="arrow-link label" href="{href(depth, lang, p)}">{e(l)} {ICON_ARROW}</a></li>'
        for i, (t, b, l, p) in enumerate(hl))
    body = f'''<section class="hero" aria-labelledby="hero-h">
  <div class="hero-art"><img src="{A}img/almond-blossoms-1600.webp" srcset="{A}img/almond-blossoms-900.webp 900w, {A}img/almond-blossoms-1200.webp 1200w, {A}img/almond-blossoms-1600.webp 1600w" sizes="(max-width: 860px) 100vw, 58vw" alt="" width="1600" height="1309" fetchpriority="high"></div>
  <div class="wrap"><div class="hero-copy">
    <h1 id="hero-h"><span class="line">Guilherme</span> <span class="line"><em>Candeias</em> Martins</span></h1>
    <p class="sub">{e(sub)}</p>
    <p class="loc meta">{e(loc)}</p>
    <p class="opening">{e(opening)}</p>
  </div></div>
  <a class="scroll-cue" href="#seeking" aria-label="{e(h_seek)}">{ICON_DOWN}</a>
</section>
<section class="section" id="seeking" aria-labelledby="seek-h"><div class="wrap seeking">
  <div class="reveal">
    <div class="section-head"><h2 id="seek-h">{e(h_seek)}</h2></div>
    <ul class="seeking-list">{seek_li}</ul>
    <div class="actions">{email_btn(lang)}{ghost(LINKEDIN, "LinkedIn")}</div>
  </div>
  <figure class="portrait reveal"><img src="{A}img/profile.webp" srcset="{A}img/profile-480.webp 480w, {A}img/profile.webp 800w" sizes="(max-width: 859px) min(420px, 92vw), 360px" alt="Guilherme Candeias Martins" width="800" height="1000" loading="lazy" decoding="async"></figure>
</div></section>
<section class="section band" aria-labelledby="hl-h"><div class="wrap">
  <div class="section-head"><h2 id="hl-h">{e(h_hl)}</h2></div>
  <ol class="highlights reveal">{hl_li}</ol>
</div></section>
{next_block(lang, depth, e(h_cta), e(cta))}'''
    return title, desc, body


def experience(lang, depth):
    A = rel(depth) + "assets/"
    if lang == "en":
        title = "Semiconductor Test & Quantum Research | Guilherme Martins"
        desc = "A year as a semiconductor test engineer intern characterizing power-management ICs, writing PyVISA instrument drivers, plus research on quantum simulation of Maxwell's equations."
        h1 = "Experience in semiconductor test and quantum research"
        opening = "I spent a year as a semiconductor test engineer intern, characterizing power-management ICs and automating lab instruments in Python. I also did research on the quantum simulation of Maxwell&#x27;s equations."
        t1 = "Test Engineer Intern, Test &amp; Laboratory team"
        rail1 = ["Aug 2025 – Jul 2026", "Lisbon, Portugal", "Full time"]
        org1 = "SiliconGate → Celera Semiconductor"
        note1 = "Celera Semiconductor bought SiliconGate. I was at SiliconGate from Aug 2025 to Jun 2026 and continued with the same team under Celera Semiconductor from Jun to Jul 2026."
        sum_label = "Summary:"
        sum1 = "I validated and characterized power-management semiconductor IP on silicon. I built and automated test setups, made hardware measurements, soldered and assembled circuits, and wrote code to control and analyze the test systems."
        more = "Show full technical detail"
        detail = [
            "About 1,500 hours of hands-on lab work.",
            "Characterization of power-management IP: startup sequencing, line transients, AC and DC measurements, and temperature-dependent tests with a thermal stream system.",
            "Powering fragile engineering samples safely: sequencing supplies to each block of the IC through relays and programmable sources, sourcing and measuring with Keithley SourceMeter units.",
            "Trimming on-chip clock, temperature, voltage and current settings through JTAG/IJTAG, and controlling electronic and programmable loads during measurements.",
            "<strong>Python instrument drivers:</strong> I wrote drivers for two arbitrary waveform generators, working from their programming manuals (SCPI over GPIB with PyVISA). They handle binary waveform upload, multi-segment sequences with trigger and marker logic, hardware limit checks and input validation, and include a GUI instrument panel. Both drivers are integrated into the company&#x27;s automated test framework.",
            "Adapting the team&#x27;s existing Python processing and plotting code (pandas, Matplotlib) to each new instrument and sample, so results stayed organized and consistent.",
            "Hand-soldering and assembling test circuits, including small SMD components under a microscope.",
            "Git used daily for all driver and test code.",
            "<strong>Equipment:</strong> Keithley SourceMeters (SMU), LCR meter, laboratory power amplifiers, oscilloscopes and current probes, arbitrary waveform and function generators, frequency counter, signal source analyzer, programmable DC power supplies, electronic and programmable loads, battery chargers, relays, JTAG/IJTAG, thermal stream system.",
        ]
        q_kicker = "Recommendation"
        quotes = ["“[…] Guilherme quickly integrated into the team and took an active role in hands-on development tasks. He learned the automated characterization test flow, contributed to the development of Python test scripts, and carried out PCB device soldering with care and precision.”",
                  "“What stands out most in Guilherme is his eagerness to learn and his resilience when confronted with technical difficulties. He does not stop at the first obstacle; instead, he seeks solutions with determination and intellectual curiosity […]”"]
        q_who = "Marcelino Santos"
        q_role = "Full Professor, IST – Universidade de Lisboa · former CTO and co-founder, SiliconGate"
        roles = [
            ("golp", "GOLP", "Research Intern, GOLP (Group for Lasers and Plasmas), IPFN", ["Sep 2025 – Mar 2026"], "Instituto Superior Técnico, University of Lisbon",
             "I researched the quantum simulation of Maxwell&#x27;s equations, where quantum physics meets electromagnetism. The work deepened my understanding of Hamiltonian mechanics, quantum systems and numerical modeling, and of how fundamental physics can be simulated and studied.", None),
            ("it", "Instituto de Telecomunicações", "Quantum and Photonics Department, Instituto de Telecomunicações", ["Feb 2025 – Jul 2025"], "Instituto Superior Técnico, University of Lisbon",
             "I attended the department&#x27;s weekly meetings, following 8 research projects and taking notes on their progress. It taught me how quantum and photonics technologies are applied in real projects and theses.", None),
            ("aeist", "AEIST", "Business Relations Collaborator, Students&#x27; Association of IST (AEIST)", ["Oct 2024 – Sep 2025", "Lisbon"], None,
             "I built relationships with external organizations and secured funding and sponsorships for the association&#x27;s activities.", "Skills: partnership development, communication, project management, sales negotiation."),
        ]
        nx = ("Need someone in your lab?", "I&#x27;m looking for an industry internship and MSc thesis from summer 2027, a part-time role alongside my studies, or a research collaboration.", ("Next: Projects", "projects"))
    else:
        title = "Experiência em Teste de Semicondutores | Guilherme Martins"
        desc = "Um ano como estagiário de engenharia de testes de semicondutores, a caracterizar circuitos integrados de gestão de energia e a desenvolver drivers PyVISA, e investigação em simulação quântica das equações de Maxwell."
        h1 = "Experiência em teste de semicondutores e investigação quântica"
        opening = "Passei um ano como estagiário de engenharia de testes de semicondutores, a caracterizar circuitos integrados de gestão de energia e a automatizar instrumentos de laboratório em Python. Fiz também investigação em simulação quântica das equações de Maxwell."
        t1 = "Estagiário de Engenharia de Testes, equipa de Teste e Laboratório"
        rail1 = ["ago. 2025 – jul. 2026", "Lisboa, Portugal", "Tempo inteiro"]
        org1 = "SiliconGate → Celera Semiconductor"
        note1 = "A Celera Semiconductor comprou a SiliconGate. Estive na SiliconGate de agosto de 2025 a junho de 2026 e continuei na mesma equipa, já como Celera Semiconductor, de junho a julho de 2026."
        sum_label = "Resumo:"
        sum1 = "Validei e caracterizei IP de semicondutores para gestão de energia em silício. Montei e automatizei bancadas de teste, fiz medições de hardware, soldei e montei circuitos, e escrevi código para controlar e analisar os sistemas de teste."
        more = "Ver detalhe técnico"
        detail = [
            "Cerca de 1500 horas de trabalho prático em laboratório.",
            "Caracterização de IP de gestão de energia: sequências de arranque, transitórios de linha, medições AC e DC e testes em temperatura com um sistema de thermal stream.",
            "Alimentação segura de amostras de engenharia frágeis: sequenciação das alimentações de cada bloco do circuito integrado através de relés e fontes programáveis, com fontes de medida Keithley SourceMeter.",
            "Ajuste (trimming) de parâmetros internos do chip (relógio, temperatura, tensão e corrente) por JTAG/IJTAG e controlo de cargas eletrónicas e programáveis durante as medições.",
            "<strong>Drivers de instrumentos em Python:</strong> desenvolvi drivers para dois geradores de formas de onda arbitrárias a partir dos respetivos manuais de programação (SCPI sobre GPIB com PyVISA). Os drivers tratam do carregamento binário de formas de onda, de sequências multissegmento com lógica de trigger e marcadores, da verificação de limites de hardware e da validação de entradas, e incluem um painel gráfico do instrumento. Ambos estão integrados na framework de testes automáticos da empresa.",
            "Adaptação do código Python da equipa para processamento e visualização de dados (pandas, Matplotlib) a cada novo instrumento e amostra, mantendo os resultados organizados e consistentes.",
            "Soldadura manual e montagem de circuitos de teste, incluindo pequenos componentes SMD ao microscópio.",
            "Git usado diariamente em todo o código de drivers e testes.",
            "<strong>Equipamento:</strong> Keithley SourceMeters (SMU), medidor LCR, amplificadores de potência de laboratório, osciloscópios e pontas de corrente, geradores de formas de onda arbitrárias e de funções, frequencímetro, analisador de fontes de sinal, fontes DC programáveis, cargas eletrónicas e programáveis, carregadores de baterias, relés, JTAG/IJTAG, sistema de thermal stream.",
        ]
        q_kicker = "Recomendação (tradução do original em inglês)"
        quotes = ["«[…] O Guilherme integrou-se rapidamente na equipa e teve um papel ativo em tarefas práticas de desenvolvimento. Aprendeu o fluxo automático de testes de caracterização, contribuiu para o desenvolvimento de scripts de teste em Python e soldou dispositivos em PCB com cuidado e precisão.»",
                  "«O que mais se destaca no Guilherme é a sua vontade de aprender e a sua resiliência perante dificuldades técnicas. Não para no primeiro obstáculo; em vez disso, procura soluções com determinação e curiosidade intelectual […]»"]
        q_who = "Marcelino Santos"
        q_role = "Professor Catedrático, IST – Universidade de Lisboa · antigo CTO e cofundador da SiliconGate"
        roles = [
            ("golp", "GOLP", "Estagiário de Investigação, GOLP (Grupo de Lasers e Plasmas), IPFN", ["set. 2025 – mar. 2026"], "Instituto Superior Técnico, Universidade de Lisboa",
             "Investiguei a simulação quântica das equações de Maxwell, onde a física quântica se cruza com o eletromagnetismo. Aprofundei os meus conhecimentos de mecânica hamiltoniana, sistemas quânticos e modelação numérica, e de como a física fundamental pode ser simulada e estudada.", None),
            ("it", "Instituto de Telecomunicações", "Departamento de Quântica e Fotónica, Instituto de Telecomunicações", ["fev. 2025 – jul. 2025"], "Instituto Superior Técnico, Universidade de Lisboa",
             "Participei nas reuniões semanais do departamento, acompanhando 8 projetos de investigação e registando a sua evolução. Aprendi como as tecnologias quânticas e fotónicas são aplicadas em projetos e teses reais.", None),
            ("aeist", "AEIST", "Colaborador para Relações Empresariais, Associação de Estudantes do IST (AEIST)", ["out. 2024 – set. 2025", "Lisboa"], None,
             "Criei e mantive relações com organizações externas e angariei financiamento e patrocínios para as atividades da associação.", "Competências: desenvolvimento de parcerias, comunicação, gestão de projetos, negociação comercial."),
        ]
        nx = ("Precisa de alguém no seu laboratório?", "Procuro um estágio na indústria e uma tese de mestrado a partir do verão de 2027, um trabalho a tempo parcial em paralelo com o mestrado, ou uma colaboração de investigação.", ("A seguir: Projetos", "projects"))

    detail_li = "".join(f"<li>{d}</li>" for d in detail)
    rail = lambda items: "".join(f'<span class="{"when" if i == 0 else ""}">{e(x)}</span>' for i, x in enumerate(items))
    q = "".join(f"<p>{e(x)}</p>" for x in quotes)
    other_roles = ""
    for key, alt, t, r, org, text, note in roles:
        org_html = f'<p class="org">{e(org)}</p>' if org else ""
        note_html = f'<p class="note">{e(note)}</p>' if note else ""
        other_roles += f'''<hr class="divider">
<article class="entry reveal">
  <div class="entry-rail">{rail(r)}</div>
  <div class="entry-body">
    <div class="entry-title">{logo(key, alt).replace("{A}", A)}<h2>{t}</h2></div>
    {org_html}<p>{text}</p>{note_html}
  </div>
</article>'''
    body = f'''{page_head(lang, "experience", e(h1), opening)}
<section class="section" style="padding-top:0"><div class="wrap entries">
<hr class="divider">
<article class="entry reveal">
  <div class="entry-rail">{rail(rail1)}</div>
  <div class="entry-body">
    <div class="entry-title">{logo("silicongate", "SiliconGate").replace("{A}", A)}<h2>{t1}</h2></div>
    <p class="org"><strong>{e(org1)}</strong></p>
    <p class="note">{e(note1)}</p>
    <p><span class="sr-only">{e(sum_label)} </span>{e(sum1)}</p>
    <details class="more">
      <summary class="btn btn-ghost">{e(more)} {ICON_CHEV}</summary>
      <div class="panel"><ul class="dots">{detail_li}</ul></div>
    </details>
    <figure class="quote">
      <p class="quote-kicker label">{e(q_kicker)}</p>
      <blockquote>{q}</blockquote>
      <figcaption class="meta"><strong class="who">{e(q_who)}</strong>, {e(q_role)}</figcaption>
    </figure>
  </div>
</article>
{other_roles}
</div></section>
{next_block(lang, depth, e(nx[0]), nx[1], nx[2])}'''
    return title, desc, body


def projects(lang, depth):
    if lang == "en":
        title = "Sentinel Anti-Drone Detection System | Guilherme Martins"
        desc = "Sentinel, a machine-learning anti-drone detection system built with the Portuguese Air Force, Thales and Mauser, plus my scholarships and awards."
        h1 = "Projects: Sentinel, an anti-drone detection system"
        opening = "For my final-year project at Instituto Superior Técnico, I was project manager of Sentinel, a six-person team that built an anti-drone detection system using machine learning. We worked with the Portuguese Air Force, Thales and Mauser."
        h2 = "Sentinel: anti-drone detection for communication jamming"
        rail = ["Dec 2024 – Jul 2025", "Lisbon", "BSc final-year project, Instituto Superior Técnico"]
        role = 'Role: <strong>Project Manager</strong>, team of six'
        problem = ("The problem.", "Drones are increasingly used for illicit activities, such as entering restricted airspace and carrying out unauthorized surveillance. Security forces need a reliable way to detect them and raise the alarm.")
        built = ("What we built.", "A camera-based system that watches the airspace and detects drones in real time using computer vision and machine learning. It tells drones apart from other objects, such as birds, and keeps tracking a drone once it&#x27;s found. This keeps a directional jammer or antenna aimed for possible neutralization. A web app shows the system&#x27;s status and sends instant alerts with a photo and a timestamp.")
        h_how = "How it works"
        how = ["Detection model: YOLO v11, first trained on about 10,000 images and then refined to separate drones from other flying objects.",
               "Hardware: built with components including a Raspberry Pi 5, with servo motors that control the camera&#x27;s orientation so it can follow a target.",
               "Prototype: full system integration reached in May 2025; the complete prototype was assembled and fabricated through metalwork and cutting by June 2025."]
        h_role = "My role"
        myrole = "As project manager, I coordinated the project, managed the team and led our work with the partners. I organized the meetings and agendas documented on the project site, including a meeting at the Portuguese Air Force&#x27;s facilities in June 2025. I also produced the project&#x27;s presentations and explanatory video."
        partners_label = "Partners:"
        partners = ["Portuguese Air Force", "Thales", "Mauser", "Instituto Superior Técnico"]
        h_proof = "Proof"
        proof = [f'Project website, with the team, schedule and live data: {ext(SENTINEL, "sentinel-anti-drone.vercel.app")}',
                 "Explanatory video (YouTube, embedded on the project site)",
                 "Project proposal, midterm pitch deck and final pitch deck (on the project site)",
                 "14 weekly progress posts, February to June 2025 (project blog)"]
        h_aw = "Scholarships and awards"
        awards = [("IST Academic Merit Diploma:", "2022/2023"), ("BONDALTI &amp; Fundação Amélia de Mello Scholarship:", "2023/2024 and 2024/2025"),
                  ("Santander Scholarship (Técnico Santander):", "2022/2023"), ("School Merit Scholarship, Alcabideche Parish:", "2022"),
                  ("School Merit Award, Cascais Municipal Council:", "2022")]
        nx = ("Working on something similar?", "If your team works on detection, embedded systems or hardware projects with real partners, I&#x27;d like to hear about it.", ("Next: Education & Skills", "education"))
    else:
        title = "Sentinel: Sistema Anti-Drone | Guilherme Candeias Martins"
        desc = "Sentinel, um sistema de deteção de drones com machine learning desenvolvido com a Força Aérea Portuguesa, a Thales e a Mauser, e as minhas bolsas e prémios."
        h1 = "Projetos: Sentinel, um sistema anti-drone"
        opening = "No meu projeto final de licenciatura no Instituto Superior Técnico, fui gestor de projeto do Sentinel, uma equipa de seis pessoas que desenvolveu um sistema de deteção de drones com machine learning. Trabalhámos com a Força Aérea Portuguesa, a Thales e a Mauser."
        h2 = "Sentinel: deteção de drones para sistemas de interferência de comunicações"
        rail = ["dez. 2024 – jul. 2025", "Lisboa", "Projeto final de licenciatura, Instituto Superior Técnico"]
        role = 'Função: <strong>Gestor de Projeto</strong>, equipa de seis'
        problem = ("O problema.", "Os drones são cada vez mais usados em atividades ilícitas, como a entrada em espaço aéreo restrito e a vigilância não autorizada. As forças de segurança precisam de uma forma fiável de os detetar e dar o alerta.")
        built = ("O que construímos.", "Um sistema com câmaras que vigia o espaço aéreo e deteta drones em tempo real com visão computacional e machine learning. Distingue drones de outros objetos, como aves, e continua a seguir o drone depois de o detetar. Assim, um jammer ou antena direcional mantém-se apontado para uma possível neutralização. Uma aplicação web mostra o estado do sistema e envia alertas imediatos com fotografia e hora.")
        h_how = "Como funciona"
        how = ["Modelo de deteção: YOLO v11, treinado inicialmente com cerca de 10 000 imagens e depois afinado para distinguir drones de outros objetos voadores.",
               "Hardware: construído com componentes que incluem um Raspberry Pi 5, com servomotores que controlam a orientação da câmara para seguir o alvo.",
               "Protótipo: integração completa do sistema em maio de 2025; o protótipo final foi montado e fabricado com trabalho de serralharia e corte até junho de 2025."]
        h_role = "O meu papel"
        myrole = "Como gestor de projeto, coordenei o projeto, geri a equipa e liderei o trabalho com os parceiros. Organizei as reuniões e agendas documentadas no site do projeto, incluindo uma reunião nas instalações da Força Aérea Portuguesa em junho de 2025. Produzi também as apresentações e o vídeo explicativo do projeto."
        partners_label = "Parceiros:"
        partners = ["Força Aérea Portuguesa", "Thales", "Mauser", "Instituto Superior Técnico"]
        h_proof = "Provas"
        proof = [f'Site do projeto, com a equipa, o cronograma e dados ao vivo: {ext(SENTINEL, "sentinel-anti-drone.vercel.app")}',
                 "Vídeo explicativo (YouTube, incorporado no site do projeto)",
                 "Proposta de projeto, pitch deck intercalar e pitch deck final (no site do projeto)",
                 "14 publicações semanais de progresso, de fevereiro a junho de 2025 (blog do projeto)"]
        h_aw = "Bolsas e prémios"
        awards = [("Diploma de Mérito Académico do IST:", "2022/2023"), ("Bolsa BONDALTI &amp; Fundação Amélia de Mello:", "2023/2024 e 2024/2025"),
                  ("Bolsa Santander (Técnico Santander):", "2022/2023"), ("Bolsa de Mérito Escolar, Junta de Freguesia de Alcabideche:", "2022"),
                  ("Prémio de Mérito Escolar, Câmara Municipal de Cascais:", "2022")]
        nx = ("Está a trabalhar em algo parecido?", "Se a sua equipa trabalha em sistemas de deteção, sistemas embebidos ou projetos de hardware com parceiros reais, gostaria de saber mais.", ("A seguir: Formação e Competências", "education"))

    how_li = "".join(f"<li>{x}</li>" for x in how)
    proof_li = "".join(f"<li>{x}</li>" for x in proof)
    tags = "".join(f'<span class="tag">{e(p)}</span>' for p in partners)
    aw_li = "".join(f'<li><strong>{a}</strong><span class="year">{y}</span></li>' for a, y in awards)
    rail_html = "".join(f'<span class="{"when" if i == 0 else ""}">{e(x)}</span>' for i, x in enumerate(rail))
    body = f'''{page_head(lang, "projects", e(h1).replace("anti-drone", '<span class="nw">anti-drone</span>'), e(opening))}
<section class="section" style="padding-top:0"><div class="wrap entries">
<hr class="divider">
<article class="entry reveal">
  <div class="entry-rail">{rail_html}<span>{role}</span></div>
  <div class="entry-body sentinel">
    <div class="entry-title"><h2>{e(h2)}</h2></div>
    <div class="prose">
      <p><strong>{e(problem[0])}</strong> {e(problem[1])}</p>
      <p><strong>{e(built[0])}</strong> {built[1]}</p>
    </div>
    <div class="two-col">
      <div><h3 class="sub-h">{e(h_how)}</h3><ul class="dots">{how_li}</ul></div>
      <div><h3 class="sub-h">{e(h_role)}</h3><p>{myrole}</p></div>
    </div>
    <div class="partners"><span class="label" style="color:var(--color-sage)">{e(partners_label)}</span> {tags}</div>
    <div><h3 class="sub-h">{e(h_proof)}</h3><ul class="links">{proof_li}</ul></div>
  </div>
</article>
<hr class="divider">
<article class="entry reveal">
  <div class="entry-rail"></div>
  <div class="entry-body">
    <div class="entry-title"><h2>{e(h_aw)}</h2></div>
    <ul class="awards">{aw_li}</ul>
  </div>
</article>
</div></section>
{next_block(lang, depth, e(nx[0]), nx[1], nx[2])}'''
    return title, desc, body


def education(lang, depth):
    A = rel(depth) + "assets/"
    TUD = "https://www.tudelft.nl/onderwijs/opleidingen/masters/ee/msc-electrical-engineering"
    IST = "https://tecnico.ulisboa.pt/en/education/courses/undergraduate-programmes/electrical-and-computer-engineering/"
    if lang == "en":
        title = "Education: TU Delft MSc & IST ECE | Guilherme Martins"
        desc = "MSc Electrical Engineering student (Microelectronics, quantum themed) at TU Delft and Instituto Superior Técnico electrical and computer engineering graduate. Skills: Python, PyVISA, Cadence Virtuoso, Qiskit."
        h1 = "Education and skills"
        opening = "I'm an MSc Electrical Engineering student at TU Delft, on the Microelectronics track with a quantum theme. I graduated in Electrical and Computer Engineering from Instituto Superior Técnico. My skills run from Python lab automation with PyVISA to Cadence Virtuoso and Qiskit."
        tud_h = "Technische Universiteit Delft (TU Delft)"
        tud_rail = ["Aug 2026 – present", "Delft, the Netherlands"]
        tud_deg = "<strong>MSc Electrical Engineering</strong>, Microelectronics track, quantum themed"
        tud_c = "Example courses: Electronic Device Fundamentals, Semiconductor Devices and Circuits for Quantum, Advanced Semiconductor Devices, Microfabrication Fundamentals, Fundamentals of Photonic Integrated Circuits, Superconducting Quantum Sensors for Astronomy."
        tud_n = "The programme's final year is built around industry experience."
        prog = "Programme details"
        ist_h = "Instituto Superior Técnico (IST), University of Lisbon"
        ist_rail = ["Sep 2022 – Jul 2025", "Lisbon, Portugal"]
        ist_deg = "<strong>BSc Electrical and Computer Engineering</strong> · <strong>Final grade 16/20</strong>"
        ist_li = ["<strong>Microelectronics: 18/20</strong>, among the top 10 of 110 students",
                  "Relevant courses: Microelectronics, Circuit Analysis, Propagation and Radiation of Electromagnetic Waves, Telecommunications, Computer Architecture, Algorithms and Data Structures"]
        sch_h = "School"
        schools = [("2019 – 2022", "<strong>São João do Estoril High School (Liceu São João do Estoril)</strong>, Cascais", "Class Representative and Honor Student · Average grade 19/20"),
                   ("before 2019", "<strong>Amor de Deus School</strong>, Cascais", "Honor Student")]
        sk_h = "Skills"
        skills = [("Programming:", "Python (pandas, Matplotlib, PyVISA), C, C++, Java, Assembly, MATLAB, Qiskit"),
                  ("Tools:", "Git, Cadence Virtuoso (Spectre), LaTeX (Overleaf), Excel"),
                  ("Lab:", "SMUs, LCR meter, oscilloscopes, waveform generators, programmable supplies and loads, JTAG/IJTAG, thermal stream, soldering and microscope work"),
                  ("Engineering foundations:", "Microelectronics, Propagation and Radiation of Electromagnetic Waves, Telecommunications, Circuit Analysis, Computer Architecture, Algorithms and Data Structures, Differential and Integral Calculus, Linear Algebra"),
                  ("Soft skills:", "Leadership, communication, conflict resolution, teamwork, proactivity, analytical thinking, adaptability and flexibility, problem solving, learning agility")]
        lg_h = "Languages"
        langs = "Portuguese: native · English: proficient (C1) · Spanish: fluent"
        nx = ("Thesis or internship in 2027?", "My MSc's final year is built around industry experience. From summer 2027, I'm looking for an industry internship and a thesis project in microelectronics, semiconductor test or quantum hardware.", ("Next: About", "about"))
    else:
        title = "Formação: Mestrado TU Delft e IST | Guilherme Martins"
        desc = "Estudante de mestrado em Engenharia Eletrotécnica (Microeletrónica, vertente quântica) na TU Delft e licenciado em Engenharia Eletrotécnica e de Computadores pelo IST. Competências: Python, PyVISA, Cadence Virtuoso, Qiskit."
        h1 = "Formação e competências"
        opening = "Estou a fazer o mestrado em Engenharia Eletrotécnica na TU Delft, na especialização em Microeletrónica com vertente quântica. Sou licenciado em Engenharia Eletrotécnica e de Computadores pelo Instituto Superior Técnico. As minhas competências vão da automação de laboratório em Python com PyVISA ao Cadence Virtuoso e ao Qiskit."
        tud_h = "Technische Universiteit Delft (TU Delft)"
        tud_rail = ["ago. 2026 – presente", "Delft, Países Baixos"]
        tud_deg = "<strong>Mestrado em Engenharia Eletrotécnica</strong>, especialização em Microeletrónica, vertente quântica"
        tud_c = "Exemplos de unidades curriculares: Electronic Device Fundamentals, Semiconductor Devices and Circuits for Quantum, Advanced Semiconductor Devices, Microfabrication Fundamentals, Fundamentals of Photonic Integrated Circuits, Superconducting Quantum Sensors for Astronomy."
        tud_n = "O último ano do mestrado está organizado em torno da experiência na indústria."
        prog = "Detalhes do curso"
        ist_h = "Instituto Superior Técnico (IST), Universidade de Lisboa"
        ist_rail = ["set. 2022 – jul. 2025", "Lisboa, Portugal"]
        ist_deg = "<strong>Licenciatura em Engenharia Eletrotécnica e de Computadores</strong> · <strong>Média final 16/20</strong>"
        ist_li = ["<strong>Microeletrónica: 18/20</strong>, entre os 10 melhores de 110 alunos",
                  "Unidades curriculares relevantes: Microeletrónica, Análise de Circuitos, Propagação e Radiação de Ondas Eletromagnéticas, Telecomunicações, Arquitetura de Computadores, Algoritmos e Estruturas de Dados"]
        sch_h = "Escola"
        schools = [("2019 – 2022", "<strong>Liceu São João do Estoril</strong>, Cascais", "Delegado de turma e Aluno de Honra · Média 19/20"),
                   ("antes de 2019", "<strong>Colégio Amor de Deus</strong>, Cascais", "Aluno de Honra")]
        sk_h = "Competências"
        skills = [("Programação:", "Python (pandas, Matplotlib, PyVISA), C, C++, Java, Assembly, MATLAB, Qiskit"),
                  ("Ferramentas:", "Git, Cadence Virtuoso (Spectre), LaTeX (Overleaf), Excel"),
                  ("Laboratório:", "SMU, medidor LCR, osciloscópios, geradores de formas de onda, fontes e cargas programáveis, JTAG/IJTAG, thermal stream, soldadura e trabalho ao microscópio"),
                  ("Bases de engenharia:", "Microeletrónica, Propagação e Radiação de Ondas Eletromagnéticas, Telecomunicações, Análise de Circuitos, Arquitetura de Computadores, Algoritmos e Estruturas de Dados, Cálculo Diferencial e Integral, Álgebra Linear"),
                  ("Competências pessoais:", "Liderança, comunicação, resolução de conflitos, trabalho em equipa, proatividade, pensamento analítico, adaptabilidade e flexibilidade, resolução de problemas, rapidez de aprendizagem")]
        lg_h = "Línguas"
        langs = "Português: nativo · Inglês: proficiente (C1) · Espanhol: fluente"
        nx = ("Tese ou estágio em 2027?", "O último ano do meu mestrado está organizado em torno da experiência na indústria. A partir do verão de 2027, procuro um estágio e um tema de tese em microeletrónica, teste de semicondutores ou hardware quântico.", ("A seguir: Sobre mim", "about"))

    rail = lambda items: "".join(f'<span class="{"when" if i == 0 else ""}">{e(x)}</span>' for i, x in enumerate(items))
    ist_ul = "".join(f"<li>{x}</li>" for x in ist_li)
    sch = "".join(f'<div><dt>{e(y)}</dt><dd>{n}<br><span class="meta">{e(d)}</span></dd></div>' for y, n, d in schools)
    sk = "".join(f'<div><dt class="label">{e(k.rstrip(":"))}<span class="sr-only">:</span></dt><dd>{e(v)}</dd></div>' for k, v in skills)
    body = f'''{page_head(lang, "education", e(h1), e(opening))}
<section class="section" style="padding-top:0"><div class="wrap entries">
<hr class="divider">
<article class="entry reveal">
  <div class="entry-rail">{rail(tud_rail)}</div>
  <div class="entry-body">
    <div class="entry-title"><h2>{e(tud_h)}</h2></div>
    <p>{tud_deg}</p>
    <p>{e(tud_c)}</p>
    <p class="note">{e(tud_n)}</p>
    <p>{ext(TUD, prog)}</p>
  </div>
</article>
<hr class="divider">
<article class="entry reveal">
  <div class="entry-rail">{rail(ist_rail)}</div>
  <div class="entry-body">
    <div class="entry-title">{logo("ist", "Instituto Superior Técnico").replace("{A}", A)}<h2>{e(ist_h)}</h2></div>
    <p>{ist_deg}</p>
    <ul class="dots">{ist_ul}</ul>
    <p>{ext(IST, prog)}</p>
  </div>
</article>
<hr class="divider">
<article class="entry reveal">
  <div class="entry-rail"></div>
  <div class="entry-body">
    <div class="entry-title small"><h2>{e(sch_h)}</h2></div>
    <dl class="facts">{sch}</dl>
  </div>
</article>
<hr class="divider">
<article class="entry reveal">
  <div class="entry-rail"></div>
  <div class="entry-body">
    <div class="entry-title small"><h2>{e(sk_h)}</h2></div>
    <dl class="facts">{sk}</dl>
  </div>
</article>
<hr class="divider">
<article class="entry reveal">
  <div class="entry-rail"></div>
  <div class="entry-body">
    <div class="entry-title small"><h2>{e(lg_h)}</h2></div>
    <p class="lead" style="max-width:none">{e(langs)}</p>
  </div>
</article>
</div></section>
{next_block(lang, depth, e(nx[0]), e(nx[1]), nx[2])}'''
    return title, desc, body


def about(lang, depth):
    A = rel(depth) + "assets/"
    if lang == "en":
        title = "About Guilherme Candeias Martins: Volunteering & Erasmus+"
        desc = "About Guilherme Candeias Martins, an engineer from Cascais: volunteer tutor, Cascais Jovem volunteer, three Erasmus+ youth exchanges, band guitarist and traveller to 18 countries."
        h1 = "About me"
        opening = "I'm Guilherme Candeias Martins, a 22-year-old engineer from Cascais, Portugal, now living in Delft. Away from the lab, I've spent years volunteering in Cascais and taken part in three Erasmus+ youth exchanges. I play guitar in my own band."
        drives_h = "What drives me"
        drives = "I'm motivated by challenging problems, by working with people whose skills differ from mine, and by turning theory into something that works in practice. I want to keep growing every day, as an engineer and as a person."
        vol_h = "Volunteering"
        vols = [("Volunteer tutor", "Cascais", "2024 – 2026", "<p>I gave educational support to around 15 children, from preschool to secondary school, finding different ways to explain the basics so each child could follow. Through this I discovered a passion for teaching. It played a big part in my decision to take a gap year in 2025/2026, both to explore new experiences and to spend time sharing knowledge and helping others grow academically.</p>"),
                ("Volunteer, Cascais Jovem", "Cascais", "2021 – 2026", "<p>I volunteered at many Cascais Jovem initiatives:</p><ul class=\"dots\"><li><strong>Occupational Safety and Health Conference:</strong> logistics and event organization</li><li><strong>Children&#x27;s Festival:</strong> working with children and families</li><li><strong>Safe Beaches Initiative:</strong> promoting beach safety and environmental awareness</li><li><strong>Portuguese elections:</strong> helping organize and coordinate the voting process</li></ul>")]
        er_h = "Erasmus+ youth exchanges"
        ex = [("SINCRON SUSTENABIL:", "Apuseni Mountains, Romania", "Oct 2025", "A one-week sustainability programme in a multinational team, with hands-on solar cooking, rainwater harvesting, composting and natural-material building.",
               [ext("https://www.instagram.com/lunca.muresului.youth.asoc/"), ext("https://www.instagram.com/p/DPMvnFLiKdE/")]),
              ("Songs Born on the Migration Road:", "Bursa, Türkiye", "8–17 May 2026", "An exchange about sharing music across countries, with young people from Portugal, Italy, Romania and Türkiye. We performed at a care home for elderly people and at the Gemlik municipality for its president, Şükrü Deviren.",
               [ext("https://www.instagram.com/songs_born_on_migration_route/", "photos and videos on Instagram")]),
              ("LAGI: Local Action, Global Impact:", "Llinars del Vallès (Barcelona), Spain", "20–27 May 2026", "46 young people from six countries used the performing arts and sensory practices to explore how local actions connect to global environmental and social challenges. Together we created installations, photo-performances and live presentations.",
               [ext("https://www.instagram.com/incateatre/"), ext("https://www.naturkultur.eu/en/youth-exchange-lagi-local-action-global-impact-20-27-05-2026-llinars-del-valles-barcelona-spain/", "naturkultur.eu/en/youth-exchange-lagi-local-action-global-impact")])]
        out_h = "Outside the lab"
        photos = [("guitar", "Guitar:", "I play in my own band, with 6 concerts so far."), ("travel", "Travel:", "18 countries across 4 continents."), ("gym", "Sport:", "climbing, gym, padel and sailing.")]
        nx = ("Say hello", "Whether it&#x27;s about engineering, music, volunteering or Erasmus+, I&#x27;m happy to talk.", ("Next: Contact", "contact"))
    else:
        title = "Sobre Guilherme Candeias Martins: Voluntariado e Erasmus+"
        desc = "Sobre Guilherme Candeias Martins, engenheiro de Cascais: explicador voluntário, voluntário da Cascais Jovem, três intercâmbios Erasmus+, guitarrista na sua própria banda e viajante por 18 países."
        h1 = "Sobre mim"
        opening = "Sou o Guilherme Candeias Martins, engenheiro de 22 anos, natural de Cascais e a viver agora em Delft. Fora do laboratório, fiz voluntariado em Cascais durante vários anos e participei em três intercâmbios Erasmus+. Toco guitarra na minha própria banda."
        drives_h = "O que me move"
        drives = "Motivam-me os problemas difíceis, trabalhar com pessoas com competências diferentes das minhas e transformar a teoria em algo que funciona na prática. Quero continuar a crescer todos os dias, como engenheiro e como pessoa."
        vol_h = "Voluntariado"
        vols = [("Explicador voluntário", "Cascais", "2024 – 2026", "<p>Dei apoio escolar a cerca de 15 crianças, do pré-escolar ao secundário, procurando formas diferentes de explicar o essencial para que cada uma conseguisse acompanhar. Foi assim que descobri o gosto por ensinar. Isso pesou muito na minha decisão de fazer um ano sabático em 2025/2026, para viver novas experiências e dedicar tempo a partilhar conhecimento e a ajudar outros a crescer academicamente.</p>"),
                ("Voluntário, Cascais Jovem", "Cascais", "2021 – 2026", "<p>Fui voluntário em várias iniciativas da Cascais Jovem:</p><ul class=\"dots\"><li><strong>Conferência de Segurança e Saúde Ocupacional:</strong> logística e organização do evento</li><li><strong>Festival das Crianças:</strong> acompanhamento de crianças e famílias</li><li><strong>Iniciativa Praias Seguras:</strong> promoção da segurança nas praias e da consciência ambiental</li><li><strong>Eleições portuguesas:</strong> apoio na organização e coordenação do processo eleitoral</li></ul>")]
        er_h = "Intercâmbios Erasmus+"
        ex = [("SINCRON SUSTENABIL:", "Montes Apuseni, Roménia", "out. 2025", "Um programa de uma semana sobre sustentabilidade, numa equipa multinacional, com prática de cozinha solar, recolha de água da chuva, compostagem e construção com materiais naturais.",
               [ext("https://www.instagram.com/lunca.muresului.youth.asoc/"), ext("https://www.instagram.com/p/DPMvnFLiKdE/")]),
              ("Songs Born on the Migration Road:", "Bursa, Turquia", "8–17 de maio de 2026", "Um intercâmbio sobre a partilha de música entre países, com jovens de Portugal, Itália, Roménia e Turquia. Atuámos num lar de idosos e no município de Gemlik, para o seu presidente, Şükrü Deviren.",
               [ext("https://www.instagram.com/songs_born_on_migration_route/", "fotografias e vídeos no Instagram")]),
              ("LAGI: Local Action, Global Impact:", "Llinars del Vallès (Barcelona), Espanha", "20–27 de maio de 2026", "46 jovens de seis países usaram as artes performativas e práticas sensoriais para explorar a ligação entre as ações locais e os desafios ambientais e sociais globais. Criámos em conjunto instalações, fotoperformances e apresentações ao vivo.",
               [ext("https://www.instagram.com/incateatre/"), ext("https://www.naturkultur.eu/en/youth-exchange-lagi-local-action-global-impact-20-27-05-2026-llinars-del-valles-barcelona-spain/", "naturkultur.eu/en/youth-exchange-lagi-local-action-global-impact")])]
        out_h = "Fora do laboratório"
        photos = [("guitar", "Guitarra:", "toco na minha própria banda, com 6 concertos até agora."), ("travel", "Viagens:", "18 países em 4 continentes."), ("gym", "Desporto:", "escalada, ginásio, padel e vela.")]
        nx = ("Diga olá", "Seja sobre engenharia, música, voluntariado ou Erasmus+, terei todo o gosto em conversar.", ("A seguir: Contacto", "contact"))

    vol_html = "".join(f'''<hr class="divider"><article class="entry reveal">
  <div class="entry-rail"><span class="when">{e(y)}</span></div>
  <div class="entry-body"><div class="entry-title small"><h3>{e(t)}<span class="h-place">, {e(place)}</span></h3></div>{body}</div>
</article>''' for t, place, y, body in vols)
    ex_html = "".join(f'''<hr class="divider"><article class="entry reveal">
  <div class="entry-rail"><span class="when">{e(y)}</span><span>{e(place)}</span></div>
  <div class="entry-body"><div class="entry-title small"><h3>{e(t.rstrip(":"))}<span class="sr-only">:</span></h3></div><p>{e(txt)}</p><div class="linkrow">{"".join(links)}</div></div>
</article>''' for t, place, y, txt, links in ex)
    ph = "".join(f'<figure><img src="{A}img/{f}.webp" srcset="{A}img/{f}-480.webp 480w, {A}img/{f}.webp 800w" sizes="(max-width: 759px) 92vw, 360px" alt="" width="800" height="1000" loading="lazy" decoding="async"><figcaption><strong>{e(k.rstrip(":"))}<span class="sr-only">:</span></strong> {e(v)}</figcaption></figure>' for f, k, v in photos)
    body = f'''<header class="page-head"><div class="wrap about-intro">
  <div style="display:grid;gap:var(--space-5)">
    <p class="eyebrow label">{e(NAV[lang]["about"])}</p>
    <h1>{e(h1)}</h1>
    <p class="lead">{e(opening)}</p>
  </div>
  <figure class="portrait"><img src="{A}img/profile.webp" srcset="{A}img/profile-480.webp 480w, {A}img/profile.webp 800w" sizes="(max-width: 859px) min(420px, 92vw), 360px" alt="Guilherme Candeias Martins" width="800" height="1000" loading="lazy" decoding="async"></figure>
</div></header>
<section class="section band" aria-labelledby="drives-h"><div class="wrap">
  <div class="entry reveal"><div class="entry-rail"></div><div class="entry-body">
    <h2 id="drives-h" style="font-size:var(--text-h2)">{e(drives_h)}</h2>
    <p class="lead" style="max-width:52ch">{e(drives)}</p>
  </div></div>
</div></section>
<section class="section" aria-labelledby="vol-h"><div class="wrap entries">
  <div class="section-head" style="margin-bottom:0"><h2 id="vol-h">{e(vol_h)}</h2></div>
  {vol_html}
</div></section>
<section class="section" aria-labelledby="er-h"><div class="wrap entries">
  <div class="section-head" style="margin-bottom:0"><h2 id="er-h">{e(er_h)}</h2></div>
  {ex_html}
</div></section>
<section class="section" aria-labelledby="out-h"><div class="wrap">
  <div class="section-head"><h2 id="out-h">{e(out_h)}</h2></div>
  <div class="photos reveal">{ph}</div>
</div></section>
{next_block(lang, depth, e(nx[0]), nx[1], nx[2])}'''
    return title, desc, body


def contact(lang, depth):
    if lang == "en":
        title = "Contact Guilherme Candeias Martins | MSc Student, TU Delft"
        desc = "Contact Guilherme Candeias Martins, a microelectronics MSc student at TU Delft with semiconductor test experience, about a microelectronics or semiconductor test internship, a thesis, a student role or research."
        h1 = "Contact me"
        opening = "I'm a microelectronics MSc student at TU Delft with a year of semiconductor test experience, looking for a microelectronics or semiconductor test internship from summer 2027. The best way to reach me is by email, and I'll get back to you."
        about_h = "Email me about"
        items = ["An industry internship and MSc thesis from summer 2027", "A part-time or student role alongside my MSc", "A research collaboration", "Anything else, from engineering to music to Erasmus+"]
        labels = ("Email", "LinkedIn", "Based in")
        based = "Delft, the Netherlands"
    else:
        title = "Contacto: Guilherme Candeias Martins | Mestrado TU Delft"
        desc = "Contacte Guilherme Candeias Martins, estudante de mestrado em microeletrónica na TU Delft com experiência em teste de semicondutores, sobre estágios, teses, trabalho para estudantes ou investigação."
        h1 = "Contacto"
        opening = "Sou estudante de mestrado em microeletrónica na TU Delft, com um ano de experiência em teste de semicondutores, e procuro um estágio em microeletrónica ou teste de semicondutores a partir do verão de 2027. A melhor forma de me contactar é por email, e eu respondo."
        about_h = "Escreva-me sobre"
        items = ["Um estágio na indústria e uma tese de mestrado a partir do verão de 2027", "Um trabalho a tempo parcial ou de estudante, em paralelo com o mestrado", "Uma colaboração de investigação", "Qualquer outro assunto, de engenharia a música ou Erasmus+"]
        labels = ("Email", "LinkedIn", "Localização")
        based = "Delft, Países Baixos"
    li = "".join(f"<li>{e(x)}</li>" for x in items)
    body = f'''{page_head(lang, "contact", e(h1), e(opening))}
<section class="section" style="padding-top:0"><div class="wrap contact-card">
  <div class="seeking" style="align-items:start">
    <div class="reveal">
      <div class="section-head"><h2>{e(about_h)}</h2></div>
      <ul class="seeking-list">{li}</ul>
    </div>
    <div></div>
  </div>
  <dl class="contact-lines reveal">
    <div><dt class="label">{labels[0]}</dt><dd><a class="big-mail" href="mailto:{EMAIL}">{EMAIL}</a>{email_btn(lang)}</dd></div>
    <div><dt class="label">{labels[1]}</dt><dd>{ext(LINKEDIN, "linkedin.com/in/guilherme-candeias-martins")}</dd></div>
    <div><dt class="label">{labels[2]}</dt><dd>{e(based)}</dd></div>
  </dl>
</div></section>'''
    return title, desc, body


BUILDERS = {"home": home, "experience": experience, "projects": projects, "education": education, "about": about, "contact": contact}


def write_seo_files(out_root):
    """sitemap.xml (with EN/PT alternates) and robots.txt."""
    import datetime
    today = datetime.date.today().isoformat()
    urls = []
    for lang in ("en", "pt"):
        for page in PAGES:
            alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{h}" href="{SITE}/{page_path(l, page)}"/>'
                           for l, h in (("en", "en"), ("pt", "pt-PT"), ("en", "x-default")))
            urls.append(f"  <url>\n    <loc>{SITE}/{page_path(lang, page)}</loc>\n    <lastmod>{today}</lastmod>{alts}\n  </url>")
    with open(os.path.join(out_root, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(out_root, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print("wrote sitemap.xml, robots.txt")


def build(out_root):
    for lang in ("en", "pt"):
        for page in PAGES:
            p = page_path(lang, page)
            depth = p.count("/")
            title, desc, body = BUILDERS[page](lang, depth)
            out = os.path.join(out_root, p, "index.html")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                f.write(layout(lang, page, depth, title, desc, body))
            print("wrote", os.path.relpath(out, out_root))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--artifact":
        ARTIFACT = True
        dest = sys.argv[2]
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(dest, "assets"))
        build(dest)
    else:
        build(ROOT)
        write_seo_files(ROOT)
