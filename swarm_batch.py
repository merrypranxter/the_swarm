#!/usr/bin/env python3
"""
THE SWARM - Batch Processor
Process multiple files through the swarm at once
"""

import anthropic
import os
import sys
import json
from pathlib import Path
from datetime import datetime
from swarm_cli import PERSONAS, call_claude, print_header

def process_file(client, input_file, output_dir):
    """Process a single file."""
    print(f"\n{'=' * 60}")
    print(f"Processing: {input_file.name}")
    print(f"{'=' * 60}\n")
    
    input_text = input_file.read_text()
    
    results = {
        "timestamp": datetime.now().isoformat().replace(':', '-')[:-7],
        "source_file": str(input_file),
        "input": input_text,
        "frontLine": {},
        "hiddenLayer": {}
    }
    
    # Front line
    print("[FRONT LINE]")
    for persona in PERSONAS["frontLine"]:
        print(f"  {persona['icon']} {persona['id']}...", end='', flush=True)
        result = call_claude(client, persona["prompt"], input_text)
        results["frontLine"][persona["id"]] = result
        print(" ✓")
    
    # Hidden layer
    print("[HIDDEN LAYER]")
    front_context = "\n\n---\n\n".join([
        f"{pid.upper()}: {result}"
        for pid, result in results["frontLine"].items()
    ])
    
    context_prompt = f"FRONT LINE OUTPUTS:\n\n{front_context}\n\n---\n\nORIGINAL INPUT:\n{input_text}"
    
    for persona in PERSONAS["hiddenLayer"]:
        print(f"  {persona['icon']} {persona['id']}...", end='', flush=True)
        result = call_claude(client, persona["prompt"], context_prompt)
        results["hiddenLayer"][persona["id"]] = result
        print(" ✓")
    
    # Save
    output_file = output_dir / f"swarm_{input_file.stem}_{results['timestamp']}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Saved: {output_file}")
    
    return results

def main():
    print_header()
    print("BATCH PROCESSOR\n")
    
    # Check API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        print("\nSet it with:")
        print("  export ANTHROPIC_API_KEY='your-key-here'\n")
        sys.exit(1)
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Get input directory/pattern
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python swarm_batch.py <input_dir> [output_dir]")
        print("  python swarm_batch.py 'inputs/*.txt' [output_dir]")
        print("\nExamples:")
        print("  python swarm_batch.py ./documents")
        print("  python swarm_batch.py 'papers/*.md' ./outputs")
        sys.exit(1)
    
    input_pattern = sys.argv[1]
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./batch_outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find files
    if '*' in input_pattern:
        # Glob pattern
        from glob import glob
        files = [Path(f) for f in glob(input_pattern)]
    else:
        # Directory
        input_path = Path(input_pattern)
        if input_path.is_dir():
            # Find all text-like files
            files = []
            for ext in ['*.txt', '*.md', '*.text']:
                files.extend(input_path.glob(ext))
        elif input_path.is_file():
            files = [input_path]
        else:
            print(f"Error: Not found: {input_pattern}")
            sys.exit(1)
    
    if not files:
        print(f"Error: No files found matching: {input_pattern}")
        sys.exit(1)
    
    print(f"Found {len(files)} files to process")
    print(f"Output directory: {output_dir}")
    print("")
    
    # Process all files
    results = []
    for i, input_file in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}]")
        try:
            result = process_file(client, input_file, output_dir)
            results.append(result)
        except Exception as e:
            print(f"✗ Error processing {input_file}: {e}")
            continue
    
    # Summary
    print(f"\n{'=' * 60}")
    print(f"BATCH COMPLETE")
    print(f"{'=' * 60}")
    print(f"Processed: {len(results)}/{len(files)} files")
    print(f"Outputs in: {output_dir}")
    print("")

if __name__ == "__main__":
    main()
