# Swarm Examples

This directory contains sample inputs and outputs demonstrating THE SWARM's capabilities.

## Available Examples

### timewave_analysis.json

**Input:** Terence McKenna's Timewave Zero theory

**Demonstrates:**
- Theme extraction (MOTIF finding pattern-obsession + apocalyptic thinking)
- Entity mapping (CATALOG tracking concepts and connections)
- Multiple perspective generation (PRISM giving 6 different readings)
- Pattern recognition (LATTICE finding recursive structure)
- Cross-synthesis (WEAVER connecting findings)
- Critical analysis (NULL questioning falsifiability)
- Signal amplification (GAIN highlighting key insights)
- **SCHEMA recommendation:** Complete file structure for organizing the analysis

**Key Insight from SCHEMA:**
```
/timewave_analysis
  /concepts - reference material (MD + JSON)
  /interpretations - individual perspectives (separate txt files)
  /synthesis - analytical narratives (MD)
  /metadata - session data (JSON + CSV)
```

This structure separates *what was found* from *how to read it* from *what it means*, mirroring the processing architecture.

## Using Examples

### Load and View
```python
import json

with open('examples/timewave_analysis.json', 'r') as f:
    swarm_output = json.load(f)

# Access specific personas
print(swarm_output['frontLine']['motif'])
print(swarm_output['hiddenLayer']['schema'])
```

### Create Your Own

1. Run THE SWARM with your content
2. Export JSON
3. Save to this folder
4. Add documentation here

## Example Categories

We're collecting examples across different domains:

- **Philosophy/Theory** - Abstract concept analysis (like Timewave)
- **Research Papers** - Academic text processing (coming soon)
- **Meeting Notes** - Synthesis and action items (coming soon)
- **Creative Content** - Analyzing art, writing, etc (coming soon)
- **Technical Docs** - Code and documentation analysis (coming soon)

Want to contribute an example? Submit a PR with:
1. Your JSON output
2. Brief description of the input
3. What made the output interesting

## Schema Patterns

From analyzing multiple outputs, SCHEMA tends to recommend:

**For Research/Analysis:**
```
/concepts - foundational material
/interpretations - different readings
/synthesis - connections and meta-analysis
/metadata - session info and graphs
```

**For Meeting/Task Content:**
```
/action_items - extracted todos
/decisions - what was decided
/context - background and discussion
/follow_up - next steps
```

**For Creative Content:**
```
/themes - core motifs and patterns
/elements - characters, settings, techniques
/analysis - deep dives on specific aspects
/variants - alternative interpretations
```

The beauty of SCHEMA is it adapts its recommendations to the *type* of content being processed.
