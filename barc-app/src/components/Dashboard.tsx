import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Metrics {
    quality_score: number;
    performance_velocity: number;
    readiness_forecast: string;
}

const Dashboard: React.FC = () => {
    const [metrics, setMetrics] = useState<Metrics | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                // In a production environment, this would be an environment variable
                const response = await axios.get('http://localhost:8002/metrics?findings_count=12&critical_gaps=1');

                setMetrics(response.data);
                setLoading(false);
            } catch (error) {
                console.error("Failed to fetch metrics", error);
                setLoading(false);
            }
        };
        fetchMetrics();
    }, []);

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

                <div className="card">
                    <h3>Integrity Center</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem', marginTop: '0.5rem' }}>
                        <div className="integrity-badge badge-zt">ZT: VERIFIED</div>
                        <div className="integrity-badge badge-ethical">ETHICS: 100%</div>
                    </div>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.5rem' }}>
                <div className="agent-pulse">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                        <h3 style={{ fontFamily: 'Outfit' }}>Agent Reasoning Stream</h3>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', background: 'rgba(255,255,255,0.05)', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>LIVE CONNECTED</div>
                    </div>
                    <div className="log">
                        [21:10:01] SYS: Connected to BARC Governance Engine v1.0.0<br />
                        [21:10:02] <strong>OPME:</strong> Analyzing backlog velocity...<br />
                        [21:10:04] <strong>THINKING-AGENT:</strong> Peer-reviewing DSA Findings for NW-001...<br />
                        [21:10:05] ORCHESTRATOR: Integrity check passed. Ready for PMO gate.<br />
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
