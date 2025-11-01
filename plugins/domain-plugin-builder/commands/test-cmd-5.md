---
description: Test command 5 for parallel execution demo
argument-hint: [message]
allowed-tools: Read, Write, Bash
---

**Arguments**: $ARGUMENTS

Goal: Demonstrate Pattern 1 simple command structure with basic bash execution and validation testing

Core Principles:
- Parse arguments to understand user input
- Execute simple deterministic operations
- Provide clear feedback on results
- Keep command concise and focused

Phase 1: Discovery
Goal: Parse user input and prepare for execution

Actions:
- Parse $ARGUMENTS for message content
- If $ARGUMENTS is empty, use default message
- Display what will be executed

Phase 2: Execution
Goal: Run test command and capture output

Actions:
- Execute test command with provided or default message
- !{bash echo "Test command 5 executing: ${ARGUMENTS:-default test message}"}
- !{bash date}
- Display execution timestamp
- Confirm successful execution

Phase 3: Summary
Goal: Report results and completion status

Actions:
- Display summary of what was executed
- Report message that was processed: $ARGUMENTS
- Confirm test command completed successfully
- Provide next steps if applicable
