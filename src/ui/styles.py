# src/ui/styles.py
"""
Modern, executive talent intelligence UI styling for Streamlit.
Clean, high-contrast, polished enterprise aesthetics (avoiding routine neon AI glow).
"""

CUSTOM_CSS = """
<style>
/* Import clean Inter font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* App Header Styling */
.app-header {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    color: #F8FAFC;
    padding: 1.75rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    border: 1px solid #334155;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.app-header h1 {
    font-size: 1.75rem;
    font-weight: 800;
    margin: 0;
    color: #FFFFFF;
    letter-spacing: -0.025em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.app-header p {
    font-size: 0.925rem;
    color: #94A3B8;
    margin: 0.4rem 0 0 0;
    font-weight: 400;
}

.badge-tag {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 9999px;
    background-color: #334155;
    color: #38BDF8;
    margin-right: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Metric Cards */
.metric-container {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.metric-container:hover {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
}

.metric-label {
    font-size: 0.775rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748B;
    margin-bottom: 0.35rem;
}

.metric-value {
    font-size: 1.65rem;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.2;
}

.metric-sub {
    font-size: 0.775rem;
    color: #059669;
    font-weight: 500;
    margin-top: 0.25rem;
}

.metric-sub.warning {
    color: #D97706;
}

/* Candidate Card */
.candidate-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    transition: all 0.2s ease;
}

.candidate-card:hover {
    border-color: #CBD5E1;
    box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.06);
}

.candidate-card.top-tier {
    border-left: 4px solid #059669;
}

.candidate-card.strong-tier {
    border-left: 4px solid #0284C7;
}

.candidate-card.good-tier {
    border-left: 4px solid #64748B;
}

.candidate-card.honeypot-tier {
    border-left: 4px solid #DC2626;
    background: #FFFDFD;
}

.rank-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 2rem;
    height: 2rem;
    padding: 0 0.5rem;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.85rem;
    background: #F1F5F9;
    color: #334155;
}

.rank-pill.rank-1 {
    background: #FEF3C7;
    color: #92400E;
    border: 1px solid #FCD34D;
}

.rank-pill.rank-2 {
    background: #F1F5F9;
    color: #475569;
    border: 1px solid #CBD5E1;
}

.rank-pill.rank-3 {
    background: #FFEDD5;
    color: #9A3412;
    border: 1px solid #FDBA74;
}

.score-badge {
    display: inline-block;
    padding: 0.3rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}

.score-badge.high {
    background: #ECFDF5;
    color: #047857;
    border: 1px solid #A7F3D0;
}

.score-badge.medium {
    background: #F0F9FF;
    color: #0369A1;
    border: 1px solid #BAE6FD;
}

.score-badge.moderate {
    background: #F8FAFC;
    color: #475569;
    border: 1px solid #E2E8F0;
}

.score-badge.flagged {
    background: #FEF2F2;
    color: #B91C1C;
    border: 1px solid #FECACA;
}

/* Skills Chips */
.skill-chip {
    display: inline-block;
    padding: 0.2rem 0.55rem;
    font-size: 0.75rem;
    border-radius: 6px;
    margin: 0.15rem 0.25rem 0.15rem 0;
    font-weight: 500;
}

.skill-chip.matched {
    background: #F0FDF4;
    color: #166534;
    border: 1px solid #BBF7D0;
}

.skill-chip.missing {
    background: #F8FAFC;
    color: #64748B;
    border: 1px solid #E2E8F0;
    text-decoration: line-through;
}

.skill-chip.neutral {
    background: #F1F5F9;
    color: #334155;
    border: 1px solid #E2E8F0;
}

/* Signal Badges */
.signal-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.2rem 0.5rem;
    font-size: 0.75rem;
    font-weight: 500;
    border-radius: 6px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    color: #475569;
}

.signal-pill.open-work {
    background: #ECFDF5;
    border-color: #A7F3D0;
    color: #065F46;
}

.signal-pill.fast-notice {
    background: #EFF6FF;
    border-color: #BFDBFE;
    color: #1E40AF;
}

.signal-pill.honeypot-alert {
    background: #FEF2F2;
    border-color: #FECACA;
    color: #991B1B;
    font-weight: 600;
}

/* Comparison View Column */
.compare-box {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.25rem;
    height: 100%;
}

.compare-row {
    padding: 0.5rem 0;
    border-bottom: 1px solid #F1F5F9;
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
}

.compare-row .lbl {
    color: #64748B;
    font-weight: 500;
}

.compare-row .val {
    color: #0F172A;
    font-weight: 600;
    text-align: right;
}

/* Callouts */
.callout-box {
    border-radius: 8px;
    padding: 0.85rem 1.15rem;
    margin: 0.75rem 0;
    font-size: 0.85rem;
    line-height: 1.45;
}

.callout-box.info {
    background: #F0F9FF;
    border: 1px solid #BAE6FD;
    color: #0369A1;
}

.callout-box.warning {
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    color: #92400E;
}

.callout-box.danger {
    background: #FEF2F2;
    border: 1px solid #FECACA;
    color: #991B1B;
}

.callout-box.success {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    color: #166534;
}

/* Clean Streamlit adjustments */
div[data-testid="stSidebar"] {
    background-color: #F8FAFC;
    border-right: 1px solid #E2E8F0;
}

div[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace;
}
</style>
"""
