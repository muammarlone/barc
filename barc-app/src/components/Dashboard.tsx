import React from 'react';

const Dashboard: React.FC = () => {
    return (
        <main>
            <div className="blob blob-1"></div>
            <div className="blob blob-2"></div>

            <div className="header">
                <div>
                    <h1>Compliance Overview</h1>
                    <p style={{ color: 'var(--text-dim)' }}>Monitoring BPO Onboarding: <strong>Global-Connect Inc.</strong></p>
                </div>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <div className="status-badge" style={{ background: 'rgba(16, 185, 129, 0.1)', color: 'var(--success)', border: '1px solid var(--success)' }}>
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                        KIW-CERTIFIED GOLDEN
                    </div>
                    <div className="status-badge">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        94% Overall Health
                    </div>
                </div>
            </div>

            <div className="integration-bar">
                <div className="int-item"><div className="int-dot"></div> SharePoint DMS</div>
                <div className="int-item"><div className="int-dot"></div> Exchange / Outlook</div>
                <div className="int-item"><div className="int-dot"></div> Slack Collab Hub</div>
                <div className="int-item"><div className="int-dot" style={{ background: 'var(--critical)', boxShadow: '0 0 5px var(--critical)' }}></div> BPO Legacy SFTP</div>
            </div>

            <div className="grid">
                <div className="card">
                    <h3>Technical Trust</h3>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                        <div className="gauge-container">
                            <svg className="gauge-svg" width="80" height="80">
                                <circle className="gauge-bg" cx="40" cy="40" r="35"></circle>
                                <circle className="gauge-fill" cx="40" cy="40" r="35" style={{ strokeDashoffset: 20 }}></circle>
                            </svg>
                            <div className="gauge-text">92%</div>
                        </div>
                        <div>
                            <div className="sub">Six Sigma</div>
                            <div style={{ fontWeight: 700, color: 'var(--success)' }}>T2</div>
                        </div>
                    </div>
                </div>

                <div className="card">
                    <h3>Active Gaps</h3>
                    <div className="value" style={{ color: 'var(--critical)' }}>03</div>
                    <div className="sub">Impact: High</div>
                </div>

                <div className="card">
                    <h3>DMS Assets</h3>
                    <div className="value">1.4k</div>
                    <div className="sub">Verified Docs</div>
                </div>

                <div className="card">
                    <h3>Governance Baseline</h3>
                    <div className="value" style={{ color: 'var(--success)' }}>Stable</div>
                    <div className="sub">Active RACI: Department-IT</div>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.5rem' }}>
                <div className="agent-pulse">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                        <h3 style={{ fontFamily: 'Outfit' }}>Agent Reasoning Stream</h3>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>v4.2.1-stable</div>
                    </div>
                    <div className="log">
                        [14:12:01] SYS: Ingesting doc 'BPO_NW_Standard.pdf'...<br />
                        [14:12:03] ORCHESTRATOR: Extracting constraints from <strong>Project Charter #GH-2026</strong>.<br />
                        [14:12:04] <strong>ZTA-ENGINE:</strong> Identity verified for DSA-Network. Least-privilege granted.<br />
                        [14:12:05] DMS-AGENT: Checksum verified. Ingesting to Evidence Layer.<br />
                        [14:12:08] <strong>ETHICS-AGENT:</strong> Running bias check on finding 'Circuit_Gap_01'...<br />
                        [14:12:12] PEAK-DSA: Running stress simulation for 5x demand surge...<br />
                        <span className="cursor"></span>
                    </div>
                </div>

                <div className="card" style={{ borderTop: '2px solid #a855f7' }}>
                    <h3>Integrity Center</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '1rem' }}>
                        <div className="integrity-badge badge-zt">
                            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
                            ZERO TRUST: VERIFIED
                        </div>
                        <div className="integrity-badge badge-ethical">
                            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg>
                            ETHICAL AI: 100%
                        </div>
                    </div>
                    <div className="sub">Compliance: 100% Mandate</div>
                </div>
            </div>
        </main>
    );
};

export default Dashboard;
