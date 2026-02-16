# 🚀 DEPLOYMENT GUIDE - Music Theory Engine

**Service ID Render**: `srv-d68r0306fj8s73c83pq0`  
**Repository**: https://github.com/ballales1984-wq/composer

---

## 📋 CONFIGURAZIONE RENDER

### 🔑 **GitHub Secrets Richiesti**

Per il deployment automatico su Render, configurare i seguenti secrets in GitHub:

1. **RENDER_SERVICE_ID**: `srv-d68r0306fj8s73c83pq0`
2. **RENDER_API_KEY**: [API Key da Render Dashboard]

### 📝 **Come Configurare i Secrets**

1. Vai su GitHub → Repository → Settings → Secrets and variables → Actions
2. Clicca "New repository secret"
3. Aggiungi:
   - **Name**: `RENDER_SERVICE_ID`
   - **Value**: `srv-d68r0306fj8s73c83pq0`
4. Aggiungi:
   - **Name**: `RENDER_API_KEY`
   - **Value**: [La tua API key da Render Dashboard]

---

## 🐳 DEPLOYMENT CON DOCKER

### **Web App**

```bash
# Build dell'immagine
docker build -f Dockerfile.web -t music-theory-engine-web .

# Run del container
docker run -p 5000:5000 \
  -e FLASK_APP=web_app.app \
  -e FLASK_ENV=production \
  music-theory-engine-web
```

### **Con Docker Compose**

```bash
# Avvia solo la web app
docker-compose --profile web up

# Avvia tutto
docker-compose up
```

---

## 🌐 DEPLOYMENT SU RENDER

### **Configurazione Automatica**

Il repository è configurato per deployment automatico su Render tramite GitHub Actions.

**Workflow**: `.github/workflows/deploy.yml`

**Trigger**:
- Push su branch `main`
- Manual dispatch da GitHub Actions

### **Configurazione Manuale su Render**

1. **Crea nuovo Web Service** su Render
2. **Connetti Repository**: `ballales1984-wq/composer`
3. **Build Command**: 
   ```bash
   pip install -r web_app/requirements.txt
   ```
4. **Start Command**:
   ```bash
   cd web_app && python app.py
   ```
5. **Environment Variables**:
   - `FLASK_APP=web_app.app`
   - `FLASK_ENV=production`
   - `PORT=5000`

### **Service ID**

- **Service ID**: `srv-d68r0306fj8s73c83pq0`
- **URL**: [Da configurare su Render Dashboard]

---

## 🔧 VARIABILI D'AMBIENTE

### **Produzione**

```env
FLASK_APP=web_app.app
FLASK_ENV=production
PORT=5000
```

### **Sviluppo**

```env
FLASK_APP=web_app.app
FLASK_ENV=development
FLASK_DEBUG=1
```

---

## 📊 MONITORAGGIO

### **Health Check Endpoint**

```bash
# Verifica che l'app sia online
curl https://your-render-url.onrender.com/
```

### **API Status**

```bash
# Verifica API
curl https://your-render-url.onrender.com/api/scales?root=C&type=major
```

---

## 🐛 TROUBLESHOOTING

### **Deployment Fallisce**

1. Verifica che i secrets GitHub siano configurati correttamente
2. Controlla i log di Render Dashboard
3. Verifica che le dipendenze siano installate correttamente

### **App Non Si Avvia**

1. Verifica le variabili d'ambiente
2. Controlla che la porta sia configurata correttamente
3. Verifica i log: `render logs srv-d68r0306fj8s73c83pq0`

### **API Non Risponde**

1. Verifica che Flask sia in esecuzione
2. Controlla CORS settings
3. Verifica che le route siano registrate correttamente

---

## 📝 NOTE

- Il deployment automatico avviene solo su push a `main`
- Per deployment manuale, usa GitHub Actions → Deploy workflow → Run workflow
- Il service ID Render è: `srv-d68r0306fj8s73c83pq0`

---

*Ultimo aggiornamento: 26 Gennaio 2026*
