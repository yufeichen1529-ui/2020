import os
from flask import Flask, render_template, send_file
from jinja2 import DictLoader
import pandas as pd

app = Flask(__name__)

# ==========================================
# 1. SMART RELATIVE PATHS
# ==========================================
# Automatically detects the directory where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(BASE_DIR, 'dcca_risk_predictions(3).csv')
MAP_HTML_PATH = os.path.join(BASE_DIR, 'dcca_risk_map.html')
LOCAL_IMG_PATH = os.path.join(BASE_DIR, '圖片1.jpg')


def load_all_data():
    if not os.path.exists(CSV_PATH):
        # Fallback data if CSV is missing
        return pd.DataFrame([{'ENAME': 'Demo District', 'risk_score': 0.45, 'risk_label': 'Medium Risk'}])
    try:
        df = pd.read_csv(CSV_PATH)
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()


# ==========================================
# 2. UI TEMPLATES (ENGLISH VERSION)
# ==========================================
templates = {
    'base': """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BuildSafe AI - Global Inspection</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
    <style>
        :root { --sidebar-bg: #0f172a; --accent: #3b82f6; }
        body { background-color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .sidebar { min-height: 100vh; background: var(--sidebar-bg); color: white; padding: 20px; position: sticky; top: 0; }
        .nav-link { color: #94a3b8; border-radius: 8px; margin-bottom: 5px; padding: 12px; transition: 0.3s; text-decoration: none; display: block;}
        .nav-link:hover, .nav-link.active { color: white; background: var(--accent); }
        .card { border: none; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); overflow: hidden; }

        /* Paywall Styling */
        .paywall-overlay { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.85); z-index:9999; justify-content:center; align-items:center; }
        .pay-card { background:white; padding:40px; border-radius:24px; text-align:center; max-width:450px; border-top: 6px solid var(--accent); }

        .repair-step { border-left: 3px solid var(--accent); padding-left: 20px; margin-bottom: 25px; position: relative; }
        .repair-step::before { 
            content: attr(data-step); position: absolute; left: -14px; top: 0; 
            width: 26px; height: 26px; background: var(--accent); color: white; 
            border-radius: 50%; font-size: 13px; display: flex; align-items: center; justify-content: center; font-weight: bold;
        }
    </style>
</head>
<body>
    <div id="paywall" class="paywall-overlay">
        <div class="pay-card shadow-lg">
            <i class="bi bi-shield-lock-fill text-primary" style="font-size: 3.5rem;"></i>
            <h3 class="fw-bold mt-3" id="pw-title">Premium Access</h3>
            <p class="text-muted" id="pw-text">Please unlock to access professional diagnostic data.</p>
            <div class="h4 fw-bold text-primary mb-4" id="pw-price">HK$ 128</div>
            <button class="btn btn-primary w-100 py-3 fw-bold rounded-pill mb-2" onclick="alert('Payment processing...')">Proceed to Payment</button>
            <button class="btn btn-link text-secondary w-100" onclick="document.getElementById('paywall').style.display='none'">Back to Dashboard</button>
        </div>
    </div>

    <div class="container-fluid">
        <div class="row">
            <nav class="col-md-2 d-none d-md-block sidebar">
                <div class="py-3 text-center mb-4 border-bottom border-secondary">
                    <h4 class="fw-bold mb-0">BuildSafe AI</h4>
                    <small style="color: #64748b;">PropTech Solutions</small>
                </div>
                <ul class="nav flex-column">
                    <li class="nav-item"><a class="nav-link {% if page=='earth' %}active{% endif %}" href="/"><i class="bi bi-earth me-2"></i> Global 3D Vision</a></li>
                    <li class="nav-item"><a class="nav-link {% if page=='hk_map' %}active{% endif %}" href="/hk_map"><i class="bi bi-geo-alt me-2"></i> HK Risk Map</a></li>
                    <li class="nav-item"><a class="nav-link {% if page=='districts' %}active{% endif %}" href="/districts"><i class="bi bi-table me-2"></i> Risk Database</a></li>
                    <li class="nav-item"><a class="nav-link {% if page=='ai_scan' %}active{% endif %}" href="/ai_scan"><i class="bi bi-wrench-adjustable me-2"></i> AI Diagnosis</a></li>
                </ul>
            </nav>
            <main class="col-md-10 p-4">{% block content %}{% endblock %}</main>
        </div>
    </div>
    <script>
        function triggerPaywall(type) { 
            const title = document.getElementById('pw-title');
            const text = document.getElementById('pw-text');
            const price = document.getElementById('pw-price');
            if(type === 'contractor') {
                title.innerText = 'Contractor Matching';
                text.innerText = 'Connect with BD-registered contractors for verified repair works.';
                price.innerText = 'HK$ 49 (Intro Offer)';
            } else {
                title.innerText = 'Full Diagnostic Report';
                text.innerText = 'Get the complete BOQ and statutory compliance guidelines.';
                price.innerText = 'HK$ 128';
            }
            document.getElementById('paywall').style.display = 'flex'; 
        }
    </script>
</body>
</html>
    """,
    'earth_page': """
{% extends "base" %}
{% block content %}
<h2 class="fw-bold mb-4">1. Global Digital Twin Monitoring</h2>
<div class="card" style="height: 75vh; background: #000; position: relative;">
    <div class="text-center text-white p-5 w-100 h-100 d-flex flex-column justify-content-center align-items-center" 
         style="background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://www.gstatic.com/earth/v7/snapshot/default.png') center/cover;">
        <i class="bi bi-globe-americas mb-3" style="font-size: 5rem; color: #3b82f6;"></i>
        <h2 class="fw-bold">Interactive 3D Asset View</h2>
        <p class="text-light mb-4">Live satellite integration for macro-risk identification.</p>
        <div class="d-flex gap-3">
            <a href="https://earth.google.com/web/data=MikKJwolCiExU0lVYloyY015VG9TVnRHSE41RGppdHUzSm9SMXN2NjkgAUICCABKBwjCjJUKEAE" target="_blank" class="btn btn-light btn-lg fw-bold px-4">Launch Google Earth</a>
            <button class="btn btn-warning btn-lg fw-bold px-4" onclick="triggerPaywall('report')">Unlock Analysis</button>
        </div>
    </div>
</div>
{% endblock %}
    """,
    'map_page': """
{% extends "base" %}
{% block content %}
<h2 class="fw-bold mb-4">2. HK District Heatmap (DCCA Analysis)</h2>
<div class="card" style="height: 75vh;">
    <iframe src="/map_render" width="100%" height="100%" frameborder="0"></iframe>
</div>
{% endblock %}
    """,
    'districts': """
{% extends "base" %}
{% block content %}
<h2 class="fw-bold mb-4">3. Risk Database & Government Subsidies</h2>
<div class="card shadow-sm">
    <table class="table table-hover align-middle mb-0">
        <thead class="table-light">
            <tr><th class="ps-4">District</th><th>Risk Score</th><th>Status</th><th>Recommended Policy</th><th class="text-center">Action</th></tr>
        </thead>
        <tbody>
            {% for index, row in df.iterrows() %}
            <tr>
                <td class="ps-4"><strong>{{ row['ENAME'] }}</strong></td>
                <td><span class="text-primary fw-bold">{{ (row['risk_score']*100)|round(1) }}</span></td>
                <td><span class="badge {% if row['risk_score'] > 0.5 %}bg-danger{% else %}bg-warning{% endif %}">{{ row['risk_label'] }}</span></td>
                <td><small class="text-muted">MBIS / OBB 2.0 Subsidy</small></td>
                <td class="text-center">
                    <button class="btn btn-sm btn-outline-info me-1" onclick="triggerPaywall('report')">Policy Detail</button>
                    <a href="/ai_scan" class="btn btn-sm btn-dark">Maintenance</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
    """,
    'ai_scan': """
{% extends "base" %}
{% block content %}
<h2 class="fw-bold mb-4">4. AI Structural Diagnosis & Action Plan</h2>
<div class="row g-4">
    <div class="col-md-6">
        <div class="card bg-dark shadow-lg">
            <img src="/local_image" class="w-100" style="height: 600px; object-fit: contain;" onerror="this.src='https://via.placeholder.com/800x600?text=Check+Local+Image+File'">
            <div class="p-2 text-white-50 small bg-black bg-opacity-50 text-center">Reference: Image1.jpg</div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card p-4 border-start border-primary border-5 h-100">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 class="fw-bold text-uppercase">AI Generated Scheme</h5>
                <span class="badge bg-danger">Critical</span>
            </div>
            <hr>
            <div class="repair-step" data-step="A">
                <strong>Phase A: Structural Clearing</strong>
                <p class="small text-muted mb-0">Removal of debonded tiles and Tapping Test execution.</p>
            </div>
            <div class="repair-step" data-step="B">
                <strong>Phase B: Epoxy Injection</strong>
                <p class="small text-muted mb-0">Pressure injection of structural resin into detected cracks.</p>
            </div>
            <div class="repair-step" data-step="C">
                <strong>Phase C: Protective Seal</strong>
                <p class="small text-muted mb-0">Application of UV-resistant waterproof membrane.</p>
            </div>
            <div class="bg-light p-3 rounded mb-4 text-center">
                <div class="row small">
                    <div class="col-4 border-end">Est. Time<br><strong>4 Days</strong></div>
                    <div class="col-4 border-end">Trade<br><strong>Repair</strong></div>
                    <div class="col-4">Budget<br><strong class="text-primary">HK$ 15k</strong></div>
                </div>
            </div>
            <div class="d-grid gap-2">
                <button class="btn btn-primary btn-lg" onclick="triggerPaywall('report')">Download Full BOQ Report</button>
                <button class="btn btn-outline-dark" onclick="triggerPaywall('contractor')">Match Contractor (HK$ 49)</button>
            </div>
        </div>
    </div>
</div>
{% endblock %}
    """
}

app.jinja_loader = DictLoader(templates)


# ==========================================
# 3. ROUTES
# ==========================================

@app.route('/')
def index(): return render_template('earth_page', page='earth')


@app.route('/hk_map')
def hk_map(): return render_template('map_page', page='hk_map')


@app.route('/districts')
def districts(): return render_template('districts', page='districts', df=load_all_data())


@app.route('/ai_scan')
def ai_scan(): return render_template('ai_scan', page='ai_scan')


@app.route('/map_render')
def map_render():
    if os.path.exists(MAP_HTML_PATH): return send_file(MAP_HTML_PATH)
    return "Map file missing", 404


@app.route('/local_image')
def local_image():
    if os.path.exists(LOCAL_IMG_PATH): return send_file(LOCAL_IMG_PATH)
    return "Image file missing", 404


if __name__ == '__main__':
    # PORT is dynamically assigned by Render/Heroku
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)