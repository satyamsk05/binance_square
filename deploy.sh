#!/bin/bash
echo "🚀 Deploying News Bot v2 on EC2..."

pip install -r requirements.txt --break-system-packages

screen -S newsbot python main.py

echo "✅ Bot started in screen 'newsbot'"
echo "👁️  View: screen -r newsbot"
echo "🔌 Detach: Ctrl+A then D"
