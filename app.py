import streamlit as st
import cv2
import sys
import time
import tempfile

# ----------------------------------------
# Import Project Modules
# ----------------------------------------

sys.path.append("src")

from pipeline import AgentDrivePipeline

# ----------------------------------------
# Streamlit Configuration
# ----------------------------------------

st.set_page_config(
    page_title="AgentDrive AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# DESIGN SYSTEM
# ----------------------------------------------------------
# A dark instrument-cluster / race-telemetry aesthetic.
#   bg        #0A0E14  panel      #12181F  panel-alt  #161D26
#   border    #212B36  border-hi  #2A3644
#   text      #E7EDF3  text-dim   #8593A3  text-faint #4C5866
#   cyan      #00D9FF  teal(low)  #00E5A0  amber(med) #FFB020
#   red(high) #FF3B4E  violet(AI) #7B61FF
# Type: Rajdhani (display/HUD labels), JetBrains Mono (telemetry
# numerals), Inter (body copy).
# ==========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

:root{
    --bg:#0A0E14;
    --bg-panel:#12181F;
    --bg-panel-alt:#161D26;
    --border:#212B36;
    --border-hi:#2A3644;
    --text:#E7EDF3;
    --text-dim:#8593A3;
    --text-faint:#4C5866;
    --cyan:#00D9FF;
    --teal:#00E5A0;
    --amber:#FFB020;
    --red:#FF3B4E;
    --violet:#7B61FF;
}

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header[data-testid="stHeader"]{background:transparent;}

.stApp{
    background:
        radial-gradient(circle at 15% 0%, rgba(0,217,255,0.05), transparent 45%),
        radial-gradient(circle at 85% 10%, rgba(123,97,255,0.05), transparent 40%),
        var(--bg);
    font-family:'Inter', sans-serif;
    color:var(--text);
}

.block-container{
    padding-top:0.6rem;
    padding-bottom:2rem;
    max-width:1500px;
}

/* ---------------- Sidebar ---------------- */

section[data-testid="stSidebar"]{
    background:var(--bg-panel);
    border-right:1px solid var(--border);
}

section[data-testid="stSidebar"] .block-container{
    padding-top:1.6rem;
}

.sidebar-title{
    font-family:'Rajdhani', sans-serif;
    font-weight:700;
    letter-spacing:2px;
    font-size:13px;
    color:var(--text-dim);
    margin:4px 0 12px 0;
}

.status-grid{
    display:flex;
    flex-direction:column;
    gap:8px;
    margin-bottom:8px;
}

.status-chip{
    display:flex;
    align-items:center;
    gap:10px;
    background:var(--bg-panel-alt);
    border:1px solid var(--border);
    border-radius:8px;
    padding:9px 12px;
}

.status-dot{
    width:8px;
    height:8px;
    min-width:8px;
    border-radius:50%;
    background:var(--teal);
    box-shadow:0 0 8px var(--teal);
}

.status-chip span.status-label{
    font-family:'JetBrains Mono', monospace;
    font-size:12.5px;
    color:var(--text);
    letter-spacing:0.2px;
}

.status-chip span.status-state{
    margin-left:auto;
    font-family:'JetBrains Mono', monospace;
    font-size:10.5px;
    color:var(--teal);
    letter-spacing:1px;
}

.sidebar-divider{
    height:1px;
    background:linear-gradient(90deg, transparent, var(--border-hi), transparent);
    margin:18px 0 16px 0;
}

/* ---------------- Header ---------------- */

.app-header{
    padding:6px 0 18px 0;
}

.app-header-eyebrow{
    display:flex;
    align-items:center;
    gap:8px;
    margin-bottom:6px;
}

.live-dot{
    width:8px;
    height:8px;
    border-radius:50%;
    background:var(--teal);
    box-shadow:0 0 10px var(--teal);
    animation:blink 1.8s ease-in-out infinite;
}

@keyframes blink{
    0%,100%{opacity:1;}
    50%{opacity:0.25;}
}

.live-text{
    font-family:'JetBrains Mono', monospace;
    font-size:11.5px;
    letter-spacing:2.5px;
    color:var(--text-dim);
}

.app-title{
    font-family:'Rajdhani', sans-serif;
    font-weight:700;
    font-size:44px;
    letter-spacing:1px;
    margin:0;
    line-height:1.05;
    color:var(--text);
}

.app-title .accent{
    background:linear-gradient(90deg, var(--cyan), var(--violet));
    -webkit-background-clip:text;
    background-clip:text;
    color:transparent;
}

.app-title .tag{
    font-size:20px;
    font-weight:600;
    color:var(--text-dim);
    letter-spacing:3px;
    vertical-align:middle;
    margin-left:6px;
}

.app-subtitle{
    font-family:'JetBrains Mono', monospace;
    font-size:12.5px;
    letter-spacing:1.5px;
    color:var(--text-faint);
    margin:8px 0 0 0;
    text-transform:uppercase;
}

.header-rule{
    height:2px;
    margin-top:16px;
    background:linear-gradient(90deg, var(--cyan) 0%, var(--violet) 35%, transparent 70%);
    opacity:0.7;
}

/* ---------------- Video frame ---------------- */

.video-eyebrow{
    display:flex;
    justify-content:space-between;
    align-items:center;
    font-family:'JetBrains Mono', monospace;
    font-size:11px;
    letter-spacing:1.5px;
    color:var(--text-dim);
    margin:20px 2px 8px 2px;
    text-transform:uppercase;
}

.video-eyebrow .rec{
    color:var(--red);
}

[data-testid="stImage"] img{
    border-radius:10px;
    border:1px solid var(--border-hi);
    box-shadow:
        0 0 0 1px rgba(0,217,255,0.12),
        0 24px 60px -24px rgba(0,217,255,0.35),
        inset 0 0 50px rgba(0,0,0,0.35);
}

/* ---------------- Telemetry cards ---------------- */

.tcard{
    display:flex;
    align-items:center;
    gap:14px;
    background:var(--bg-panel);
    border:1px solid var(--border);
    border-left:3px solid var(--cyan);
    border-radius:10px;
    padding:16px 18px;
    margin-top:4px;
}

.tcard-icon{
    font-size:26px;
    line-height:1;
}

.tcard-label{
    font-family:'JetBrains Mono', monospace;
    font-size:10.5px;
    letter-spacing:1.8px;
    color:var(--text-dim);
    text-transform:uppercase;
    margin-bottom:4px;
}

.tcard-value{
    font-family:'Rajdhani', sans-serif;
    font-weight:700;
    font-size:24px;
    color:var(--text);
    letter-spacing:0.5px;
}

.tcard-cyan{ border-left-color:var(--cyan); }
.tcard-cyan .tcard-value{ color:var(--cyan); }

.tcard-violet{ border-left-color:var(--violet); }
.tcard-violet .tcard-value{ color:var(--violet); }

.tcard-teal{ border-left-color:var(--teal); }
.tcard-teal .tcard-value{ color:var(--teal); }

.tcard-amber{ border-left-color:var(--amber); }
.tcard-amber .tcard-value{ color:var(--amber); }

.tcard-red{ border-left-color:var(--red); }
.tcard-red .tcard-value{ color:var(--red); }

.pulse-red{
    animation:pulseRed 1.6s ease-in-out infinite;
}

@keyframes pulseRed{
    0%,100%{ box-shadow:0 0 0 0 rgba(255,59,78,0.0); }
    50%{ box-shadow:0 0 26px 2px rgba(255,59,78,0.35); }
}

/* ---------------- Section panels ---------------- */

.panel{
    background:var(--bg-panel);
    border:1px solid var(--border);
    border-radius:12px;
    padding:18px 20px;
    margin-top:20px;
}

.panel-header{
    display:flex;
    align-items:center;
    gap:8px;
    font-family:'Rajdhani', sans-serif;
    font-weight:700;
    font-size:15px;
    letter-spacing:1.5px;
    text-transform:uppercase;
    color:var(--text);
    margin-bottom:14px;
}

.panel-cyan{ border-left:3px solid var(--cyan); }
.panel-amber{ border-left:3px solid var(--amber); }
.panel-violet{ border-left:3px solid var(--violet); background:linear-gradient(135deg, rgba(123,97,255,0.06), rgba(0,217,255,0.03)); }
.panel-teal{ border-left:3px solid var(--teal); }
.panel-faint{ border-left:3px solid var(--border-hi); }

.object-grid{
    display:grid;
    grid-template-columns:repeat(4, 1fr);
    gap:12px;
}

.object-stat{
    background:var(--bg-panel-alt);
    border:1px solid var(--border);
    border-radius:8px;
    padding:12px 10px;
    text-align:center;
}

.object-stat .icon{ font-size:20px; }

.object-stat .num{
    font-family:'JetBrains Mono', monospace;
    font-weight:700;
    font-size:22px;
    color:var(--cyan);
    margin:4px 0 2px 0;
}

.object-stat .lbl{
    font-family:'JetBrains Mono', monospace;
    font-size:10px;
    letter-spacing:1px;
    color:var(--text-dim);
    text-transform:uppercase;
}

.panel-body{
    font-family:'Inter', sans-serif;
    font-size:14.5px;
    line-height:1.55;
    color:var(--text);
}

.panel-body.mono{
    font-family:'JetBrains Mono', monospace;
    font-size:13px;
}

.voice-active .panel-body{ color:var(--teal); font-weight:500; }
.voice-standby .panel-body{ color:var(--text-faint); }

/* ---------------- Footer bar ---------------- */

.telemetry-footer{
    display:flex;
    justify-content:flex-end;
    margin-top:10px;
}

.fps-pill{
    font-family:'JetBrains Mono', monospace;
    font-size:12px;
    color:var(--text-dim);
    background:var(--bg-panel);
    border:1px solid var(--border);
    border-radius:20px;
    padding:5px 14px;
    letter-spacing:0.5px;
}

.app-footer{
    text-align:center;
    margin-top:36px;
    padding-top:22px;
    border-top:1px solid var(--border);
}

.app-footer h3{
    font-family:'Rajdhani', sans-serif;
    font-weight:700;
    letter-spacing:1.5px;
    color:var(--text);
    margin-bottom:4px;
}

.app-footer p{
    font-family:'JetBrains Mono', monospace;
    font-size:11.5px;
    color:var(--text-faint);
    letter-spacing:0.5px;
    margin:3px 0;
}

.app-footer .credit{
    color:var(--text-dim);
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# Render helpers
# ----------------------------------------

def render_metric_card(icon, label, value, accent="cyan", extra_class=""):
    return f"""
    <div class="tcard tcard-{accent} {extra_class}">
        <div class="tcard-icon">{icon}</div>
        <div>
            <div class="tcard-label">{label}</div>
            <div class="tcard-value">{value}</div>
        </div>
    </div>
    """


def render_risk_card(risk_level):
    mapping = {
        "High":   ("red",   "🔴", "HIGH RISK",   "pulse-red"),
        "Medium": ("amber", "🟡", "MEDIUM RISK", ""),
        "Low":    ("teal",  "🟢", "LOW RISK",    ""),
    }
    accent, icon, label, anim = mapping.get(risk_level, mapping["Low"])
    return render_metric_card(icon, "RISK LEVEL", label, accent=accent, extra_class=anim)


def render_object_panel(cars, persons, trucks, bicycles):
    return f"""
    <div class="panel panel-cyan">
        <div class="panel-header">📦 Detected Objects</div>
        <div class="object-grid">
            <div class="object-stat"><div class="icon">🚗</div><div class="num">{cars}</div><div class="lbl">Cars</div></div>
            <div class="object-stat"><div class="icon">👤</div><div class="num">{persons}</div><div class="lbl">Persons</div></div>
            <div class="object-stat"><div class="icon">🚛</div><div class="num">{trucks}</div><div class="lbl">Trucks</div></div>
            <div class="object-stat"><div class="icon">🚲</div><div class="num">{bicycles}</div><div class="lbl">Bicycles</div></div>
        </div>
    </div>
    """


def render_motion_panel(motion_summary):
    return f"""
    <div class="panel panel-amber">
        <div class="panel-header">🚦 Motion Summary</div>
        <div class="panel-body">{motion_summary}</div>
    </div>
    """


def render_voice_panel(last_alert):
    if last_alert:
        return f"""
        <div class="panel panel-teal voice-active">
            <div class="panel-header">🔊 Last Voice Alert</div>
            <div class="panel-body">{last_alert}</div>
        </div>
        """
    return """
    <div class="panel panel-faint voice-standby">
        <div class="panel-header">🔇 Voice Alert</div>
        <div class="panel-body">Standby — no alert issued</div>
    </div>
    """


def render_advice_panel(advice):
    return f"""
    <div class="panel panel-violet">
        <div class="panel-header">🤖 AI Driving Advisory</div>
        <div class="panel-body">{advice}</div>
    </div>
    """


# ----------------------------------------
# Header
# ----------------------------------------

st.markdown("""
<div class="app-header">
    <div class="app-header-eyebrow">
        <span class="live-dot"></span>
        <span class="live-text">SYSTEM ONLINE</span>
    </div>
    <h1 class="app-title">AGENT<span class="accent">DRIVE</span><span class="tag">AI</span></h1>
    <p class="app-subtitle">Autonomous Perception &amp; Advisory System · YOLO11 // ByteTrack // LangChain // Groq Llama 3.3</p>
    <div class="header-rule"></div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------
# Sidebar
# ----------------------------------------

with st.sidebar:

    st.markdown('<div class="sidebar-title">🚘 SYSTEM STATUS</div>', unsafe_allow_html=True)

    status_items = [
        "YOLO11", "ByteTrack", "Scene Analyzer",
        "Risk Engine", "Motion Analyzer", "LLM", "Voice Assistant",
    ]

    status_html = '<div class="status-grid">' + "".join(
        f'<div class="status-chip"><span class="status-dot"></span>'
        f'<span class="status-label">{name}</span>'
        f'<span class="status-state">ACTIVE</span></div>'
        for name in status_items
    ) + "</div>"

    st.markdown(status_html, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-title">🎥 VIDEO INPUT</div>', unsafe_allow_html=True)

    uploaded_video = st.file_uploader(
        "Upload a Driving Video",
        type=["mp4", "avi", "mov"],
        label_visibility="collapsed",
    )

# ----------------------------------------
# Video Loading
# ----------------------------------------

if uploaded_video is not None:

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp4"
    )

    temp_file.write(uploaded_video.read())

    video_path = temp_file.name

    st.sidebar.success("Uploaded Video Loaded")

else:

    video_path = "videos/road.mp4"

    st.sidebar.info("Using Demo Video")

# ----------------------------------------
# Initialize Pipeline
# ----------------------------------------

pipeline = AgentDrivePipeline()

video = cv2.VideoCapture(video_path)

# ----------------------------------------
# Dashboard Placeholders
# ----------------------------------------

st.markdown("""
<div class="video-eyebrow">
    <span><span class="rec">●</span> LIVE FEED — PERCEPTION OVERLAY</span>
    <span id="video-src-label">SRC: DASHCAM_01</span>
</div>
""", unsafe_allow_html=True)

video_placeholder = st.empty()

metric1, metric2, metric3 = st.columns(3)

traffic_placeholder = metric1.empty()

risk_placeholder = metric2.empty()

objects_placeholder = metric3.empty()

object_placeholder = st.empty()

motion_placeholder = st.empty()

voice_placeholder = st.empty()

advice_placeholder = st.empty()

fps_placeholder = st.empty()

# ==========================================
# Main Processing Loop
# ==========================================

previous_time = time.time()

while video.isOpened():

    success, frame = video.read()

    if not success:

        # Restart the demo video automatically
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # --------------------------------------
    # Run Complete AI Pipeline
    # --------------------------------------

    output = pipeline.process_frame(frame)

    processed_frame = output["frame"]

    scene = output["scene"]

    risk = output["risk"]

    motion_summary = output["motion_summary"]

    advice = output["advice"]

    last_alert = output["last_alert"]

    # --------------------------------------
    # Convert BGR → RGB
    # --------------------------------------

    rgb_frame = cv2.cvtColor(
        processed_frame,
        cv2.COLOR_BGR2RGB
    )

    video_placeholder.image(
        rgb_frame,
        channels="RGB",
        use_container_width=True
    )

    # --------------------------------------
    # Object Counts
    # --------------------------------------

    counts = scene["object_counts"]

    total_objects = sum(counts.values())

    cars = counts.get("car", 0)

    persons = counts.get("person", 0)

    trucks = counts.get("truck", 0)

    bicycles = counts.get("bicycle", 0)

    # --------------------------------------
    # Traffic Card
    # --------------------------------------

    traffic_placeholder.markdown(
        render_metric_card("🚦", "TRAFFIC LEVEL", scene["traffic_level"], accent="cyan"),
        unsafe_allow_html=True,
    )

    # --------------------------------------
    # Risk Card
    # --------------------------------------

    risk_level = risk["risk_level"]

    risk_placeholder.markdown(render_risk_card(risk_level), unsafe_allow_html=True)

    # --------------------------------------
    # Total Objects
    # --------------------------------------

    objects_placeholder.markdown(
        render_metric_card("📦", "OBJECTS TRACKED", total_objects, accent="violet"),
        unsafe_allow_html=True,
    )

    # --------------------------------------
    # Individual Object Cards
    # --------------------------------------

    object_placeholder.markdown(
        render_object_panel(cars, persons, trucks, bicycles),
        unsafe_allow_html=True,
    )

    # --------------------------------------
    # Motion Summary
    # --------------------------------------

    motion_placeholder.markdown(
        render_motion_panel(motion_summary),
        unsafe_allow_html=True,
    )

    # --------------------------------------
    # Last Voice Alert
    # --------------------------------------

    voice_placeholder.markdown(
        render_voice_panel(last_alert),
        unsafe_allow_html=True,
    )

    # --------------------------------------
    # AI Driving Advice
    # --------------------------------------

    advice_placeholder.markdown(
        render_advice_panel(advice),
        unsafe_allow_html=True,
    )

    # --------------------------------------
    # FPS Counter
    # --------------------------------------

    current_time = time.time()

    fps = 1 / (current_time - previous_time)

    previous_time = current_time

    fps_placeholder.markdown(
        f"""<div class="telemetry-footer"><span class="fps-pill">🎥 FPS {fps:.1f}</span></div>""",
        unsafe_allow_html=True,
    )

    # --------------------------------------
    # Small Delay
    # --------------------------------------

    time.sleep(0.01)

# ==========================================
# Cleanup
# ==========================================

video.release()

# ==========================================
# Footer
# ==========================================

st.markdown(
    """
<div class="app-footer">
    <h3>🚗 AGENTDRIVE AI</h3>
    <p>Industry-Level AI Driving Assistant</p>
    <p>YOLO11 · ByteTrack · LangChain · Groq Llama 3.3 · Microsoft Edge TTS</p>
    <p class="credit">Built by Chethan M S</p>
</div>
""",
    unsafe_allow_html=True
)