"""
THE SWARM - Multi-Persona Pattern Processor
Gradio interface with Conductor meta-window and pass memory system.

8 AI personas process your input:
- Front Line: MOTIF, CATALOG, PRISM, LATTICE
- Hidden Layer: WEAVER, NULL, GAIN, SCHEMA

New in this version:
- CONDUCTOR: meta-window to direct the swarm between passes
- PASS LEDGER: per-document memory of what each pass extracted
- ANOTHER PASS: re-runs swarm on same doc with full history injected
"""

import gradio as gr
import anthropic
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
import base64

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


def make_doc_id(text):
    """Stable hash for a document so we can track passes per doc."""
    return hashlib.md5(text.strip()[:2000].encode()).hexdigest()[:12]


def build_pass_history_block(ledger):
    """Render the pass ledger into a prompt-injectable block."""
    if not ledger:
        return ""
    lines = ["[PASS HISTORY — what previous passes already extracted. Do NOT repeat these findings. Go deeper, go sideways, find what's left on the bone.]"]
    for entry in ledger:
        lines.append(f"\n--- PASS {entry['pass_number']} ({entry['timestamp']}) ---")
        lines.append(f"THEMES COVERED: {entry['motif_summary']}")
        lines.append(f"ENTITIES MAPPED: {entry['catalog_summary']}")
        lines.append(f"PERSPECTIVES TAKEN: {entry['prism_summary']}")
        lines.append(f"PATTERNS FOUND: {entry['lattice_summary']}")
        lines.append(f"GAPS FLAGGED BY NULL: {entry['null_gaps']}")
        lines.append(f"SIGNALS AMPLIFIED BY GAIN: {entry['gain_signals']}")
    lines.append("\n[END PASS HISTORY — find the remaining meat on this carcass.]")
    return "\n".join(lines)


def build_conductor_block(directives):
    """Render queued conductor directives into a prompt-injectable block."""
    if not directives:
        return ""
    lines = ["[CONDUCTOR DIRECTIVES — the human operator has flagged these priorities for this pass. Incorporate them into your analysis.]"]
    for i, d in enumerate(directives, 1):
        lines.append(f"  {i}. {d}")
    lines.append("[END CONDUCTOR DIRECTIVES]")
    return "\n".join(lines)


def inject_context(base_prompt, pass_history_block, conductor_block):
    """Prepend pass history and conductor notes to a persona's system prompt."""
    prefix = ""
    if pass_history_block:
        prefix += pass_history_block + "\n\n"
    if conductor_block:
        prefix += conductor_block + "\n\n"
    return prefix + base_prompt if prefix else base_prompt


def summarize_output(text, max_chars=300):
    """Trim an output to a short summary for the ledger."""
    text = text.strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "…"


def call_claude(system_prompt, user_prompt, image_data=None):
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
        messages_content.append({"type": "text", "text": user_prompt})
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": messages_content}]
        )
        return message.content[0].text
    except Exception as e:
        return f"Error: {str(e)}"


def extract_text_from_file(file_path):
    if not file_path:
        return ""
    path = Path(file_path)
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
            return f"[PDF: {path.name}]\nNote: Install pypdf: pip install pypdf"
        except Exception as e:
            return f"[PDF: {path.name}]\nError: {str(e)}"
    elif path.suffix == '.docx':
        try:
            import docx
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
            return f"[DOCX: {path.name}]\n\n{text}"
        except ImportError:
            return f"[DOCX: {path.name}]\nNote: Install python-docx: pip install python-docx"
        except Exception as e:
            return f"[DOCX: {path.name}]\nError: {str(e)}"
    else:
        return f"[Unsupported file type: {path.suffix}]"


def process_image(image_path):
    if not image_path:
        return None
    try:
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        path = Path(image_path)
        media_type_map = {
            '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
            '.png': 'image/png', '.gif': 'image/gif', '.webp': 'image/webp'
        }
        media_type = media_type_map.get(path.suffix.lower(), 'image/jpeg')
        return {"media_type": media_type, "data": image_data}
    except:
        return None


def process_swarm(input_text, uploaded_file, uploaded_image, session_state, progress=gr.Progress()):
    """Run all personas, injecting pass history and conductor directives."""

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
        return "⚠️ Need input to process!", "{}", session_state, format_ledger_display(session_state)

    # --- Session / document tracking ---
    doc_id = make_doc_id(complete_input)

    # If this is a new document, reset ledger for it
    if session_state.get("doc_id") != doc_id:
        session_state = {
            "doc_id": doc_id,
            "pass_ledger": [],
            "conductor_queue": session_state.get("conductor_queue", []),
            "raw_input": complete_input
        }

    pass_number = len(session_state["pass_ledger"]) + 1
    pass_history_block = build_pass_history_block(session_state["pass_ledger"])
    conductor_block = build_conductor_block(session_state.get("conductor_queue", []))

    results = {
        "timestamp": datetime.now().isoformat().replace(':', '-')[:19],
        "pass_number": pass_number,
        "doc_id": doc_id,
        "input": complete_input,
        "hasImage": bool(image_data),
        "frontLine": {},
        "hiddenLayer": {}
    }

    # --- Front line (parallel) ---
    progress(0.1, desc=f"Pass {pass_number} — front line firing...")
    for i, persona in enumerate(PERSONAS["frontLine"]):
        progress((i + 1) / 12, desc=f"Pass {pass_number} — {persona['name']}...")
        augmented_prompt = inject_context(persona["prompt"], pass_history_block, conductor_block)
        result = call_claude(augmented_prompt, complete_input, image_data)
        results["frontLine"][persona["id"]] = result

    # --- Hidden layer (sequential) ---
    progress(0.5, desc=f"Pass {pass_number} — hidden layer synthesizing...")
    front_context = "\n\n---\n\n".join([
        f"{pid.upper()}: {result}"
        for pid, result in results["frontLine"].items()
    ])
    context_prompt = f"FRONT LINE OUTPUTS:\n\n{front_context}\n\n---\n\nORIGINAL INPUT:\n{complete_input}"

    for i, persona in enumerate(PERSONAS["hiddenLayer"]):
        progress(0.5 + (i + 1) / 16, desc=f"Pass {pass_number} — {persona['name']}...")
        augmented_prompt = inject_context(persona["prompt"], pass_history_block, conductor_block)
        result = call_claude(augmented_prompt, context_prompt, image_data)
        results["hiddenLayer"][persona["id"]] = result

    progress(1.0, desc=f"Pass {pass_number} complete.")

    # --- Build ledger entry ---
    ledger_entry = {
        "pass_number": pass_number,
        "timestamp": results["timestamp"],
        "motif_summary": summarize_output(results["frontLine"].get("motif", "")),
        "catalog_summary": summarize_output(results["frontLine"].get("catalog", "")),
        "prism_summary": summarize_output(results["frontLine"].get("prism", "")),
        "lattice_summary": summarize_output(results["frontLine"].get("lattice", "")),
        "null_gaps": summarize_output(results["hiddenLayer"].get("null", "")),
        "gain_signals": summarize_output(results["hiddenLayer"].get("gain", "")),
        "conductor_directives_used": list(session_state.get("conductor_queue", []))
    }
    session_state["pass_ledger"].append(ledger_entry)
    # Clear conductor queue after it's been consumed by this pass
    session_state["conductor_queue"] = []

    # --- Format output ---
    output_text = f"# ⬡ THE SWARM — Pass {pass_number}\n\n"
    output_text += f"**Doc ID:** `{doc_id}` | **Session:** {results['timestamp']}\n\n"
    if pass_number > 1:
        output_text += f"*This is pass {pass_number} on this document. Previous passes have been factored in.*\n\n"
    if ledger_entry["conductor_directives_used"]:
        output_text += "**Conductor directives applied this pass:**\n"
        for d in ledger_entry["conductor_directives_used"]:
            output_text += f"- {d}\n"
        output_text += "\n"
    output_text += "---\n\n## FRONT LINE ANALYSIS\n\n"
    for persona in PERSONAS["frontLine"]:
        pid = persona["id"]
        output_text += f"### {persona['name']} — {persona['role']}\n\n"
        output_text += results["frontLine"][pid] + "\n\n"
    output_text += "---\n\n## HIDDEN LAYER SYNTHESIS\n\n"
    for persona in PERSONAS["hiddenLayer"]:
        pid = persona["id"]
        output_text += f"### {persona['name']} — {persona['role']}\n\n"
        output_text += results["hiddenLayer"][pid] + "\n\n"

    json_export = json.dumps(results, indent=2)

    return output_text, json_export, session_state, format_ledger_display(session_state)


def format_ledger_display(session_state):
    """Render the pass ledger as readable markdown for the UI panel."""
    ledger = session_state.get("pass_ledger", [])
    doc_id = session_state.get("doc_id", "—")
    if not ledger:
        return "*No passes run yet. Load a document and activate the swarm.*"
    lines = [f"**Doc ID:** `{doc_id}` | **Passes completed:** {len(ledger)}\n"]
    lines.append("---")
    for entry in ledger:
        lines.append(f"\n### 🦴 Pass {entry['pass_number']} — {entry['timestamp']}")
        if entry.get("conductor_directives_used"):
            lines.append("**Conductor directives applied:**")
            for d in entry["conductor_directives_used"]:
                lines.append(f"  - {d}")
        lines.append(f"**🔴 MOTIF extracted:** {entry['motif_summary']}")
        lines.append(f"**🟢 CATALOG mapped:** {entry['catalog_summary']}")
        lines.append(f"**🟡 PRISM perspectives:** {entry['prism_summary']}")
        lines.append(f"**🔵 LATTICE patterns:** {entry['lattice_summary']}")
        lines.append(f"**⚫ NULL gaps flagged:** {entry['null_gaps']}")
        lines.append(f"**⚪ GAIN signals boosted:** {entry['gain_signals']}")
        lines.append("---")
    return "\n".join(lines)


def add_conductor_directive(directive, session_state):
    """Queue a conductor directive for the next pass."""
    if not directive or not directive.strip():
        return session_state, format_conductor_queue(session_state), ""
    if "conductor_queue" not in session_state:
        session_state["conductor_queue"] = []
    session_state["conductor_queue"].append(directive.strip())
    return session_state, format_conductor_queue(session_state), ""


def clear_conductor_queue(session_state):
    session_state["conductor_queue"] = []
    return session_state, format_conductor_queue(session_state)


def format_conductor_queue(session_state):
    queue = session_state.get("conductor_queue", [])
    if not queue:
        return "*Queue empty — directives you add here will shape the next pass.*"
    lines = [f"**{len(queue)} directive(s) queued for next pass:**\n"]
    for i, d in enumerate(queue, 1):
        lines.append(f"{i}. {d}")
    return "\n".join(lines)


def new_document_session(session_state):
    """Wipe the current document state so a fresh doc starts clean."""
    new_state = {
        "doc_id": None,
        "pass_ledger": [],
        "conductor_queue": session_state.get("conductor_queue", []),
        "raw_input": ""
    }
    return new_state, format_ledger_display(new_state), "*Session cleared. Load a new document.*"


# ─── GRADIO UI ────────────────────────────────────────────────────────────────

CSS = """
.gradio-container {
    font-family: 'Courier New', monospace !important;
    background: #0a0a0a !important;
}
h1, h2, h3 {
    color: #00ff00 !important;
    letter-spacing: 2px;
}
h1 {
    text-align: center;
    text-shadow: 0 0 20px #00ff00;
    letter-spacing: 4px;
}
.conductor-panel {
    border: 1px solid #ff00ff !important;
    border-radius: 6px;
    padding: 8px;
}
.ledger-panel {
    border: 1px solid #00ffaa !important;
    border-radius: 6px;
    padding: 8px;
}
label {
    color: #00ff88 !important;
}
"""

with gr.Blocks(
    theme=gr.themes.Base(primary_hue="green", secondary_hue="cyan", neutral_hue="slate"),
    css=CSS,
    title="THE SWARM"
) as app:

    # ── Persistent session state ──
    session_state = gr.State({
        "doc_id": None,
        "pass_ledger": [],
        "conductor_queue": [],
        "raw_input": ""
    })

    gr.Markdown("# ⬡ THE SWARM ⬡\n### Multi-Persona Pattern Processor")

    with gr.Row():
        # ── LEFT: Input + Controls ──────────────────────────────────────────
        with gr.Column(scale=3):
            with gr.Row():
                file_upload = gr.File(
                    label="📁 Upload File",
                    file_types=[".txt", ".md", ".json", ".csv", ".pdf", ".docx"]
                )
                image_upload = gr.Image(label="🖼️ Upload Image", type="filepath")

            input_box = gr.Textbox(
                label="TEXT INPUT",
                placeholder="Paste content here, or upload a file above…",
                lines=10, max_lines=20
            )

            with gr.Row():
                process_btn = gr.Button("⚡ ACTIVATE SWARM ⚡", variant="primary", size="lg")
                another_pass_btn = gr.Button("🔁 ANOTHER PASS", variant="secondary", size="lg")
                new_doc_btn = gr.Button("🆕 NEW DOCUMENT", size="sm")

        # ── RIGHT: Conductor + Ledger ────────────────────────────────────────
        with gr.Column(scale=2):
            gr.Markdown("## 🎛️ CONDUCTOR\n*Talk to the swarm. Directives queue here and fire on the next pass.*")

            conductor_input = gr.Textbox(
                label="Directive",
                placeholder="e.g. 'Next pass: PRISM should look at this from a legal angle' or 'LATTICE missed the rhythm in section 3'",
                lines=3,
                elem_classes=["conductor-panel"]
            )
            with gr.Row():
                add_directive_btn = gr.Button("➕ Queue Directive", variant="secondary")
                clear_queue_btn = gr.Button("🗑️ Clear Queue", size="sm")

            conductor_display = gr.Markdown(
                value="*Queue empty — directives you add here will shape the next pass.*",
                label="Queued Directives",
                elem_classes=["conductor-panel"]
            )

            gr.Markdown("---\n## 🦴 PASS LEDGER\n*What each pass already carved off this carcass.*")
            ledger_display = gr.Markdown(
                value="*No passes run yet.*",
                label="Pass History",
                elem_classes=["ledger-panel"]
            )

    # ── Output area ──────────────────────────────────────────────────────────
    with gr.Row():
        output_box = gr.Markdown(label="SWARM OUTPUT")

    with gr.Row():
        json_output = gr.Code(label="JSON EXPORT", language="json", lines=10)

    # ── Wiring ───────────────────────────────────────────────────────────────

    def run_pass(input_text, file, image, state):
        output, json_out, new_state, ledger_md = process_swarm(input_text, file, image, state)
        return output, json_out, new_state, ledger_md

    process_btn.click(
        fn=run_pass,
        inputs=[input_box, file_upload, image_upload, session_state],
        outputs=[output_box, json_output, session_state, ledger_display]
    )

    another_pass_btn.click(
        fn=run_pass,
        inputs=[input_box, file_upload, image_upload, session_state],
        outputs=[output_box, json_output, session_state, ledger_display]
    )

    add_directive_btn.click(
        fn=add_conductor_directive,
        inputs=[conductor_input, session_state],
        outputs=[session_state, conductor_display, conductor_input]
    )

    clear_queue_btn.click(
        fn=clear_conductor_queue,
        inputs=[session_state],
        outputs=[session_state, conductor_display]
    )

    new_doc_btn.click(
        fn=new_document_session,
        inputs=[session_state],
        outputs=[session_state, ledger_display, output_box]
    )


if __name__ == "__main__":
    app.launch()
