#!/usr/bin/env python3
"""
Bulk sync ALL components from a plugin to Airtable in parallel

Usage:
    python bulk-sync-airtable.py --plugin=clerk --marketplace=domain-plugin-builder
    python bulk-sync-airtable.py --plugin=nextjs-frontend --marketplace=ai-dev-marketplace --type=agents
    python bulk-sync-airtable.py --plugin=planning --marketplace=dev-lifecycle-marketplace --type=commands,skills

This script discovers ALL components in a plugin and syncs them to Airtable efficiently.
"""

import os
import sys
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from pyairtable import Api
import subprocess

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

def discover_components(plugin_path, component_types):
    """Discover all components of specified types in a plugin"""
    components = []

    if 'agents' in component_types:
        agents_dir = os.path.join(plugin_path, 'agents')
        if os.path.exists(agents_dir):
            for file in os.listdir(agents_dir):
                if file.endswith('.md'):
                    name = file.replace('.md', '')
                    components.append(('agent', name))

    if 'commands' in component_types:
        commands_dir = os.path.join(plugin_path, 'commands')
        if os.path.exists(commands_dir):
            for file in os.listdir(commands_dir):
                if file.endswith('.md'):
                    name = file.replace('.md', '')
                    components.append(('command', name))

    if 'skills' in component_types:
        skills_dir = os.path.join(plugin_path, 'skills')
        if os.path.exists(skills_dir):
            for skill_name in os.listdir(skills_dir):
                skill_path = os.path.join(skills_dir, skill_name)
                if os.path.isdir(skill_path) and os.path.exists(os.path.join(skill_path, 'SKILL.md')):
                    components.append(('skill', skill_name))

    if 'hooks' in component_types:
        hooks_dir = os.path.join(plugin_path, 'hooks')
        if os.path.exists(hooks_dir):
            for file in os.listdir(hooks_dir):
                if file.endswith('.sh'):
                    # Extract event type from filename (e.g., pre-commit.sh -> pre-commit)
                    name = file.replace('.sh', '')
                    components.append(('hook', name))

    return components

def sync_single_component(component_type, component_name, plugin_name, marketplace_name):
    """Sync a single component using sync-component.py"""
    script_path = os.path.join(
        os.path.dirname(__file__),
        'sync-component.py'
    )

    cmd = [
        'python',
        script_path,
        f'--type={component_type}',
        f'--name={component_name}',
        f'--plugin={plugin_name}',
        f'--marketplace={marketplace_name}'
    ]

    # Add event-type for hooks (parse from name)
    if component_type == 'hook':
        cmd.append(f'--event-type={component_name}')
        # Add script path for hooks
        marketplace_root = MARKETPLACE_PATHS[marketplace_name]
        hook_path = f'{marketplace_root}/plugins/{plugin_name}/hooks/{component_name}.sh'
        cmd.append(f'--script-path={hook_path}')

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            return (True, component_type, component_name, result.stdout)
        else:
            return (False, component_type, component_name, result.stderr)
    except subprocess.TimeoutExpired:
        return (False, component_type, component_name, "Timeout after 30 seconds")
    except Exception as e:
        return (False, component_type, component_name, str(e))

def main():
    parser = argparse.ArgumentParser(description='Bulk sync all components from a plugin to Airtable')
    parser.add_argument('--plugin', required=True,
                        help='Plugin name (e.g., clerk, nextjs-frontend)')
    parser.add_argument('--marketplace', required=True,
                        help='Marketplace name (e.g., domain-plugin-builder)')
    parser.add_argument('--type',
                        help='Comma-separated component types to sync (agents,commands,skills,hooks). Default: all')
    parser.add_argument('--max-workers', type=int, default=5,
                        help='Maximum parallel workers (default: 5)')

    args = parser.parse_args()

    # Validate Airtable token
    if not AIRTABLE_TOKEN:
        print("❌ ERROR: AIRTABLE_TOKEN or MCP_AIRTABLE_TOKEN environment variable not set")
        return 1

    # Validate marketplace
    if args.marketplace not in MARKETPLACE_PATHS:
        print(f"❌ ERROR: Unknown marketplace: {args.marketplace}")
        print(f"   Valid marketplaces: {list(MARKETPLACE_PATHS.keys())}")
        return 1

    # Determine component types
    if args.type:
        component_types = [t.strip() for t in args.type.split(',')]
    else:
        component_types = ['agents', 'commands', 'skills', 'hooks']

    # Build plugin path
    marketplace_root = MARKETPLACE_PATHS[args.marketplace]
    plugin_path = os.path.join(marketplace_root, 'plugins', args.plugin)

    if not os.path.exists(plugin_path):
        print(f"❌ ERROR: Plugin path not found: {plugin_path}")
        return 1

    print()
    print("=" * 80)
    print("🔄 BULK SYNC TO AIRTABLE")
    print("=" * 80)
    print(f"   Plugin: {args.plugin}")
    print(f"   Marketplace: {args.marketplace}")
    print(f"   Component Types: {', '.join(component_types)}")
    print(f"   Max Workers: {args.max_workers}")
    print()

    # Discover all components
    print("📋 Discovering components...")
    components = discover_components(plugin_path, component_types)

    if not components:
        print("⚠️  No components found!")
        return 0

    print(f"✅ Found {len(components)} components:")
    for component_type, component_name in components:
        print(f"   - {component_type}: {component_name}")
    print()

    # Sync components in parallel
    print(f"🚀 Syncing {len(components)} components in parallel...")
    print()

    results = []
    with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        # Submit all sync tasks
        futures = {
            executor.submit(
                sync_single_component,
                comp_type,
                comp_name,
                args.plugin,
                args.marketplace
            ): (comp_type, comp_name)
            for comp_type, comp_name in components
        }

        # Process results as they complete
        for future in as_completed(futures):
            success, comp_type, comp_name, output = future.result()
            results.append((success, comp_type, comp_name, output))

            if success:
                print(f"✅ {comp_type}: {comp_name}")
            else:
                print(f"❌ {comp_type}: {comp_name}")
                if output:
                    print(f"   Error: {output[:200]}")

    # Summary
    print()
    print("=" * 80)
    print("📊 SYNC SUMMARY")
    print("=" * 80)

    success_count = sum(1 for s, _, _, _ in results if s)
    failure_count = len(results) - success_count

    print(f"   Total: {len(results)}")
    print(f"   ✅ Success: {success_count}")
    print(f"   ❌ Failed: {failure_count}")
    print()

    if failure_count > 0:
        print("Failed components:")
        for success, comp_type, comp_name, output in results:
            if not success:
                print(f"   - {comp_type}: {comp_name}")
        print()
        return 1

    print("✅ All components synced successfully!")
    print("=" * 80)
    return 0

if __name__ == "__main__":
    sys.exit(main())
