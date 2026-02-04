#!/usr/bin/env python3
"""Wrapper script for colcon build and test operations."""

import argparse
import os
import subprocess
import sys


def main():
    """Main entry point for the colcon wrapper."""
    parser = argparse.ArgumentParser(description='Wrapper for colcon operations')
    parser.add_argument('command', choices=['build', 'test', 'test-up-to'],
                        help='Colcon command to run')
    parser.add_argument('packages', nargs='*',
                        help='Package name(s) to build or test (empty means all)')

    args = parser.parse_args()

    # Map wrapper commands to colcon commands and package selection modes
    command_config = {
        'build': {
            'colcon_cmd': 'build',
            'package_arg': 'packages-up-to',
            'extra_args': ['--symlink-install',
                          '--ament-cmake-args', '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON']
        },
        'test': {
            'colcon_cmd': 'test',
            'package_arg': 'packages-select',
            'extra_args': ['--event-handlers', 'console_cohesion+']
        },
        'test-up-to': {
            'colcon_cmd': 'test',
            'package_arg': 'packages-up-to',
            'extra_args': ['--event-handlers', 'console_cohesion+']
        }
    }

    config = command_config[args.command]

    # Setup parallel workers environment variables
    parallel_workers = os.environ.get('PIXI_PARALLEL_WORKERS', '')
    if parallel_workers:
        os.environ['CMAKE_BUILD_PARALLEL_LEVEL'] = parallel_workers
        os.environ['MAKEFLAGS'] = f'-j{parallel_workers}'

    # Build the colcon command
    cmd = ['colcon', config['colcon_cmd']]

    # Add extra arguments (build options or test event handlers)
    cmd.extend(config['extra_args'])

    # Add package selection if packages specified
    if args.packages:
        cmd.extend([f"--{config['package_arg']}"] + args.packages)

    # Add parallel workers to colcon
    if parallel_workers:
        cmd.extend(['--parallel-workers', parallel_workers])

    # Execute the command
    try:
        result = subprocess.run(cmd, check=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error executing colcon {args.command}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
