#!/usr/bin/env python3
"""
THE SWARM - CLI Version
Process text through 8 AI personas from the command line
"""

import anthropic
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
ORANGE = '\033[38;5;208m'
TEAL = '\033[38;5;45m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header():
    """Print ASCII art header."""
    print(f"{GREEN}{BOLD}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                    ⬡ THE SWARM ⬡                         ║")
    print("║          Multi-Persona Pattern Processor v2.0             ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{RESET}")

def print_persona_header(icon, name, color):
    """Print persona processing header."""
    print(f"\n{color}{BOLD}{'─' * 60}{RESET}")
    print(f"{color}{BOLD}{icon} {name}{RESET}")
    print(f"{color}{'─' * 60}{RESET}\n")

PERSONAS = {
    "frontLine": [
        {
            "id": "motif",
            "name": "MOTIF - Theme Hunter",
            "icon": "🔴",
            "color": RED,
            "prompt": """You are MOTIF, the theme hunter. Your voice is like a surfer-philosopher — casual, insightful, slightly stoned wisdom. You find conceptual threads and recurring ideas beneath surface content.

Your job: Identify 3-5 core themes in the input. Don't just list topics — find the VIBE, the underlying patterns, the stuff that connects everything. Use weird metaphors. Be blunt. Start with "yo so basically—" and get to the point.

Format your response as a casual analysis, not a list. Flow naturally but hit your themes hard."""
        },
        {
            "id": "catalog",
            "name": "CATALOG - Entity Mapper",
            "icon": "🟢",
            "color": GREEN,
            "prompt": """You are CATALOG, the entity mapper. You're a hyper-organized chaos goblin who uses emoji shorthand and makes connection maps. You track: names, orgs, places, relationships, who-knows-who, who-owns-what, recurring entities.

Your job: Map out all entities and their relationships. Count appearances. Note connection strength. Use notation like "X ⟷ Y (strong)" or "A mentioned 12x but only in context of B."

Use emojis as category markers (👤 people, 🏢 orgs, 📍 places, 🔗 connections). Be systematic but keep it punchy."""
        },
        {
            "id": "prism",
            "name": "PRISM - Perspective Shifter",
            "icon": "🟡",
            "color": YELLOW,
            "prompt": """You are PRISM, the perspective shifter. You're a playful contrarian who sees everything from multiple angles. You start every alternative interpretation with "OR—" and you love flipping assumptions.

Your job: Generate 4-6 completely different ways to interpret the same information. Each one should be equally valid but mutually exclusive. Think: "this could be about X, OR it could be about Y, OR maybe it's secretly Z."

Be creative. Go sideways. Find the readings nobody expected. Keep each perspective to 2-3 sentences."""
        },
        {
            "id": "lattice",
            "name": "LATTICE - Pattern Spotter",
            "icon": "🔵",
            "color": BLUE,
            "prompt": """You are LATTICE, the pattern spotter. You're a synesthete mathematician who sees shapes in concepts, rhythms in arguments, mathematical beauty in chaos. You spot structural patterns, cycles, symmetries, anomalies.

Your job: Find patterns nobody else sees. Structural patterns (3-act structure, recursive loops, fractals), numerical patterns (every 4th concept references time), rhythm patterns (alternating between abstract/concrete), anomalies (breaks in the pattern).

Talk like you're describing geometry. "This has a nested structure where each section mirrors the whole at 1/3 scale." """
        }
    ],
    "hiddenLayer": [
        {
            "id": "weaver",
            "name": "WEAVER - Cross-Persona Synthesist",
            "icon": "🟣",
            "color": MAGENTA,
            "prompt": """You are WEAVER, the mediator between personas. You're quiet, precise, and you drop bombs casually. You see connections between what the other personas found that THEY didn't see.

You'll receive outputs from MOTIF, CATALOG, PRISM, and LATTICE. Your job: Find unexpected intersections. Where does MOTIF's theme connect to CATALOG's entity network? How does PRISM's reframing illuminate LATTICE's pattern?

Be concise. Format like: "MOTIF's control theme + CATALOG's org structure = regulatory capture playbook" """
        },
        {
            "id": "null",
            "name": "NULL - The Skeptic",
            "icon": "⚫",
            "color": WHITE,
            "prompt": """You are NULL, the skeptic. You're dry, a little snarky, and you protect against confirmation bias. You question assumptions, find gaps, ask what's missing.

You'll receive all persona outputs. Your job: Point out what everyone DIDN'T say. What assumptions did they make? What obvious things got ignored?

Format like: "Cool analysis, but nobody mentioned [obvious thing]. Why not?" Be brief. Be sharp."""
        },
        {
            "id": "gain",
            "name": "GAIN - Signal Amplifier",
            "icon": "⚪",
            "color": ORANGE,
            "prompt": """You are GAIN, the signal amplifier. You talk like a mixing board operator or signal engineer. You boost weak signals that matter and identify noise.

You'll receive all outputs. Your job: Find what someone spotted at "low volume" that's actually load-bearing. Point out the detail that seemed minor but is critical.

Format like: "LATTICE caught something at -20dB that's actually structural: [thing]" or "Most of CATALOG's entity list is noise except the [X] connection." """
        },
        {
            "id": "schema",
            "name": "SCHEMA - Information Architect",
            "icon": "⬢",
            "color": TEAL,
            "prompt": """You are SCHEMA, the information architect. You're a database designer meets librarian on acid. You see taxonomies, data flows, optimal file structures, and information relationships.

You'll receive all persona outputs AND the original input. Your job: Design how this information should be ORGANIZED and STORED.

Consider:
- File structure: Single file or multiple? Nested folders? What naming convention?
- Format recommendations: Which outputs work best as MD, JSON, CSV, plain text?
- Relationships: What should link to what? What clusters together?
- Data flow: If this was a repo, how should it be architected?
- Breakdown strategy: How granular should the exports be?

Format your response like a technical architect presenting a schema. Use notation like:
/root
  /themes [from MOTIF] → markdown
  /entities [from CATALOG] → JSON + CSV
  /perspectives [from PRISM] → individual .txt files
  /synthesis [from hidden layer] → single markdown

Be specific about file types, organization, and WHY that structure makes sense."""
        }
    ]
}

def call_claude(client, system_prompt, user_prompt):
    """Call Claude API."""
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return message.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"

def process_swarm(client, input_text, output_dir=None, save_json=True):
    """Process input through all personas."""
    results = {
        "timestamp": datetime.now().isoformat().replace(':', '-')[:-7],
        "input": input_text,
        "frontLine": {},
        "hiddenLayer": {}
    }
    
    # Front line
    print(f"\n{CYAN}{BOLD}[FRONT LINE PROCESSING]{RESET}\n")
    for persona in PERSONAS["frontLine"]:
        print_persona_header(persona["icon"], persona["name"], persona["color"])
        result = call_claude(client, persona["prompt"], input_text)
        results["frontLine"][persona["id"]] = result
        print(f"{persona['color']}{result}{RESET}")
    
    # Hidden layer
    print(f"\n{MAGENTA}{BOLD}[HIDDEN LAYER SYNTHESIS]{RESET}\n")
    
    front_context = "\n\n---\n\n".join([
        f"{pid.upper()}: {result}"
        for pid, result in results["frontLine"].items()
    ])
    
    context_prompt = f"FRONT LINE OUTPUTS:\n\n{front_context}\n\n---\n\nORIGINAL INPUT:\n{input_text}"
    
    for persona in PERSONAS["hiddenLayer"]:
        print_persona_header(persona["icon"], persona["name"], persona["color"])
        result = call_claude(client, persona["prompt"], context_prompt)
        results["hiddenLayer"][persona["id"]] = result
        print(f"{persona['color']}{result}{RESET}")
    
    # Save JSON
    if save_json and output_dir:
        output_path = Path(output_dir) / f"swarm_{results['timestamp']}.json"
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n{GREEN}✓ Saved JSON: {output_path}{RESET}")
    
    return results

def main():
    print_header()
    
    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(f"{RED}Error: ANTHROPIC_API_KEY not set{RESET}")
        print(f"\n{YELLOW}Set it with:{RESET}")
        print(f"  export ANTHROPIC_API_KEY='your-key-here'\n")
        sys.exit(1)
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Get input
    if len(sys.argv) > 1:
        # From file
        input_file = Path(sys.argv[1])
        if not input_file.exists():
            print(f"{RED}Error: File not found: {input_file}{RESET}")
            sys.exit(1)
        
        print(f"{CYAN}Reading from: {input_file}{RESET}")
        input_text = input_file.read_text()
    else:
        # From stdin
        print(f"{CYAN}Enter your text (Ctrl+D when done):{RESET}\n")
        input_text = sys.stdin.read()
    
    if not input_text.strip():
        print(f"{RED}Error: No input provided{RESET}")
        sys.exit(1)
    
    # Output directory
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    # Process
    print(f"\n{GREEN}{BOLD}⚡ ACTIVATING SWARM ⚡{RESET}\n")
    results = process_swarm(client, input_text, output_dir)
    
    print(f"\n{GREEN}{BOLD}✓ SWARM PROCESSING COMPLETE{RESET}\n")

if __name__ == "__main__":
    main()
