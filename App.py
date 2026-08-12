<!DOCTYPE html>
<html lang="sk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AutoSpec AI Ultra v3.0</title>
  <style>
    :root {
      --bg-color: #0B0E14;
      --card-bg: #131B2E;
      --border-color: #1E293B;
      --accent-cyan: #38BDF8;
      --accent-purple: #A855F7;
      --accent-green: #22C55E;
      --text-main: #E2E8F0;
      --text-muted: #94A3B8;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg-color);
      color: var(--text-main);
      margin: 0;
      padding: 20px;
      display: flex;
      justify-content: center;
    }

    .container {
      max-width: 800px;
      width: 100%;
    }

    header {
      border-bottom: 2px solid var(--border-color);
      padding-bottom: 15px;
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    h1 {
      margin: 0;
      font-size: 1.8rem;
      color: #FFF;
    }

    .badge {
      background: #0F172A;
      border: 1px solid var(--accent-cyan);
      color: var(--accent-cyan);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: bold;
    }

    .card {
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 20px;
      margin-bottom: 20px;
    }

    .card-title {
      font-size: 1.1rem;
      font-weight: bold;
      margin-bottom: 15px;
      color: var(--accent-cyan);
      text-transform: uppercase;
    }

    .form-group {
      margin-bottom: 15px;
    }

    label {
      display: block;
      margin-bottom: 5px;
      color: var(--text-muted);
      font-size: 0.9rem;
    }

    select, input[type="file"], button {
      width: 100%;
      padding: 10px;
      background: #07090E;
      border: 1px solid var(--border-color);
      color: var(--text-main);
      border-radius: 6px;
      box-sizing: border-box;
      font-size: 1rem;
    }

    button {
      background: linear-gradient(135deg, #0284C7, #0369A1);
      color: white;
      font-weight: bold;
      border: none;
      cursor: pointer;
      transition: opacity 0.2s;
      margin-top: 10px;
    }

    button:hover {
      opacity: 0.9;
    }

    .results {
      display: none;
      margin-top: 20px;
    }

    .stat-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 10px;
      margin-top: 15px;
    }

    .stat-box {
      background: #07090E;
      border: 1px solid var(--border-color);
      padding: 12px;
      border-radius: 6px;
      text-align: center;
    }

    .stat-value {
      font-size: 1.4rem;
      font-weight: bold;
      color: var(--accent-cyan);
    }

    .stat-label {
      font-size: 0.75rem;
      color: var(--text-muted);
      text-transform: uppercase;
    }

    .tuning-box {
      border-left: 4px solid var(--accent-purple);
      background: #07090E;
      padding: 10px 15px;
      margin-top: 10px;
      border-radius: 4px;
    }
  </style>
</head>
<body>

  <div class="container">
    <header>
      <div>
        <h1>AutoSpec AI <span style="color: var(--accent-cyan)">v3.0</span></h1>
        <div style="color: var(--accent-cyan); font-size: 0.8rem; font-weight: bold;">WEB CLIENT ENGINE</div>
      </div>
      <span class="badge">GITHUB PAGES LIVE</span>
    </header>

    <!-- FORM CARD -->
    <div class="card">
      <div class="card-title">🔍 Skenovanie & Databáza Vozidiel</div>
      
      <div class="form-group">
        <label for="brandSelect">Vyber Značku:</label>
        <select id="brandSelect" onchange="updateModels()">
          <option value="">-- Vyber značku --</option>
        </select>
      </div>

      <div class="form-group">
        <label for="modelSelect">Vyber Model & Generáciu:</label>
        <select id="modelSelect">
          <option value="">-- Najprv vyber značku --</option>
        </select>
      </div>

      <div class="form-group">
        <label for="fileInput">Nahraj fotku auta (Simulácia Vision AI):</label>
        <input type="file" id="fileInput" accept="image/*">
      </div>

      <button onclick="analyzeVehicle()">SPUSTIŤ ANALÝZU</button>
    </div>

    <!-- RESULTS CARD -->
    <div class="card results" id="resultsCard">
      <div class="card-title" style="color: var(--accent-green)">⚡ Výsledky Analýzy</div>
      
      <div id="vehicleTitle" style="font-size: 1.4rem; font-weight: bold; margin-bottom: 10px;"></div>

      <div class="stat-grid">
        <div class="stat-box">
          <div class="stat-label">Sériový Výkon</div>
          <div class="stat-value" id="stockHp">-</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">Kód Motora</div>
          <div class="stat-value" style="color: var(--accent-purple);" id="engineCode">-</div>
        </div>
        <div class="stat-box">
          <div class="stat-label">Rarity Index</div>
          <div class="stat-value" style="color: var(--accent-green);" id="rarityScore">-</div>
        </div>
      </div>

      <h3 style="margin-top: 20px; color: var(--text-main);">🚀 Možnosti Úpravy (Tuning Stages)</h3>
      
      <div class="tuning-box">
        <strong style="color: var(--accent-cyan)">Stage 1 Chiptuning</strong>
        <div id="stage1Details" style="margin-top: 5px; color: var(--text-muted);"></div>
      </div>

      <div class="tuning-box" style="border-left-color: var(--accent-green);">
        <strong style="color: var(--accent-green)">Stage 2 Performance</strong>
        <div id="stage2Details" style="margin-top: 5px; color: var(--text-muted);"></div>
      </div>
    </div>
  </div>

  <script>
    // ZÁKLADNÁ DATABÁZA V JAVASCRIPTE
    const database = {
      "BMW": [
        {
          model: "M3 E46 (2000-2006)",
          engine: "S54B32",
          stockHp: "343 HP / 365 Nm",
          rarity: "92.5%",
          stage1: "+22 HP, +20 Nm (Cena cca 550 €)",
          stage2: "+45 HP, +40 Nm + Carbon Airbox (Cena cca 1 800 €)"
        },
        {
          model: "M5 E60 (2005-2010)",
          engine: "S85B50 V10",
          stockHp: "507 HP / 520 Nm",
          rarity: "94.0%",
          stage1: "+30 HP, +35 Nm (Cena cca 650 €)",
          stage2: "+60 HP, +60 Nm + Decat Exhaust (Cena cca 2 500 €)"
        }
      ],
      "Škoda": [
        {
          model: "Superb MK3 2.0 TDI (2015-2023)",
          engine: "CRMB / DFHA",
          stockHp: "150 HP / 340 Nm",
          rarity: "45.0%",
          stage1: "+40 HP, +80 Nm (Cena cca 350 €)",
          stage2: "+65 HP, +110 Nm + Downpipe (Cena cca 1 200 €)"
        },
        {
          model: "Octavia RS 2.0 TSI (2020+)",
          engine: "DNPA",
          stockHp: "245 HP / 370 Nm",
          rarity: "65.0%",
          stage1: "+55 HP, +80 Nm (Cena cca 450 €)",
          stage2: "+90 HP, +130 Nm + Intercooler (Cena cca 2 000 €)"
        }
      ],
      "Audi": [
        {
          model: "RS6 C8 (2019+)",
          engine: "DJPB 4.0 V8 TFSI",
          stockHp: "600 HP / 800 Nm",
          rarity: "95.0%",
          stage1: "+100 HP, +150 Nm (Cena cca 1 200 €)",
          stage2: "+180 HP, +220 Nm + Exhaust System (Cena cca 4 500 €)"
        }
      ]
    };

    // INICIALIZÁCIA ZNAČIEK
    window.onload = function() {
      const brandSelect = document.getElementById("brandSelect");
      for (let brand in database) {
        let opt = document.createElement("option");
        opt.value = brand;
        opt.innerHTML = brand;
        brandSelect.appendChild(opt);
      }
    };

    // AKTUALIZÁCIA MODELOV PODĽA ZNAČKY
    function updateModels() {
      const brandSelect = document.getElementById("brandSelect").value;
      const modelSelect = document.getElementById("modelSelect");
      modelSelect.innerHTML = '<option value="">-- Vyber model --</option>';

      if (brandSelect && database[brandSelect]) {
        database[brandSelect].forEach((item, index) => {
          let opt = document.createElement("option");
          opt.value = index;
          opt.innerHTML = item.model;
          modelSelect.appendChild(opt);
        });
      }
    }

    // VYHODNOTENIE
    function analyzeVehicle() {
      const brand = document.getElementById("brandSelect").value;
      const modelIndex = document.getElementById("modelSelect").value;

      if (!brand || modelIndex === "") {
        alert("Prosím vyber značku a model!");
        return;
      }

      const data = database[brand][modelIndex];

      document.getElementById("vehicleTitle").innerText = `${brand} ${data.model}`;
      document.getElementById("stockHp").innerText = data.stockHp;
      document.getElementById("engineCode").innerText = data.engine;
      document.getElementById("rarityScore").innerText = data.rarity;
      document.getElementById("stage1Details").innerText = data.stage1;
      document.getElementById("stage2Details").innerText = data.stage2;

      document.getElementById("resultsCard").style.display = "block";
    }
  </script>
</body>
</html>
