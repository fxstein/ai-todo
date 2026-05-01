## Release Summary

`v4.0.0b4` was tagged but never published to GitHub Releases or PyPI due to a CI gate bug where downstream release jobs were skipped after a failed `Create Release Tag` job. That skipped-dependency behavior has now been fixed in PR #114.

This `v4.0.0b5` release validates the corrected PR-driven release pipeline end-to-end (prepare -> merge -> auto-tag -> GitHub Release -> PyPI publish).
