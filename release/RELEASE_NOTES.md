# Release 4.0.0b4

This release introduces significant improvements to task lifecycle management with two powerful new commands for managing TODO.md files. The empty trash functionality automatically removes tasks from the Deleted section after 30 days, providing a clean safety net for accidentally deleted items while preventing TODO.md from growing indefinitely. Users no longer need to manually clean up deleted tasks, as the system now handles this transparently on startup.

The prune command offers powerful control over archived task retention with flexible filtering options. Users can remove archived tasks based on age thresholds using `--days`, specific task ranges with `--from-task` and `--to-task`, or individual task IDs. The command includes robust safety features such as automatic backups before pruning, git history analysis to determine archive dates, and preservation of task metadata for audit trails. All pruned tasks are saved to timestamped archive files in the `.ai-todo/archives/` directory, enabling recovery if needed. Comprehensive usage examples are available in [docs/examples/PRUNE_EXAMPLES.md](https://github.com/fxstein/ai-todo/blob/main/docs/examples/PRUNE_EXAMPLES.md).

Several bug fixes improve robustness and reliability. Timezone-aware datetime comparisons now work correctly across different system configurations in prune operations. Task ID sorting in archive backups uses proper numeric sorting to maintain correct task ordering. Regex metacharacter escaping prevents errors when working with tasks that contain special characters. Duplicate prevention in subtask operations ensures data integrity during complex task manipulations.

Python 3.10 compatibility has been fully restored by replacing `datetime.UTC` with `timezone.utc` throughout the codebase, ensuring the tool works reliably across all supported Python versions.

---

- chore(deps): bump pytest from 9.0.2 to 9.0.3 (#107)
- chore(deps): bump virtualenv from 20.35.4 to 20.36.1 (#87)
- chore(deps): bump cryptography from 46.0.3 to 46.0.7 (#102)
- fix(tests): replace fastmcp 2.x private API with 3.x Client API (AIT-23) (#106)
- chore(deps): bump softprops/action-gh-release from 2 to 3 (#103)
- chore(deps): bump fastmcp from 2.14.4 to 3.2.0 (#101)
- chore(deps): bump pygments from 2.19.2 to 2.20.0 (#100)
- chore(deps): bump codecov/codecov-action from 5 to 6 (#99)
- chore(deps): bump DavidAnson/markdownlint-cli2-action from 22 to 23 (#98)
- chore(deps): bump requests from 2.32.5 to 2.33.0 (#96)
- chore(deps): bump authlib from 1.6.6 to 1.6.9 (#95)
- chore(deps): bump dorny/paths-filter from 3 to 4 (#94)
- chore(deps): bump pyjwt from 2.10.1 to 2.12.0 (#93)
- chore(deps): bump python-multipart from 0.0.20 to 0.0.22 (#90)
- chore(deps): bump urllib3 from 2.6.2 to 2.6.3 (#88)
- fix(test): use dynamic dates in prune tests to prevent time drift failures (AIT-22) (#105)
- chore(deps): bump filelock from 3.20.0 to 3.20.3 (#85)
- chore(deps): bump pynacl from 1.6.1 to 1.6.2 (#86)
- fix(ci): exempt Dependabot branches from branch name check (AIT-20) (#104)
- chore(deps): bump softprops/action-gh-release from 1 to 2 (#84)
