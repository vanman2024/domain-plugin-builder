---
description: Test command 2 for parallel execution demo
argument-hint: [test-message]
allowed-tools: Read, Write, Bash
---

**Arguments**: $ARGUMENTS

Goal: Demonstrate a simple test command that validates basic command structure and parallel execution capabilities.

Core Principles:
- Parse arguments cleanly
- Execute simple operations
- Provide clear feedback
- Follow validation requirements

Phase 1: Discovery
Goal: Parse and validate the provided arguments

Actions:
- Parse $ARGUMENTS to extract test message
- If no arguments provided, use default message "Hello from test-cmd-2"
- Display parsed arguments for confirmation
- Verify working directory context

Phase 2: Execution
Goal: Execute test operations

Actions:
- Echo the test message to demonstrate command execution
- Display current timestamp to show when command ran
- Create a simple output showing the command is working
- Example: !{bash echo "Test Command 2 executed: $ARGUMENTS at $(date)"}

Phase 3: Summary
Goal: Display results and completion status

Actions:
- Confirm command executed successfully
- Display the test message that was processed
- Show completion timestamp
- Indicate command is ready for parallel validation testing

Expected Output:
- Parsed arguments confirmation
- Execution timestamp
- Success message with test content
- Clear indication of completion
