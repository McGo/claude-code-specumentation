#!/usr/bin/env bash
# install.sh – Installs the specumentation skill and MCP server globally for Claude Code
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="$HOME/.claude/skills"
LINK_PATH="$TARGET_DIR/specumentation"
MCP_DIR="$HOME/.claude/specumentation-mcp"
MCP_CLI_LINK="/usr/local/bin/specumentation-mcp"

# --- Skill Installation ---

# Ensure ~/.claude/skills/ exists
if [ ! -d "$TARGET_DIR" ]; then
  mkdir -p "$TARGET_DIR"
  echo "Created $TARGET_DIR"
fi

# Create or update symlink
if [ -L "$LINK_PATH" ]; then
  echo "Updating existing symlink..."
  rm "$LINK_PATH"
elif [ -e "$LINK_PATH" ]; then
  echo "Error: $LINK_PATH exists but is not a symlink. Remove it manually."
  exit 1
fi

ln -s "$SKILL_DIR" "$LINK_PATH"
echo "Symlink created: $LINK_PATH -> $SKILL_DIR"

# --- MCP Server Installation ---

echo ""
echo "Installing MCP server..."

# Create MCP directory and copy server
mkdir -p "$MCP_DIR"
cp "$SKILL_DIR/mcp-server/server.py" "$MCP_DIR/server.py"
echo "Copied server.py to $MCP_DIR/server.py"

# Symlink the CLI tool
if [ -L "$MCP_CLI_LINK" ]; then
  rm "$MCP_CLI_LINK"
fi
if ln -sf "$SKILL_DIR/mcp-server/specumentation-mcp" "$MCP_CLI_LINK" 2>/dev/null; then
  echo "CLI symlink created: $MCP_CLI_LINK"
else
  # Fallback to ~/.local/bin if /usr/local/bin is not writable
  LOCAL_BIN="$HOME/.local/bin"
  mkdir -p "$LOCAL_BIN"
  ln -sf "$SKILL_DIR/mcp-server/specumentation-mcp" "$LOCAL_BIN/specumentation-mcp"
  echo "CLI symlink created: $LOCAL_BIN/specumentation-mcp"
  echo "  (Add $LOCAL_BIN to your PATH if not already present)"
fi

# --- Summary ---

echo ""
echo "Installation complete."
echo "  Skill:      /specumentation is now available in Claude Code"
echo "  MCP Server: $MCP_DIR/server.py"
echo "  CLI:        specumentation-mcp init|list"
echo ""
echo "To enable the MCP server in Claude Desktop, add this to:"
echo "  ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
echo '{
  "mcpServers": {
    "specumentation": {
      "command": "python3",
      "args": ["'"$MCP_DIR/server.py"'"]
    }
  }
}'
echo ""
echo "Then register projects with: specumentation-mcp init (from project dir)"
