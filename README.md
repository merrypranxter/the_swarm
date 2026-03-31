# ⬡ THE SWARM ⬡

**Multi-Persona Pattern Processor**

8 specialized AI personas process your information through different cognitive lenses, then synthesize their findings into comprehensive analysis.

![Version](https://img.shields.io/badge/version-2.0-00ff00)
![License](https://img.shields.io/badge/license-MIT-00ffaa)
![Personas](https://img.shields.io/badge/personas-8-ff00ff)

## What Is This?

THE SWARM is a cognitive collective that processes text, research, concepts — anything — through 8 distinct AI personas, each with their own specialty:

### Front Line (Parallel Processing)
- 🔴 **MOTIF** - Theme Hunter: Finds conceptual threads and the vibe beneath the words
- 🟢 **CATALOG** - Entity Mapper: Tracks names, orgs, relationships, who-knows-who
- 🟡 **PRISM** - Perspective Shifter: Generates 4-6 radically different interpretations
- 🔵 **LATTICE** - Pattern Spotter: Sees structural patterns, rhythms, mathematical beauty

### Hidden Layer (Sequential Synthesis)
- 🟣 **WEAVER** - Cross-Persona Synthesist: Finds connections between personas' findings
- ⚫ **NULL** - The Skeptic: Questions assumptions, finds gaps, protects against bias
- ⚪ **GAIN** - Signal Amplifier: Boosts weak signals that matter, dismisses noise
- ⬢ **SCHEMA** - Information Architect: Designs optimal file structure and data flow

## Quick Start

### Option 1: Browser (Easiest)

1. Open `index.html` in your browser
2. Paste your content
3. Hit "ACTIVATE SWARM"
4. Export in multiple formats

**No setup required.** Just needs your Anthropic API key in the browser console if running locally.

### Option 2: Gradio Web Interface

```bash
# Clone repo
git clone https://github.com/yourusername/the-swarm.git
cd the-swarm

# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Run
python app.py
```

Open `http://localhost:7860` in your browser.

### Option 3: GitHub Codespaces (Zero Local Setup)

1. Click the green "Code" button on GitHub
2. Select "Codespaces" → "Create codespace on main"
3. Wait for environment to build
4. Set your API key: `export ANTHROPIC_API_KEY="your-key"`
5. Run `python app.py`
6. Click the forwarded port to open the interface

### Option 4: Hugging Face Spaces (Coming Soon)

Deploy your own Space or use the public one at [huggingface.co/spaces/YourUsername/the-swarm](https://huggingface.co/spaces)

## Features

### Multi-Format Export
- **TXT** - Plain text, human-readable
- **Markdown** - GitHub-ready formatted docs
- **JSON** - Structured data for further processing
- **YAML** - Config-style output
- **CSV** - Tabular format for analysis

### SCHEMA Persona
The newest addition! SCHEMA analyzes all outputs and recommends:
- Optimal file structure and organization
- Best formats for each type of data
- How information should flow in a repository
- Relationship mapping between outputs
- Granularity and breakdown strategies

### Use Cases
- **Research Analysis**: Process papers, articles, notes
- **Content Curation**: Organize and synthesize information
- **Idea Exploration**: Get multiple perspectives on concepts
- **Pattern Recognition**: Find hidden structures in text
- **Information Architecture**: Design how to organize findings

## Architecture

```
Input Text
    ↓
[FRONT LINE - Parallel Processing]
  ├─ MOTIF → Themes
  ├─ CATALOG → Entities
  ├─ PRISM → Perspectives
  └─ LATTICE → Patterns
    ↓
[HIDDEN LAYER - Sequential Synthesis]
  ├─ WEAVER → Cross-connections
  ├─ NULL → Skepticism & gaps
  ├─ GAIN → Signal boost
  └─ SCHEMA → Information architecture
    ↓
Formatted Outputs (TXT/MD/JSON/YAML/CSV)
```

## Examples

Check the `/examples` folder for sample inputs and outputs:

- `research_paper.json` - Academic paper analysis
- `meeting_notes.json` - Meeting synthesis
- `concept_exploration.json` - Abstract idea processing

## Configuration

### API Key

**Browser version (index.html):**
The HTML file calls the Anthropic API directly. No config needed, but you'll hit CORS if running from `file://`. Use a local server:

```bash
python -m http.server 8000
# Open http://localhost:8000
```

**Gradio version (app.py):**
Set environment variable:
```bash
export ANTHROPIC_API_KEY="your-key-here"
# or use .env file
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

### Customizing Personas

Edit persona prompts in:
- **HTML version**: Modify the `personas` object in `index.html`
- **Python version**: Edit `PERSONAS` dict in `app.py`

## Development

### Local Development

```bash
# Clone
git clone https://github.com/yourusername/the-swarm.git
cd the-swarm

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install deps
pip install -r requirements.txt

# Run
python app.py
```

### Codespaces Development

The repo includes `.devcontainer/devcontainer.json` for one-click Codespaces setup:

1. Open in Codespaces
2. Environment auto-configures
3. Set your API key
4. Start coding

### Adding New Personas

1. Add persona definition to `PERSONAS` dict
2. Choose `frontLine` (parallel) or `hiddenLayer` (sequential)
3. Define system prompt
4. Pick icon and color
5. Test!

## Deployment

### Hugging Face Spaces

1. Create new Space on Hugging Face
2. Choose "Gradio" as SDK
3. Upload `app.py` and `requirements.txt`
4. Add `ANTHROPIC_API_KEY` to Space secrets
5. Deploy!

### Self-Hosted

```bash
# Install
pip install -r requirements.txt

# Run with gunicorn
gunicorn app:app --bind 0.0.0.0:7860
```

## Export Formats Explained

### JSON Structure
```json
{
  "timestamp": "2026-03-31T12-34-56",
  "input": "original text",
  "frontLine": {
    "motif": "themes analysis...",
    "catalog": "entities mapping...",
    "prism": "alternative perspectives...",
    "lattice": "pattern identification..."
  },
  "hiddenLayer": {
    "weaver": "cross-synthesis...",
    "null": "skeptical analysis...",
    "gain": "signal amplification...",
    "schema": "architecture recommendation..."
  }
}
```

### SCHEMA Output Example
```
/project_root
  /themes
    - overview.md [MOTIF output]
    - theme_breakdown.json
  /entities
    - entity_graph.json [CATALOG output]
    - relationships.csv
  /perspectives
    - perspective_01.txt [PRISM outputs]
    - perspective_02.txt
    - ...
  /analysis
    - patterns.md [LATTICE output]
    - synthesis.md [WEAVER output]
  /meta
    - critique.txt [NULL output]
    - signals.txt [GAIN output]
```

## Troubleshooting

**"API key not found"**
- Set `ANTHROPIC_API_KEY` environment variable
- Or add to `.env` file
- Or paste into browser console for HTML version

**"CORS error" (browser version)**
- Don't open `index.html` directly (`file://`)
- Use local server: `python -m http.server 8000`

**"Module not found"**
```bash
pip install -r requirements.txt
```

**Gradio not starting**
```bash
# Try specific version
pip install gradio==6.7.0
```

## Roadmap

- [x] 8 persona system
- [x] Browser interface
- [x] Gradio interface
- [x] Multi-format export
- [x] SCHEMA architecture persona
- [x] Codespaces support
- [ ] Hugging Face Space deployment
- [ ] Batch processing mode
- [ ] Custom persona builder UI
- [ ] Persistent session storage
- [ ] Persona conversation history
- [ ] Visual network graphs
- [ ] API endpoint mode

## Contributing

Want to add personas, improve prompts, or enhance features? 

1. Fork the repo
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit PR

## Credits

Built with Claude Sonnet 4 and maximalist chaos energy.

**Created by:** [merrypranxter](https://github.com/merrypranxter)

## License

MIT License - See LICENSE file for details

---

**Need help?** Open an issue or check existing discussions.

**Love it?** Star the repo ⭐
