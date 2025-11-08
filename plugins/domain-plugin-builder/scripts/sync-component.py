#!/usr/bin/env python3
"""
Sync a single component (agent, command, or skill) to Airtable

Usage:
    python sync-component.py --type=agent --name=my-agent --plugin=nextjs-frontend --marketplace=ai-dev-marketplace
    python sync-component.py --type=command --name=my-command --plugin=planning --marketplace=dev-lifecycle-marketplace
    python sync-component.py --type=skill --name=my-skill --plugin=quality --marketplace=dev-lifecycle-marketplace

This script is called at the end of component creation commands to immediately sync to Airtable.
"""

import os
import sys
import re
import yaml
import argparse
from pathlib import Path
from pyairtable import Api

# Airtable configuration
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN") or os.getenv("MCP_AIRTABLE_TOKEN")
BASE_ID = "appHbSB7WhT1TxEQb"

# Marketplace root paths
MARKETPLACE_PATHS = {
    "dev-lifecycle-marketplace": "/home/gotime2022/.claude/plugins/marketplaces/dev-lifecycle-marketplace",
    "ai-dev-marketplace": "/home/gotime2022/.claude/plugins/marketplaces/ai-dev-marketplace",
    "mcp-servers-marketplace": "/home/gotime2022/.claude/plugins/marketplaces/mcp-servers-marketplace",
    "domain-plugin-builder": "/home/gotime2022/.claude/plugins/marketplaces/domain-plugin-builder",
}

def extract_frontmatter(file_path):
    """Extract YAML frontmatter from markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match YAML frontmatter
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            frontmatter_text = match.group(1)

            # Fix argument-hint lines with square brackets
            lines = frontmatter_text.split('\n')
            fixed_lines = []
            for line in lines:
                if 'argument-hint:' in line and '[' in line:
                    if not (line.strip().endswith('"') or line.strip().endswith("'")):
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            key = parts[0]
                            value = parts[1].strip()
                            line = f'{key}: "{value}"'
                fixed_lines.append(line)

            frontmatter_text = '\n'.join(fixed_lines)
            return yaml.safe_load(frontmatter_text)
        return None
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return None

def get_plugin_record_id(api, plugin_name, marketplace_name):
    """Get or create Plugin record and return its ID"""
    plugins_table = api.table(BASE_ID, "Plugins")

    # Search for existing plugin by name only
    formula = f"{{Name}}='{plugin_name}'"
    records = plugins_table.all(formula=formula)

    if records:
        # Plugin exists - return first match
        # Note: If multiple marketplaces have same plugin name, this returns the first
        return records[0]['id']

    # Plugin doesn't exist - create it
    print(f"📝 Creating plugin '{plugin_name}' in Airtable...")
    print(f"   Note: Marketplace '{marketplace_name}' will need to be linked manually in Airtable")

    # Create with just the Name field - other fields can be filled manually
    plugin_data = {
        "Name": plugin_name,
    }

    try:
        new_record = plugins_table.create(plugin_data)
        print(f"✅ Created plugin: {plugin_name} (ID: {new_record['id']})")
        return new_record['id']
    except Exception as e:
        print(f"❌ Failed to create plugin: {e}")
        print(f"   You may need to create the plugin '{plugin_name}' manually in Airtable")
        return None

def sync_agent(api, name, plugin_name, marketplace_name, file_path):
    """Sync agent to Airtable"""
    print(f"📋 Syncing agent: {name}")

    # Read frontmatter
    frontmatter = extract_frontmatter(file_path)
    if not frontmatter:
        print(f"❌ Could not extract frontmatter from {file_path}")
        return False

    # Get plugin record ID
    plugin_record_id = get_plugin_record_id(api, plugin_name, marketplace_name)
    if not plugin_record_id:
        return False

    # Prepare agent data with ONLY required fields
    # We'll discover the correct field names through trial
    agent_data = {
        "Agent Name": frontmatter.get('name', name),
        "Plugin": [plugin_record_id],
    }

    # Check if agent exists
    agents_table = api.table(BASE_ID, "Agents")
    formula = f"AND({{Agent Name}}='{name}', {{Plugin}}='{plugin_record_id}')"
    existing = agents_table.all(formula=formula)

    if existing:
        # Update existing
        record_id = existing[0]['id']
        agents_table.update(record_id, agent_data)
        print(f"✅ Updated agent: {name} (ID: {record_id})")
    else:
        # Create new
        record = agents_table.create(agent_data)
        print(f"✅ Created agent: {name} (ID: {record['id']})")

    return True

def sync_command(api, name, plugin_name, marketplace_name, file_path):
    """Sync command to Airtable"""
    print(f"📋 Syncing command: {name}")

    # Read frontmatter
    frontmatter = extract_frontmatter(file_path)
    if not frontmatter:
        print(f"❌ Could not extract frontmatter from {file_path}")
        return False

    # Get plugin record ID
    plugin_record_id = get_plugin_record_id(api, plugin_name, marketplace_name)
    if not plugin_record_id:
        return False

    # Prepare command data
    command_data = {
        "Name": name,
        "Command Name": f"/{plugin_name}:{name}",
        "Description": frontmatter.get('description', ''),
        "Argument Hint": frontmatter.get('argument-hint', ''),
        "Plugin": [plugin_record_id],
        "Directory Path": f"plugins/{plugin_name}/commands/{name}.md",
    }

    # Check if command exists
    commands_table = api.table(BASE_ID, "Commands")
    formula = f"AND({{Name}}='{name}', {{Plugin}}='{plugin_record_id}')"
    existing = commands_table.all(formula=formula)

    if existing:
        # Update existing
        record_id = existing[0]['id']
        commands_table.update(record_id, command_data)
        print(f"✅ Updated command: {name} (ID: {record_id})")
    else:
        # Create new
        record = commands_table.create(command_data)
        print(f"✅ Created command: {name} (ID: {record['id']})")

    return True

def sync_skill(api, name, plugin_name, marketplace_name, dir_path):
    """Sync skill to Airtable"""
    print(f"📋 Syncing skill: {name}")

    # Read SKILL.md frontmatter
    skill_file = os.path.join(dir_path, "SKILL.md")
    frontmatter = extract_frontmatter(skill_file)
    if not frontmatter:
        print(f"❌ Could not extract frontmatter from {skill_file}")
        return False

    # Get plugin record ID
    plugin_record_id = get_plugin_record_id(api, plugin_name, marketplace_name)
    if not plugin_record_id:
        return False

    # Prepare skill data
    skill_data = {
        "Skill Name": frontmatter.get('name', name),
        "Description": frontmatter.get('description', ''),
        "Plugin": [plugin_record_id],
        "Directory Path": f"plugins/{plugin_name}/skills/{name}/",
    }

    # Check if skill exists
    skills_table = api.table(BASE_ID, "Skills")
    formula = f"AND({{Skill Name}}='{name}', {{Plugin}}='{plugin_record_id}')"
    existing = skills_table.all(formula=formula)

    if existing:
        # Update existing
        record_id = existing[0]['id']
        skills_table.update(record_id, skill_data)
        print(f"✅ Updated skill: {name} (ID: {record_id})")
    else:
        # Create new
        record = skills_table.create(skill_data)
        print(f"✅ Created skill: {name} (ID: {record['id']})")

    return True

def main():
    parser = argparse.ArgumentParser(description='Sync a component to Airtable')
    parser.add_argument('--type', required=True, choices=['agent', 'command', 'skill'],
                        help='Component type')
    parser.add_argument('--name', required=True,
                        help='Component name')
    parser.add_argument('--plugin', required=True,
                        help='Plugin name (e.g., nextjs-frontend)')
    parser.add_argument('--marketplace', required=True,
                        help='Marketplace name (e.g., ai-dev-marketplace)')

    args = parser.parse_args()

    # Validate Airtable token
    if not AIRTABLE_TOKEN:
        print("❌ ERROR: AIRTABLE_TOKEN environment variable not set")
        print("   Export it: export AIRTABLE_TOKEN=your_token_here")
        return 1

    # Validate marketplace
    if args.marketplace not in MARKETPLACE_PATHS:
        print(f"❌ ERROR: Unknown marketplace: {args.marketplace}")
        print(f"   Valid marketplaces: {list(MARKETPLACE_PATHS.keys())}")
        return 1

    # Construct file path
    marketplace_root = MARKETPLACE_PATHS[args.marketplace]

    if args.type == 'agent':
        file_path = f"{marketplace_root}/plugins/{args.plugin}/agents/{args.name}.md"
    elif args.type == 'command':
        file_path = f"{marketplace_root}/plugins/{args.plugin}/commands/{args.name}.md"
    elif args.type == 'skill':
        file_path = f"{marketplace_root}/plugins/{args.plugin}/skills/{args.name}/"
    else:
        print(f"❌ ERROR: Unknown component type: {args.type}")
        return 1

    # Check if file exists
    if args.type in ['agent', 'command']:
        if not os.path.exists(file_path):
            print(f"❌ ERROR: File not found: {file_path}")
            return 1
    else:  # skill
        skill_md = os.path.join(file_path, "SKILL.md")
        if not os.path.exists(skill_md):
            print(f"❌ ERROR: SKILL.md not found: {skill_md}")
            return 1

    # Initialize Airtable API
    api = Api(AIRTABLE_TOKEN)

    # Sync component
    print()
    print("=" * 80)
    print(f"🔄 Syncing {args.type} to Airtable")
    print("=" * 80)
    print(f"   Component: {args.name}")
    print(f"   Plugin: {args.plugin}")
    print(f"   Marketplace: {args.marketplace}")
    print(f"   File: {file_path}")
    print()

    success = False
    if args.type == 'agent':
        success = sync_agent(api, args.name, args.plugin, args.marketplace, file_path)
    elif args.type == 'command':
        success = sync_command(api, args.name, args.plugin, args.marketplace, file_path)
    elif args.type == 'skill':
        success = sync_skill(api, args.name, args.plugin, args.marketplace, file_path)

    if success:
        print()
        print("=" * 80)
        print("✅ Sync complete!")
        print("=" * 80)
        return 0
    else:
        print()
        print("=" * 80)
        print("❌ Sync failed!")
        print("=" * 80)
        return 1

if __name__ == "__main__":
    sys.exit(main())
