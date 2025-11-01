---
description: Test command 4 for parallel execution demo
argument-hint: [demo-message]
allowed-tools: Read, Write, Bash
---

**Arguments**: $ARGUMENTS

Goal: Demonstrate a simple test command that validates command structure, execution flow, and parallel execution readiness.

Core Principles:
- Parse arguments cleanly
- Execute simple operations
- Provide clear feedback
- Follow validation requirements

Phase 1: Discovery
Goal: Parse and validate the provided arguments

Actions:
- Parse $ARGUMENTS to extract demo message
- If no arguments provided, use default message "Hello from test-cmd-4"
- Display parsed arguments for confirmation
- Verify working directory context
- Example: !{bash pwd}

Phase 2: Execution
Goal: Execute test operations

Actions:
- Echo the demo message to demonstrate command execution
- Display current timestamp to show when command ran
- Create a simple output showing the command is working
- Example: !{bash echo "Test Command 4 executed: $ARGUMENTS at $(date)"}
- Verify command completed successfully

Phase 3: Summary
Goal: Display results and completion status

Actions:
- Confirm command executed successfully
- Display the demo message that was processed
- Show completion timestamp
- Indicate command is ready for validation testing
- Report status: SUCCESS

Expected Output:
- Parsed arguments confirmation
- Working directory information
- Execution timestamp
- Success message with demo content
- Clear indication of completion
