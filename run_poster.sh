#!/bin/bash
# Binance Square Auto Poster Runner
# This script ensures the bot runs using the local virtual environment (.venv)

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ ! -d "$DIR/.venv" ]; then
    echo "❌ Virtual environment .venv not found in $DIR"
    exit 1
fi

echo "🚀 Starting Auto Poster using .venv/bin/python..."
$DIR/.venv/bin/python $DIR/auto_poster.py

# Handle normal exit or Ctrl+C if python process finishes
echo "👋 Runner finished."
