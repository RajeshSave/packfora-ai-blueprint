import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Packfora · AI Blueprint",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Brand Colours ──────────────────────────────────────────────────────────────
ORANGE   = "#F05A28"
DARK     = "#1A1A2E"
DARK2    = "#16213E"
CARD_BG  = "#0F3460"
WHITE    = "#FFFFFF"
MUTED    = "#A0AEC0"
GREEN    = "#38A169"
AMBER    = "#D69E2E"
RED      = "#E53E3E"
BLUE     = "#3182CE"
TEAL     = "#319795"
PURPLE   = "#805AD5"

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600&display=swap');

  /* Global */
  html, body, [class*="css"] {{
    font-family: 'Outfit', sans-serif;
    background-color: {DARK};
    color: {WHITE};
  }}
  .main .block-container {{ padding-top: 0rem; padding-bottom: 2rem; max-width: 100%; }}

  /* Sidebar — FIX: do not hide header so toggle button stays visible */
  section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {DARK2} 0%, {DARK} 100%);
    border-right: 1px solid rgba(240,90,40,0.2);
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
  }}
  section[data-testid="stSidebar"] * {{
    color: {WHITE} !important;
    visibility: visible !important;
  }}
  section[data-testid="stSidebar"] .stSelectbox label,
  section[data-testid="stSidebar"] .stMultiSelect label {{ color: {ORANGE} !important; font-weight: 600; font-size:0.78rem; letter-spacing:0.08em; text-transform:uppercase; }}

  /* Selectbox & multiselect dropdowns */
  .stSelectbox > div > div, .stMultiSelect > div > div {{
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(240,90,40,0.3) !important;
    border-radius: 8px !important;
    color: {WHITE} !important;
  }}

  /* Header bar */
  .header-bar {{
    background: linear-gradient(135deg, {DARK2} 0%, {DARK} 60%, rgba(240,90,40,0.08) 100%);
    border-bottom: 2px solid {ORANGE};
    padding: 1rem 2rem 0.8rem;
    display: flex; align-items: center; gap: 1.5rem;
    margin-bottom: 0;
  }}
  .header-logo {{ height: 48px; }}
  .header-title {{ font-family: 'Space Grotesk', sans-serif; font-size: 1.6rem; font-weight: 700; color: {WHITE}; line-height:1.1; }}
  .header-sub {{ font-size: 0.82rem; color: {ORANGE}; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; margin-top:2px; }}

  /* Vision card — FIX: brighter text colour */
  .vision-card {{
    background: linear-gradient(135deg, rgba(240,90,40,0.12) 0%, rgba(15,52,96,0.4) 100%);
    border: 1px solid rgba(240,90,40,0.35);
    border-left: 4px solid {ORANGE};
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    margin: 1rem 0 1.2rem;
    font-size: 0.88rem;
    line-height: 1.7;
    color: #FFFFFF;
  }}
  .vision-card .vision-title {{ font-size:1rem; font-weight:700; color:{ORANGE}; margin-bottom:6px; letter-spacing:0.04em; }}

  /* Metric cards */
  .metric-row {{ display:flex; gap:12px; margin-bottom:1.2rem; flex-wrap:wrap; }}
  .metric-card {{
    flex:1; min-width:130px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    text-align:center;
  }}
  .metric-card .m-val {{ font-size:2rem; font-weight:700; color:{ORANGE}; line-height:1; }}
  .metric-card .m-lbl {{ font-size:0.72rem; color:{MUTED}; margin-top:4px; text-transform:uppercase; letter-spacing:0.06em; }}

  /* Table styling */
  .dataframe-container {{ border-radius:12px; overflow:hidden; border:1px solid rgba(255,255,255,0.08); }}
  thead tr th {{
    background: {DARK2} !important;
    color: {ORANGE} !important;
    font-size: 0.72rem !important;
    font-weight:600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    border-bottom: 1px solid rgba(240,90,40,0.3) !important;
    padding: 10px 12px !important;
    white-space: nowrap;
  }}
  tbody tr {{ background: rgba(255,255,255,0.02) !important; }}
  tbody tr:nth-child(even) {{ background: rgba(255,255,255,0.045) !important; }}
  tbody tr:hover {{ background: rgba(240,90,40,0.08) !important; }}
  tbody tr td {{ font-size:0.8rem !important; padding:9px 12px !important; border-bottom:1px solid rgba(255,255,255,0.05) !important; vertical-align:top !important; }}

  /* Phase badges */
  .phase-badge {{
    display:inline-block; padding:2px 10px; border-radius:20px;
    font-size:0.68rem; font-weight:600; letter-spacing:0.05em;
  }}
  .phase-1 {{ background:rgba(56,161,105,0.18); color:#68D391; border:1px solid rgba(56,161,105,0.4); }}
  .phase-2 {{ background:rgba(214,158,46,0.18); color:#F6E05E; border:1px solid rgba(214,158,46,0.4); }}
  .phase-3 {{ background:rgba(240,90,40,0.18); color:#FC8181; border:1px solid rgba(240,90,40,0.4); }}

  /* Priority colours */
  .pr-critical {{ color:#FC8181; font-weight:600; }}
  .pr-high     {{ color:#68D391; font-weight:600; }}
  .pr-medium   {{ color:#F6E05E; }}
  .pr-low      {{ color:{MUTED}; }}

  /* Section header */
  .section-hdr {{
    font-family:'Space Grotesk',sans-serif;
    font-size:1.05rem; font-weight:700;
    color:{WHITE}; letter-spacing:0.02em;
    border-left:3px solid {ORANGE};
    padding-left:10px;
    margin: 1.2rem 0 0.7rem;
  }}

  /* Tab styling */
  .stTabs [data-baseweb="tab-list"] {{
    background: rgba(255,255,255,0.03);
    border-radius:10px; padding:4px; gap:4px;
  }}
  .stTabs [data-baseweb="tab"] {{
    color: {MUTED} !important;
    border-radius:8px !important;
    font-size:0.82rem !important;
    font-weight:500 !important;
    padding:8px 16px !important;
  }}
  .stTabs [aria-selected="true"] {{
    background: {ORANGE} !important;
    color: {WHITE} !important;
  }}
  .stTabs [data-baseweb="tab-panel"] {{ padding-top:1rem; }}

  /* Scrollbar */
  ::-webkit-scrollbar {{ width:6px; height:6px; }}
  ::-webkit-scrollbar-track {{ background:rgba(255,255,255,0.04); border-radius:3px; }}
  ::-webkit-scrollbar-thumb {{ background:{ORANGE}; border-radius:3px; }}

  /* FIX: only hide footer and deploy button, NOT header or MainMenu */
  footer {{ visibility:hidden; }}
  .stDeployButton {{ display:none; }}

  /* Sidebar section labels */
  .sidebar-section {{
    font-size:0.65rem; font-weight:700; color:{ORANGE};
    text-transform:uppercase; letter-spacing:0.1em;
    margin: 1.2rem 0 0.4rem; padding-bottom:4px;
    border-bottom:1px solid rgba(240,90,40,0.2);
  }}

  /* Runway timeline cards */
  .timeline-phase {{
    background: rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:14px;
    padding:1.2rem 1.4rem;
    margin-bottom:1rem;
    position:relative;
  }}
  .timeline-phase::before {{
    content:'';
    position:absolute; left:-1px; top:0; bottom:0;
    width:4px; border-radius:4px 0 0 4px;
  }}
  .tp-1::before {{ background:{GREEN}; }}
  .tp-2::before {{ background:{AMBER}; }}
  .tp-3::before {{ background:{ORANGE}; }}
  .tp-4::before {{ background:{PURPLE}; }}
  .tp-5::before {{ background:{TEAL}; }}
  .tp-label {{ font-size:0.68rem; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:4px; }}
  .tp-title {{ font-size:1rem; font-weight:700; color:{WHITE}; margin-bottom:6px; }}
  .tp-desc  {{ font-size:0.82rem; color:#FFFFFF; line-height:1.6; }}
  .tp-tags  {{ display:flex; flex-wrap:wrap; gap:6px; margin-top:10px; }}
  .tp-tag   {{ font-size:0.68rem; padding:2px 8px; border-radius:20px; background:rgba(255,255,255,0.07); color:{MUTED}; }}
</style>
""", unsafe_allow_html=True)

# ── Data ───────────────────────────────────────────────────────────────────────
DATA = [
  # HUMAN RESOURCES
  dict(Function="Human Resources", Process="Resume Screening & Shortlisting",
       Application="ML classifier ranks packaging consultants and specialists based on domain fit (material science, supply chain, design) from historical hire data. Gen AI explains match rationale to hiring managers.",
       AI_Types="ML + Gen AI (Hybrid)", Dev_Cost="Medium", Op_Cost="Low",
       Cost_Note="ML inference zero; Gen AI tokens only for summaries",
       Priority="Critical", Effort="Low", Phase=1,
       ROI="Reduces time-to-hire by 40%; critical for Packfora's 150+ expert talent model"),
  dict(Function="Human Resources", Process="Expert Attrition Prediction",
       Application="ML predicts which senior packaging experts are flight risks using engagement, tenure, project load and compensation signals — protecting Packfora's 1000+ years of collective expertise.",
       AI_Types="ML", Dev_Cost="Medium", Op_Cost="Zero",
       Cost_Note="Pure ML model; zero operational token cost after training",
       Priority="Critical", Effort="Low", Phase=1,
       ROI="Each senior expert loss costs 6-12 months to replace; model ROI is immediate"),
  dict(Function="Human Resources", Process="JD & Offer Letter Generation",
       Application="Gen AI drafts specialised job descriptions for niche packaging roles (mould engineer, sustainability lead, procurement specialist) from structured inputs.",
       AI_Types="Gen AI", Dev_Cost="Low", Op_Cost="Medium",
       Cost_Note="Per-document token cost; low volume keeps spend manageable",
       Priority="High", Effort="Low", Phase=1,
       ROI="Saves 2-3 hours per JD; frees senior leaders from admin"),
  dict(Function="Human Resources", Process="Onboarding Document Processing",
       Application="OCR + Gen AI extracts and validates onboarding documents (ID, certificates, NDA, tax forms) for new packaging consultants and associates across 21+ countries.",
       AI_Types="OCR + Gen AI", Dev_Cost="Medium", Op_Cost="Low",
       Cost_Note="OCR near-zero; Gen AI for validation exceptions only",
       Priority="High", Effort="Medium", Phase=2,
       ROI="Cuts onboarding admin from 3 days to same-day for global hires"),
  dict(Function="Human Resources", Process="L&D Pathway Recommendation",
       Application="ML recommends personalised training paths (packaging innovation, sustainability, procurement) based on consultant role, skill gaps and project history — powering Packfora's School of Packaging.",
       AI_Types="ML", Dev_Cost="Medium", Op_Cost="Zero",
       Cost_Note="Collaborative filtering; zero inference cost post-training",
       Priority="High", Effort="Medium", Phase=2,
       ROI="Directly supports Packfora's School of Packaging initiative"),
  dict(Function="Human Resources", Process="Performance Review Summarisation",
       Application="Gen AI summarises 360-degree consultant feedback; ML scores performance trends against project delivery KPIs over time.",
       AI_Types="ML + Gen AI (Hybrid)", Dev_Cost="Medium", Op_Cost="Medium",
       Cost_Note="ML handles scoring free; Gen AI only for narrative summaries",
       Priority="Medium", Effort="Medium", Phase=2,
       ROI="Reduces review cycle from weeks to days for 150+ expert team"),
  dict(Function="Human Resources", Process="HR Policy Chatbot",
       Application="RAG-based Gen AI answers employee queries on leave, benefits, policies across Packfora's global operations (5 continents, 21 countries).",
       AI_Types="Gen AI", Dev_Cost="Medium", Op_Cost="Medium",
       Cost_Note="Token cost per query; FAQ caching reduces operational spend",
       Priority="Medium", Effort="Medium", Phase=3,
       ROI="Reduces HR admin queries by 60%; critical for multi-geography workforce"),

  # PACKAGING CONSULTING (CORE BUSINESS)
  dict(Function="Packaging Consulting", Process="Packaging Brief Intelligence",
       Application="Gen AI analyses client briefs (brand, category, material, market) and auto-generates structured packaging strategy frameworks, benchmarking against global best practices.",
       AI_Types="Gen AI", Dev_Cost="Medium", Op_Cost="High",
       Cost_Note="High token cost per brief; offset by premium consulting rate saved",
       Priority="Critical", Effort="Low", Phase=1,
       ROI="Cuts brief-to-strategy time from 2 weeks to 2 days; scalable across 100+ clients"),
  dict(Function="Packaging Consulting", Process="Design-to-Value Optimisation",
       Application="ML models optimise material choices against cost, sustainability and performance vectors — core to Packfora's proprietary Design-to-Value methodology. Prescribes optimal configurations.",
       AI_Types="ML", Dev_Cost="High", Op_Cost="Zero",
       Cost_Note="Zero inference cost; huge ROI — clients saved $30M+ in material costs",
       Priority="Critical", Effort="High", Phase=1,
       ROI="Directly digitises Packfora's highest-value proprietary methodology"),
  dict(Function="Packaging Consulting", Process="Sustainability Roadmap Generation",
       Application="ML scores packaging options on carbon footprint, recyclability, regulatory compliance. Gen AI generates 2030 sustainability roadmaps tailored to client category and geography.",
       AI_Types="ML + Gen AI (Hybrid)", Dev_Cost="High", Op_Cost="Medium",
       Cost_Note="ML analysis free; Gen AI for narrative roadmap documents",
       Priority="Critical", Effort="High", Phase=2,
       ROI="Packfora already delivers sustainability roadmaps — AI multiplies delivery speed 5x"),
  dict(Function="Packaging Consulting", Process="Packaging Innovation Intelligence",
       Application="NLP + Web scraping monitors global packaging patents, material innovations, competitor launches and regulatory changes — feeds Packfora's Knowledge Centre automatically.",
       AI_Types="NLP + ML", Dev_Cost="High", Op_Cost="Low",
       Cost_Note="ML classification free; NLP processing modest token cost",
       Priority="High", Effort="High", Phase=2,
       ROI="Keeps 150+ experts current; powers Packfora's packforum insights and whitepapers"),
  dict(Function="Packaging Consulting", Process="Client Proposal Generation",
       Application="Gen AI drafts tailored client proposals from engagement templates, past case studies, and client brief inputs — covering strategy, design and delivery scope.",
       AI_Types="Gen AI", Dev_Cost="Medium", Op_Cost="Medium",
       Cost_Note="Per-proposal token cost; high ROI vs consultant hours spent",
       Priority="High", Effort="Low", Phase=1,
       ROI="Reduces proposal creation from 3 days to 3 hours per engagement"),
  dict(Function="Packaging Consulting", Process="Case Study Knowledge Mining",
       Application="RAG-based Gen AI mines Packfora's internal case studies and project archives to surface relevant precedents when consultants begin new engagements.",
       AI_Types="Gen AI", Dev_Cost="Medium", Op_Cost="Medium",
       Cost_Note="Embedding + retrieval; token cost on query only",
       Priority="High", Effort="Medium", Phase=2,
       ROI="100+ client engagements become searchable intelligence for every consultant"),

  # SUPPLY CHAIN & PROCUREMENT
  dict(Function="Supply Chain & Procurement", Process="Supplier Risk Scoring",
       Application="ML scores packaging suppliers globally on delivery reliability, financial health, sustainability credentials and geopolitical risk — critical for Packfora's Packaging Procurement service.",
       AI_Types="ML", Dev_Cost="High", Op_Cost="Zero",
       Cost_Note="Batch ML model; zero token cost after training",
       Priority="Critical", Effort="High", Phase=1,
       ROI="Direct value to Packfora's procurement clients; potential product offering"),
  dict(Function="Supply Chain & Procurement", Process="Demand & Cost Forecasting",
       Application="ML time-series models forecast packaging material prices (resin, paper, aluminium) and client order demand — enabling proactive procurement strategies.",
       AI_Types="ML", Dev_Cost="High", Op_Cost="Zero",
       Cost_Note="Zero inference cost; batch weekly forecasts",
       Priority="Critical", Effort="High", Phase=2,
       ROI="Material cost savings directly passed to clients; differentiates Packfora's procurement advisory"),
  dict(Function="Supply Chain & Procurement", Process="Purchase Order & Invoice Automation",
       Application="OCR + Gen AI extracts PO/invoice data from emails and PDFs, validates against contracts, auto-posts to systems. Workflow automation handles approval routing.",
       AI_Types="OCR + Gen AI + Automation", Dev_Cost="Medium", Op_Cost="Low",
       Cost_Note="OCR free; Gen AI validation tokens per document; automation zero cost",
       Priority="Critical", Effort="Low", Phase=1,
       ROI="Eliminates manual data entry; accelerates client billing and supplier payments"),
  dict(Function="Supply Chain & Procurement", Process="Shipment Delay Prediction",
       Application="ML predicts packaging material shipment delays from carrier, port congestion and route data — triggers automated re-routing or client alerts.",
       AI_Types="ML + Automation", Dev_Cost="High", Op_Cost="Zero",
       Cost_Note="Zero op cost; automation triggers at no cost",
       Priority="High", Effort="High", Phase=3,
       ROI="Reduces supply disruption impact for Packfora's global client base"),
  dict(Function="Supply Chain & Procurement", Process="Contract Clause Extraction",
       Application="OCR + Gen AI reads supplier and client contracts, extracts payment terms, renewal dates, sustainability clauses and SLA obligations into structured databases.",
       AI_Types="OCR + Gen AI", Dev_Cost="Medium", Op_Cost="Low",
       Cost_Note="Token cost proportional to contract volume; high ROI vs legal review time",
       Priority="High", Effort="Medium", Phase=2,
       ROI="Cuts contract review time from days to minutes across multi-country operations"),

  # MAXMOLD
  dict(Function="MaxMold (Mould Management)", Process="Predictive Mould Maintenance",
       Application="ML analyses mould cycle counts, temperature, pressure and dimensional data to predict maintenance needs before failures occur — core intelligence for Packfora's MaxMold product.",
       AI_Types="ML", Dev_Cost="High", Op_Cost="Zero",
       Cost_Note="Edge ML on IoT sensor data; near-zero inference cost at scale",
       Priority="Critical", Effort="High", Phase=2,
       ROI="Directly monetisable within MaxMold SaaS product; reduces client downtime by 30-50%"),
  dict(Function="MaxMold (Mould Management)", Process="Mould Lifecycle Analytics",
       Application="ML tracks mould performance over full lifecycle, predicts end-of-life, benchmarks across client portfolio and recommends refurbishment vs replace decisions.",
       AI_Types="ML + Gen AI (Hybrid)", Dev_Cost="High", Op_Cost="Low",
       Cost_Note="ML analytics free; Gen AI for management reports on demand",
       Priority="Critical", Effort="High", Phase=2,
       ROI="Extends mould life 20-30%; significant capex savings for packaging manufacturers"),
  dict(Function="MaxMold (Mould Management)", Process="Mould Specification OCR",
       Application="OCR + Gen AI digitises legacy mould drawings, specifications and maintenance logs into MaxMold's structured database — enabling AI analytics on historical data.",
       AI_Types="OCR + Gen AI", Dev_Cost="Medium", Op_Cost="Low",
       Cost_Note="One-time batch digitisation; low ongoing token cost",
       Priority="High", Effort="Medium", Phase=1,
       ROI="Unlocks historical data for MaxMold analytics; accelerates client onboarding"),

  # SALES & MARKETING
  dict(Function="Sales & Marketing", Process="Client Lead Scoring",
       Application="ML scores inbound leads (brand owners, packaging manufacturers) on conversion probability using industry, company size, packaging maturity and engagement signals.",
       AI_Types="ML", Dev_Cost="Medium", Op_Cost="Zero",
       Cost_Note="Zero inference cost; runs on CRM data nightly",
       Priority="Critical", Effort="Low", Phase=1,
       ROI="Focuses Packfora's senior partner time on highest-value prospects"),
  dict(Function="Sales & Marketing", Process="Personalised Thought Leadership",
       Application="Gen AI generates personalised packaging insights, whitepapers and LinkedIn content tailored to target client segments (food, pharma, FMCG, automotive).",
       AI_Types="Gen AI", Dev_Cost="Low", Op_Cost="Medium",
       Cost_Note="Per-piece token cost; batch generation reduces spend",
       Priority="High", Effort="Low", Phase=1,
       ROI="Amplifies Packfora's Knowledge Centre and packforum brand building at scale"),
  dict(Function="Sales & Marketing", Process="Client Churn Prediction",
       Application="ML predicts which retainer clients show disengagement signals — enabling proactive relationship management before renewal.",
       AI_Types="ML + Automation", Dev_Cost="Medium", Op_Cost="Zero",
       Cost_Note="Zero inference cost; automation triggers relationship outreach",
       Priority="High", Effort="Low", Phase=2,
       ROI="Protecting multi-year client relationships is Packfora's core commercial model"),
  dict(Function="Sales & Marketing", Process="Competitive Intelligence Monitor",
       Application="NLP monitors competitor activity, packaging trends and regulatory changes across geographies — auto-summarises weekly for business development team.",
       AI_Types="NLP", Dev_Cost="Medium", Op_Cost="Low",
       Cost_Note="Classifier free; modest token cost for weekly digests",
       Priority="Medium", Effort="Medium", Phase=3,
       ROI="Keeps Packfora ahead of market shifts across 21 countries"),

  # FINANCE
  dict(Function="Finance", Process="Project Revenue Forecasting",
       Application="ML forecasts consulting project revenue by engagement type, duration and consultant utilisation — enabling accurate financial planning for Packfora's 65% CAGR growth trajectory.",
       AI_Types="ML", Dev_Cost="Medium", Op_Cost="Zero",
       Cost_Note="Zero inference cost; weekly batch forecasts",
       Priority="Critical", Effort="Medium", Phase=1,
       ROI="Critical for managing growth at Rs 35.5Cr revenue with 65% CAGR"),
  dict(Function="Finance", Process="Invoice Processing & AP Automation",
       Application="OCR + Gen AI extracts vendor invoice data; workflow automation routes approvals and posts to accounting system — zero manual touch for standard invoices.",
       AI_Types="OCR + Gen AI + Automation", Dev_Cost="Medium", Op_Cost="Low",
       Cost_Note="OCR free; Gen AI for exceptions; automation zero cost per-run",
       Priority="Critical", Effort="Low", Phase=1,
       ROI="Eliminates finance bottlenecks as Packfora scales across 21 countries"),
  dict(Function="Finance", Process="Expense Anomaly Detection",
       Application="ML detects suspicious expense claims or billing anomalies across multi-geography operations using pattern recognition on transaction history.",
       AI_Types="ML", Dev_Cost="Medium", Op_Cost="Zero",
       Cost_Note="Pure ML; zero operational cost",
       Priority="High", Effort="Low", Phase=2,
       ROI="Protects financial integrity as headcount and project volume scales"),
  dict(Function="Finance", Process="Financial Narrative Generation",
       Application="Gen AI converts management accounts and project P&L data into board-ready commentary and investor narrative for Packfora's leadership team.",
       AI_Types="Gen AI", Dev_Cost="Low", Op_Cost="Medium",
       Cost_Note="Monthly cadence limits token spend; high-value time saving",
       Priority="Medium", Effort="Low", Phase=3,
       ROI="Saves co-founders 8-10 hours per month on financial reporting"),

  # IT & OPERATIONS
  dict(Function="IT & Operations", Process="IT Helpdesk Automation",
       Application="Gen AI chatbot resolves common IT requests (access, VPN, M365) for Packfora's distributed global team — escalates complex issues to IT support.",
       AI_Types="Gen AI + Automation", Dev_Cost="Medium", Op_Cost="Medium",
       Cost_Note="Token cost per session; automation handles simple flows free",
       Priority="High", Effort="Low", Phase=2,
       ROI="Reduces IT friction for globally distributed 150+ expert workforce"),
  dict(Function="IT & Operations", Process="Cybersecurity Threat Detection",
       Application="ML analyses network and user behaviour logs to detect anomalies and potential breaches — critical for protecting Packfora's confidential client IP and proprietary methodologies.",
       AI_Types="ML", Dev_Cost="High", Op_Cost="Zero",
       Cost_Note="Stream ML; negligible inference cost",
       Priority="Critical", Effort="High", Phase=3,
       ROI="Protects Packfora's strategic client data and proprietary Design-to-Value methodology"),
  dict(Function="IT & Operations", Process="Knowledge Management & Search",
       Application="RAG-based Gen AI enables consultants to search across all internal documents, case studies, methodologies, and client reports with natural language queries.",
       AI_Types="Gen AI", Dev_Cost="High", Op_Cost="Medium",
       Cost_Note="Embedding cost one-time; query token cost ongoing",
       Priority="Critical", Effort="High", Phase=2,
       ROI="Makes Packfora's 1000+ years of collective expertise instantly searchable"),
]

df = pd.DataFrame(DATA)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding:1rem 0 0.5rem;">
      <img src="https://packfora.com/assets/img/packfora-white-logo.png"
           style="max-height:52px; max-width:90%; object-fit:contain;"
           onerror="this.style.display='none';document.getElementById('logo-fallback').style.display='block'"/>
      <div id="logo-fallback" style="display:none; font-family:'Space Grotesk',sans-serif;
           font-size:1.3rem; font-weight:700; color:{ORANGE};">PACKFORA</div>
      <div style="font-size:0.62rem; color:{MUTED}; letter-spacing:0.12em; text-transform:uppercase; margin-top:4px;">
        Make Your Packaging Shine
      </div>
    </div>
    <hr style="border:none; border-top:1px solid rgba(240,90,40,0.2); margin:0.8rem 0;"/>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="sidebar-section">🎯 Filter by Function</div>', unsafe_allow_html=True)
    all_fns = sorted(df["Function"].unique().tolist())
    fn_sel = st.multiselect("Function", all_fns, default=all_fns, label_visibility="collapsed")

    st.markdown(f'<div class="sidebar-section">🤖 Filter by AI Type</div>', unsafe_allow_html=True)
    all_ai = ["ML", "Gen AI", "Hybrid", "OCR + Gen AI", "Automation", "NLP"]
    ai_sel = st.multiselect("AI Type", all_ai, default=all_ai, label_visibility="collapsed")

    st.markdown(f'<div class="sidebar-section">🚦 Filter by Priority</div>', unsafe_allow_html=True)
    pr_sel = st.multiselect("Priority", ["Critical","High","Medium","Low"],
                            default=["Critical","High","Medium","Low"], label_visibility="collapsed")

    st.markdown(f'<div class="sidebar-section">💰 Filter by Operational Cost</div>', unsafe_allow_html=True)
    op_sel = st.multiselect("Op Cost", ["Zero","Low","Medium","High"],
                            default=["Zero","Low","Medium","High"], label_visibility="collapsed")

    st.markdown(f'<div class="sidebar-section">📅 Filter by Phase</div>', unsafe_allow_html=True)
    ph_sel = st.multiselect("Phase", [1,2,3], default=[1,2,3], label_visibility="collapsed",
                            format_func=lambda x: f"Phase {x}")

    st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.08);margin:1rem 0'/>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.7rem; color:{MUTED}; line-height:1.6;">
      <b style="color:{ORANGE};">Dev Cost</b> is one-time investment<br>
      <b style="color:{ORANGE};">Op Cost</b> is ongoing per-use spend<br>
      <span style="color:#68D391">&#9632;</span> Zero — pure ML models<br>
      <span style="color:#F6E05E">&#9632;</span> Low — OCR + selective tokens<br>
      <span style="color:{ORANGE}">&#9632;</span> Medium — moderate Gen AI<br>
      <span style="color:#FC8181">&#9632;</span> High — heavy Gen AI volume
    </div>
    """, unsafe_allow_html=True)

# ── Apply Filters ──────────────────────────────────────────────────────────────
def ai_match(row_ai, sel):
    r = row_ai.lower()
    for s in sel:
        smap = {"ML":"ml","Gen AI":"gen ai","Hybrid":"hybrid",
                "OCR + Gen AI":"ocr","Automation":"automation","NLP":"nlp"}
        if smap.get(s,"").lower() in r:
            return True
    return False

mask = (
    df["Function"].isin(fn_sel) &
    df["Priority"].isin(pr_sel) &
    df["Op_Cost"].isin(op_sel) &
    df["Phase"].isin(ph_sel) &
    df["AI_Types"].apply(lambda x: ai_match(x, ai_sel))
)
filtered = df[mask].copy()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="header-bar">
  <img src="https://packfora.com/assets/img/packfora-white-logo.png"
       class="header-logo"
       onerror="this.style.display='none'"/>
  <div>
    <div class="header-title">AI Transformation Blueprint</div>
    <div class="header-sub">Packfora · Packaging Intelligence · 3-Year AI Runway 2025–2028</div>
  </div>
  <div style="margin-left:auto; text-align:right; font-size:0.75rem; color:{MUTED};">
    <div style="font-size:1.1rem; font-weight:700; color:{ORANGE};">{len(filtered)}</div>
    <div>Use Cases</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Vision Card ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="vision-card">
  <div class="vision-title">🚀 Packfora AI Vision — Packaging Intelligence 2028</div>
  Packfora will become the world's first <b>AI-native packaging consulting firm</b> — embedding intelligence across every dimension of the packaging value chain.
  Drawing on 1000+ years of collective expert knowledge and 100+ client engagements across 21 countries,
  Packfora's AI strategy follows three principles: <b>Zero-cost ML</b> for predictions and prescriptions across procurement,
  supply chain and talent; <b>Hybrid models</b> to reduce Gen AI token spend while delivering intelligent outputs;
  and <b>Gen AI + OCR</b> to eliminate manual work and scale consulting delivery without scaling headcount.
  The MaxMold product line will be the first fully AI-powered SaaS offering, and the School of Packaging will be
  powered by personalised ML-driven learning paths.
</div>
""", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋  AI Use Case Blueprint",
    "📊  Analytics & Insights",
    "🗓️  3-Year Implementation Runway",
    "💡  Priority Quick Wins",
    "📖  AI Glossary",
])

# ─────────────────────────── TAB 1: MAIN TABLE ──────────────────────────────
with tab1:
    zero_cnt   = len(filtered[filtered["Op_Cost"]=="Zero"])
    crit_cnt   = len(filtered[filtered["Priority"]=="Critical"])
    hybrid_cnt = len(filtered[filtered["AI_Types"].str.contains("Hybrid",na=False)])
    ph1_cnt    = len(filtered[filtered["Phase"]==1])

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card"><div class="m-val">{len(filtered)}</div><div class="m-lbl">Total Use Cases</div></div>
      <div class="metric-card"><div class="m-val" style="color:#68D391">{zero_cnt}</div><div class="m-lbl">Zero Op Cost (ML)</div></div>
      <div class="metric-card"><div class="m-val" style="color:#FC8181">{crit_cnt}</div><div class="m-lbl">Critical Priority</div></div>
      <div class="metric-card"><div class="m-val" style="color:#B794F4">{hybrid_cnt}</div><div class="m-lbl">Hybrid (Cost Savers)</div></div>
      <div class="metric-card"><div class="m-val" style="color:#F6E05E">{ph1_cnt}</div><div class="m-lbl">Phase 1 (Year 1)</div></div>
    </div>
    """, unsafe_allow_html=True)

    if filtered.empty:
        st.info("No use cases match the selected filters. Adjust the sidebar filters.")
    else:
        display = filtered[[
            "Function","Process","Application","AI_Types",
            "Dev_Cost","Op_Cost","Priority","Phase","ROI"
        ]].copy()

        display.columns = [
            "Function","Use Case / Process","AI Application Detail","AI Type(s)",
            "Dev Cost","Op Cost","Priority","Phase","ROI / Business Value"
        ]

        # FIX: use .map() instead of deprecated .applymap()
        def style_priority(val):
            colours = {"Critical":"color:#FC8181;font-weight:700",
                       "High":"color:#68D391;font-weight:700",
                       "Medium":"color:#F6E05E","Low":"color:#A0AEC0"}
            return colours.get(val,"")

        def style_opcost(val):
            colours = {"Zero":"color:#68D391","Low":"color:#C6F6D5",
                       "Medium":"color:#F6AD55","High":"color:#FC8181"}
            return colours.get(val,"")

        def style_phase(val):
            colours = {1:"color:#68D391",2:"color:#F6E05E",3:"color:#FC8181"}
            return colours.get(val,"")

        styled = display.style\
            .map(style_priority, subset=["Priority"])\
            .map(style_opcost, subset=["Op Cost"])\
            .map(style_phase, subset=["Phase"])\
            .set_properties(**{
                "background-color":"rgba(255,255,255,0.02)",
                "color":"#E2E8F0",
                "font-size":"0.8rem",
                "border":"1px solid rgba(255,255,255,0.05)",
            })\
            .set_table_styles([
                {"selector":"thead th","props":[
                    ("background-color",DARK2),("color",ORANGE),
                    ("font-size","0.72rem"),("font-weight","600"),
                    ("text-transform","uppercase"),("letter-spacing","0.06em"),
                    ("border-bottom",f"1px solid {ORANGE}"),("padding","10px 12px"),
                ]},
                {"selector":"tbody tr:hover","props":[("background-color","rgba(240,90,40,0.06)")]},
                {"selector":"td","props":[("padding","9px 12px"),("vertical-align","top"),("line-height","1.5")]},
            ])\
            .hide(axis="index")

        st.dataframe(
            display,
            use_container_width=True,
            height=min(60 + len(display)*55, 620),
            hide_index=True,
            column_config={
                "Function":              st.column_config.TextColumn("Function", width=130),
                "Use Case / Process":    st.column_config.TextColumn("Use Case", width=160),
                "AI Application Detail": st.column_config.TextColumn("AI Application", width=280),
                "AI Type(s)":            st.column_config.TextColumn("AI Type(s)", width=140),
                "Dev Cost":              st.column_config.TextColumn("Dev Cost", width=80),
                "Op Cost":               st.column_config.TextColumn("Op Cost", width=80),
                "Priority":              st.column_config.TextColumn("Priority", width=80),
                "Phase":                 st.column_config.NumberColumn("Phase", width=60, format="%d"),
                "ROI / Business Value":  st.column_config.TextColumn("ROI / Business Value", width=280),
            }
        )

        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download Full Blueprint (CSV)", csv, "packfora_ai_blueprint.csv", "text/csv")

# ─────────────────────────── TAB 2: ANALYTICS ───────────────────────────────
with tab2:
    if filtered.empty:
        st.info("No data to visualise with current filters.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="section-hdr">Use Cases by Function</div>', unsafe_allow_html=True)
            fn_count = filtered["Function"].value_counts().reset_index()
            fn_count.columns = ["Function","Count"]
            fig1 = px.bar(fn_count, x="Count", y="Function", orientation="h",
                          color="Count", color_continuous_scale=[[0,"#1A1A2E"],[0.5,"#c94a1e"],[1,ORANGE]],
                          template="plotly_dark")
            fig1.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False, margin=dict(l=0,r=0,t=0,b=0),
                yaxis=dict(tickfont=dict(size=11), gridcolor="rgba(255,255,255,0.05)"),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)"), height=300,
                font=dict(family="Outfit",color=WHITE),
            )
            fig1.update_traces(marker_line_width=0)
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.markdown('<div class="section-hdr">Priority Distribution</div>', unsafe_allow_html=True)
            pr_count = filtered["Priority"].value_counts().reset_index()
            pr_count.columns = ["Priority","Count"]
            colour_map = {"Critical":"#FC8181","High":"#68D391","Medium":"#F6E05E","Low":"#A0AEC0"}
            fig2 = px.pie(pr_count, values="Count", names="Priority",
                          color="Priority", color_discrete_map=colour_map,
                          hole=0.55, template="plotly_dark")
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0,r=0,t=0,b=0), height=300,
                legend=dict(font=dict(size=11,color=WHITE)),
                font=dict(family="Outfit",color=WHITE),
            )
            fig2.update_traces(textfont_size=12)
            st.plotly_chart(fig2, use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            st.markdown('<div class="section-hdr">Operational Cost Distribution</div>', unsafe_allow_html=True)
            op_count = filtered["Op_Cost"].value_counts().reset_index()
            op_count.columns = ["Op_Cost","Count"]
            cost_colours = {"Zero":"#68D391","Low":"#F6E05E","Medium":"#F6AD55","High":"#FC8181"}
            fig3 = px.bar(op_count, x="Op_Cost", y="Count",
                          color="Op_Cost", color_discrete_map=cost_colours,
                          template="plotly_dark", text="Count")
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False, margin=dict(l=0,r=0,t=10,b=0), height=260,
                xaxis=dict(gridcolor="rgba(0,0,0,0)",title=None),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                font=dict(family="Outfit",color=WHITE),
            )
            fig3.update_traces(marker_line_width=0, textposition="outside",
                               textfont=dict(size=13,color=WHITE))
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            st.markdown('<div class="section-hdr">Dev Cost vs Op Cost Matrix</div>', unsafe_allow_html=True)
            order_map = {"Zero":0,"Low":1,"Medium":2,"High":3}
            cross = filtered.groupby(["Dev_Cost","Op_Cost"]).size().reset_index(name="Count")
            cross["dev_n"] = cross["Dev_Cost"].map(order_map)
            cross["op_n"]  = cross["Op_Cost"].map(order_map)
            fig4 = px.scatter(cross, x="op_n", y="dev_n", size="Count", color="Count",
                              color_continuous_scale=[[0,DARK2],[0.5,"#c94a1e"],[1,ORANGE]],
                              template="plotly_dark",
                              hover_data={"Dev_Cost":True,"Op_Cost":True,"Count":True,
                                          "op_n":False,"dev_n":False})
            tick_labels = ["Zero","Low","Medium","High"]
            fig4.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0), height=260,
                xaxis=dict(tickvals=[0,1,2,3], ticktext=tick_labels, title="Operational Cost",
                           gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(tickvals=[0,1,2,3], ticktext=tick_labels, title="Dev Cost",
                           gridcolor="rgba(255,255,255,0.05)"),
                font=dict(family="Outfit",color=WHITE),
            )
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown('<div class="section-hdr">AI Type Distribution Across Functions</div>', unsafe_allow_html=True)
        ai_types_flat = []
        for _, row in filtered.iterrows():
            for t in ["ML","Gen AI","Hybrid","OCR + Gen AI","Automation","NLP"]:
                if t.lower() in row["AI_Types"].lower():
                    ai_types_flat.append({"Function":row["Function"], "AI_Type":t})
        if ai_types_flat:
            at_df = pd.DataFrame(ai_types_flat)
            pivot  = at_df.groupby(["Function","AI_Type"]).size().reset_index(name="Count")
            ai_colours = {
                "ML":BLUE,"Gen AI":PURPLE,"Hybrid":ORANGE,
                "OCR + Gen AI":TEAL,"Automation":AMBER,"NLP":"#D53F8C"
            }
            fig5 = px.bar(pivot, x="Function", y="Count", color="AI_Type",
                          color_discrete_map=ai_colours, barmode="stack",
                          template="plotly_dark")
            fig5.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0,r=0,t=10,b=0), height=300,
                xaxis=dict(tickangle=-25, gridcolor="rgba(0,0,0,0)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=11)),
                font=dict(family="Outfit",color=WHITE),
            )
            fig5.update_traces(marker_line_width=0)
            st.plotly_chart(fig5, use_container_width=True)

# ─────────────────────────── TAB 3: RUNWAY ──────────────────────────────────
with tab3:
    st.markdown('<div class="section-hdr">Packfora AI Implementation Runway · 2025–2028</div>', unsafe_allow_html=True)

    phases = [
        dict(num=1, cls="tp-1", years="2025 · Phase 1", label_col="#68D391",
             title="Foundation & Quick Wins — Prove the Value",
             desc="""Deploy zero-cost ML models and automation for immediate ROI. Focus on Packfora's core pain points:
             <b>resume screening</b> for packaging talent, <b>lead scoring</b> to focus senior partner time,
             <b>invoice automation</b> across 21 countries, <b>Design-to-Value ML</b> (core IP digitisation),
             and <b>client proposal Gen AI</b>. MaxMold OCR digitisation of mould specs begins.
             Estimated investment: <b>Rs 80-120 lakhs</b>. Expected savings/value unlock: <b>Rs 200-300 lakhs</b>.""",
             tags=["ML Attrition Model","Lead Scoring ML","Invoice OCR Automation","Design-to-Value ML",
                   "Proposal Gen AI","Resume Screening","Revenue Forecasting ML","Mould Spec OCR"]),
        dict(num=2, cls="tp-2", years="2026 · Phase 2 (Part 1)", label_col="#F6E05E",
             title="Intelligence Layer — Scale the Smarts",
             desc="""Deploy ML + Hybrid models that leverage Phase 1 data assets. <b>MaxMold Predictive Maintenance</b>
             becomes a monetisable SaaS feature. <b>Sustainability Roadmap Gen AI</b> digitises Packfora's highest-value
             consulting deliverable. <b>Knowledge Management RAG</b> makes 1000+ years of expertise searchable.
             <b>Supplier Risk Scoring ML</b> powers procurement advisory. <b>L&D Recommendation ML</b> supports
             School of Packaging.
             Estimated investment: <b>Rs 150-200 lakhs</b>. Expected revenue uplift: <b>Rs 400-600 lakhs</b>.""",
             tags=["MaxMold Predictive Maintenance","Sustainability Roadmap AI","Knowledge RAG System",
                   "Supplier Risk ML","Contract Extraction OCR","Client Churn ML","Packaging Innovation NLP",
                   "L&D Recommendation ML"]),
        dict(num=3, cls="tp-3", years="2027 · Phase 2 (Part 2)", label_col="#F6AD55",
             title="Client-Facing AI — Differentiate the Offering",
             desc="""Launch <b>client-facing AI tools</b> as part of Packfora's consulting deliverables.
             A <b>Packaging Intelligence Portal</b> (RAG + ML) gives clients live access to insights.
             <b>Demand and material cost forecasting</b> becomes a subscription analytics product.
             <b>HR Policy chatbot</b> and <b>IT helpdesk automation</b> mature the internal operations.
             <b>Price optimisation ML</b> added to procurement advisory. Begin building Packfora AI platform brand.
             Estimated investment: <b>Rs 200-250 lakhs</b>. New recurring revenue potential: <b>Rs 500 lakhs+</b>.""",
             tags=["Client Intelligence Portal","Material Price Forecasting","Shipment Delay Prediction",
                   "HR Chatbot","IT Helpdesk AI","Competitive Intelligence NLP","Financial Narrative Gen AI"]),
        dict(num=4, cls="tp-4", years="2027-28 · Phase 3", label_col="#B794F4",
             title="AI-Native Products — Monetise the Intelligence",
             desc="""Packfora's AI capabilities become <b>standalone product offerings</b>.
             MaxMold evolves into a full <b>AI-powered SaaS platform</b> for packaging manufacturers globally.
             A <b>Packaging Intelligence SaaS</b> product (design, sustainability, procurement analytics)
             is launched for brand owners. The <b>School of Packaging</b> becomes an AI-personalised digital
             learning platform. Cybersecurity ML protects the growing IP portfolio.
             Estimated investment: <b>Rs 300-400 lakhs</b>. SaaS ARR target: <b>Rs 1,000 lakhs+</b>.""",
             tags=["MaxMold SaaS AI Platform","Packaging Intelligence SaaS","School of Packaging AI",
                   "Cybersecurity ML","Full Automation Suite","AI Consulting Product Line"]),
        dict(num=5, cls="tp-5", years="2028+ · Vision Horizon", label_col="#81E6D9",
             title="AI-First Enterprise — Packaging Intelligence Global Leader",
             desc="""Packfora operates as a <b>fully AI-augmented consulting and product company</b>.
             Every consultant is amplified by AI — briefing intelligence, design optimisation,
             sustainability scoring, procurement analytics and client reporting are all AI-assisted.
             Packfora's proprietary AI models, trained on 10+ years of packaging data across 100+ clients
             and 21 countries, become a <b>defensible competitive moat</b> that no competitor can replicate.
             <b>Target: Top 3 global AI-native packaging consulting firm.</b>""",
             tags=["Autonomous Design Optimisation","Global Packaging AI Index","Predictive Brand Analytics",
                   "Self-Learning Procurement AI","Industry AI Standard Setter"]),
    ]

    for p in phases:
        tags_html = "".join(f'<span class="tp-tag">{t}</span>' for t in p["tags"])
        st.markdown(f"""
        <div class="timeline-phase {p['cls']}">
          <div class="tp-label" style="color:{p['label_col']}">📅 {p['years']}</div>
          <div class="tp-title">{p['title']}</div>
          <div class="tp-desc">{p['desc']}</div>
          <div class="tp-tags">{tags_html}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-hdr" style="margin-top:1.5rem">Implementation Timeline Gantt</div>', unsafe_allow_html=True)
    gantt_data = [
        dict(Task="ML Attrition & Lead Scoring", Start="2025-01-01", Finish="2025-04-01", Phase="Phase 1"),
        dict(Task="Invoice OCR Automation", Start="2025-02-01", Finish="2025-05-01", Phase="Phase 1"),
        dict(Task="Design-to-Value ML", Start="2025-03-01", Finish="2025-09-01", Phase="Phase 1"),
        dict(Task="Client Proposal Gen AI", Start="2025-04-01", Finish="2025-07-01", Phase="Phase 1"),
        dict(Task="Mould Spec OCR (MaxMold)", Start="2025-05-01", Finish="2025-08-01", Phase="Phase 1"),
        dict(Task="Revenue Forecasting ML", Start="2025-06-01", Finish="2025-10-01", Phase="Phase 1"),
        dict(Task="MaxMold Predictive Maintenance", Start="2026-01-01", Finish="2026-09-01", Phase="Phase 2"),
        dict(Task="Sustainability Roadmap AI", Start="2026-03-01", Finish="2026-10-01", Phase="Phase 2"),
        dict(Task="Knowledge RAG Platform", Start="2026-04-01", Finish="2026-12-01", Phase="Phase 2"),
        dict(Task="Supplier Risk Scoring ML", Start="2026-06-01", Finish="2026-12-01", Phase="Phase 2"),
        dict(Task="Contract Extraction OCR", Start="2026-08-01", Finish="2027-02-01", Phase="Phase 2"),
        dict(Task="Client Intelligence Portal", Start="2027-01-01", Finish="2027-08-01", Phase="Phase 3"),
        dict(Task="Material Price Forecasting", Start="2027-03-01", Finish="2027-10-01", Phase="Phase 3"),
        dict(Task="MaxMold SaaS AI Platform", Start="2027-06-01", Finish="2028-06-01", Phase="Phase 3+"),
        dict(Task="Packaging Intelligence SaaS", Start="2027-09-01", Finish="2028-06-01", Phase="Phase 3+"),
        dict(Task="School of Packaging AI", Start="2028-01-01", Finish="2028-09-01", Phase="Vision"),
    ]
    gdf = pd.DataFrame(gantt_data)
    phase_colours = {
        "Phase 1":GREEN,"Phase 2":AMBER,"Phase 3":ORANGE,"Phase 3+":RED,"Vision":PURPLE
    }
    fig_g = px.timeline(gdf, x_start="Start", x_end="Finish", y="Task",
                        color="Phase", color_discrete_map=phase_colours,
                        template="plotly_dark")
    fig_g.update_yaxes(autorange="reversed")
    fig_g.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0.15)",
        margin=dict(l=0,r=0,t=10,b=0), height=460,
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)", title=None),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(size=10)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(size=11)),
        font=dict(family="Outfit",color=WHITE),
    )
    st.plotly_chart(fig_g, use_container_width=True)

# ─────────────────────────── TAB 4: QUICK WINS ──────────────────────────────
with tab4:
    st.markdown('<div class="section-hdr">Priority Quick Wins — Start Here, Maximum Impact</div>', unsafe_allow_html=True)

    quick_wins = df[(df["Priority"]=="Critical") & (df["Phase"]==1)].copy()

    for _, row in quick_wins.iterrows():
        op_col = {"Zero":"#68D391","Low":"#F6E05E","Medium":"#F6AD55","High":"#FC8181"}.get(row["Op_Cost"],"#A0AEC0")
        st.markdown(f"""
        <div class="timeline-phase tp-1" style="margin-bottom:0.7rem;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;">
            <div>
              <div style="font-size:0.68rem;font-weight:700;color:{ORANGE};text-transform:uppercase;letter-spacing:0.08em;margin-bottom:3px;">{row['Function']}</div>
              <div style="font-size:1rem;font-weight:700;color:{WHITE};margin-bottom:4px;">{row['Process']}</div>
              <div style="font-size:0.81rem;color:#FFFFFF;line-height:1.6;max-width:680px;">{row['Application']}</div>
            </div>
            <div style="text-align:right;min-width:100px;">
              <div style="font-size:0.68rem;color:{MUTED};text-transform:uppercase;">AI Type</div>
              <div style="font-size:0.78rem;font-weight:600;color:{ORANGE};margin-bottom:6px;">{row['AI_Types']}</div>
              <div style="font-size:0.68rem;color:{MUTED};text-transform:uppercase;">Op Cost</div>
              <div style="font-size:0.9rem;font-weight:700;color:{op_col};">{row['Op_Cost']}</div>
            </div>
          </div>
          <div style="margin-top:10px;padding:8px 12px;background:rgba(240,90,40,0.1);border-radius:8px;border-left:3px solid {ORANGE};">
            <span style="font-size:0.7rem;font-weight:700;color:{ORANGE};text-transform:uppercase;">ROI Rationale · </span>
            <span style="font-size:0.8rem;color:#FFFFFF;">{row['ROI']}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top:1.5rem;padding:1rem 1.2rem;background:rgba(240,90,40,0.08);
         border:1px solid rgba(240,90,40,0.25);border-radius:12px;">
      <div style="font-size:0.85rem;font-weight:700;color:{ORANGE};margin-bottom:6px;">💡 Implementation Recommendation for Packfora</div>
      <div style="font-size:0.82rem;color:#FFFFFF;line-height:1.7;">
        Begin with the <b>6 Critical Phase 1 use cases</b> above. Five of them (ML Attrition, Lead Scoring, Revenue Forecasting,
        Expense Detection, Supplier Risk) carry <b>zero operational cost</b> — pure ML models trained once and run forever.
        The Design-to-Value ML directly digitises Packfora's core proprietary methodology and creates immediate IP value.
        Collectively these can be built in <b>6-9 months</b> with a focused data + engineering team,
        generating <b>Rs 200-400 lakhs</b> in cost savings and value unlock before Phase 2 begins.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────── TAB 5: GLOSSARY ────────────────────────────────
with tab5:
    st.markdown('<div class="section-hdr">AI Terminology Glossary — Plain English for Packfora</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.85rem;color:#FFFFFF;margin-bottom:1.2rem;line-height:1.7;">
      Every AI term used in this Blueprint is explained below in plain English, with a specific example
      of how it applies to Packfora's business. No technical background needed.
    </div>
    """, unsafe_allow_html=True)

    GLOSSARY = [
        dict(term="Machine Learning (ML)", icon="🤖", category="Core AI",
             plain="A computer that learns patterns from past data and uses them to make predictions or decisions — without being told the rules explicitly.",
             packfora="Packfora feeds historical hiring data into an ML model. It learns what makes a great packaging consultant and automatically scores future CVs — no manual shortlisting needed.",
             cost_note="Once trained, ML models run at near-zero cost — no ongoing fees per use."),
        dict(term="Generative AI (Gen AI)", icon="✍️", category="Core AI",
             plain="AI that can create new content — text, documents, summaries, proposals — by understanding context and generating human-quality output.",
             packfora="Packfora types in a client brief (e.g. 'sustainable FMCG packaging for India'). Gen AI writes a full structured strategy framework in minutes instead of 2 weeks.",
             cost_note="Charges per 'token' (roughly per word processed). More text = higher cost."),
        dict(term="Large Language Model (LLM)", icon="🧠", category="Core AI",
             plain="The engine behind Generative AI. A massive AI model trained on billions of pages of text that understands and generates language at human level. GPT-4 and Claude are examples.",
             packfora="When Packfora's proposal Gen AI writes a client document, it is powered by an LLM underneath. Packfora doesn't build this — it uses existing LLMs via API.",
             cost_note="API usage charged per token. Hybrid models reduce LLM calls to save cost."),
        dict(term="OCR (Optical Character Recognition)", icon="📄", category="Document AI",
             plain="Technology that reads text from scanned documents, PDFs, or images and converts it into editable, searchable digital data — like a very fast, accurate typist.",
             packfora="Packfora receives hundreds of supplier invoices as scanned PDFs. OCR reads every invoice automatically and extracts vendor name, amount, tax, and line items into the ERP — zero manual entry.",
             cost_note="OCR processing is very cheap — near-zero cost per document."),
        dict(term="RAG (Retrieval-Augmented Generation)", icon="🔍", category="Document AI",
             plain="A technique where AI first searches through a company's own documents to find relevant information, then generates an answer based on that — rather than guessing from general knowledge.",
             packfora="A Packfora consultant asks: 'What packaging solutions did we use for pharma blister packs in 2022?' The RAG system searches all past case studies and project files, then writes a precise answer.",
             cost_note="Embedding (indexing documents) is one-time cost. Query tokens charged per question."),
        dict(term="NLP (Natural Language Processing)", icon="💬", category="Language AI",
             plain="AI that understands, reads and interprets human language — emails, documents, social media, reports — and extracts meaning, sentiment or categories from it.",
             packfora="Packfora uses NLP to automatically read thousands of packaging regulatory updates, patents and competitor press releases — and classify which ones are relevant to which client categories.",
             cost_note="NLP classifiers are ML-based — near-zero inference cost once trained."),
        dict(term="Sentiment Analysis", icon="😊", category="Language AI",
             plain="AI that reads text (emails, reviews, feedback) and detects the emotional tone — positive, negative, neutral — or urgency level.",
             packfora="Packfora's support team receives client emails. Sentiment AI automatically flags messages with negative or urgent tone, pushing them to the top of the queue before a human even reads them.",
             cost_note="Lightweight classifier — near-zero cost at scale."),
        dict(term="Predictive ML / Forecasting", icon="📈", category="ML Techniques",
             plain="ML models that analyse historical patterns to predict what will happen in the future — sales, demand, prices, failures, churn.",
             packfora="Packfora feeds 3 years of packaging material price data into a forecasting model. It predicts resin and paper prices 3 months ahead, helping procurement clients buy at the right time.",
             cost_note="Batch forecasts — run weekly or monthly. Zero operational token cost."),
        dict(term="Prescriptive AI", icon="🎯", category="ML Techniques",
             plain="Goes one step beyond prediction — it not only tells you what will happen, but recommends the best action to take in response.",
             packfora="Packfora's Design-to-Value ML doesn't just score packaging options — it prescribes the optimal material, thickness and structure combination for a client's cost, weight and sustainability targets.",
             cost_note="Pure ML — zero ongoing cost after model training."),
        dict(term="Anomaly Detection", icon="🚨", category="ML Techniques",
             plain="AI that learns what 'normal' looks like in your data, and automatically flags anything unusual — suspicious transactions, equipment irregularities, security threats.",
             packfora="Packfora's finance team processes expenses across 21 countries. Anomaly detection ML flags unusual claims — duplicate invoices, out-of-policy amounts, suspicious timing — before payment.",
             cost_note="ML-based — zero operational cost once deployed."),
        dict(term="Classification (ML)", icon="🏷️", category="ML Techniques",
             plain="AI that sorts items into categories automatically — spam vs not spam, high risk vs low risk, relevant vs irrelevant.",
             packfora="Packfora classifies every inbound client enquiry into the right service category (Design-to-Value, Sustainability, Procurement, MaxMold) and routes it to the right expert team automatically.",
             cost_note="Lightweight ML classifier — near-zero cost."),
        dict(term="Computer Vision (CV)", icon="👁️", category="ML Techniques",
             plain="AI that can 'see' and interpret images or video — detecting objects, defects, patterns or reading information from visual inputs.",
             packfora="On a packaging production line, Computer Vision ML inspects every unit in real time — spotting print defects, seal failures, label misalignment — faster and more accurately than any human inspector.",
             cost_note="Runs on-device or on edge hardware — very low inference cost at scale."),
        dict(term="Hybrid AI Model", icon="🔀", category="Architecture",
             plain="A smart combination of ML and Gen AI — using ML for the heavy analytical work (free) and only calling Gen AI for the final human-readable output (paid). Dramatically reduces token costs.",
             packfora="Packfora's Sustainability Roadmap: ML scores 50 packaging options on carbon and recyclability (free). Only the final narrative roadmap document is written by Gen AI (small token cost). Result: 80% cheaper than pure Gen AI.",
             cost_note="Key cost strategy — use ML where possible, Gen AI only for the last mile."),
        dict(term="Workflow Automation", icon="⚙️", category="Architecture",
             plain="Software that automatically moves data, triggers actions, sends notifications and routes approvals between systems — removing manual, repetitive steps from a process.",
             packfora="When a supplier invoice is received, automation extracts the data (OCR), checks it against the PO (ML), routes it for approval (workflow), and posts it to the accounting system — all without a human touching it.",
             cost_note="Zero per-run cost once set up. Platform licence is the only spend."),
        dict(term="API (Application Programming Interface)", icon="🔌", category="Architecture",
             plain="A connector that lets two software systems talk to each other. When Packfora's app calls an AI model, it does so through an API — like a waiter taking your order to the kitchen.",
             packfora="Packfora's proposal generation tool sends a brief to Claude or GPT-4 via API, receives the generated proposal back, and displays it to the consultant — all in seconds.",
             cost_note="API usage is the source of 'token cost' — charged per call based on text volume."),
        dict(term="Token", icon="🪙", category="Cost Concepts",
             plain="The unit Gen AI providers use to measure and charge for text. Roughly 1 token = 0.75 words. Both the input (your prompt) and the output (AI's response) consume tokens.",
             packfora="A Packfora client brief of 500 words costs roughly 650 tokens to send to Gen AI. A 1,000-word proposal response costs ~1,300 tokens. At $0.003 per 1K tokens, one proposal costs under Rs 0.30.",
             cost_note="This is why high-volume Gen AI (chatbots, content) has medium-high op cost, while ML has zero."),
        dict(term="Embedding", icon="🗺️", category="Cost Concepts",
             plain="Converting documents or text into a mathematical representation (a list of numbers) that AI can search through extremely fast. The foundation of RAG knowledge search.",
             packfora="Packfora's 100+ client case studies are converted into embeddings and stored. When a consultant asks a question, the system finds the most relevant case study in milliseconds by comparing embeddings.",
             cost_note="One-time cost to embed documents. Very cheap — fractions of a penny per page."),
        dict(term="SaaS (Software as a Service)", icon="☁️", category="Business Terms",
             plain="Software delivered over the internet on a subscription basis — no installation, no servers to manage. You pay monthly or annually for access.",
             packfora="MaxMold is Packfora's path to SaaS — packaging manufacturers would pay a monthly subscription to access predictive maintenance AI, mould analytics and lifecycle dashboards online.",
             cost_note="SaaS revenue is recurring — the most valuable business model for Packfora's AI products."),
        dict(term="IoT (Internet of Things)", icon="📡", category="Data Sources",
             plain="Physical devices (sensors, machines, equipment) connected to the internet that continuously send data — temperatures, pressures, cycle counts, locations.",
             packfora="MaxMold attaches sensors to packaging moulds. These IoT sensors stream temperature, pressure and cycle count data to Packfora's ML model, which predicts when maintenance is needed before failure.",
             cost_note="IoT infrastructure is a one-time hardware cost. Data streaming is very cheap."),
        dict(term="CAGR (Compound Annual Growth Rate)", icon="📊", category="Business Terms",
             plain="The steady yearly growth rate of a business over a period of time — if a company grows from Rs 10Cr to Rs 27Cr in 3 years, the CAGR is roughly 40%.",
             packfora="Packfora is growing at 65% CAGR — one of the fastest growth rates in consulting. AI is critical to sustaining this without proportionally scaling headcount and costs.",
             cost_note="At 65% CAGR, Packfora doubles revenue every ~15 months. AI must scale operations faster than hiring can."),
    ]

    # Group by category
    categories = list(dict.fromkeys(g["category"] for g in GLOSSARY))

    for cat in categories:
        terms = [g for g in GLOSSARY if g["category"] == cat]
        cat_icons = {"Core AI":"🧩","Document AI":"📂","Language AI":"💬",
                     "ML Techniques":"⚡","Architecture":"🏗️",
                     "Cost Concepts":"💰","Business Terms":"📊","Data Sources":"📡"}
        st.markdown(f"""
        <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;
             letter-spacing:0.1em;color:{ORANGE};margin:1.4rem 0 0.6rem;
             padding-bottom:6px;border-bottom:1px solid rgba(240,90,40,0.25);">
          {cat_icons.get(cat,'📌')} {cat}
        </div>
        """, unsafe_allow_html=True)

        for g in terms:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                 border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.7rem;">

              <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <span style="font-size:1.2rem;">{g['icon']}</span>
                <span style="font-size:1rem;font-weight:700;color:{WHITE};">{g['term']}</span>
              </div>

              <div style="font-size:0.8rem;font-weight:600;color:{ORANGE};
                   text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">
                What it means
              </div>
              <div style="font-size:0.84rem;color:#FFFFFF;line-height:1.65;margin-bottom:10px;">
                {g['plain']}
              </div>

              <div style="font-size:0.8rem;font-weight:600;color:#68D391;
                   text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">
                📦 How Packfora uses it
              </div>
              <div style="font-size:0.84rem;color:#FFFFFF;line-height:1.65;margin-bottom:10px;">
                {g['packfora']}
              </div>

              <div style="background:rgba(240,90,40,0.08);border-left:3px solid {ORANGE};
                   border-radius:0 6px 6px 0;padding:6px 10px;">
                <span style="font-size:0.72rem;font-weight:700;color:{ORANGE};
                     text-transform:uppercase;">💰 Cost note · </span>
                <span style="font-size:0.78rem;color:#FFFFFF;">{g['cost_note']}</span>
              </div>

            </div>
            """, unsafe_allow_html=True)
