#!/bin/bash
echo "🚀 Deploying News Bot v2 on EC2..."

# Check if .venv exists and use it, otherwise fallback to system python
if [ -d ".venv" ]; then
    echo "📦 Using virtual environment (.venv)..."
    ./.venv/bin/pip install -r requirements.txt
    screen -S newsbot ./.venv/bin/python main.py
else
    echo "⚠️  .venv not found, falling back to system python..."
    pip install -r requirements.txt --break-system-packages
    screen -S newsbot python main.py
fi

echo "✅ Bot started in screen 'newsbot'"
echo "👁️  View: screen -r newsbot"
echo "🔌 Detach: Ctrl+A then D"
