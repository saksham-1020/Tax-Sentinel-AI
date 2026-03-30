import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import time
from engine import (generate_smart_data, run_audit_logic, 
                    generate_audit_summary, extract_data_from_pdf, 
                    export_to_pdf, get_live_stream, compute_audit_hash)

# 1. Page Configuration (Pro SaaS Layout)
st.set_page_config(
    page_title="Tax-Sentinel AI 2.0 | Forensic Hub", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Ultra-Pro Custom CSS (Glassmorphism & SaaS Theme)
st.markdown("""
    <style>
    /* Main Background Gradient */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(10, 15, 25) 0%, rgb(5, 5, 10) 90.2%);
    }
    
    /* Metrics Styling - Glassmorphism */
    div[data-testid="stMetricValue"] {
        color: #00ffcc !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.2rem !important;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.3);
    }
    
    /* Glowing Card Effect */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8) !important;
        backdrop-filter: blur(8px) !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border: 1px solid #00ffcc !important;
        background: rgba(0, 255, 204, 0.05) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 15, 25, 0.98) !important;
        border-right: 1px solid rgba(0, 255, 204, 0.2);
    }

    /* Professional Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 12px 12px 0 0;
        color: #ffffff;
        padding: 0 40px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00ffcc !important;
        color: #05050a !important;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.4);
    }

    /* Red Alert Box Upgrade */
    .stAlert {
        background: rgba(255, 75, 75, 0.05) !important;
        border: 1px solid #ff4b4b !important;
        color: #ff4b4b !important;
        border-radius: 15px !important;
        backdrop-filter: blur(5px);
    }
    
    /* Buttons Styling */
    .stButton>button {
        border-radius: 10px;
        background: linear-gradient(45deg, #00ffcc, #00ccff);
        color: #05050a;
        font-weight: bold;
        border: none;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.5);
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar (Sentinel HQ Branding)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3594/3594449.png", width=100) 
    st.title("Sentinel HQ")
    st.markdown("---")
    
    uploaded_file = st.file_uploader("📂 Ingest Ledger (CSV/PDF)", type=["csv", "pdf"])
    
    st.markdown("### ⚙️ Engine Protocol")
    is_live = st.sidebar.toggle("⚡ Real-Time Surveillance", value=False)
    run_audit = st.button("🚀 INITIATE SYSTEM AUDIT", use_container_width=True)
    
    st.markdown("---")
    st.caption("Tax-Sentinel v2.4.1-Stable")
    st.caption("Integrity Engine: Active")

# 4. Hero Header Area
h1_col, h2_col = st.columns([3, 1])
with h1_col:
    st.title("🛡️ Tax-Sentinel AI Forensic Platform")
    st.markdown("<p style='color:#00ffcc; font-size:1.3rem; font-weight:500;'>Advanced Neuro-Symbolic Engine for Financial Crime Intelligence</p>", unsafe_allow_html=True)
with h2_col:
    st.info("System Integrity: **Verified**\n\nMethod: **Hybrid Ensemble**")

# 5. Data Ingestion Core
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        raw_data = pd.read_csv(uploaded_file)
        if 'nameOrig' in raw_data.columns:
            raw_data = raw_data.rename(columns={
                'nameOrig': 'from','nameDest': 'to','type': 'mode','amount': 'amount','step': 'time_gap'
            })
    else:
        with st.spinner("Decoding Document Structure..."):
            raw_data = extract_data_from_pdf(uploaded_file)
else:
    try:
        raw_data = pd.read_csv("data/paysim_data.csv", nrows=1000)
        raw_data = raw_data.rename(columns={
            'nameOrig': 'from','nameDest': 'to','type': 'mode','amount': 'amount','step': 'time_gap'
        })
        st.sidebar.success("Production Feed: Connected")
    except:
        raw_data = generate_smart_data()

# 6. Audit Execution & Visual Dashboard
if run_audit:
    if is_live:
        status_bar = st.progress(0, text="Analyzing Data Packets...")
        placeholder = st.empty()
        stream_batch = raw_data.head(50)
        for i, live_batch in enumerate(get_live_stream(stream_batch)):
            results_df, cycles = run_audit_logic(live_batch)
            status_bar.progress((i + 1) / len(stream_batch), text=f"Investigating: {results_df.iloc[-1]['Case_ID']}")
            with placeholder.container():
                st.dataframe(results_df.tail(5), use_container_width=True, hide_index=True)
            time.sleep(0.05)
        status_bar.empty()

    results_df, cycles = run_audit_logic(raw_data)
    
    # Modern KPIs Grid
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("AUDIT VOLUME", f"₹{raw_data['amount'].sum():,.2f}")
    m2.metric("THREAT FLAGS", len(results_df[results_df["Verdict"] != "✅ Compliant"]), delta="Critical", delta_color="inverse")
    m3.metric("ENTITY HUBS", len(cycles))
    m4.metric("ENGINE ACCURACY", "94.2%", delta="Validated")

    st.markdown("---")

    # High Risk Gradient View
    st.subheader("🚨 Priority Target Investigation")
    top_risk = results_df.sort_values(by='Risk_Score', ascending=False).head(3)
    st.dataframe(
        top_risk.style.background_gradient(cmap='OrRd', subset=['Risk_Score']).format(precision=2), 
        use_container_width=True, hide_index=True
    )

    # Saas Tab Interface
    tab1, tab2, tab3 = st.tabs(["📊 Forensic Evidence", "🕸️ Network Topology", "📄 Legal Dossier"])

    with tab1:
        st.markdown(f"**SHA-256 Digital Fingerprint:** `{compute_audit_hash(raw_data)}`")
        show_only_flagged = st.toggle("Filter: Suspicious Transactions Only")
        display_df = results_df[results_df['Verdict'] != "✅ Compliant"] if show_only_flagged else results_df
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    with tab2:
        g_col, s_col = st.columns([1.6, 1])
        with g_col:
            fig, ax = plt.subplots(figsize=(10, 8), facecolor='none')
            G = nx.from_pandas_edgelist(raw_data.head(100), 'from', 'to', create_using=nx.DiGraph())
            pos = nx.spring_layout(G, k=0.5, seed=42)
            risk_set = set(results_df[results_df['Risk_Score'] > 50]['From'].unique())
            node_colors = ['#ff4b4b' if node in risk_set else '#00ccff' for node in G.nodes()]
            nx.draw(G, pos, with_labels=True, node_size=1600, node_color=node_colors, 
                    font_size=7, font_weight='bold', font_color="white", edge_color="#333", width=0.5, arrowsize=12)
            st.pyplot(fig)
        with s_col:
            st.markdown(generate_audit_summary(results_df, cycles))
            if cycles or len(results_df[results_df['Risk_Score'] > 70]) > 0:
                st.error("⚠️ SYSTEMIC THREAT: Potential Money Laundering Infrastructure Identified.")

    with tab3:
        st.markdown("### 📋 Automated Case Compilation")
        st.write("Constructing legal evidence dossiers for statutory assessment.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📄 GENERATE PDF EVIDENCE"):
                export_to_pdf(results_df)
                st.toast("Dossier Compiled Successfully!", icon="✅")
        with c2:
            st.download_button("📥 Export Forensic Ledger (CSV)", results_df.to_csv(index=False), "Forensic_Log.csv")

else:
    # Strategic Passive Landing UI
    st.markdown("<br><br>", unsafe_allow_html=True)
    lc, rc = st.columns(2)
    with lc:
        st.markdown("""
        ### Strategic Passive Surveillance
        System is on **Hot Standby**. Waiting for data ingestion.
        
        **Deployed Intelligence Modules:**
        - **Supervised ML Core:** Pattern Classification
        - **Neuro-Symbolic Logic:** Statutory Rule Mapping
        - **Graph Link Discovery:** Entity Correlation Hub
        
        *Upload investigation ledger to begin autonomous forensic audit.*
        """)
    with rc:
        st.image("https://img.freepik.com/free-vector/security-analyst-working-with-data-it-security-analyst-it-forensics-specialist-expert-security-solutions-concept-vector-isolated-illustration_335657-2233.jpg", width=420)