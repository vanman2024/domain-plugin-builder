#!/usr/bin/env python3
"""
Validate that all components are synced to Airtable

Usage:
    python sync-validator.py                    # Check sync status for all marketplaces
    python sync-validator.py --marketplace=ai-dev-marketplace  # Check specific marketplace
    python sync-validator.py --auto-sync        # Auto-sync missing components
    python sync-validator.py --fix-orphans      # Remove orphaned Airtable records

This script ensures that the filesystem and Airtable are always in sync.
"""

import os
import sys
import json
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

        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            frontmatter_text = match.group(1)

            # Fix argument-hint lines
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

def scan_filesystem_components(marketplace_name, marketplace_path):
    """Scan filesystem for all components in a marketplace"""
    components = {
        'agents': [],
        'commands': [],
        'skills': [],
        'hooks': []
    }

    plugins_dir = os.path.join(marketplace_path, 'plugins')
    if not os.path.exists(plugins_dir):
        return components

    for plugin_name in os.listdir(plugins_dir):
        plugin_path = os.path.join(plugins_dir, plugin_name)
        if not os.path.isdir(plugin_path):
            continue

        # Scan agents
        agents_dir = os.path.join(plugin_path, 'agents')
        if os.path.exists(agents_dir):
            for agent_file in os.listdir(agents_dir):
                if agent_file.endswith('.md'):
                    agent_name = agent_file.replace('.md', '')
                    agent_path = os.path.join(agents_dir, agent_file)
                    frontmatter = extract_frontmatter(agent_path)
                    components['agents'].append({
                        'name': agent_name,
                        'plugin': plugin_name,
                        'marketplace': marketplace_name,
                        'path': agent_path,
                        'frontmatter': frontmatter
                    })

        # Scan commands
        commands_dir = os.path.join(plugin_path, 'commands')
        if os.path.exists(commands_dir):
            for cmd_file in os.listdir(commands_dir):
                if cmd_file.endswith('.md'):
                    cmd_name = cmd_file.replace('.md', '')
                    cmd_path = os.path.join(commands_dir, cmd_file)
                    frontmatter = extract_frontmatter(cmd_path)
                    components['commands'].append({
                        'name': cmd_name,
                        'plugin': plugin_name,
                        'marketplace': marketplace_name,
                        'path': cmd_path,
                        'frontmatter': frontmatter
                    })

        # Scan skills
        skills_dir = os.path.join(plugin_path, 'skills')
        if os.path.exists(skills_dir):
            for skill_name in os.listdir(skills_dir):
                skill_path = os.path.join(skills_dir, skill_name)
                skill_md = os.path.join(skill_path, 'SKILL.md')
                if os.path.isdir(skill_path) and os.path.exists(skill_md):
                    frontmatter = extract_frontmatter(skill_md)
                    components['skills'].append({
                        'name': skill_name,
                        'plugin': plugin_name,
                        'marketplace': marketplace_name,
                        'path': skill_path,
                        'frontmatter': frontmatter
                    })

        # Scan hooks
        hooks_json = os.path.join(plugin_path, 'hooks', 'hooks.json')
        if os.path.exists(hooks_json):
            with open(hooks_json, 'r') as f:
                hooks_data = json.load(f)
                for event_type, hook_scripts in hooks_data.get('hooks', {}).items():
                    for hook_script in hook_scripts:
                        # Extract hook name from script path
                        hook_name = os.path.basename(hook_script).replace('.sh', '')
                        components['hooks'].append({
                            'name': hook_name,
                            'plugin': plugin_name,
                            'marketplace': marketplace_name,
                            'event_type': event_type,
                            'script_path': hook_script
                        })

    return components

def fetch_airtable_components(api):
    """Fetch all components from Airtable"""
    components = {
        'agents': [],
        'commands': [],
        'skills': [],
        'hooks': []
    }

    try:
        # Fetch all agents
        agents_table = api.table(BASE_ID, "Agents")
        for record in agents_table.all():
            components['agents'].append({
                'id': record['id'],
                'name': record['fields'].get('Agent Name', ''),
                'plugin_id': record['fields'].get('Plugin', [])
            })

        # Fetch all commands
        commands_table = api.table(BASE_ID, "Commands")
        for record in commands_table.all():
            components['commands'].append({
                'id': record['id'],
                'name': record['fields'].get('Name', ''),
                'plugin_id': record['fields'].get('Plugin', [])
            })

        # Fetch all skills
        skills_table = api.table(BASE_ID, "Skills")
        for record in skills_table.all():
            components['skills'].append({
                'id': record['id'],
                'name': record['fields'].get('Skill Name', ''),
                'plugin_id': record['fields'].get('Plugin', [])
            })

        # Fetch all hooks
        hooks_table = api.table(BASE_ID, "Hooks")
        for record in hooks_table.all():
            components['hooks'].append({
                'id': record['id'],
                'name': record['fields'].get('Hook Name', ''),
                'event_type': record['fields'].get('Event Type', ''),
                'plugin_id': record['fields'].get('Plugin', [])
            })

    except Exception as e:
        print(f"❌ Error fetching from Airtable: {e}")

    return components

def compare_components(fs_components, at_components, api):
    """Compare filesystem and Airtable components"""
    # Get plugin name to ID mapping
    plugins_table = api.table(BASE_ID, "Plugins")
    plugin_map = {}
    for record in plugins_table.all():
        plugin_name = record['fields'].get('Name', '')
        plugin_map[plugin_name] = record['id']

    results = {
        'missing_in_airtable': {'agents': [], 'commands': [], 'skills': [], 'hooks': []},
        'orphaned_in_airtable': {'agents': [], 'commands': [], 'skills': [], 'hooks': []},
        'synced': {'agents': 0, 'commands': 0, 'skills': 0, 'hooks': 0}
    }

    for comp_type in ['agents', 'commands', 'skills', 'hooks']:
        # Check for missing components
        for fs_comp in fs_components[comp_type]:
            plugin_id = plugin_map.get(fs_comp['plugin'])
            if not plugin_id:
                results['missing_in_airtable'][comp_type].append(fs_comp)
                continue

            found = False
            for at_comp in at_components[comp_type]:
                if (at_comp['name'] == fs_comp['name'] and
                    plugin_id in at_comp.get('plugin_id', [])):
                    found = True
                    results['synced'][comp_type] += 1
                    break

            if not found:
                results['missing_in_airtable'][comp_type].append(fs_comp)

        # Check for orphaned components
        for at_comp in at_components[comp_type]:
            found = False
            for fs_comp in fs_components[comp_type]:
                plugin_id = plugin_map.get(fs_comp['plugin'])
                if (at_comp['name'] == fs_comp['name'] and
                    plugin_id in at_comp.get('plugin_id', [])):
                    found = True
                    break

            if not found:
                results['orphaned_in_airtable'][comp_type].append(at_comp)

    return results

def print_report(results):
    """Print validation report"""
    print()
    print("=" * 80)
    print("📊 AIRTABLE SYNC VALIDATION REPORT")
    print("=" * 80)
    print()

    total_synced = sum(results['synced'].values())
    total_missing = sum(len(v) for v in results['missing_in_airtable'].values())
    total_orphaned = sum(len(v) for v in results['orphaned_in_airtable'].values())

    print(f"✅ Synced:   {total_synced} components")
    print(f"⚠️  Missing:  {total_missing} components (in filesystem but not Airtable)")
    print(f"🗑️  Orphaned: {total_orphaned} components (in Airtable but not filesystem)")
    print()

    if total_missing == 0 and total_orphaned == 0:
        print("🎉 ALL COMPONENTS ARE SYNCED!")
        print()
        return True

    # Detail missing components
    if total_missing > 0:
        print("=" * 80)
        print("⚠️  MISSING IN AIRTABLE (need to sync)")
        print("=" * 80)
        for comp_type, components in results['missing_in_airtable'].items():
            if components:
                print(f"\n{comp_type.upper()}:")
                for comp in components:
                    print(f"  - {comp['plugin']}/{comp['name']}")
        print()

    # Detail orphaned components
    if total_orphaned > 0:
        print("=" * 80)
        print("🗑️  ORPHANED IN AIRTABLE (should be removed)")
        print("=" * 80)
        for comp_type, components in results['orphaned_in_airtable'].items():
            if components:
                print(f"\n{comp_type.upper()}:")
                for comp in components:
                    print(f"  - {comp['name']} (ID: {comp['id']})")
        print()

    return False

def auto_sync_missing(results, api):
    """Auto-sync missing components to Airtable"""
    print()
    print("=" * 80)
    print("🔄 AUTO-SYNCING MISSING COMPONENTS")
    print("=" * 80)
    print()

    for comp_type, components in results['missing_in_airtable'].items():
        for comp in components:
            if comp_type == 'agent':
                cmd = f"python sync-component.py --type=agent --name={comp['name']} --plugin={comp['plugin']} --marketplace={comp['marketplace']}"
            elif comp_type == 'command':
                cmd = f"python sync-component.py --type=command --name={comp['name']} --plugin={comp['plugin']} --marketplace={comp['marketplace']}"
            elif comp_type == 'skill':
                cmd = f"python sync-component.py --type=skill --name={comp['name']} --plugin={comp['plugin']} --marketplace={comp['marketplace']}"
            elif comp_type == 'hook':
                cmd = f"python sync-component.py --type=hook --name={comp['name']} --plugin={comp['plugin']} --marketplace={comp['marketplace']} --event-type={comp['event_type']} --script-path={comp['script_path']}"

            print(f"Syncing: {comp_type} {comp['plugin']}/{comp['name']}")
            os.system(cmd)

def main():
    parser = argparse.ArgumentParser(description='Validate Airtable sync status')
    parser.add_argument('--marketplace',
                        help='Validate specific marketplace only')
    parser.add_argument('--auto-sync', action='store_true',
                        help='Automatically sync missing components')
    parser.add_argument('--fix-orphans', action='store_true',
                        help='Remove orphaned Airtable records')

    args = parser.parse_args()

    # Validate Airtable token
    if not AIRTABLE_TOKEN:
        print("❌ ERROR: AIRTABLE_TOKEN or MCP_AIRTABLE_TOKEN environment variable not set")
        return 1

    # Initialize Airtable API
    api = Api(AIRTABLE_TOKEN)

    # Determine marketplaces to scan
    if args.marketplace:
        if args.marketplace not in MARKETPLACE_PATHS:
            print(f"❌ ERROR: Unknown marketplace: {args.marketplace}")
            print(f"   Valid: {list(MARKETPLACE_PATHS.keys())}")
            return 1
        marketplaces = {args.marketplace: MARKETPLACE_PATHS[args.marketplace]}
    else:
        marketplaces = MARKETPLACE_PATHS

    # Scan filesystem
    print("🔍 Scanning filesystem...")
    all_fs_components = {'agents': [], 'commands': [], 'skills': [], 'hooks': []}
    for marketplace_name, marketplace_path in marketplaces.items():
        print(f"   - {marketplace_name}")
        fs_components = scan_filesystem_components(marketplace_name, marketplace_path)
        for comp_type in all_fs_components:
            all_fs_components[comp_type].extend(fs_components[comp_type])

    # Fetch Airtable data
    print("📥 Fetching from Airtable...")
    at_components = fetch_airtable_components(api)

    # Compare
    print("🔄 Comparing...")
    results = compare_components(all_fs_components, at_components, api)

    # Print report
    all_synced = print_report(results)

    # Auto-sync if requested
    if not all_synced and args.auto_sync:
        auto_sync_missing(results, api)
        print("\n✅ Auto-sync complete! Run validation again to verify.")

    return 0 if all_synced else 1

if __name__ == "__main__":
    sys.exit(main())
