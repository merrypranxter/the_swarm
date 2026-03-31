# THE SWARM - Complete Setup Guide

## Choose Your Adventure

### 1. Zero-Setup Browser Version

**Best for:** Quick testing, one-off analyses

```bash
# Just open index.html in a browser
# That's it!
```

**Note:** For CORS reasons, serve it locally:
```bash
python -m http.server 8000
# Open http://localhost:8000
```

---

### 2. Local Python/Gradio

**Best for:** Regular use, customization

```bash
# Clone repo
git clone https://github.com/yourusername/the-swarm.git
cd the-swarm

# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Run
./start.sh
# or: python app.py
```

Open `http://localhost:7860`

---

### 3. GitHub Codespaces

**Best for:** No local setup, cloud development

1. Go to repo on GitHub
2. Click green "Code" button
3. Select "Codespaces" → "Create codespace"
4. Wait for build (auto-installs deps)
5. Set API key: `export ANTHROPIC_API_KEY="sk-ant-..."`
6. Run: `./start.sh`
7. Click forwarded port URL

**Codespaces includes:**
- Python 3.11
- GitHub CLI
- Node.js
- Auto-installed dependencies
- VSCode extensions

---

### 4. Hugging Face Spaces

**Best for:** Public deployment, sharing

#### Method A: Fork Space (Easiest)
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Find "THE SWARM" space
3. Click "Duplicate this Space"
4. Add your `ANTHROPIC_API_KEY` to secrets
5. Done!

#### Method B: Create New Space
1. Create new Space on HF
2. Choose "Gradio" SDK
3. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `README_HUGGINGFACE.md` (rename to `README.md`)
4. Add `ANTHROPIC_API_KEY` to Space secrets
5. Space will auto-deploy

---

## API Key Setup

You need an Anthropic API key from [console.anthropic.com](https://console.anthropic.com)

### Environment Variable (Local/Codespaces)
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### .env File (Local)
```bash
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### Hugging Face Secrets (Spaces)
1. Go to Space settings
2. "Repository secrets"
3. Add `ANTHROPIC_API_KEY`
4. Paste key

---

## Customization

### Adding Personas

Edit `app.py` or `index.html`:

```python
{
    "id": "yourpersona",
    "name": "🟠 YOURNAME",
    "role": "Your Role",
    "prompt": """Your system prompt here..."""
}
```

Add to `frontLine` (parallel) or `hiddenLayer` (sequential).

### Changing Models

In `app.py`, change:
```python
model="claude-sonnet-4-20250514"
```

To any Anthropic model.

### Adjusting Token Limits

Change `max_tokens` in API calls:
```python
max_tokens=1000  # Default
max_tokens=2000  # Longer responses
```

---

## Troubleshooting

### "Module not found: gradio"
```bash
pip install -r requirements.txt
```

### "API key not set"
```bash
export ANTHROPIC_API_KEY="your-key"
```

### Browser version CORS errors
Don't open `index.html` directly. Use:
```bash
python -m http.server 8000
```

### Codespaces port not forwarding
1. Check terminal for port number
2. Click "Ports" tab in VSCode
3. Right-click port → "Open in Browser"

### Gradio not accessible externally
Make sure you have:
```python
app.launch(server_name="0.0.0.0")
```

### Hugging Face Space timeout
Spaces have compute limits. Consider:
- Upgrading Space tier
- Reducing token limits
- Caching results

---

## Performance Tips

### Faster Processing
- Use `max_tokens=500` for quicker responses
- Comment out personas you don't need
- Process front-line only (skip hidden layer)

### Better Results
- Give more context in input
- Use `max_tokens=2000` for detailed analysis
- Enable all 8 personas
- Try different models (Opus for depth, Haiku for speed)

### Cost Optimization
- Use Claude Haiku for testing
- Reduce `max_tokens`
- Cache results
- Use browser version (direct API calls)

---

## Development Workflow

### Local Testing
```bash
# Make changes
vim app.py

# Test
./start.sh

# Iterate
```

### Codespaces Testing
```bash
# Changes auto-reload in Codespaces
# Just edit files and Gradio hot-reloads
```

### Deploying to HF
```bash
# Commit changes
git add .
git commit -m "Update personas"
git push

# HF Space auto-rebuilds
```

---

## Common Use Cases

### Research Analysis
1. Paste paper/article
2. Run swarm
3. Export SCHEMA recommendation
4. Follow file structure for organizing findings

### Meeting Synthesis
1. Paste meeting notes
2. Get themes (MOTIF), action items (CATALOG), perspectives (PRISM)
3. Export as MD for sharing

### Concept Exploration
1. Paste abstract idea
2. Get multiple interpretations (PRISM)
3. Find patterns (LATTICE)
4. Synthesize (WEAVER)

### Information Architecture
1. Paste any content
2. Focus on SCHEMA output
3. Use recommended structure for organizing

---

## Next Steps

- [ ] Try the browser version
- [ ] Set up local Gradio
- [ ] Test in Codespaces
- [ ] Deploy to Hugging Face
- [ ] Customize personas
- [ ] Add your own examples
- [ ] Share your results!

---

Need help? Check README.md or open an issue on GitHub.
