#!/bin/bash
#
# Remove AskUserQuestion from all command allowed-tools
#

set -e

MARKETPLACES=(
    "/home/gotime2022/.claude/plugins/marketplaces/dev-lifecycle-marketplace"
    "/home/gotime2022/.claude/plugins/marketplaces/ai-dev-marketplace"
    "/home/gotime2022/.claude/plugins/marketplaces/mcp-servers-marketplace"
    "/home/gotime2022/.claude/plugins/marketplaces/domain-plugin-builder"
)

total_updated=0

for marketplace in "${MARKETPLACES[@]}"; do
    echo "Processing: $marketplace"

    # Find all command files
    while IFS= read -r cmd_file; do
        if [ -f "$cmd_file" ]; then
            # Check if file has AskUserQuestion in allowed-tools
            if grep -q "allowed-tools:.*AskUserQuestion" "$cmd_file"; then
                echo "  Updating: $cmd_file"

                # Remove AskUserQuestion from allowed-tools line
                sed -i 's/allowed-tools: \(.*\)AskUserQuestion, \(.*\)/allowed-tools: \1\2/' "$cmd_file"
                sed -i 's/allowed-tools: \(.*\), AskUserQuestion\(.*\)/allowed-tools: \1\2/' "$cmd_file"
                sed -i 's/allowed-tools: AskUserQuestion, \(.*\)/allowed-tools: \1/' "$cmd_file"
                sed -i 's/allowed-tools: \(.*\), AskUserQuestion$/allowed-tools: \1/' "$cmd_file"
                sed -i 's/allowed-tools: AskUserQuestion$/allowed-tools: Task, Read, Write, Bash/' "$cmd_file"

                # Clean up double commas and spaces
                sed -i 's/, ,/,/g' "$cmd_file"
                sed -i 's/,  /, /g' "$cmd_file"

                ((total_updated++))
            fi
        fi
    done < <(find "$marketplace/plugins" -name "*.md" -path "*/commands/*" 2>/dev/null)
done

echo ""
echo "✅ Updated $total_updated command files"
echo "🔍 Removed AskUserQuestion from allowed-tools"
