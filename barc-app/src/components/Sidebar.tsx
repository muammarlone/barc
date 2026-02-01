import React from 'react';

const Sidebar: React.FC = () => {
    return (
        <aside className="sidebar">
            <div className="logo">
                <div className="logo-icon">B</div>
                BARC / KIW
            </div>

            <div className="persona-box">
                <div style={{ fontSize: '0.6rem', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '1px' }}>Active Persona</div>
                <select className="persona-select">
                    <option>Enterprise Architect</option>
                    <option>Compliance Officer</option>
                    <option>Network Specialist</option>
                    <option>Cloud Ops Manager</option>
                </select>
            </div>
            <nav>
                <ul>
                    <li className="active">Infrastructure Dashboard</li>
                    <li>Domain Assessments</li>
                    <li>
                        Specialty Lab
                        <span style={{ fontSize: '0.6rem', background: 'var(--accent)', color: 'var(--bg-deep)', padding: '0.1rem 0.3rem', borderRadius: '4px', marginLeft: '5px' }}>
                            PRIVATE
                        </span>
                    </li>
                    <li>Audit Traceability</li>
                    <li>Email Ingestion Hub</li>
                    <li>DMS Explorer</li>
                    <li>
                        Workflow Orchestrator
                        <span style={{ fontSize: '0.6rem', background: 'var(--success)', color: 'var(--bg-deep)', padding: '0.1rem 0.3rem', borderRadius: '4px', marginLeft: '5px' }}>
                            LIVE
                        </span>
                    </li>
                    <li>Lifecycle & Change Hub</li>
                    <li>
                        FS Asset Factory
                        <span style={{ fontSize: '0.6rem', background: 'var(--accent)', color: 'var(--bg-deep)', padding: '0.1rem 0.3rem', borderRadius: '4px', marginLeft: '5px' }}>
                            M-MODAL
                        </span>
                    </li>
                    <li>System Governance</li>
                </ul>
            </nav>
            <div className="sidebar-status">
                <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginBottom: '0.2rem' }}>Orchestrator Status</div>
                <div style={{ fontSize: '0.9rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span style={{ width: '8px', height: '8px', background: 'var(--success)', borderRadius: '50%' }}></span>
                    Autonomous Ready
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
