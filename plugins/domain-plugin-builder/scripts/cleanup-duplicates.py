#!/usr/bin/env python3
"""
Clean up duplicate components in Airtable

Usage:
    python cleanup-duplicates.py --plugin=celery --type=agents --dry-run
    python cleanup-duplicates.py --plugin=celery --type=agents  # Actually delete
"""

import os
import sys
import argparse
from collections import defaultdict
from pyairtable import Api

# Airtable configuration
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN") or os.getenv("MCP_AIRTABLE_TOKEN")
BASE_ID = "appHbSB7WhT1TxEQb"

def cleanup_agents(api, plugin_name, dry_run=True):
    """Clean up duplicate agents for a plugin"""

    # Get plugin ID
    plugins_table = api.table(BASE_ID, "Plugins")
    plugin_records = plugins_table.all(formula=f"{{Name}}='{plugin_name}'")

    if not plugin_records:
        print(f"❌ Plugin '{plugin_name}' not found in Airtable")
        return

    plugin_id = plugin_records[0]['id']
    print(f"✅ Found plugin: {plugin_name} (ID: {plugin_id})\n")

    # Get all agents for this plugin
    agents_table = api.table(BASE_ID, "Agents")
    all_agents = agents_table.all()

    plugin_agents = []
    for agent in all_agents:
        fields = agent['fields']
        plugins = fields.get('Plugin', [])
        if plugin_id in plugins:
            agent_name = fields.get('Agent Name', 'NO NAME')
            created_time = agent.get('createdTime', '')
            plugin_agents.append((agent_name, agent['id'], created_time))

    print(f"📋 Total agents for {plugin_name}: {len(plugin_agents)}\n")

    # Group by name
    by_name = defaultdict(list)
    for name, aid, created in plugin_agents:
        by_name[name].append((aid, created))

    # Find duplicates
    duplicates_found = 0
    records_to_delete = []

    for name in sorted(by_name.keys()):
        records = by_name[name]
        if len(records) > 1:
            duplicates_found += 1
            print(f"⚠️  DUPLICATE: {name} ({len(records)} records)")

            # Sort by creation time (oldest first)
            sorted_records = sorted(records, key=lambda x: x[1])

            # Keep the OLDEST, delete the rest
            keep_id = sorted_records[0][0]
            delete_ids = [r[0] for r in sorted_records[1:]]

            print(f"   ✅ KEEP: {keep_id} (created: {sorted_records[0][1]})")
            for did, dcreated in sorted_records[1:]:
                print(f"   🗑️  DELETE: {did} (created: {dcreated})")
                records_to_delete.append(did)
            print()

    if duplicates_found == 0:
        print("✅ No duplicates found!")
        return

    print(f"\n📊 Summary:")
    print(f"   Duplicate agent names: {duplicates_found}")
    print(f"   Records to delete: {len(records_to_delete)}\n")

    if dry_run:
        print("🔍 DRY RUN - No records will be deleted")
        print("   Remove --dry-run to actually delete duplicates")
    else:
        print("⚠️  DELETING DUPLICATES...")
        for record_id in records_to_delete:
            try:
                agents_table.delete(record_id)
                print(f"   ✅ Deleted: {record_id}")
            except Exception as e:
                print(f"   ❌ Failed to delete {record_id}: {e}")

        print(f"\n✅ Cleanup complete! Deleted {len(records_to_delete)} duplicate records")

def main():
    parser = argparse.ArgumentParser(description='Clean up duplicate components in Airtable')
    parser.add_argument('--plugin', required=True, help='Plugin name (e.g., celery)')
    parser.add_argument('--type', required=True, choices=['agents', 'commands', 'skills', 'hooks'],
                        help='Component type to clean up')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be deleted without actually deleting')

    args = parser.parse_args()

    # Validate token
    if not AIRTABLE_TOKEN:
        print("❌ ERROR: AIRTABLE_TOKEN or MCP_AIRTABLE_TOKEN environment variable not set")
        return 1

    api = Api(AIRTABLE_TOKEN)

    print("=" * 80)
    print("🧹 AIRTABLE DUPLICATE CLEANUP")
    print("=" * 80)
    print(f"   Plugin: {args.plugin}")
    print(f"   Type: {args.type}")
    print(f"   Dry Run: {args.dry_run}")
    print("=" * 80)
    print()

    if args.type == 'agents':
        cleanup_agents(api, args.plugin, args.dry_run)
    else:
        print(f"❌ Cleanup for {args.type} not yet implemented")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
