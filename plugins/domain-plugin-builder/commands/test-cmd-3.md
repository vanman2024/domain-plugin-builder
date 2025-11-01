---
description: Test command 3 for parallel execution demo
argument-hint: [test-message]
allowed-tools: Read, Write, Bash
---

**Arguments**: $ARGUMENTS

Goal: Demonstrate a simple test command that validates basic command structure and execution flow with enhanced reporting.

Core Principles:
- Parse arguments cleanly
- Execute simple operations
- Provide clear feedback
- Follow validation requirements

Phase 1: Discovery
Goal: Parse and validate the provided arguments

Actions:
- Parse $ARGUMENTS to extract test message
- If no arguments provided, use default message "Hello from test-cmd-3"
- Display parsed arguments for confirmation
- Verify working directory context
- Example: !{bash pwd}

Phase 2: Execution
Goal: Execute test operations with enhanced output

Actions:
- Echo the test message to demonstrate command execution
- Display current timestamp to show when command ran
- Show system information for context
- Create a simple output showing the command is working
- Example: !{bash echo "Test Command 3 executed: $ARGUMENTS at $(date)"}
- Example: !{bash echo "Working directory: $(pwd)"}

Phase 3: Summary
Goal: Display results and completion status

Actions:
- Confirm command executed successfully
- Display the test message that was processed
- Show completion timestamp
- Indicate command is ready for validation testing
- Report any relevant system context discovered

Expected Output:
- Parsed arguments confirmation
- Execution timestamp with full details
- System context information
- Success message with test content
- Clear indication of completion
