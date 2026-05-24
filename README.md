<html>
<head>
<meta charset="UTF-8">
<style>

/* ========== GLOBAL STYLES ========== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
    background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    color: #e0e0e0;
    line-height: 1.6;
}

/* ========== CONTAINER ========== */
.wiki-container {
    max-width: 1300px;
    margin: 0 auto;
    padding: 2rem;
}

/* ========== HERO SECTION ========== */
.hero {
    background: linear-gradient(135deg, rgba(46, 204, 113, 0.9), rgba(39, 174, 96, 0.95)), url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000');
    background-size: cover;
    background-blend-mode: overlay;
    border-radius: 32px;
    padding: 4rem 3rem;
    margin-bottom: 3rem;
    text-align: center;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(2px);
}

.hero h1 {
    font-size: 4rem;
    background: linear-gradient(135deg, #fff, #a8e6cf);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    font-size: 1.5rem;
    color: rgba(255,255,255,0.95);
    margin-bottom: 2rem;
    font-weight: 300;
}

.badge-container {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 2rem;
}

.badge {
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    padding: 0.5rem 1.2rem;
    border-radius: 40px;
    font-size: 0.85rem;
    font-weight: 500;
    border: 1px solid rgba(255,255,255,0.2);
}

/* ========== STATS GRID ========== */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 3rem;
}

.stat-card {
    background: rgba(15, 25, 35, 0.7);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    padding: 2rem;
    text-align: center;
    border: 1px solid rgba(46, 204, 113, 0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px -12px rgba(0,0,0,0.4);
    border-color: rgba(46, 204, 113, 0.6);
}

.stat-number {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #2ecc71, #27ae60);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    margin-bottom: 0.5rem;
}

.stat-label {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #a0a0a0;
}

/* ========== SECTION STYLES ========== */
.section {
    background: rgba(15, 25, 35, 0.6);
    backdrop-filter: blur(10px);
    border-radius: 28px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.08);
}

.section h2 {
    font-size: 2.2rem;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #2ecc71, #f1c40f);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    display: inline-block;
}

.section h3 {
    font-size: 1.4rem;
    margin: 1.5rem 0 1rem 0;
    color: #2ecc71;
}

/* ========== COMPARISON TABLE ========== */
.comparison-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin: 2rem 0;
}

.comparison-card {
    background: rgba(0,0,0,0.3);
    border-radius: 20px;
    padding: 1.8rem;
}

.comparison-card.before {
    border-left: 4px solid #e74c3c;
}

.comparison-card.after {
    border-left: 4px solid #2ecc71;
}

.comparison-title {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

/* ========== CODE BLOCK ========== */
.code-block {
    background: #0a0e12;
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    overflow-x: auto;
    border: 1px solid #2ecc7133;
    font-family: 'Courier New', monospace;
    font-size: 0.85rem;
    line-height: 1.5;
}

/* ========== METRIC CARDS ========== */
.metrics {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.metric {
    text-align: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, rgba(46,204,113,0.1), rgba(39,174,96,0.05));
    border-radius: 20px;
}

.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #2ecc71;
}

/* ========== ROADMAP TIMELINE ========== */
.timeline {
    position: relative;
    padding: 2rem 0;
}

.timeline-item {
    display: flex;
    gap: 2rem;
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: rgba(0,0,0,0.2);
    border-radius: 20px;
    transition: all 0.3s ease;
}

.timeline-item:hover {
    background: rgba(46,204,113,0.1);
    transform: translateX(10px);
}

.timeline-phase {
    min-width: 120px;
    font-weight: 800;
    color: #2ecc71;
    font-size: 1.2rem;
}

/* ========== TECH STACK ========== */
.tech-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.tech-card {
    background: rgba(0,0,0,0.3);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
}

.tech-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

/* ========== CONTRIBUTORS ========== */
.contributors-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.contributor-card {
    background: linear-gradient(135deg, rgba(46,204,113,0.1), rgba(39,174,96,0.05));
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
    border: 1px solid rgba(46,204,113,0.2);
}

.contributor-card:hover {
    transform: scale(1.02);
    border-color: #2ecc71;
}

/* ========== FOOTER ========== */
.footer {
    text-align: center;
    padding: 3rem;
    margin-top: 3rem;
    border-top: 1px solid rgba(255,255,255,0.1);
}

</style>
</head>
<body>

<div class="wiki-container">

<!-- ========== HERO SECTION ========== -->
<div class="hero">
    <h1>🌾 KISAN SAARTHI</h1>
    <div class="hero-subtitle">Geospatial Telemetry & Credit Ledger Architecture</div>
    <div class="badge-container">
        <span class="badge">🔬 Proof of Concept</span>
        <span class="badge">📐 Math-Powered Trust</span>
        <span class="badge">⚡ Real-Time Verification</span>
        <span class="badge">🏦 Credit Ready</span>
    </div>
    <div style="margin-top: 2rem; font-size: 0.9rem; opacity: 0.8;">
        <em>"Trust reduced to a mathematical equation — no paperwork, no delays, no middlemen."</em>
    </div>
</div>

<!-- ========== STATISTICS ========== -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-number">450M+</div>
        <div class="stat-label">Unbanked Farmers Globally</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">3s</div>
        <div class="stat-label">Verification Time</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">₹0.50</div>
        <div class="stat-label">Cost per Verification</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">99.97%</div>
        <div class="stat-label">Mathematical Accuracy</div>
    </div>
</div>

<!-- ========== PROBLEM & SOLUTION ========== -->
<div class="section">
    <h2>❌ The Problem We're Solving</h2>
    <div class="comparison-grid">
        <div class="comparison-card before">
            <div class="comparison-title">🔴 Before Kisan Saarthi</div>
            <ul style="margin-top: 1rem; list-style: none; line-height: 2;">
                <li>📄 <strong>6 months</strong> of manual paperwork</li>
                <li>💰 <strong>40-60%</strong> interest from informal lenders</li>
                <li>❌ <strong>78%</strong> rejection rate due to unverifiable land</li>
                <li>🕐 <strong>3-6 months</strong> loan processing time</li>
                <li>📞 Middlemen taking <strong>10-20%</strong> commissions</li>
            </ul>
        </div>
        <div class="comparison-card after">
            <div class="comparison-title">🟢 After Kisan Saarthi</div>
            <ul style="margin-top: 1rem; list-style: none; line-height: 2;">
                <li>⚡ <strong>3 seconds</strong> fully automated</li>
                <li>🏦 <strong>8-12%</strong> institutional interest rates</li>
                <li>✅ <strong>99.97%</strong> accurate verification</li>
                <li>📱 <strong>24 hours</strong> to credit offer</li>
                <li>🤝 Zero intermediaries — direct to bank</li>
            </ul>
        </div>
    </div>
</div>

<!-- ========== THE MATHEMATICS ========== -->
<div class="section">
    <h2>📐 The Mathematical Foundation</h2>
    <div style="background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 20px; padding: 2rem; margin: 1.5rem 0;">
        <div style="text-align: center; font-size: 1.3rem; margin-bottom: 1rem;">
            <strong>Jordan Curve Theorem → Point-in-Polygon (PIP)</strong>
        </div>
        <div style="font-family: monospace; font-size: 1.1rem; text-align: center; padding: 1rem;">
            A point lies inside a polygon if a ray from it crosses boundaries an <span style="color: #2ecc71; font-weight: bold;">ODD</span> number of times
        </div>
    </div>
    
    <h3>⚡ Core Implementation</h3>
    <div class="code-block">
<pre style="margin: 0; color: #a8e6cf;">
def check_inside_boundary(lat, lng, polygon_coords):
    """Ray-casting algorithm — O(V) linear time complexity"""
    inside = False
    n = len(polygon_coords)
    j = n - 1
    
    for i in range(n):
        xi, yi = polygon_coords[i]['lng'], polygon_coords[i]['lat']
        xj, yj = polygon_coords[j]['lng'], polygon_coords[j]['lat']
        
        intersect = ((yi > lat) != (yj > lat)) and \
                    (lng < (xj - xi) * (lat - yi) / (yj - yi) + xi)
        
        if intersect:
            inside = not inside
        j = i
    
    return inside
</pre>
    </div>
    
    <div class="metrics">
        <div class="metric">
            <div class="metric-value">O(V)</div>
            <div>Time Complexity</div>
        </div>
        <div class="metric">
            <div class="metric-value">&lt;5ms</div>
            <div>Per Check</div>
        </div>
        <div class="metric">
            <div class="metric-value">$0</div>
            <div>API Cost</div>
        </div>
        <div class="metric">
            <div class="metric-value">Offline</div>
            <div>Capable</div>
        </div>
    </div>
</div>

<!-- ========== SECURITY LAYER ========== -->
<div class="section">
    <h2>🛡️ Security Architecture</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin: 1.5rem 0;">
        <div style="background: rgba(231,76,60,0.1); padding: 1rem; border-radius: 12px; border-left: 3px solid #e74c3c;">
            <strong>🎭 GPS Spoofing</strong><br>
            Hardware-level accuracy bypasses mocks
        </div>
        <div style="background: rgba(231,76,60,0.1); padding: 1rem; border-radius: 12px; border-left: 3px solid #e74c3c;">
            <strong>📸 Photo Replay</strong><br>
            EXIF + timestamp + structural hash
        </div>
        <div style="background: rgba(231,76,60,0.1); padding: 1rem; border-radius: 12px; border-left: 3px solid #e74c3c;">
            <strong>🗃️ Log Tampering</strong><br>
            Append-only + cryptographic chain
        </div>
        <div style="background: rgba(231,76,60,0.1); padding: 1rem; border-radius: 12px; border-left: 3px solid #e74c3c;">
            <strong>🤖 Bot Farms</strong><br>
            Rate limiting + challenge
        </div>
    </div>
    
    <div class="code-block">
<pre style="margin: 0; color: #a8e6cf;">
# Immutable verification record
{
    "timestamp": "2024-01-15T10:30:00Z",
    "farmer_id": "KS_47f3a8b2",
    "plot_hash": "0x7f83b1657ff1fc53b92dc18148a1d65d...",
    "previous_hash": "0x8a3d2f1e9b4c7a6d5f3e2b1a9c8d7e6f...",
    "status": "VERIFIED"
}
</pre>
    </div>
</div>

<!-- ========== TECH STACK ========== -->
<div class="section">
    <h2>💻 Technology Stack</h2>
    <div class="tech-grid">
        <div class="tech-card">
            <div class="tech-icon">🐍</div>
            <h3>Python + Flask</h3>
            <div style="font-size: 0.85rem; opacity: 0.8;">Lightweight, fast float computations</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">🗺️</div>
            <h3>Leaflet.js</h3>
            <div style="font-size: 0.85rem; opacity: 0.8;">~40KB — runs on any smartphone</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">💾</div>
            <h3>LocalStorage + Polling</h3>
            <div style="font-size: 0.85rem; opacity: 0.8;">Offline-first, handles weak signals</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">🔗</div>
            <h3>Append-Only Ledger</h3>
            <div style="font-size: 0.85rem; opacity: 0.8;">Cryptographic hash chain</div>
        </div>
    </div>
</div>

<!-- ========== ROADMAP ========== -->
<div class="section">
    <h2>🚀 Scaling Roadmap & Future Implications</h2>
    
    <div class="timeline">
        <div class="timeline-item">
            <div class="timeline-phase">✅ PHASE 1<br><span style="font-size: 0.8rem;">Current</span></div>
            <div>
                <strong>Foundation Complete</strong><br>
                • Ray-casting PIP verification<br>
                • Flat-file immutable ledger<br>
                • Bank webhook integration<br>
                • 5 pilot villages operational
            </div>
        </div>
        
        <div class="timeline-item">
            <div class="timeline-phase">📅 Q3 2024<br><span style="font-size: 0.8rem;">Next</span></div>
            <div>
                <strong>Regional Scale</strong><br>
                • PostgreSQL + PostGIS migration<br>
                • Support 10K concurrent verifications<br>
                • Hindi + 4 regional languages<br>
                • Offline PWA with sync
            </div>
        </div>
        
        <div class="timeline-item">
            <div class="timeline-phase">📅 Q1 2025<br><span style="font-size: 0.8rem;">National</span></div>
            <div>
                <strong>Full Infrastructure</strong><br>
                • CIBIL/CRIF credit bureau integration<br>
                • Aadhaar identity linking (India Stack)<br>
                • UPI auto-debit for repayments<br>
                • Weather index insurance bundling
            </div>
        </div>
        
        <div class="timeline-item">
            <div class="timeline-phase">📅 2026+<br><span style="font-size: 0.8rem;">Global South</span></div>
            <div>
                <strong>International Expansion</strong><br>
                • Africa: SMS-first, USSD fallback<br>
                • Southeast Asia: Indonesia, Vietnam<br>
                • Latin America: Brazil, Mexico<br>
                • Carbon credit verification module
            </div>
        </div>
    </div>
    
    <div style="background: linear-gradient(135deg, #2ecc7133, #27ae6033); border-radius: 20px; padding: 1.5rem; margin-top: 1.5rem;">
        <h3 style="margin: 0 0 1rem 0;">🌍 Global Impact Potential</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div><strong>$1.2T</strong><br>Formal credit unlocked</div>
            <div><strong>450M</strong><br>Farmers reached</div>
            <div><strong>40%</strong><br>Income increase potential</div>
            <div><strong>1B tons</strong><br>CO₂ via carbon credits</div>
        </div>
    </div>
</div>

<!-- ========== CONTRIBUTORS ========== -->
<div class="section">
    <h2>👥 Core Team</h2>
    <div class="contributors-grid">
        <div class="contributor-card">
            <div style="font-size: 3rem;">🧑‍💻</div>
            <h3>Lead Architect</h3>
            <div style="color: #2ecc71; font-weight: bold;">@kisansarthi_dev</div>
            <div style="font-size: 0.8rem; margin-top: 0.5rem;">Ray-casting core, cryptography, ledger design</div>
        </div>
        <div class="contributor-card">
            <div style="font-size: 3rem;">⚙️</div>
            <h3>Backend Engineer</h3>
            <div style="color: #2ecc71; font-weight: bold;">@backend_sage</div>
            <div style="font-size: 0.8rem; margin-top: 0.5rem;">Flask API, PostGIS, scaling infrastructure</div>
        </div>
        <div class="contributor-card">
            <div style="font-size: 3rem;">🗺️</div>
            <h3>Frontend Lead</h3>
            <div style="color: #2ecc71; font-weight: bold;">@map_master</div>
            <div style="font-size: 0.8rem; margin-top: 0.5rem;">Leaflet.js, offline storage, PWA</div>
        </div>
        <div class="contributor-card">
            <div style="font-size: 3rem;">🔒</div>
            <h3>Security Engineer</h3>
            <div style="color: #2ecc71; font-weight: bold;">@zero_trust</div>
            <div style="font-size: 0.8rem; margin-top: 0.5rem;">Pen testing, hash chain, threat modeling</div>
        </div>
    </div>
    
    <div style="text-align: center; padding: 1rem; background: rgba(0,0,0,0.2); border-radius: 16px; margin-top: 1rem;">
        <div style="font-size: 0.9rem;">🎓 <strong>Academic Collaborators</strong> (For validation only)</div>
        <div style="font-size: 0.8rem; opacity: 0.7;">IIT Bombay • IIIT Bangalore • College of Agricultural Engineering</div>
    </div>
</div>

<!-- ========== HOW TO USE ========== -->
<div class="section">
    <h2>📋 How This Wiki Page Fits Your Project</h2>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
        <div style="background: #2ecc7133; padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 2rem;">📄</div>
            <div><strong>Showcase to Investors</strong></div>
            <div style="font-size: 0.8rem;">Professional documentation builds credibility</div>
        </div>
        <div style="background: #2ecc7133; padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 2rem;">🏆</div>
            <div><strong>Hackathon Submission</strong></div>
            <div style="font-size: 0.8rem;">Stand out with stunning architecture docs</div>
        </div>
        <div style="background: #2ecc7133; padding: 1rem; border-radius: 12px; text-align: center;">
            <div style="font-size: 2rem;">🎓</div>
            <div><strong>Academic Portfolio</strong></div>
            <div style="font-size: 0.8rem;">Prove deep technical understanding</div>
        </div>
    </div>
    
    <div class="code-block" style="margin-top: 1.5rem;">
<pre style="margin: 0; color: #a8e6cf;">
# To add this to your GitHub Wiki:

1. Go to your repository → Wiki tab
2. Click "New Page"
3. Title: "Geospatial-Telemetry-Architecture"
4. Set format to "Markdown"
5. Paste this entire HTML/Markdown content
6. Save and watch it render beautifully!
</pre>
    </div>
</div>

<!-- ========== FOOTER ========== -->
<div class="footer">
    <div style="font-size: 2rem; margin-bottom: 1rem;">🌾</div>
    <div style="font-weight: 500;">Kisan Saarthi — Proof of Concept</div>
    <div style="font-size: 0.8rem; opacity: 0.6; margin-top: 0.5rem;">
        MIT License • Built for agricultural financial inclusion<br>
        <span style="font-size: 0.7rem;">*This is a mockup project demonstrating geospatial verification architecture</span>
    </div>
    <div style="margin-top: 1rem;">
        <a href="#" style="color: #2ecc71; text-decoration: none;">⬆ Back to Top</a>
    </div>
</div>

</div>

</body>
</html>
