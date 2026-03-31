# THE SWARM - Architecture & Usage

## System Architecture

```
                           ┌─────────────────────┐
                           │   INPUT TEXT        │
                           │  (Any content)      │
                           └──────────┬──────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │                                   │
        ┌───────────▼──────────┐          ┌────────────▼────────────┐
        │  FRONT LINE LAYER    │          │  Processes in PARALLEL  │
        │  (Parallel)          │          └─────────────────────────┘
        └──────────────────────┘
                    │
        ┌───────────┴────────────────────────┐
        │                                    │
   ┌────▼────┐  ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
   │ 🔴      │  │ 🟢      │  │ 🟡      │  │ 🔵      │
   │ MOTIF   │  │ CATALOG │  │ PRISM   │  │ LATTICE │
   │ Themes  │  │ Entities│  │ Alts    │  │ Patterns│
   └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘
        │            │            │            │
        └────────────┴────────────┴────────────┘
                         │
            ┌────────────▼────────────┐
            │  CONTEXT AGGREGATION    │
            │  (All front-line        │
            │   outputs combined)     │
            └────────────┬────────────┘
                         │
        ┌────────────────┴────────────────┐
        │  HIDDEN LAYER                   │
        │  (Sequential Synthesis)         │
        └─────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
   ┌────▼────┐  ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
   │ 🟣      │  │ ⚫      │  │ ⚪      │  │ ⬢       │
   │ WEAVER  │→ │ NULL    │→ │ GAIN    │→ │ SCHEMA  │
   │ Connect │  │ Skeptic │  │ Signal  │  │ Architect│
   └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘
        │            │            │            │
        └────────────┴────────────┴────────────┘
                         │
            ┌────────────▼────────────┐
            │    STRUCTURED OUTPUT    │
            │  - TXT / MD / JSON      │
            │  - YAML / CSV           │
            │  - SCHEMA recommend.    │
            └─────────────────────────┘
```

## Data Flow

### Front Line (Parallel)
All 4 personas receive the same input simultaneously:

```
INPUT → ┬→ MOTIF   → Theme analysis
        ├→ CATALOG → Entity mapping
        ├→ PRISM   → Alternative perspectives  
        └→ LATTICE → Pattern recognition
```

### Hidden Layer (Sequential)
Each persona receives ALL front-line outputs + original input:

```
Front-Line Context → WEAVER  → Cross-persona synthesis
                  ↓
                  NULL    → Gap analysis
                  ↓
                  GAIN    → Signal amplification
                  ↓
                  SCHEMA  → Architecture design
```

## Persona Specializations

### 🔴 MOTIF - Theme Hunter
**Input:** Raw text  
**Output:** 3-5 core themes with metaphors  
**Style:** Surfer-philosopher ("yo so basically—")  
**Use case:** Understanding underlying concepts

### 🟢 CATALOG - Entity Mapper
**Input:** Raw text  
**Output:** Entity graph with relationships  
**Style:** Organized chaos with emojis  
**Use case:** Who/what/where tracking

### 🟡 PRISM - Perspective Shifter
**Input:** Raw text  
**Output:** 4-6 alternative interpretations  
**Style:** Playful contrarian ("OR—")  
**Use case:** Exploring multiple readings

### 🔵 LATTICE - Pattern Spotter
**Input:** Raw text  
**Output:** Structural/mathematical patterns  
**Style:** Synesthete mathematician  
**Use case:** Finding hidden structures

### 🟣 WEAVER - Cross-Persona Synthesist
**Input:** All front-line outputs  
**Output:** Unexpected connections  
**Style:** Quiet precision  
**Use case:** Meta-analysis

### ⚫ NULL - The Skeptic
**Input:** All outputs  
**Output:** Gaps and assumptions  
**Style:** Dry wit  
**Use case:** Quality control

### ⚪ GAIN - Signal Amplifier
**Input:** All outputs  
**Output:** Amplified weak signals  
**Style:** Mixing board operator  
**Use case:** Finding overlooked insights

### ⬢ SCHEMA - Information Architect
**Input:** All outputs + original  
**Output:** File structure recommendations  
**Style:** Database designer on acid  
**Use case:** Organizing findings

## Usage Patterns

### Research Analysis
```
Research Paper
    ↓ SWARM
Themes (MOTIF) + Entities (CATALOG) + Patterns (LATTICE)
    ↓ SCHEMA
Recommended structure:
  /concepts - reference
  /interpretations - analysis  
  /synthesis - meta
```

### Meeting Notes
```
Meeting Transcript
    ↓ SWARM
Themes (MOTIF) + Action Items (CATALOG) + Perspectives (PRISM)
    ↓ SCHEMA
Recommended structure:
  /decisions - what was decided
  /actions - todos with owners
  /context - background
```

### Creative Content
```
Story/Concept
    ↓ SWARM
Themes (MOTIF) + Elements (CATALOG) + Alternatives (PRISM)
    ↓ SCHEMA
Recommended structure:
  /themes - motifs
  /elements - characters/settings
  /variants - alt interpretations
```

## API Call Flow

### Browser Version (index.html)
```
1. User pastes input
2. Click "ACTIVATE SWARM"
3. JavaScript makes 8 sequential fetch() calls to Anthropic API
4. Results stream into UI
5. Export buttons generate files client-side
```

### Gradio Version (app.py)
```
1. User submits input
2. Python makes 4 parallel API calls (front-line)
3. Python makes 4 sequential API calls (hidden layer)
4. Results displayed in Markdown
5. JSON export available
```

### CLI Version (swarm_cli.py)
```
1. Input from file or stdin
2. Front-line processes (4 calls)
3. Hidden layer processes (4 calls)
4. Terminal output with colors
5. JSON saved to disk
```

## Cost & Performance

### API Usage
- **Total calls per run:** 8
- **Front-line:** 4 parallel (faster)
- **Hidden layer:** 4 sequential (context-dependent)

### Typical Metrics
- **Processing time:** 30-45 seconds
- **Cost (Sonnet 4):** ~$0.05-0.10 per run
- **Input limit:** ~100K tokens
- **Output:** ~8K tokens total

### Optimization Strategies
1. **Use Haiku** for testing (faster, cheaper)
2. **Reduce max_tokens** for quicker responses
3. **Skip personas** you don't need
4. **Cache results** for iteration
5. **Batch process** multiple files

## Integration Patterns

### As Library
```python
from swarm_cli import process_swarm
import anthropic

client = anthropic.Anthropic(api_key="...")
results = process_swarm(client, "Your text here")
```

### As CLI Tool
```bash
# Single file
python swarm_cli.py input.txt ./outputs

# From stdin
echo "Your text" | python swarm_cli.py

# Batch processing
python swarm_batch.py ./documents ./outputs
```

### As Web Service
```bash
# Gradio
python app.py

# Custom Flask/FastAPI
# (Build your own wrapper around process_swarm())
```

## Extension Points

### Add New Personas
```python
PERSONAS["frontLine"].append({
    "id": "newpersona",
    "name": "NEWPERSONA",
    "prompt": "System prompt...",
    # ... other fields
})
```

### Custom Processing Pipeline
```python
def custom_pipeline(input_text):
    # Run only specific personas
    results = {}
    results["motif"] = call_claude(MOTIF_PROMPT, input_text)
    results["schema"] = call_claude(SCHEMA_PROMPT, input_text)
    return results
```

### Custom Export Formats
```python
def export_custom(results):
    # Transform results however you want
    return generate_your_format(results)
```

## Troubleshooting

**Slow processing?**
- Front-line is parallel, but API rate limits may apply
- Hidden layer is intentionally sequential (needs context)
- Consider caching results

**Inconsistent outputs?**
- LLMs are non-deterministic
- Set temperature=0 for more consistency (edit API calls)
- Multiple runs may give different perspectives (feature, not bug!)

**High costs?**
- Use Claude Haiku instead of Sonnet
- Reduce max_tokens
- Process fewer personas
- Batch related content

---

## Architecture Philosophy

**Why 8 personas?**  
Different cognitive modes for comprehensive analysis:
- 4 front-line = diverse parallel perspectives
- 4 hidden layer = meta-analysis + synthesis

**Why this order?**  
Sequential hidden layer builds on front-line:
- WEAVER needs all perspectives to synthesize
- NULL needs everything to find gaps
- GAIN needs everything to identify signals
- SCHEMA needs everything to design structure

**Why SCHEMA last?**  
SCHEMA's job is to recommend how to organize ALL the other outputs. It needs the complete picture before designing the architecture.
