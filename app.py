"""LessonForge AI - Streamlit app (warm dashboard theme). Run: streamlit run app.py"""

import io

import os

import re

import zipfile
from datetime import datetime



import streamlit as st



from research.research_engine import conduct_research

from generation.lesson_generator import generate_lesson, apply_qc_recommendations

from quality_control.factual_checker import check_factual_accuracy

from quality_control.instructional_checker import check_instructional_quality



st.set_page_config(page_title="LessonForge AI", page_icon="📚", layout="wide", initial_sidebar_state="expanded")



# ---------------------------------------------------------------- THEME

st.markdown(

    """<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');



:root {

  --ink: #191B24;

  --muted: #747783;

  --canvas: #F3F4F7;

  --surface: #FFFFFF;

  --navy: #151720;

  --navy-soft: #20232E;

  --line: #E8E5E0;

  --coral: #E85D45;

  --pink: #D83F78;

}



html, body, [class*="css"] {

  font-family: 'DM Sans', sans-serif;

}

.stApp {

  background: var(--canvas);

  color: var(--ink);

}

[data-testid="stHeader"] {

  background: rgba(255,255,255,.94);

}

[data-testid="stToolbar"] { right: 1rem; }

.block-container {

  max-width: 1480px;

  padding: 1.8rem 2rem 3rem;

}

h1, h2, h3, h4 {

  color: var(--ink) !important;

  font-family: 'Manrope', sans-serif !important;

  font-weight: 800 !important;

  letter-spacing: -.035em;

}

h1 { font-size: clamp(2rem, 3vw, 2.8rem) !important; }

h2 { font-size: 1.75rem !important; }

h3 { font-size: 1.25rem !important; }

p, li, label, .stCaption {

  color: #454752;

}

small { color: var(--muted); }



/* Clean LMS-style sidebar inspired by the supplied reference */

section[data-testid="stSidebar"] {

  background: #FFFFFF !important;

  border-right: 1px solid #E9EAF0;

  min-width: 245px;

}

section[data-testid="stSidebar"] > div {

  background: #FFFFFF !important;

  padding: 1.15rem .9rem 1.3rem;

}

section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: .30rem; }

.brand {

  display:flex; align-items:center; gap:10px;

  padding:8px 8px 19px; margin-bottom:18px;

  border-bottom:1px solid #ECECF2;

}

.mark {

  width:39px; height:39px; border-radius:12px;

  background:linear-gradient(140deg,#8B5CF6 0%,#D946EF 100%);

  color:#fff; font:800 18px 'Manrope',sans-serif;

  display:flex; align-items:center; justify-content:center;

  box-shadow:0 5px 13px rgba(139,92,246,.20);

}

.bname { color:#24233A; font:800 17px 'Manrope',sans-serif; letter-spacing:-.45px; }

.bsub { color:#9292A4; font-size:8px; font-weight:800; letter-spacing:.16em; margin-top:3px; }

.navcap { color:#A0A0AE; font-size:9px; font-weight:800; letter-spacing:.15em; padding:0 10px 7px; }

section[data-testid="stSidebar"] div.stButton { margin:0 !important; }

section[data-testid="stSidebar"] div.stButton > button {

  width:100%; min-height:39px; justify-content:flex-start; text-align:left;

  padding:0 11px; border-radius:9px; background:transparent !important;

  border:1px solid transparent !important; color:#55566A !important;

  box-shadow:none !important; transition:background .15s ease,color .15s ease;

}

section[data-testid="stSidebar"] div.stButton > button p { color:inherit !important; font-size:12px; font-weight:600; }

section[data-testid="stSidebar"] div.stButton > button:hover {

  background:#F5F2FF !important; border-color:#EEE8FF !important; color:#7047C8 !important;

}

section[data-testid="stSidebar"] div.stButton > button[kind="primary"],

section[data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-primary"] {

  background:linear-gradient(100deg,#F1EAFE,#FCEBFA) !important;

  border-color:#EEE5FC !important; color:#6741B5 !important;

}

section[data-testid="stSidebar"] div.stButton > button[kind="primary"] p,

section[data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-primary"] p {

  color:#6741B5 !important; font-weight:800;

}

.proj {

  background:#FAF9FD; border:1px solid #ECEAF3; border-radius:13px;

  padding:12px; margin:22px 2px 0; box-shadow:none;

}

.proj .t { color:#9A96A9; font-size:8px; font-weight:800; letter-spacing:.15em; }

.proj .m { color:#343247; font-size:12px; font-weight:800; margin:8px 0 4px; }

.proj .d { color:#858295; font-size:10px; line-height:1.45; overflow-wrap:anywhere; }



/* Page hero */

.hero {

  background: linear-gradient(112deg, #7048E8 0%, #8758EF 58%, #B18AF5 100%);

  border-radius: 25px;

  padding: 34px 38px;

  margin: 0 0 27px;

  color: #FFFFFF;

  box-shadow: 0 12px 28px rgba(112, 75, 210, .14);

}

.hero .e {

  color: rgba(255,255,255,.84);

  font-size: 10px;

  font-weight: 800;

  letter-spacing: .19em;

  margin-bottom: 13px;

}

.hero .t {

  color: #FFFFFF;

  font: 800 clamp(27px, 3vw, 39px)/1.15 'Manrope', sans-serif;

  letter-spacing: -.04em;

}

.hero .c {

  color: rgba(255,255,255,.92);

  font-size: 14px;

  line-height: 1.6;

  margin: 12px 0 0;

  max-width: 760px;

}



/* Dashboard and content cards */

.card {

  background: #FFFFFF;

  border: 1px solid var(--line);

  border-radius: 22px;

  padding: 23px;

  box-sizing: border-box;

  box-shadow: 0 5px 18px rgba(25,27,36,.025);

}

.lbl {

  color: #777A84;

  font-size: 11px;

  line-height: 1.5;

}

.big {

  color: var(--ink);

  font: 800 43px 'Manrope', sans-serif;

  letter-spacing: -.045em;

  margin: 4px 0 10px;

}

.pill {

  display: inline-block;

  padding: 5px 10px;

  border-radius: 99px;

  font-size: 10px;

  font-weight: 800;

  white-space: nowrap;

}

.ok { background: #E2F2E8; color: #267044; }

.next { background: #FCE9DF; color: #A34A2B; }

.lock { background: #ECEBE8; color: #696B73; }

.bad { background: #FBE4E2; color: #A12D2D; }

.row {

  display: flex;

  align-items: center;

  gap: 13px;

  padding: 12px 13px;

  border-radius: 14px;

}

.row.cur {

  background: #F7F4F1;

  border: 1px solid #EEE9E3;

}

.th {

  width: 36px;

  height: 36px;

  border-radius: 11px;

  display: flex;

  align-items: center;

  justify-content: center;

  font-weight: 800;

  flex: none;

  color: var(--ink);

}

.bar {

  width: 25px;

  border-radius: 99px;

  background: #D8D5D0;

}



/* Streamlit widgets */

div[data-testid="stVerticalBlockBorderWrapper"] {

  background: #FFFFFF;

  border: 1px solid var(--line) !important;

  border-radius: 20px;

  padding: 2px;

}

div.stButton > button, div.stDownloadButton > button {

  border-radius: 12px;

  min-height: 43px;

  font-weight: 700;

  padding: 0 18px;

  border: 1px solid #DCD8D2;

  background: #FFFFFF;

  color: var(--ink);

  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;

}

div.stButton > button:hover, div.stDownloadButton > button:hover {

  border-color: #B9B2A9;

  box-shadow: 0 5px 14px rgba(25,27,36,.07);

  transform: translateY(-1px);

}

div.stButton > button[kind="primary"],

button[data-testid="stBaseButton-primary"] {

  background: #191B24 !important;

  color: #FFFFFF !important;

  border: 1px solid #191B24 !important;

}

div.stButton > button[kind="primary"]:hover,

button[data-testid="stBaseButton-primary"]:hover {

  background: #303340 !important;

  border-color: #303340 !important;

}

/* Keep text readable on dark primary buttons, including disabled buttons. */

div.stButton > button[kind="primary"],

div.stButton > button[data-testid="stBaseButton-primary"] {

  color: #FFFFFF !important;

}

div.stButton > button[kind="primary"] p,

div.stButton > button[data-testid="stBaseButton-primary"] p,

div.stButton > button[kind="primary"]:disabled,

div.stButton > button[data-testid="stBaseButton-primary"]:disabled {

  color: #FFFFFF !important;

  opacity: 1 !important;

}

div[data-testid="stTextInput"] input,

div[data-testid="stTextArea"] textarea {

  background: #FFFFFF;

  border: 1px solid #DEDAD4;

  border-radius: 12px;

  color: var(--ink);

}

div[data-testid="stTextInput"] input:focus,

div[data-testid="stTextArea"] textarea:focus {

  border-color: #8B5CF6;

  box-shadow: 0 0 0 2px rgba(139,92,246,.14);

}

div[data-testid="stExpander"] {

  background: #FFFFFF;

  border: 1px solid var(--line);

  border-radius: 15px;

  overflow: hidden;

}

div[data-testid="stTabs"] button {

  font-weight: 700;

}

[data-testid="stAlert"] {

  border-radius: 14px;

}

a { color: #7048C8 !important; }

hr { border-color: #E8E5E0; }

@media (max-width: 900px) {

  .block-container { padding: 1.2rem 1rem 2rem; }

  .hero { padding: 25px 23px; border-radius: 20px; }

}




/* Compact white learning-platform sidebar — spacing and width fix */
section[data-testid="stSidebar"] {
  background: #FFFFFF !important;
  border-right: 1px solid #E9EAF1 !important;
  width: 270px !important;
  min-width: 270px !important;
  max-width: 270px !important;
  flex: 0 0 270px !important;
}
section[data-testid="stSidebar"] > div {
  background: #FFFFFF !important;
  padding: 1.35rem .85rem 1.4rem !important;
}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: .42rem !important; }
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { overflow: visible !important; }
section[data-testid="stSidebar"] .navcap {
  display: block !important;
  position: relative !important;
  clear: both !important;
  line-height: 1.5 !important;
  height: auto !important;
  margin: 12px 0 9px !important;
  padding: 5px 10px 7px !important;
  white-space: nowrap !important;
}
section[data-testid="stSidebar"] div.stButton {
  margin: 3px 0 5px !important;
  position: relative !important;
  clear: both !important;
}
section[data-testid="stSidebar"] .brand {
  padding: 8px 7px 18px;
  margin: 0 0 12px;
  border-bottom: 1px solid #ECECF2;
}
section[data-testid="stSidebar"] .mark {
  width: 38px; height: 38px; border-radius: 12px;
  background: linear-gradient(140deg,#8B5CF6,#D946EF);
  color: #fff; box-shadow: 0 4px 12px rgba(139,92,246,.18);
}
section[data-testid="stSidebar"] .bname { color:#25233B; font-size:16px; }
section[data-testid="stSidebar"] .bsub { color:#9693A6; font-size:8px; }
section[data-testid="stSidebar"] .navcap {
  color:#9997A8; font-size:9px; letter-spacing:.13em;
  padding: 7px 10px 6px;
}
section[data-testid="stSidebar"] div.stButton { margin:0 !important; }
section[data-testid="stSidebar"] div.stButton > button {
  min-height: 38px; padding: 0 10px; border-radius: 9px;
  background: transparent !important; border: 1px solid transparent !important;
  color:#4E4D60 !important; box-shadow:none !important;
}
section[data-testid="stSidebar"] div.stButton > button p {
  color:inherit !important; font-size:12px; font-weight:600;
}
section[data-testid="stSidebar"] div.stButton > button:hover {
  background:#F6F2FF !important; border-color:#EEE8FF !important;
  color:#7146C8 !important;
}
section[data-testid="stSidebar"] div.stButton > button[kind="primary"],
section[data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-primary"] {
  background:#F0EAFE !important; border-color:#E9DFFF !important;
  color:#693FC0 !important;
}
section[data-testid="stSidebar"] div.stButton > button[kind="primary"] p,
section[data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-primary"] p {
  color:#693FC0 !important; font-weight:800;
}
section[data-testid="stSidebar"] .proj {
  background:linear-gradient(145deg,#F8F4FF,#FDF1FA);
  border:1px solid #EEE7FA; border-radius:14px;
  padding:13px; margin:22px 2px 0; box-shadow:none;
}
section[data-testid="stSidebar"] .proj .t { color:#9388A8; font-size:8px; letter-spacing:.14em; }
section[data-testid="stSidebar"] .proj .m { color:#37314B; font-size:12px; margin:8px 0 4px; }
section[data-testid="stSidebar"] .proj .d { color:#817A91; font-size:10px; line-height:1.45; }
.block-container { max-width: 1600px; padding: 1.1rem 1.6rem 2.5rem !important; }
[data-testid="stHeader"] { background:rgba(255,255,255,.96) !important; }

</style>""",

    unsafe_allow_html=True,

)



# ---------------------------------------------------------------- STATE

ss = st.session_state

for k, v in {

    "lesson": "", "research": {}, "qc1_report": "", "qc2_report": "", "lesson_title": "", "objective": "",

    "lesson_version": 0, "draft": None, "errors": {}, "history": [], "flash": "", "applied": False,

    "in_title": "", "in_obj": "", "page": "Dashboard",

}.items():

    ss.setdefault(k, v)



SAMPLE = ("HTTP Requests and Responses",

          "Explain GET and POST methods and distinguish between 2xx, 4xx, and 5xx response status categories.")





def H(s):  # collapse HTML so Markdown never turns indented lines into code blocks

    return "".join(line.strip() for line in s.splitlines())





def html(s):

    st.markdown(H(s), unsafe_allow_html=True)





def save_output(name, text):

    os.makedirs("outputs", exist_ok=True)

    with open(os.path.join("outputs", name), "w", encoding="utf-8") as f:

        f.write(text)





def time_check(md):

    """Sum '(N min)' labels on ## / ### headings. Returns (total, [(name, minutes)])."""

    rows = []

    for line in md.splitlines():

        m = re.match(r"^#{2,3}\s*(.*?)\s*\((\d+)\s*min", line.strip(), re.I)

        if m:

            rows.append((re.sub(r"^[\d.\s]+", "", m.group(1)).strip(" -:"), int(m.group(2))))

    return sum(x for _, x in rows), rows





def references_md(research):

    out = ["## References", ""]

    for key, head in (("websites", "Websites"), ("books", "Books"), ("youtube", "YouTube videos")):

        items = research.get(key, [])

        if items:

            out.append(f"### {head}")

            for it in items:

                title = it.get("title") or "Untitled"

                extra = f" - {it['channel']}" if it.get("channel") else ""

                out.append(f"- [{title}]({it['url']}){extra}" if it.get("url") else f"- {title}{extra}")

            out.append("")

    return "\n".join(out)





def full_lesson():
    """Return the lesson with research references appended exactly once."""
    lesson = ss.lesson or ""

    # Accept Markdown headings such as '# References' or '## References'.
    if re.search(r"(?im)^\s*#{1,6}\s*references\b", lesson):
        return lesson

    refs = references_md(ss.research)
    if not refs.strip() or refs.strip() == "## References":
        return lesson

    return lesson.rstrip() + "\n\n---\n\n" + refs





def set_lesson(new, note):

    ss.history.append((note, ss.lesson))  # previous text is never lost

    ss.lesson = new

    ss.lesson_version += 1

    ss.qc1_report = ss.qc2_report = ""

    save_output("generated_lesson.md", new)





def go(name):

    ss.page = name





def use_sample():

    ss.in_title, ss.in_obj = SAMPLE





def flash():

    if ss.flash:

        st.success(ss.flash)

        ss.flash = ""





def hero(title, sub, eyebrow):

    html(f'<div class="hero"><div class="e">{eyebrow}</div><div class="t">{title}</div><p class="c">{sub}</p></div>')





# ---------------------------------------------------------------- GENERATION PIPELINE

def _research(d):

    try:

        d["research"] = conduct_research(d["title"], d["objective"])

    except TypeError:  # older conduct_research(query) signature

        d["research"] = conduct_research(d["title"])





def _lesson(d):

    text = generate_lesson(d["title"], d["objective"], d["research"])

    if not text or not text.strip():

        raise ValueError("AI returned an empty lesson.")

    d["lesson"] = text





def run_generation():

    """Runs missing steps only, so a retry never repeats finished research.

    The saved lesson is replaced only after BOTH steps succeed."""

    d = ss.draft

    for key, label, fn in (("research", "Researching websites, books and videos...", _research),

                           ("lesson", "Generating your lesson with Gemini...", _lesson)):

        if key in d:

            continue

        try:

            with st.spinner(label):

                fn(d)

            ss.errors.pop(key, None)

        except Exception as e:

            ss.errors[key] = str(e)

            return False

    ss.research, ss.lesson = d["research"], d["lesson"]

    ss.lesson_title, ss.objective = d["title"], d["objective"]

    ss.qc1_report = ss.qc2_report = ""

    ss.history, ss.applied = [], False

    ss.lesson_version += 1

    ss.draft = None

    save_output("generated_lesson.md", ss.lesson)

    ss.flash = "Your lesson has been generated. Review it in the Lesson Editor."

    return True





# ---------------------------------------------------------------- SIDEBAR

NAV = [("⌂  Dashboard", "Dashboard"), ("＋  Create Lesson", "Create Lesson"), ("▱  Research Library", "Research Library"),
       ("✎  Lesson Editor", "Lesson Editor"), ("✓  Quality Assurance", "Quality Assurance"), ("⇩  Export Center", "Export Center")]

with st.sidebar:
    html('<div class="brand"><div class="mark">L</div><div><div class="bname">LessonForge AI</div><div class="bsub">AI LESSON STUDIO</div></div></div><div class="navcap">OVERVIEW</div>')
    for label, name in NAV[:4]:
        st.button(label, key=f"nav_{name}", type="primary" if ss.page == name else "secondary", on_click=go, args=(name,), use_container_width=True)
    html('<div class="navcap" style="margin-top:14px;border-top:1px solid #ECECF2;padding-top:16px;">QUALITY &amp; EXPORT</div>')
    for label, name in NAV[4:]:
        st.button(label, key=f"nav_{name}", type="primary" if ss.page == name else "secondary", on_click=go, args=(name,), use_container_width=True)
    page = ss.page

    ready = bool(ss.lesson)

    html(f'<div class="proj"><div class="t">CURRENT PROJECT</div><div class="m">{"● Lesson ready" if ready else "○ No lesson yet"}</div>'

         f'<div class="d">{ss.lesson_title if ready else "Create a lesson to begin"}</div></div>')



# ---------------------------------------------------------------- DASHBOARD
if page == "Dashboard":
    flash()

    total, rows = time_check(ss.lesson) if ss.lesson else (0, [])
    words = len(re.findall(r"\w+", ss.lesson))
    r = ss.research
    n_web, n_book, n_vid = (len(r.get(k, [])) for k in ("websites", "books", "youtube"))
    n_src = n_web + n_book + n_vid
    done_qc = int(bool(ss.qc1_report)) + int(bool(ss.qc2_report))
    ready = bool(ss.lesson)

    workflow = [
        ("Research resources", bool(r), "Research Library"),
        ("Create lesson content", ready, "Create Lesson"),
        ("Edit and refine lesson", bool(ready and ss.history), "Lesson Editor"),
        ("Run both quality checks", bool(ss.qc1_report and ss.qc2_report), "Quality Assurance"),
        ("Export final lesson", bool(ready and ss.qc1_report and ss.qc2_report), "Export Center"),
    ]
    completed = sum(1 for _, done, _ in workflow if done)
    pct = int(completed / len(workflow) * 100)
    next_task = next((label for label, done, _ in workflow if not done), "All steps completed")
    today = datetime.now().strftime("%A, %d %B")

    # Compact page header
    hleft, hright = st.columns([3, 1])
    with hleft:
        html("""
        <div style="display:flex;align-items:center;gap:11px;margin:2px 0 16px;">
          <div style="width:39px;height:39px;border-radius:12px;background:#F0E9FF;color:#8054D6;display:flex;align-items:center;justify-content:center;font-size:21px;">▥</div>
          <div><div style="font:800 23px 'Manrope',sans-serif;color:#24233B;">Dashboard</div>
          <div style="font-size:11px;color:#8C8A9B;margin-top:2px;">Your AI lesson creation workspace</div></div>
        </div>
        """)
    with hright:
        html(f'<div style="text-align:right;padding:8px 3px;color:#89869A;font-size:10px;font-weight:700;">{today}<br><span style="color:#A29CAF;font-weight:500;">LESSONFORGE AI</span></div>')

    # Three-column inspired layout: central workspace + right schedule rail.
    main_col, rail = st.columns([2.08, 1], gap="medium")

    with main_col:
        # Hero banner
        html(f"""
        <div style="position:relative;overflow:hidden;background:linear-gradient(110deg,#7048E8 0%,#8758EF 55%,#B18AF5 100%);border-radius:18px;padding:22px 23px;margin-bottom:13px;color:#fff;min-height:160px;box-shadow:0 8px 20px rgba(112,75,210,.12);">
          <div style="position:absolute;right:-35px;top:-80px;width:235px;height:235px;border-radius:50%;background:rgba(255,255,255,.10);"></div>
          <div style="position:relative;max-width:65%;">
            <div style="font-size:9px;font-weight:800;letter-spacing:.15em;color:#EDE5FF;">✦ AI LEARNING STUDIO</div>
            <div style="font:800 clamp(23px,2.4vw,32px)/1.12 'Manrope',sans-serif;color:#fff;margin-top:9px;">Enhance your learning<br>with AI.</div>
            <div style="font-size:10px;line-height:1.55;color:#F3EDFF;margin-top:8px;">Research trusted resources, create structured lessons, validate quality and export classroom-ready content.</div>
          </div>
          <div style="position:absolute;right:16px;top:25px;width:31%;min-width:145px;background:rgba(255,255,255,.95);border-radius:14px;padding:12px;color:#30264A;box-shadow:0 7px 18px rgba(46,24,94,.10);">
            <div style="font-size:8px;font-weight:800;letter-spacing:.1em;color:#8C7AAE;">✦ LESSON ASSISTANT</div>
            <div style="font:800 12px 'Manrope',sans-serif;margin-top:7px;">{'Your lesson is ready!' if ready else 'Ready when you are!'}</div>
            <div style="font-size:9px;color:#827A91;line-height:1.4;margin-top:4px;">{next_task if not ready else 'Continue refining your lesson.'}</div>
          </div>
        </div>
        """)

        act1, act2, spacer = st.columns([1, 1, 2])
        with act1:
            st.button("✦  Create new lesson", type="primary", on_click=go, args=("Create Lesson",), use_container_width=True)
        with act2:
            st.button("▱  Browse research", on_click=go, args=("Research Library",), use_container_width=True)

        # Four compact metric cards
        st.write("")
        metrics = [
            ("LESSON STATUS", "Ready" if ready else "Not started", ss.lesson_title if ready else "Your current lesson", "#F3EAFE", "▣", "#8555D6"),
            ("RESEARCH SOURCES", str(n_src), f"{n_web} websites · {n_book} books · {n_vid} videos", "#E8F3FF", "▱", "#368BCB"),
            ("LESSON DURATION", f"{total if rows else 45} min", "Target learning session", "#FFF3E4", "◷", "#D18A28"),
            ("QUALITY CHECKS", f"{done_qc} / 2", "Factual + instructional", "#E8F8EE", "✓", "#31A267"),
        ]
        metric_cols = st.columns(4, gap="small")
        for col, (label, value, note, tint, symbol, accent) in zip(metric_cols, metrics):
            with col:
                html(f"""
                <div style="height:98px;background:#fff;border:1px solid #E9EAF1;border-radius:13px;padding:11px 12px;box-shadow:0 3px 12px rgba(30,35,60,.025);">
                  <div style="display:flex;align-items:center;justify-content:space-between;"><span style="font-size:8px;font-weight:800;letter-spacing:.07em;color:#9292A1;">{label}</span><span style="width:27px;height:27px;border-radius:9px;background:{tint};display:flex;align-items:center;justify-content:center;color:{accent};font-size:15px;">{symbol}</span></div>
                  <div style="font:800 19px 'Manrope',sans-serif;color:#28263F;margin-top:8px;">{value}</div>
                  <div style="font-size:8px;color:#8C8B9C;margin-top:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{note}</div>
                </div>
                """)

        # Continue learning cards
        st.write("")
        html('<div style="display:flex;align-items:center;justify-content:space-between;margin:4px 0 9px;"><span style="font:800 15px Manrope,sans-serif;color:#29273E;">Continue learning</span><span style="font-size:9px;color:#8055D4;font-weight:700;">YOUR WORKSPACE</span></div>')
        learning_cards = [
            ("Research & collect", "Find trusted websites, books and videos", "#F1EAFE", "⌕", "Research Library", n_src, "sources collected"),
            ("Create & edit lesson", "Generate, review and refine content", "#E8F3FF", "✎", "Lesson Editor", words, "words in lesson"),
            ("Run quality checks", "Validate facts and teaching quality", "#FCEAF3", "✓", "Quality Assurance", done_qc, "of 2 checks done"),
        ]
        learning_cols = st.columns(3, gap="small")
        for col, (title, desc, tint, icon, target, number, suffix) in zip(learning_cols, learning_cards):
            with col:
                html(f"""
                <div style="background:#fff;border:1px solid #E9EAF1;border-radius:13px;padding:12px;min-height:116px;box-shadow:0 3px 10px rgba(30,35,60,.02);">
                  <div style="height:48px;border-radius:9px;background:{tint};display:flex;align-items:center;justify-content:center;color:#7850CA;font-size:23px;">{icon}</div>
                  <div style="font:800 10px 'Manrope',sans-serif;color:#302D46;margin-top:9px;">{title}</div>
                  <div style="font-size:8px;color:#89889A;line-height:1.4;margin-top:4px;">{desc}</div>
                  <div style="font-size:8px;color:#8B70C5;font-weight:700;margin-top:7px;">{number} {suffix}</div>
                </div>
                """)
                st.button(f"Open {title}", key=f"dash_open_{target}", on_click=go, args=(target,), use_container_width=True)

        # Bottom row: upcoming tasks + activity overview
        st.write("")
        lower_left, lower_right = st.columns([1.05, 1], gap="small")
        with lower_left:
            task_html = "".join(
                f'<div style="display:flex;align-items:center;gap:8px;padding:7px 0;border-top:1px solid #F1F0F5;"><span style="color:{"#2B9B61" if done else "#8B8798"};font-size:12px;">{"✓" if done else "○"}</span><span style="flex:1;font-size:9px;color:#4E4B60;">{label}</span><span style="font-size:8px;color:{"#2B9B61" if done else "#8B8798"};font-weight:800;">{"DONE" if done else "TO DO"}</span></div>'
                for label, done, target in workflow
            )
            html(f'<div style="background:#fff;border:1px solid #E9EAF1;border-radius:13px;padding:13px 14px;"><div style="font:800 13px Manrope,sans-serif;color:#302D46;margin-bottom:8px;">Upcoming tasks</div>{task_html}</div>')
        with lower_right:
            html(f"""
            <div style="background:#fff;border:1px solid #E9EAF1;border-radius:13px;padding:13px 14px;min-height:190px;">
              <div style="font:800 13px Manrope,sans-serif;color:#302D46;">Learning activity</div>
              <div style="font:800 23px Manrope,sans-serif;color:#29263F;margin-top:10px;">{words if ready else 0} <span style="font-size:10px;font-weight:600;color:#8B8999;">lesson words</span></div>
              <div style="font-size:8px;color:#9290A0;">{n_src} research sources collected · {done_qc}/2 quality checks</div>
              <div style="display:flex;align-items:flex-end;gap:7px;height:65px;margin-top:13px;border-bottom:1px solid #ECEAF2;">
                {''.join(f'<div style="flex:1;height:{18 + (i*7 if ready else 0)}px;background:linear-gradient(180deg,#B58AF5,#E9DDFB);border-radius:5px 5px 0 0;"></div>' for i in range(7))}
              </div>
              <div style="display:flex;justify-content:space-between;font-size:8px;color:#9693A3;margin-top:5px;"><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span></div>
            </div>
            """)

    with rail:
        # Schedule-style right rail, with real workflow steps rather than invented appointments.
        schedule_rows = "".join(
            f"""
            <div style="display:flex;align-items:center;gap:9px;padding:10px 8px;margin-top:7px;background:#FAF9FC;border-radius:10px;">
              <div style="width:26px;height:26px;border-radius:8px;background:{'#E7F7ED' if done else '#F5F0FF'};color:{'#27965B' if done else '#8055D4'};display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;">{'✓' if done else idx + 1}</div>
              <div style="flex:1;font-size:9px;font-weight:700;color:#4A465D;">{label}</div>
              <div style="font-size:8px;color:{'#27965B' if done else '#8055D4'};font-weight:800;">{'DONE' if done else 'NEXT' if label == next_task else 'LATER'}</div>
            </div>
            """
            for idx, (label, done, target) in enumerate(workflow)
        )
        html(f"""
        <div style="background:#fff;border:1px solid #E9EAF1;border-radius:15px;padding:15px;box-shadow:0 4px 14px rgba(30,35,60,.025);">
          <div style="display:flex;align-items:center;gap:8px;font:800 15px 'Manrope',sans-serif;color:#29273E;">▦  Your schedule</div>
          <div style="display:flex;align-items:center;gap:10px;margin:14px 0 13px;">
            <div style="width:42px;height:42px;border-radius:50%;background:#F0E9FF;color:#8055D4;display:flex;align-items:center;justify-content:center;font-size:19px;">✦</div>
            <div><div style="font-size:11px;font-weight:800;color:#343148;">Welcome to LessonForge! 👋</div><div style="font-size:9px;color:#9290A0;margin-top:3px;">{today}</div><div style="font-size:9px;color:#9290A0;">Your next lesson starts here.</div></div>
          </div>
          <div style="border-top:1px solid #F0EFF4;padding-top:12px;">
            <div style="font:800 12px 'Manrope',sans-serif;color:#343148;">Your next steps</div>
            <div style="font-size:9px;color:#9996A6;margin-top:3px;">A simple path to a classroom-ready lesson</div>
            {schedule_rows}
          </div>
          <div style="border-top:1px solid #F0EFF4;margin-top:14px;padding-top:12px;">
            <div style="display:flex;justify-content:space-between;font-size:10px;font-weight:800;color:#39364D;"><span>Overall progress</span><span style="color:#8055D4;">{pct}%</span></div>
            <div style="height:7px;background:#F0EDF6;border-radius:99px;margin-top:8px;overflow:hidden;"><div style="height:100%;width:{pct}%;background:linear-gradient(90deg,#8559E8,#C16BDF);border-radius:99px;"></div></div>
          </div>
          <div style="border-top:1px solid #F0EFF4;margin-top:14px;padding-top:12px;">
            <div style="font:800 11px 'Manrope',sans-serif;color:#4A3A70;">💡 Tip of the day</div>
            <div style="font-size:9px;line-height:1.55;color:#777287;margin-top:6px;">Use a mix of websites, books and videos to build a more reliable and engaging lesson.</div>
          </div>
        </div>
        """)
        st.write("")
        html(f"""
        <div style="background:linear-gradient(145deg,#F5EFFF,#FDF0FA);border:1px solid #EEE5FA;border-radius:14px;padding:14px;">
          <div style="font-size:9px;font-weight:800;letter-spacing:.1em;color:#907CB4;">CURRENT PROJECT</div>
          <div style="font:800 13px 'Manrope',sans-serif;color:#3C3157;margin-top:7px;">{ss.lesson_title if ready else 'No lesson yet'}</div>
          <div style="font-size:9px;color:#898398;line-height:1.5;margin-top:4px;">{(str(words) + ' words · ' + str(n_src) + ' sources') if ready else 'Create a lesson to see your project progress here.'}</div>
        </div>
        """)



# ---------------------------------------------------------------- CREATE LESSON

elif page == "Create Lesson":

    hero("Create a new lesson", "Start with a topic and a measurable learning objective. LessonForge will research and structure the lesson.", "LESSON CREATION")

    flash()

    with st.container(border=True):

        st.subheader("Lesson details")

        st.text_input("Lesson title", key="in_title", placeholder="e.g. HTTP Requests and Responses")

        st.text_area("Learning objective", key="in_obj", height=120, placeholder="By the end of this lesson, learners should be able to...")

        st.caption("Designed for a 45-minute learning session.")

        c1, c2, _ = st.columns([1, 1, 3])

        gen = c1.button("✨  Generate lesson", type="primary")

        c2.button("Use sample input", on_click=use_sample)

    if gen:

        t, o = ss.in_title.strip(), ss.in_obj.strip()

        if not t or not o:

            st.error("Please enter both the lesson title and learning objective.")

        else:

            if ss.draft is None or ss.draft["title"] != t or ss.draft["objective"] != o:

                ss.draft, ss.errors = {"title": t, "objective": o}, {}

            if run_generation():

                st.rerun()

    for key, label in (("research", "Research"), ("lesson", "Lesson generation")):

        if key in ss.errors and ss.draft:

            st.error(f"{label} failed: {ss.errors[key]}")

            st.caption("Your previously saved lesson is untouched, and finished steps are kept.")

            if st.button(f"↻  Retry {label.lower()}", key=f"retry_{key}"):

                if run_generation():

                    st.rerun()

                st.rerun()

    if ss.draft and "research" in ss.draft and not ss.errors:

        st.info("Research is done for this draft. Press Generate again to continue.")

    if ss.lesson:

        st.success(f"Current lesson: {ss.lesson_title}")



# ---------------------------------------------------------------- RESEARCH LIBRARY

elif page == "Research Library":

    hero("Research library", "Review the websites, books and videos collected for your lesson.", "SOURCE COLLECTION")

    if not ss.research:

        st.info("No research references yet. Generate a lesson to populate this library.")

    for key, icon, head in (("websites", "🌐", "Website references"), ("books", "📚", "Book references"), ("youtube", "▶️", "YouTube references")):

        if not ss.research:

            break

        items = ss.research.get(key, [])

        with st.container(border=True):

            st.subheader(f"{icon}  {head}")

            html(f'<span class="pill {"ok" if items else "bad"}">{len(items)} found</span>')

            if key == "youtube" and not items:

                st.warning("No verified videos were found. Go to Create Lesson and generate again to retry.")

            for i, it in enumerate(items, 1):

                tag = ""

                if it.get("reliability"):

                    tag = f' <span class="pill {"ok" if it["reliability"] == "high" else "lock"}">{it["reliability"]} reliability</span>'

                html(f'<b>{i}. {it.get("title", "Untitled")}</b>{tag}')

                for field in ("snippet", "description"):

                    if it.get(field):

                        st.write(it[field][:300])

                if it.get("authors"):

                    st.caption("Authors: " + ", ".join(it["authors"]))

                if it.get("channel"):

                    st.caption("Channel: " + it["channel"] + (f" · {it['duration']}" if it.get("duration") else ""))

                if it.get("url"):

                    st.markdown(f"[Open source ↗]({it['url']})")

                st.divider()



# ---------------------------------------------------------------- LESSON EDITOR

elif page == "Lesson Editor":

    hero("Lesson editor", "Review, edit and preview the lesson. Every change keeps a restorable version.", "CONTENT WORKSPACE")

    flash()

    if not ss.lesson:

        st.info("Generate a lesson before opening the editor.")

    else:

        total, rows = time_check(ss.lesson)

        if rows:

            html(f'<span class="pill {"ok" if total == 45 else "bad"}">Section minutes: {total} / 45</span>')

        else:

            st.caption("Tip: ask for section headings like '## Core Concepts (15 min)' to enable the 45-minute check.")

        edit_tab, prev_tab = st.tabs(["✎  Edit content", "◉  Preview lesson"])

        with edit_tab:

            text = st.text_area("Lesson content (Markdown)", value=ss.lesson, height=540, key=f"lesson_editor_{ss.lesson_version}")

            if st.button("💾  Save lesson changes", type="primary"):

                if not text.strip():

                    st.error("Lesson content cannot be empty. Your saved lesson is unchanged.")

                elif text != ss.lesson:

                    set_lesson(text, "manual edit")

                    ss.flash = "Changes saved. Run both QC checks again to validate the edited lesson."

                    st.rerun()

            if ss.history:

                with st.expander(f"Version history ({len(ss.history)})"):

                    for i in range(len(ss.history) - 1, -1, -1):

                        if st.button(f"Restore version before: {ss.history[i][0]} (#{i + 1})", key=f"rv{i}"):

                            set_lesson(ss.history[i][1], f"restore #{i + 1}")

                            ss.flash = "Previous version restored."

                            st.rerun()

        with prev_tab:

            st.markdown(full_lesson())

            for v in ss.research.get("youtube", [])[:2]:

                if v.get("url"):

                    st.video(v["url"])



# ---------------------------------------------------------------- QUALITY ASSURANCE

elif page == "Quality Assurance":

    hero("Quality assurance center", "Audit the lesson with two independent quality control layers.", "QUALITY CONTROL")

    flash()

    if not ss.lesson:

        st.info("Generate a lesson before running quality checks.")

    else:

        c1, c2 = st.columns(2, gap="large")

        for col, num, name, desc, field, fn in (

            (c1, 1, "Factual accuracy", "Checks factual correctness, unsupported claims, source reliability and gaps.", "qc1_report", lambda: check_factual_accuracy(ss.lesson, ss.research)),

            (c2, 2, "Instructional quality", "Checks objective alignment, clarity, structure, examples and activities.", "qc2_report", lambda: check_instructional_quality(ss.lesson, ss.lesson_title, ss.objective)),

        ):

            with col, st.container(border=True):

                st.markdown(f"### QC{num} · {name}")

                st.caption(desc)

                html(f'<span class="pill {"ok" if ss[field] else "lock"}">{"Completed" if ss[field] else "Pending"}</span>')

                if st.button(f"{'Re-run' if ss[field] else 'Run'} QC{num} audit", key=f"run_{num}", type="primary", use_container_width=True):

                    try:

                        with st.spinner(f"Running QC{num}..."):

                            report = fn()

                        if not report or not str(report).strip():

                            raise ValueError("The audit returned an empty report.")

                        ss[field] = report

                        save_output(f"qc{num}_{'factual' if num == 1 else 'instructional'}_report.md", report)

                        ss.flash = f"QC{num} completed."

                        ss.errors.pop(f"qc{num}", None)

                        st.rerun()

                    except Exception as e:

                        ss.errors[f"qc{num}"] = str(e)

                if f"qc{num}" in ss.errors:

                    st.error(f"QC{num} failed: {ss.errors[f'qc{num}']} Press the button to retry; your lesson is unchanged.")

        st.write("")

        r1, r2 = st.columns(2, gap="large")

        with r1:

            if ss.qc1_report:

                with st.expander("QC1 · Factual accuracy report", expanded=True):

                    st.markdown(ss.qc1_report)

        with r2:

            if ss.qc2_report:

                with st.expander("QC2 · Instructional quality report", expanded=True):

                    st.markdown(ss.qc2_report)

        st.subheader("Improve your lesson")

        if ss.qc1_report and ss.qc2_report:

            st.success("Both quality checks are complete.")

            if st.button("✨  Apply QC recommendations", type="primary"):

                try:

                    with st.spinner("Applying recommendations..."):

                        improved = apply_qc_recommendations(ss.lesson, ss.qc1_report, ss.qc2_report)

                    if not improved or not improved.strip():

                        raise ValueError("The improved lesson is empty.")

                    set_lesson(improved, "applied QC recommendations")  # old text kept in version history

                    save_output("improved_lesson.md", improved)

                    ss.applied = True

                    ss.flash = "Recommendations applied. Your previous version is in the Lesson Editor history. Run both QC checks again."

                    st.rerun()

                except Exception as e:

                    st.error(f"Could not improve lesson: {e}. Your lesson is unchanged; try again.")

        else:

            st.warning("Complete both QC1 and QC2 to unlock lesson improvement.")



# ---------------------------------------------------------------- EXPORT

elif page == "Export Center":

    hero("Export your work", "Download the final lesson with references, plus both quality audit reports.", "DELIVERABLES")

    if not ss.lesson:

        st.info("Generate a lesson before exporting.")

    else:

        files = {"final_lesson.md": full_lesson(), "research_references.md": references_md(ss.research)}

        if ss.qc1_report:

            files["qc1_factual_report.md"] = ss.qc1_report

        if ss.qc2_report:

            files["qc2_instructional_report.md"] = ss.qc2_report

        buf = io.BytesIO()

        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:

            for n, t in files.items():

                z.writestr(n, t)

        with st.container(border=True):

            st.subheader("Everything in one file")

            st.caption("Lesson (with references), research references and any completed QC reports.")

            st.download_button("⬇  Download all (.zip)", buf.getvalue(), "lesson_package.zip", "application/zip")

        cols = st.columns(2, gap="large")

        for i, (n, t) in enumerate(files.items()):

            with cols[i % 2], st.container(border=True):

                st.markdown(f"**{n}**")

                st.download_button(f"Download {n}", t, n, "text/markdown", key=f"dl{i}", use_container_width=True)

        if not (ss.qc1_report and ss.qc2_report):

            st.warning("Run both QC checks to include both reports in the export.")



st.markdown("<div style='text-align:center;color:#85838A;font-size:11px;padding:34px 0 8px;letter-spacing:.02em'><b>LessonForge AI</b> · Built with Streamlit and Google Gemini</div>", unsafe_allow_html=True)
