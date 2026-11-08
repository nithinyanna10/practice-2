# Workflow
- Use Superpowers for every task: write a plan first, then build with
  subagent-driven development, test-first, with a review after each task.
  Skip brainstorming when the spec is given.

# Git
- Never work on main. Each plan runs on its own feature branch in a git worktree
  (superpowers:using-git-worktrees), named feat/<short-name>.
- Commit after every completed task, small commits, messages like
  "feat: add redirect loop detection". No Co-Authored-By lines.
- Independent tasks (no shared files) may run in parallel, each on its own branch
  (superpowers:dispatching-parallel-agents). Anything that touches the same
  files runs in sequence.
- When done, use superpowers:finishing-a-development-branch: run all tests,
  then merge into main.

# Code
- Python 3, type hints, small functions, pytest for every behavior.
- No real network calls in tests; mock them.

# Review speed
- One review per task, keep it short.
- Final whole-branch review: report findings only. Fix Critical issues;
  list Important/Minor ones for me to decide. Don't start a fix wave on your own.