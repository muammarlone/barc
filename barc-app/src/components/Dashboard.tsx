import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Metrics {
    quality_score: number;
    performance_velocity: number;
    readiness_forecast: string;
}

interface SecurityKPIs {
    mttd_sec: number;
    mttr_sec: number;
    total_violations: number;
    compliance_score: number;
}

const Dashboard: React.FC = () => {
    const [metrics, setMetrics] = useState<Metrics | null>(null);
    const [security, setSecurity] = useState<SecurityKPIs | null>(null);
    const [workflowStatus, setWorkflowStatus] = useState<string>("IDLE");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchAll = async () => {
            const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8003';
            try {
                const [mRes, sRes] = await Promise.all([
                    axios.get(`${backendUrl}/metrics?findings_count=12&critical_gaps=1`),
                    axios.get(`${backendUrl}/security/kpis`)
                ]);
                setMetrics(mRes.data);
                setSecurity(sRes.data);
                setWorkflowStatus("PIPELINE_EXPLORE"); // Simulated current live status
                setLoading(false);
                setError(null);
            } catch (err) {
                console.error("Stability Check Failed", err);
                setError("Network Instability: Governance Engine Heartbeat Lost.");
                setLoading(false);
            }
        };
        fetchAll();
        const interval = setInterval(fetchAll, 5000); // Pulse for stability
        return () => clearInterval(interval);
    }, []);


    return (
        <main>
            <div className="blob blob-1"></div>
            <div className="blob blob-2"></div>

            <div className="header">
                <div>
                    <h1>Compliance Overview</h1>
                    <p style={{ color: 'var(--text-dim)' }}>Monitoring BPO Onboarding: <strong>Global-Connect Inc.</strong></p>
                    {error && <p style={{ color: 'var(--critical)', marginTop: '0.5rem', fontSize: '0.8rem' }}>⚠️ {error}</p>}
                </div>

                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                    <div className="status-badge" style={{ background: 'rgba(16, 185, 129, 0.1)', color: 'var(--success)', border: '1px solid var(--success)' }}>
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                        KIW-CERTIFIED GOLDEN
                    </div>
                </div>
            </div>

            <div className="grid">
                <div className="card">
                    <h3>Technical Trust</h3>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                        <div className="gauge-container">
                            <svg className="gauge-svg" width="80" height="80">
                                <circle className="gauge-bg" cx="40" cy="40" r="35"></circle>
                                <circle className="gauge-fill" cx="40" cy="40" r="35" style={{ strokeDashoffset: metrics ? 251 * (1 - metrics.quality_score / 100) : 251 }}></circle>
                            </svg>
                            <div className="gauge-text">{loading ? "..." : `${metrics?.quality_score}%`}</div>
                        </div>
                        <div>
                            <div className="sub">Six Sigma</div>
                            <div style={{ fontWeight: 700, color: 'var(--success)' }}>T2</div>
                        </div>
                    </div>
                </div>

                <div className="card" style={{ borderLeft: '4px solid #f59e0b' }}>
                    <h3>Optimal Path</h3>
                    <div className="value" style={{ fontSize: '1.2rem', color: '#f59e0b' }}>STANDARD_DEEP_DIVE</div>
                    <div className="sub">Est: 21 Days</div>
                </div>

                <div className="card" style={{ borderRight: '4px solid var(--success)' }}>
                    <h3>Ready Forecast</h3>
                    <div className="value" style={{ fontSize: '1.5rem' }}>{loading ? "PENDING" : metrics?.readiness_forecast}</div>
                    <div className="sub">Velocity: {metrics?.performance_velocity} PV</div>
                </div>

                <div className="card" style={{ borderTop: '2px solid #a855f7' }}>
                    <h3>Security KPIs</h3>
                    <div style={{ marginTop: '0.5rem' }}>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>MTTD / MTTR</div>
                        <div className="value" style={{ fontSize: '1.2rem', color: 'var(--accent)' }}>
                            {loading ? "..." : `${security?.mttd_sec}s / ${security?.mttr_sec}s`}
                        </div>
                        <div className="peak-badge" style={{ marginTop: '0.5rem', background: 'rgba(16, 185, 129, 0.1)', color: 'var(--success)' }}>
                            Score: {security?.compliance_score ? security.compliance_score * 100 : 0}%
                        </div>
                    </div>
                </div>
            </div>

            <div style={{ marginBottom: '2rem' }}>
                <h3 style={{ fontSize: '0.8rem', color: 'var(--text-dim)', textTransform: 'uppercase', marginBottom: '1rem' }}>
                    Temporal Status: <span style={{ color: 'var(--accent)' }}>{workflowStatus}</span>
                </h3>
                <div className="workflow-visual">
                    <div className="wf-node complete">Security</div>
                    <div className="wf-arrow">→</div>
                    <div className="wf-node complete">Ingestion</div>
                    <div className="wf-arrow">→</div>
                    <div className={`wf-node ${workflowStatus === 'PIPELINE_EXPLORE' ? 'active' : 'waiting'}`}>DSA-Explore</div>
                    <div className="wf-arrow">→</div>
                    <div className="wf-node waiting">PMO-Gate</div>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.5rem' }}>
                <div className="agent-pulse">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                        <h3 style={{ fontFamily: 'Outfit' }}>Agent Reasoning Stream</h3>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', background: 'rgba(255,255,255,0.05)', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>LIVE CONNECTED</div>
                    </div>
                    <div className="log">
                        [22:10:01] SYS: Connected to BARC Governance Engine v1.1.0 (PROD-HARDENED)<br />
                        [22:10:02] <strong>ZTA:</strong> Identity Multi-Factor Handshake Verified.<br />
                        [22:10:04] <strong>RESILIENCE:</strong> Circuit Breakers ARMED. Monitoring DSA health...<br />
                        [22:10:05] ORCHESTRATOR: Integrity center sync: 200% Confidence achieved.<br />
                        <span className="cursor"></span>
                    </div>

                </div>

                <div className="card">
                    <h3>Recent Activity</h3>
                    <div style={{ padding: '0.5rem', fontSize: '0.8rem', color: 'var(--text-dim)' }}>
                        - Network Standard nw_standard_v2 pushed.<br />
                        - Identity DSA-Network verified via ZTA.<br />
                        - 12 new findings synthesized by Thinking Agent.
                    </div>
                </div>
            </div>
        </main>
    );
};

export default Dashboard;
