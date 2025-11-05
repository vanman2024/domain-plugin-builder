#!/usr/bin/env bash
# Script: validate-agent.sh
# Purpose: Validate agent file compliance with framework standards
# Subsystem: build-system
# Called by: /build:agent command after generation
# Outputs: Validation report to stdout

set -euo pipefail

AGENT_FILE="${1:?Usage: $0 <agent-file>}"

echo "[INFO] Validating agent file: $AGENT_FILE"

# Check file exists
if [[ ! -f "$AGENT_FILE" ]]; then
    echo "❌ ERROR: File not found: $AGENT_FILE"
    exit 1
fi

# Check frontmatter exists
if ! grep -q "^---$" "$AGENT_FILE"; then
    echo "❌ ERROR: Missing frontmatter"
    exit 1
fi

# Check required frontmatter fields
REQUIRED_FIELDS=("name:" "description:" "model:")
for field in "${REQUIRED_FIELDS[@]}"; do
    if ! grep -q "^$field" "$AGENT_FILE"; then
        echo "❌ ERROR: Missing required field: $field"
        exit 1
    fi
done

# Warn if tools field is present (agents should inherit tools)
if grep -q "^tools:" "$AGENT_FILE"; then
    echo "⚠️  WARNING: tools field found - agents should inherit tools from parent, not specify them"
fi

# Check for incorrect MCP server naming (common mistake: mcp__supabase instead of mcp__plugin_supabase_supabase)
INVALID_MCP_NAMES=("mcp__supabase" "mcp__shadcn" "mcp__nextjs" "mcp__vercel-ai")
for invalid_name in "${INVALID_MCP_NAMES[@]}"; do
    if grep -q "\`$invalid_name\`" "$AGENT_FILE" 2>/dev/null; then
        echo "❌ ERROR: Found $invalid_name - plugin-specific MCP servers must use full name:"
        echo "   - Use: mcp__plugin_supabase_supabase (not mcp__supabase)"
        echo "   - Use: mcp__plugin_*_shadcn (not mcp__shadcn)"
        echo "   Generic MCP servers are fine: mcp__github, mcp__filesystem, mcp__docker, mcp__fetch, etc."
        exit 1
    fi
done

# Check Step 0 exists (optional - only for validator agents)
if ! grep -q "### Step 0: Load Required Context" "$AGENT_FILE"; then
    echo "⚠️  WARNING: Missing Step 0: Load Required Context section (only required for validator agents)"
fi

# Check for @ symbol references
if ! grep -q 'Read("' "$AGENT_FILE"; then
    echo "⚠️  WARNING: No Read() calls found - agent may not load context"
fi

# Check Success Criteria exists (optional - only for validator agents)
if ! grep -q "## Success Criteria" "$AGENT_FILE"; then
    echo "⚠️  WARNING: Missing Success Criteria section (only required for validator agents)"
fi

echo "✅ Agent validation passed"
exit 0
