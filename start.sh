#!/bin/bash

echo "⬡ THE SWARM - Quick Start ⬡"
echo ""

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set!"
    echo ""
    echo "Set it with:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    echo "Or create a .env file:"
    echo "  echo \"ANTHROPIC_API_KEY=your-key-here\" > .env"
    echo ""
    exit 1
fi

# Check if requirements are installed
if ! python -c "import gradio" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

echo "🚀 Starting Gradio interface..."
echo ""
echo "Open your browser to: http://localhost:7860"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python app.py
