# THE SWARM ASCII Art & Quick Reference

## Banner

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ████████╗██╗  ██╗███████╗    ███████╗██╗    ██╗ █████╗     ║
║   ╚══██╔══╝██║  ██║██╔════╝    ██╔════╝██║    ██║██╔══██╗    ║
║      ██║   ███████║█████╗      ███████╗██║ █╗ ██║███████║    ║
║      ██║   ██╔══██║██╔══╝      ╚════██║██║███╗██║██╔══██║    ║
║      ██║   ██║  ██║███████╗    ███████║╚███╔███╔╝██║  ██║    ║
║      ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝    ║
║                                                               ║
║              ⬡ MULTI-PERSONA PATTERN PROCESSOR ⬡             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

         🔴 MOTIF    🟢 CATALOG   🟡 PRISM    🔵 LATTICE
         🟣 WEAVER   ⚫ NULL       ⚪ GAIN      ⬢ SCHEMA
```

## Mini Banner

```
⬡ THE SWARM ⬡
8 AI Personas | Multi-Perspective Analysis | Information Architecture
```

## Persona Icons

```
Front Line:
  🔴 MOTIF   - Theme Hunter
  🟢 CATALOG - Entity Mapper
  🟡 PRISM   - Perspective Shifter
  🔵 LATTICE - Pattern Spotter

Hidden Layer:
  🟣 WEAVER  - Cross-Persona Synthesist
  ⚫ NULL    - The Skeptic
  ⚪ GAIN    - Signal Amplifier
  ⬢ SCHEMA  - Information Architect
```

## Quick Command Reference

### Browser
```bash
# Serve locally
python -m http.server 8000
# Open http://localhost:8000
```

### Gradio
```bash
# Quick start
./start.sh

# Manual
export ANTHROPIC_API_KEY="sk-ant-..."
python app.py
```

### CLI
```bash
# From file
python swarm_cli.py input.txt ./outputs

# From stdin
echo "Your text" | python swarm_cli.py

# With pipe
cat file.txt | python swarm_cli.py > output.txt
```

### Batch
```bash
# Process directory
python swarm_batch.py ./documents ./outputs

# Process pattern
python swarm_batch.py 'papers/*.md' ./results
```

## One-Liners

### Quick Test
```bash
echo "Terence McKenna's Timewave Zero theory" | python swarm_cli.py
```

### Process & View
```bash
python swarm_cli.py input.txt . && cat swarm_*.json | jq '.hiddenLayer.schema'
```

### Batch & Count
```bash
python swarm_batch.py ./docs ./out && echo "Processed: $(ls ./out/*.json | wc -l) files"
```

## Environment Variables

```bash
# Required
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional
export SWARM_MODEL="claude-sonnet-4-20250514"  # Model to use
export SWARM_MAX_TOKENS="1000"                 # Token limit
export SWARM_OUTPUT_DIR="./outputs"            # Default output
```

## File Patterns

### Input
```
input.txt          → swarm_input_2026-03-31T12-34-56.json
research.md        → swarm_research_2026-03-31T12-34-56.json
meeting_notes.txt  → swarm_meeting_notes_2026-03-31T12-34-56.json
```

### Output Structure (from SCHEMA)
```
/project_root
  /concepts      - Reference material (MD + JSON)
  /interpretations - Alt readings (TXT files)
  /synthesis     - Meta-analysis (MD)
  /metadata      - Session data (JSON + CSV)
```

## Common Workflows

### Research Paper Analysis
```bash
# 1. Process
python swarm_cli.py paper.pdf.txt ./analysis

# 2. Extract SCHEMA recommendation
cat analysis/swarm_*.json | jq -r '.hiddenLayer.schema'

# 3. Create structure
# (Follow SCHEMA's recommendation)
```

### Meeting Synthesis
```bash
# Process meeting transcript
python swarm_cli.py meeting_transcript.txt ./meetings

# Get action items
cat meetings/swarm_*.json | jq -r '.frontLine.catalog' | grep "👤"
```

### Batch Research
```bash
# Process all papers
python swarm_batch.py ./research_papers ./swarm_analysis

# View all SCHEMA recommendations
for f in swarm_analysis/*.json; do
    echo "=== $(basename $f) ==="
    jq -r '.hiddenLayer.schema' "$f"
done
```

## Export Shortcuts

### Get Specific Persona
```bash
# Just MOTIF themes
jq -r '.frontLine.motif' swarm_output.json

# Just SCHEMA architecture
jq -r '.hiddenLayer.schema' swarm_output.json
```

### Convert to Markdown
```bash
python -c "
import json
with open('swarm_output.json') as f:
    data = json.load(f)
    print('# SWARM Analysis')
    for pid, result in data['frontLine'].items():
        print(f'\n## {pid.upper()}\n{result}')
" > output.md
```

### Extract All Themes
```bash
for f in outputs/*.json; do
    jq -r '.frontLine.motif' "$f" >> all_themes.txt
    echo -e "\n---\n" >> all_themes.txt
done
```

## Status Indicators

### Processing
```
[FRONT LINE PROCESSING]
  🔴 motif... ✓
  🟢 catalog... ✓
  🟡 prism... ✓
  🔵 lattice... ✓

[HIDDEN LAYER SYNTHESIS]
  🟣 weaver... ✓
  ⚫ null... ✓
  ⚪ gain... ✓
  ⬢ schema... ✓

✓ SWARM PROCESSING COMPLETE
```

### Batch
```
[1/5] Processing: paper_01.txt... ✓
[2/5] Processing: paper_02.txt... ✓
[3/5] Processing: paper_03.txt... ✓
[4/5] Processing: paper_04.txt... ✗ Error
[5/5] Processing: paper_05.txt... ✓

BATCH COMPLETE
Processed: 4/5 files
```

## Troubleshooting Quick Reference

```
Error: ANTHROPIC_API_KEY not set
Fix: export ANTHROPIC_API_KEY="your-key"

Error: Module not found
Fix: pip install -r requirements.txt

Error: CORS in browser
Fix: python -m http.server 8000

Error: Port in use
Fix: lsof -ti:7860 | xargs kill

Error: Rate limit
Fix: Wait 60s or use different API key
```

## Performance Tips

```
Fast testing:     Use Haiku, max_tokens=500
Best quality:     Use Sonnet, max_tokens=2000
Cheap processing: Use Haiku, skip personas
Full analysis:    Use Sonnet, all 8 personas
```

## API Cost Calculator

```
Input tokens:  ~1000
Output tokens: ~8000 (8 personas × 1000)
Total:         ~9000 tokens

Claude Sonnet 4:
  Input:  $3/M tokens   = $0.003
  Output: $15/M tokens  = $0.120
  Total:               ≈ $0.123 per run

Claude Haiku:
  Input:  $0.25/M tokens = $0.00025
  Output: $1.25/M tokens = $0.01000
  Total:                ≈ $0.01025 per run
```

---

Need more? Check the full docs:
- README.md - Overview
- SETUP_GUIDE.md - Deployment
- ARCHITECTURE.md - Technical details
- CONTRIBUTING.md - How to help
