# Agent Instructions

This project uses **bd** (beads) for issue tracking. Run `bd onboard` to get started.

## Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd sync               # Sync with git
bd dep tree <id>      # Show dependency tree for an issue
```

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds

## Building ROS 2 Packages

### Build Strategy

This project builds ROS 2 packages using pixi. The workflow is:

### Build Commands

```bash
# Build a specific package and its dependencies
pixi run build <package_name>

# Control build parallelism (optional)
PIXI_PARALLEL_WORKERS=8 pixi run build <package_name>
```

If on machine cubesat, use PIXI_PARALLEL_WORKERS=2 to not overload it. Otherwise, don't use the prefix and use all available cores.

Build issues are tracked using beads issues. If missing dependencies are identified, add them to the `pixi.toml` under `[target.linux-64.dependencies]`. Pin to specific versions for reproducibility. The versions should be consistent with the timeline of other pinned versions, currently about the release time of Ubuntu 24.04.

### Important Constraints

- **DO NOT modify source code** in the repositories
- **ONLY add dependencies** to pixi.toml `[target.linux-64.dependencies]` section
- If source code issues are suspected, ask user for guidance first

### Key Fixes Applied

- **Parallelism control**: MAKEFLAGS and CMAKE_BUILD_PARALLEL_LEVEL controlled by PIXI_PARALLEL_WORKERS environment variable
- **GCC version**: Pinned to GCC 13.4 (Ubuntu 24.04 LTS timeline) for compatibility with mcap_vendor
