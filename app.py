import streamlit as st
import os
from agentic_brief import make_client, generate_brief, fact_check, today_str
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Intelligence Lab | Agentic Researcher",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;600&display=swap');
    
    :root {
        --bg-color: #FFFFFF;
        --sidebar-bg: #F8F9FA;
        --accent-primary: #0066FF;
        --accent-secondary: #7000FF;
        --text-main: #111827;
        --text-muted: #6B7280;
        --glass-bg: rgba(255, 255, 255, 0.85);
        --glass-border: rgba(229, 231, 235, 0.8);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-color);
        color: var(--text-main);
    }
    
    h1, h2, h3, .main-header {
        font-family: 'Outfit', sans-serif;
    }

    /* Limit content width for better balance */
    .block-container {
        max-width: 1000px !important;
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }

    .stApp {
        background-image: radial-gradient(circle at 50% -20%, #F0F4F8 0%, var(--bg-color) 80%);
    }
    
    /* Sidebar Overhaul */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--glass-border) !important;
    }
    
    section[data-testid="stSidebar"] .st-emotion-cache-6q9sum {
        padding: 2rem 1.5rem;
    }
    
    /* Header Animation */
    @keyframes gradientText {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary), var(--accent-primary));
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientText 6s ease infinite;
        margin-bottom: 0.2rem;
        letter-spacing: -0.04em;
    }
    
    .sub-header {
        color: var(--text-muted);
        font-size: 1.15rem;
        margin-bottom: 2.5rem;
        font-weight: 300;
        line-height: 1.6;
    }

    /* Section Labels */
    .section-label {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.1em;
        color: var(--accent-primary);
        margin-bottom: 0.8rem;
        text-transform: uppercase;
    }

    /* Glassmorphism Input & Buttons */
    .stTextInput>div>div>input {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border) !important;
        color: var(--text-main) !important;
        border-radius: 12px !important;
        padding: 1.2rem !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 25px rgba(0, 102, 255, 0.15) !important;
    }
    
    /* Button Alignment & Center */
    .stButton {
        display: flex;
        justify-content: flex-start;
        margin-top: 1rem;
    }

    .stButton>button {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
        color: white !important;
        border: none !important;
        padding: 0.85rem 3rem !important;
        border-radius: 100px !important;
        font-weight: 600 !important;
        font-family: 'Outfit', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.9rem !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 10px 25px rgba(0, 102, 255, 0.2) !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.05) translateY(-3px);
        box-shadow: 0 15px 35px rgba(112, 0, 255, 0.3) !important;
    }

    /* Results Cards Polish */
    .result-container {
        margin-top: 3rem;
        animation: fadeIn 0.8s ease-out;
    }

    .result-card {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        padding: 2.5rem;
        border-radius: 24px;
        border: 1px solid var(--glass-border);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.05);
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Tabs Styling Polish */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent !important;
        border-bottom: 2px solid transparent !important;
        color: var(--text-muted) !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.05em;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--accent-primary) !important;
        border-bottom: 2px solid var(--accent-primary) !important;
    }

    /* Status Boxes Polish */
    div[data-testid="stStatus"] {
        background: rgba(0, 102, 255, 0.05) !important;
        border: 1px solid rgba(0, 102, 255, 0.1) !important;
        border-radius: 14px !important;
        margin-top: 1.5rem;
    }

    /* Footer Polishing */
    .footer-text {
        text-align: center;
        color: #9CA3AF;
        font-size: 0.75rem;
        letter-spacing: 0.25em;
        margin-top: 4rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    # Fixed icon: Using a reliable SVG path-based icon or emoji ensemble
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
        <span style="font-size: 45px;">🧠</span>
        <h2 style='font-family:Outfit; letter-spacing:-1px; margin:0; line-height:1;'>Intelligence<br>Terminal</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='color:#8B949E; font-size:0.85rem; opacity:0.8;'>v2.1 Precision Edition</p>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>SYSTEM SETTINGS</p>", unsafe_allow_html=True)
    
    model = st.selectbox(
        "AI Research Engine",
        options=["gpt-5.2", "gpt-4o", "gpt-4-turbo"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    if not os.getenv("OPENAI_API_KEY"):
        st.error("🛰️ DISCONNECTED: KEY MISSING")
    else:
        st.success("🛰️ UPLINK ESTABLISHED")
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<p style="color:#4a515a; font-size:0.7rem; font-weight:600; text-align:center;">AUTHENTICATED UNIT:<br>AGENTIC RESEARCH LABS</p>', unsafe_allow_html=True)

# Main Dashboard
st.markdown('<h1 class="main-header">Research Intelligence Lab</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced agentic synthesis for factual validation and technical summarization.</p>', unsafe_allow_html=True)

# Interaction Area
with st.container():
    st.markdown("<p class='section-label'>CORE RESEARCH OBJECTIVE</p>", unsafe_allow_html=True)
    topic = st.text_input("ENTER RESEARCH TOPIC", placeholder="Identify the core question or domain to explore...", label_visibility="collapsed")
    
    run_research = st.button("INITIATE AGENTIC LOOP")

if run_research and topic:
    try:
        with st.status("EXECUTING NEURAL PIPELINE...", expanded=True) as status:
            client = make_client()
            
            st.write("🌐 Establishing multi-node web connection...")
            brief, prev_id = generate_brief(client, topic, model)
            
            st.write("⚖️ Performing recursive fact-check pass...")
            fc = fact_check(client, brief, model, previous_response_id=prev_id)
            
            status.update(label="CYBER-SYNTHESIS COMPLETE", state="complete", expanded=False)
        
        # Display Results in a Refined Container
        st.markdown('<div class="result-container"><div class="result-card">', unsafe_allow_html=True)
        
        # Using Unicode characters instead of potentially problematic emojis for tabs
        tab1, tab2 = st.tabs(["[ ANALYSIS BRIEF ]", "[ VALIDATION AUDIT ]"])
        
        with tab1:
            st.markdown(brief)
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="EXPORT DATASET",
                data=brief + "\n\n---\n\n" + fc,
                file_name=f"research_intel_{today_str()}.md",
                mime="text/markdown"
            )
            
        with tab2:
            st.markdown(fc)
            
        st.markdown('</div></div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"PIPELINE FAILURE: {str(e)}")
elif run_research and not topic:
    st.warning("ERROR: Subject matter not specified.")

# Footer
st.markdown(
    '<p class="footer-text">INTELLIGENCE DEPLOYED // AGENTIC RESEARCH LABS © 2026</p>', 
    unsafe_allow_html=True
)
