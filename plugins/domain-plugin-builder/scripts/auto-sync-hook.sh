#!/bin/bash
#
# Auto-sync hook for component creation
# Triggered on PostToolUse after Write/Edit tools create component files
#
# This provides a FAILSAFE that syncs components to Airtable
# even if the agent forgets to run the sync command.
#

set -e

# Get the tool use event data from stdin
TOOL_EVENT=$(cat)

# Extract tool name and file path from event
TOOL_NAME=$(echo "$TOOL_EVENT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$TOOL_EVENT" | jq -r '.tool_input.file_path // empty')

# Only process Write and Edit tools
if [[ "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" ]]; then
    exit 0
fi

# Check if this is a component file
if [[ ! "$FILE_PATH" =~ /plugins/([^/]+)/(agents|commands|skills)/(.+)\.(md|SKILL\.md)$ ]]; then
    exit 0
fi

# Extract plugin name and component type
PLUGIN_NAME=$(echo "$FILE_PATH" | grep -oP '/plugins/\K[^/]+')
COMP_TYPE=""
COMP_NAME=""

if [[ "$FILE_PATH" =~ /agents/([^/]+)\.md$ ]]; then
    COMP_TYPE="agent"
    COMP_NAME="${BASH_REMATCH[1]}"
elif [[ "$FILE_PATH" =~ /commands/([^/]+)\.md$ ]]; then
    COMP_TYPE="command"
    COMP_NAME="${BASH_REMATCH[1]}"
elif [[ "$FILE_PATH" =~ /skills/([^/]+)/SKILL\.md$ ]]; then
    COMP_TYPE="skill"
    COMP_NAME="${BASH_REMATCH[1]}"
else
    exit 0
fi

# Determine marketplace from file path
MARKETPLACE_NAME=""
if [[ "$FILE_PATH" =~ /ai-dev-marketplace/ ]]; then
    MARKETPLACE_NAME="ai-dev-marketplace"
elif [[ "$FILE_PATH" =~ /dev-lifecycle-marketplace/ ]]; then
    MARKETPLACE_NAME="dev-lifecycle-marketplace"
elif [[ "$FILE_PATH" =~ /mcp-servers-marketplace/ ]]; then
    MARKETPLACE_NAME="mcp-servers-marketplace"
elif [[ "$FILE_PATH" =~ /domain-plugin-builder/ ]]; then
    MARKETPLACE_NAME="domain-plugin-builder"
else
    exit 0
fi

# Background sync to avoid blocking the agent
(
    # Wait 2 seconds to let file settle
    sleep 2

    # Run sync
    python ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/scripts/sync-component.py \
        --type="$COMP_TYPE" \
        --name="$COMP_NAME" \
        --plugin="$PLUGIN_NAME" \
        --marketplace="$MARKETPLACE_NAME" \
        > /tmp/auto-sync-$COMP_TYPE-$COMP_NAME.log 2>&1

    # Log result
    if [ $? -eq 0 ]; then
        echo "[$(date)] ✅ Auto-synced $COMP_TYPE: $PLUGIN_NAME/$COMP_NAME" >> ~/.claude/auto-sync.log
    else
        echo "[$(date)] ❌ Auto-sync failed for $COMP_TYPE: $PLUGIN_NAME/$COMP_NAME" >> ~/.claude/auto-sync.log
    fi
) &

exit 0
