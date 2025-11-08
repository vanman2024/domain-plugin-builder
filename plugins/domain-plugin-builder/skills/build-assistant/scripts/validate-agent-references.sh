#!/bin/bash
# Validate that all agent references in commands exist

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <plugin-path>"
    echo "Example: $0 plugins/domain-plugin-builder"
    exit 1
fi

PLUGIN_PATH="$1"

if [ ! -d "$PLUGIN_PATH" ]; then
    echo "❌ Error: Plugin directory not found: $PLUGIN_PATH"
    exit 1
fi

echo "🔍 Validating agent references in: $PLUGIN_PATH"
echo ""

# Extract all agent references from commands
AGENT_REFS=$(grep -rh 'subagent_type="[^"]*"' "$PLUGIN_PATH/commands/" 2>/dev/null | \
             grep -o 'subagent_type="[^"]*"' | \
             sed 's/subagent_type="//; s/"$//' | \
             sed 's/.*://' | \
             sort -u)

if [ -z "$AGENT_REFS" ]; then
    echo "✅ No agent references found in commands"
    exit 0
fi

TOTAL=0
VALID=0
INVALID=0
MISSING_AGENTS=()

echo "📋 Checking agent references..."
echo ""

for agent in $AGENT_REFS; do
    TOTAL=$((TOTAL + 1))
    AGENT_FILE="$PLUGIN_PATH/agents/${agent}.md"

    if [ -f "$AGENT_FILE" ]; then
        echo "  ✅ $agent"
        VALID=$((VALID + 1))
    else
        echo "  ❌ $agent (MISSING: $AGENT_FILE)"
        INVALID=$((INVALID + 1))
        MISSING_AGENTS+=("$agent")
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Summary:"
echo "  Total agent references: $TOTAL"
echo "  Valid: $VALID"
echo "  Invalid: $INVALID"
echo ""

if [ $INVALID -gt 0 ]; then
    echo "❌ VALIDATION FAILED"
    echo ""
    echo "Commands reference non-existent agents:"
    for agent in "${MISSING_AGENTS[@]}"; do
        echo "  - $agent (referenced in commands but agents/$agent.md doesn't exist)"
    done
    echo ""
    echo "🔧 FIX THIS BY:"
    echo "   1. Check which commands reference these agents:"
    echo "      grep -r 'subagent_type=\".*:$agent\"' $PLUGIN_PATH/commands/"
    echo ""
    echo "   2. Update commands to use ACTUAL agent names from agents/ directory:"
    echo "      ls $PLUGIN_PATH/agents/"
    echo ""
    echo "   3. Fix the subagent_type in commands to match real agent filenames"
    echo ""
    echo "❌ DO NOT create new agents to match wrong command references!"
    echo "✅ FIX the commands to use correct existing agent names!"
    exit 1
else
    echo "✅ ALL AGENT REFERENCES VALID"
    exit 0
fi
