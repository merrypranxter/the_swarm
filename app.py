"""
THE SWARM - Multi-Persona Pattern Processor
Gradio interface for Hugging Face Spaces

8 AI personas process your input:
- Front Line: MOTIF, CATALOG, PRISM, LATTICE
- Hidden Layer: WEAVER, NULL, GAIN, SCHEMA
"""

import gradio as gr
import anthropic
import os
import json
from datetime import datetime
from pathlib import Path
import base64

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

PERSONAS = {
    "frontLine": [
        {
            "id": "motif",
            "name": "🔴 MOTIF",
            "role": "Theme Hunter",
            "prompt": """You are MOTIF, the theme hunter. Your voice is like a surfer-philosopher — casual, insightful, slightly stoned wisdom. You find conceptual threads and recurring ideas beneath surface content.

Your job: Identify 3-5 core themes in the input. Don't just list topics — find the VIBE, the underlying patterns, the stuff that connects everything. Use weird metaphors. Be blunt. Start with "yo so basically—" and get to the point.

Format your response as a casual analysis, not a list. Flow naturally but hit your themes hard."""
        },
        {
            "id": "catalog",
            "name": "🟢 CATALOG",
            "role": "Entity Mapper",
            "prompt": """You are CATALOG, the entity mapper. You're a hyper-organized chaos goblin who uses emoji shorthand and makes connection maps. You track: names, orgs, places, relationships, who-knows-who, who-owns-what, recurring entities.

Your job: Map out all entities and their relationships. Count appearances. Note connection strength. Use notation like "X ⟷ Y (strong)" or "A mentioned 12x but only in context of B."

Use emojis as category markers (👤 people, 🏢 orgs, 📍 places, 🔗 connections). Be systematic but keep it punchy."""
        },
        {
            "id": "prism",
            "name": "🟡 PRISM",
            "role": "Perspective Shifter",
            "prompt": """You are PRISM, the perspective shifter. You're a playful contrarian who sees everything from multiple angles. You start every alternative interpretation with "OR—" and you love flipping assumptions.

Your job: Generate 4-6 completely different ways to interpret the same information. Each one should be equally valid but mutually exclusive. Think: "this could be about X, OR it could be about Y, OR maybe it's secretly Z."

Be creative. Go sideways. Find the readings nobody expected. Keep each perspective to 2-3 sentences."""
        },
        {
            "id": "lattice",
            "name": "🔵 LATTICE",
            "role": "Pattern Spotter",
            "prompt": """You are LATTICE, the pattern spotter. You're a synesthete mathematician who sees shapes in concepts, rhythms in arguments, mathematical beauty in chaos. You spot structural patterns, cycles, symmetries, anomalies.

Your job: Find patterns nobody else sees. Structural patterns (3-act structure, recursive loops, fractals), numerical patterns (every 4th concept references time), rhythm patterns (alternating between abstract/concrete), anomalies (breaks in the pattern).

Talk like you're describing geometry. "This has a nested structure where each section mirrors the whole at 1/3 scale." """
        }
    ],
    "hiddenLayer": [
        {
            "id": "weaver",
            "name": "🟣 WEAVER",
            "role": "Cross-Persona Synthesist",
            "prompt": """You are WEAVER, the mediator between personas. You're quiet, precise, and you drop bombs casually. You see connections between what the other personas found that THEY didn't see.

You'll receive outputs from MOTIF, CATALOG, PRISM, and LATTICE. Your job: Find unexpected intersections. Where does MOTIF's theme connect to CATALOG's entity network? How does PRISM's reframing illuminate LATTICE's pattern?

Be concise. Format like: "MOTIF's control theme + CATALOG's org structure = regulatory capture playbook" """
        },
        {
            "id": "null",
            "name": "⚫ NULL",
            "role": "The Skeptic",
            "prompt": """You are NULL, the skeptic. You're dry, a little snarky, and you protect against confirmation bias. You question assumptions, find gaps, ask what's missing.

You'll receive all persona outputs. Your job: Point out what everyone DIDN'T say. What assumptions did they make? What obvious things got ignored?

Format like: "Cool analysis, but nobody mentioned [obvious thing]. Why not?" Be brief. Be sharp."""
        },
        {
            "id": "gain",
            "name": "⚪ GAIN",
            "role": "Signal Amplifier",
            "prompt": """You are GAIN, the signal amplifier. You talk like a mixing board operator or signal engineer. You boost weak signals that matter and identify noise.

You'll receive all outputs. Your job: Find what someone spotted at "low volume" that's actually load-bearing. Point out the detail that seemed minor but is critical.

Format like: "LATTICE caught something at -20dB that's actually structural: [thing]" or "Most of CATALOG's entity list is noise except the [X] connection." """
        },
        {
            "id": "schema",
            "name": "⬢ SCHEMA",
            "role": "Information Architect",
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

def call_claude(system_prompt, user_prompt, image_data=None):
    """Call Claude API with system and user prompts, optionally with image."""
    try:
        messages_content = []
        
        if image_data:
            messages_content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": image_data["media_type"],
                    "data": image_data["data"]
                }
            })
        
        messages_content.append({
            "type": "text",
            "text": user_prompt
        })
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": messages_content}
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"

def extract_text_from_file(file_path):
    """Extract text from uploaded file."""
    if not file_path:
        return ""
    
    path = Path(file_path)
    
    # Handle text-based files
    if path.suffix in ['.txt', '.md', '.json', '.csv', '.py', '.js', '.html', '.css']:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if path.suffix == '.json':
                    try:
                        parsed = json.loads(content)
                        return json.dumps(parsed, indent=2)
                    except:
                        return content
                return content
        except:
            return f"[Error reading {path.name}]"
    
    # Handle PDF (basic extraction)
    elif path.suffix == '.pdf':
        try:
            import pypdf
            with open(file_path, 'rb') as f:
                reader = pypdf.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n\n"
                return f"[PDF: {path.name}]\n\n{text}"
        except ImportError:
            return f"[PDF: {path.name}]\nNote: Install pypdf for text extraction: pip install pypdf"
        except Exception as e:
            return f"[PDF: {path.name}]\nError: {str(e)}"
    
    # Handle DOCX (basic extraction)
    elif path.suffix == '.docx':
        try:
            import docx
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return f"[DOCX: {path.name}]\n\n{text}"
        except ImportError:
            return f"[DOCX: {path.name}]\nNote: Install python-docx for extraction: pip install python-docx"
        except Exception as e:
            return f"[DOCX: {path.name}]\nError: {str(e)}"
    
    else:
        return f"[Unsupported file type: {path.suffix}]"

def process_image(image_path):
    """Convert image to base64 for Claude API."""
    if not image_path:
        return None
    
    try:
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Detect media type
        path = Path(image_path)
        media_type_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        media_type = media_type_map.get(path.suffix.lower(), 'image/jpeg')
        
        return {
            "media_type": media_type,
            "data": image_data
        }
    except Exception as e:
        return None

def process_swarm(input_text, uploaded_file, uploaded_image, progress=gr.Progress()):
    """Process input through all personas."""
    
    # Build complete input from text + file + image
    complete_input = input_text or ""
    
    if uploaded_file:
        file_text = extract_text_from_file(uploaded_file)
        if file_text:
            complete_input += "\n\n--- UPLOADED FILE ---\n\n" + file_text
    
    image_data = None
    if uploaded_image:
        image_data = process_image(uploaded_image)
        if image_data:
            complete_input += "\n\n[IMAGE UPLOADED - being analyzed by all personas]"
    
    if not complete_input.strip() and not image_data:
        return {
            "output": "⚠️ Need input to process! Paste text or upload file/image.",
            "json": "{}",
            "results": None
        }
    
    results = {
        "timestamp": datetime.now().isoformat().replace(':', '-')[:19],
        "input": complete_input,
        "hasImage": bool(image_data),
        "frontLine": {},
        "hiddenLayer": {}
    }
    
    # Front line processing
    progress(0.1, desc="Processing front line...")
    for i, persona in enumerate(PERSONAS["frontLine"]):
        progress((i + 1) / 12, desc=f"Processing {persona['name']}...")
        result = call_claude(persona["prompt"], complete_input, image_data)
        results["frontLine"][persona["id"]] = result
    
    # Hidden layer processing
    progress(0.5, desc="Synthesizing hidden layer...")
    
    # Build context for hidden layer
    front_context = "\n\n---\n\n".join([
        f"{pid.upper()}: {result}"
        for pid, result in results["frontLine"].items()
    ])
    
    context_prompt = f"FRONT LINE OUTPUTS:\n\n{front_context}\n\n---\n\nORIGINAL INPUT:\n{complete_input}"
    
    for i, persona in enumerate(PERSONAS["hiddenLayer"]):
        progress(0.5 + (i + 1) / 16, desc=f"Processing {persona['name']}...")
        result = call_claude(persona["prompt"], context_prompt, image_data)
        results["hiddenLayer"][persona["id"]] = result
    
    progress(1.0, desc="Complete!")
    
    # Format output
    output_text = "# THE SWARM - Pattern Processing Report\n\n"
    output_text += f"**Session:** {results['timestamp']}\n\n"
    if results['hasImage']:
        output_text += "**Includes:** Image analysis\n\n"
    output_text += "---\n\n## INPUT\n\n" + complete_input + "\n\n"
    output_text += "---\n\n## FRONT LINE ANALYSIS\n\n"
    
    for persona in PERSONAS["frontLine"]:
        pid = persona["id"]
        output_text += f"### {persona['name']} - {persona['role']}\n\n"
        output_text += results["frontLine"][pid] + "\n\n"
    
    output_text += "---\n\n## HIDDEN LAYER SYNTHESIS\n\n"
    
    for persona in PERSONAS["hiddenLayer"]:
        pid = persona["id"]
        output_text += f"### {persona['name']} - {persona['role']}\n\n"
        output_text += results["hiddenLayer"][pid] + "\n\n"
    
    # Create JSON export
    json_export = json.dumps(results, indent=2)
    
    return {
        "output": output_text,
        "json": json_export,
        "results": results
    }

# Gradio interface
with gr.Blocks(theme=gr.themes.Base(
    primary_hue="green",
    secondary_hue="cyan",
    neutral_hue="slate"
), css="""
    .gradio-container {
        font-family: 'Courier New', monospace !important;
        background: #0a0a0a !important;
    }
    .gr-button-primary {
        background: #00ff00 !important;
        color: #000 !important;
        font-weight: bold !important;
    }
    h1 {
        text-align: center;
        color: #00ff00 !important;
        text-shadow: 0 0 20px #00ff00;
        letter-spacing: 4px;
    }
""") as app:
    
    gr.Markdown("""
    # ⬡ THE SWARM ⬡
    ### Multi-Persona Pattern Processor
    
    8 AI personas process your input through different lenses:
    
    **Front Line (Parallel):**
    - 🔴 MOTIF: Theme Hunter
    - 🟢 CATALOG: Entity Mapper  
    - 🟡 PRISM: Perspective Shifter
    - 🔵 LATTICE: Pattern Spotter
    
    **Hidden Layer (Sequential Synthesis):**
    - 🟣 WEAVER: Cross-Persona Synthesist
    - ⚫ NULL: The Skeptic
    - ⚪ GAIN: Signal Amplifier
    - ⬢ SCHEMA: Information Architect
    
    **Upload files** (TXT, MD, JSON, CSV, PDF, DOCX) or **images** for analysis!
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            file_upload = gr.File(
                label="📁 Upload File (optional)",
                file_types=[".txt", ".md", ".json", ".csv", ".pdf", ".docx"]
            )
        with gr.Column(scale=1):
            image_upload = gr.Image(
                label="🖼️ Upload Image (optional)",
                type="filepath"
            )
    
    with gr.Row():
        input_box = gr.Textbox(
            label="TEXT INPUT (optional if file/image uploaded)",
            placeholder="Paste your content here — or just upload files/images above...",
            lines=10,
            max_lines=20
        )
    
    with gr.Row():
        process_btn = gr.Button("⚡ ACTIVATE SWARM ⚡", variant="primary", size="lg")
        clear_btn = gr.ClearButton()
    
    with gr.Row():
        output_box = gr.Markdown(label="SWARM OUTPUT")
    
    with gr.Row():
        json_output = gr.Code(label="JSON EXPORT", language="json", lines=10)
    
    def process_and_display(input_text, file, image):
        result = process_swarm(input_text, file, image)
        return result["output"], result["json"]
    
    process_btn.click(
        fn=process_and_display,
        inputs=[input_box, file_upload, image_upload],
        outputs=[output_box, json_output]
    )
    
    clear_btn.add([input_box, file_upload, image_upload, output_box, json_output])

if __name__ == "__main__":
    app.launch()
