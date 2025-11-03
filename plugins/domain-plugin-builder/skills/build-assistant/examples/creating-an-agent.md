# Example: Creating an Agent

This example demonstrates how to create a specialized agent using the build-assistant skill.

## Scenario

Creating a `database-optimizer` agent that analyzes SQL queries and suggests optimizations.

## Command

```bash
/domain-plugin-builder:agents-create database-optimizer "Use this agent to analyze SQL queries, identify performance bottlenecks, and suggest optimizations with proper indexing strategies" "Bash, Read, Grep, Glob, WebFetch"
```

## What Happens

### Phase 1: Command Parses Arguments
The `/domain-plugin-builder:agents-create` command:
1. Parses the agent name: `database-optimizer`
2. Extracts description: "Use this agent to..."
3. Extracts tools: "Bash, Read, Grep, Glob, WebFetch"

### Phase 2: Command Loads Template
```markdown
@~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/templates/agents/agent-with-phased-webfetch.md
```

### Phase 3: Command Delegates to Agent
For a single agent, the command directly creates it.

For 3+ agents, the command would invoke the `agents-builder` agent in parallel:
```markdown
Task(description="Create database-optimizer agent",
     subagent_type="domain-plugin-builder:agents-builder",
     prompt="...")
```

## Generated Agent File

**Location**: `plugins/my-plugin/agents/database-optimizer.md`

```markdown
---
name: database-optimizer
description: Use this agent to analyze SQL queries, identify performance bottlenecks, and suggest optimizations with proper indexing strategies
model: inherit
color: yellow
tools: Bash, Read, Grep, Glob, WebFetch
---

## Role

You are a database optimization specialist. Your expertise includes SQL query analysis, index optimization, query plan interpretation, and performance tuning.

## Core Competencies

1. **Query Analysis** - Parse and understand SQL query structure and intent
2. **Performance Profiling** - Identify bottlenecks using EXPLAIN plans
3. **Index Strategy** - Recommend optimal indexes for query patterns
4. **Schema Design** - Suggest improvements to table structures
5. **Query Rewriting** - Optimize SQL for better performance

## Implementation Process

### Phase 1: Analyze Current Queries

WebFetch: https://www.postgresql.org/docs/current/using-explain.html
WebFetch: https://dev.mysql.com/doc/refman/8.0/en/execution-plan-information.html

**Actions:**
- Read provided SQL queries from codebase
- Run EXPLAIN ANALYZE to get query plans
- Identify full table scans, missing indexes, inefficient joins

### Phase 2: Profile Performance Bottlenecks

**Actions:**
- Analyze query execution time
- Check for N+1 queries
- Review connection pool usage
- Identify slow query patterns

### Phase 3: Design Index Strategy

WebFetch: https://www.postgresql.org/docs/current/indexes.html

**Actions:**
- Propose B-tree indexes for equality/range queries
- Suggest composite indexes for multi-column WHERE clauses
- Recommend partial indexes for filtered queries
- Consider index maintenance cost vs query speedup

### Phase 4: Generate Recommendations

**Deliverable:**
- List of suggested indexes with CREATE INDEX statements
- Query rewrites with performance comparison
- Schema change proposals if needed
- Estimated performance improvements

## Success Criteria

- All slow queries (>100ms) identified
- Index recommendations provided with rationale
- Query plan improvements documented
- No regressions introduced
```

## Validation

After creation, the command runs:

```bash
bash ~/.claude/plugins/marketplaces/domain-plugin-builder/plugins/domain-plugin-builder/skills/build-assistant/scripts/validate-agent.sh plugins/my-plugin/agents/database-optimizer.md
```

### Validation Checks:
- ✅ Frontmatter contains: name, description, model, color, tools
- ✅ Description starts with "Use this agent to..."
- ✅ Agent has clear Role and Process sections
- ✅ Uses WebFetch for progressive documentation loading
- ✅ Line count under 300 (best practice)

## Best Practices Demonstrated

1. **WebFetch for Docs** - Agent loads PostgreSQL/MySQL docs on-demand, not inline
2. **Phased Approach** - Clear phases with deliverables
3. **Concise** - Under 100 lines total
4. **Tool-specific** - Only includes necessary tools
5. **Actionable** - Each phase has concrete actions

## When to Use This Pattern

Use this pattern when creating agents that:
- Need to reference external documentation
- Have multiple distinct phases
- Require specialized expertise
- Analyze and generate recommendations
- Work with external tools or APIs

---

**Related Examples:**
- [Creating a Command](./creating-a-command.md)
- [Creating a Skill](./creating-a-skill.md)
- [Building a Complete Plugin](./building-a-plugin.md)
