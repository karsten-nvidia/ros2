# Agent Instructions

This project uses **bd** (beads) for issue tracking. Run `bd onboard` to get started.

## Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd sync               # Sync with git
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

1. Build packages starting with foundational ones (ament_package, rcutils, etc.)
2. When a build fails due to missing dependencies, identify the missing system library
3. Add the missing dependency to `[target.linux-64.dependencies]` section of `pixi.toml`
4. Retry the build and continue
5. Track build status using beads issues

### Build Commands

```bash
# Build a specific package and its dependencies
pixi run build <package_name>

# Control build parallelism (optional)
PIXI_PARALLEL_WORKERS=8 pixi run build <package_name>
```

### Adding Dependencies

When builds fail due to missing system libraries:

1. Identify the missing library from build error messages
2. Add to `pixi.toml` under `[target.linux-64.dependencies]`
3. Pin to specific versions for reproducibility
4. Document the reason in comments or git commit message

**Example dependencies added:**
- `lttng-ust = "2.13.9"` - Required for tracetools package
- `xorg-libxt = "1.3.0"` - Required for rviz_rendering (X11 Xt library)
- `xorg-libxaw = "1.0.14"` - Required for rviz_rendering (X11 Xaw library)

### Important Constraints

- **DO NOT modify source code** in the repositories
- **ONLY add dependencies** to pixi.toml `[target.linux-64.dependencies]` section
- If source code issues are suspected, ask user for guidance first

### Key Fixes Applied

- **Parallelism control**: MAKEFLAGS and CMAKE_BUILD_PARALLEL_LEVEL controlled by PIXI_PARALLEL_WORKERS environment variable
- **GCC version**: Pinned to GCC 13.4 (Ubuntu 24.04 LTS timeline) for compatibility with mcap_vendor
- **Pinned dependencies**: All Linux dependencies pinned to specific versions for reproducibility

