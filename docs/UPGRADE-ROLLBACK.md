# Upgrade and rollback (operator runbook; nothing is deployed automatically)

1. Unzip into a new local checkout; run all tests. Do not overwrite the live directory directly.
2. On the existing server, record `git rev-parse HEAD`, current service configuration and working
   directory. Confirm secrets remain in `/etc/groupmate/groupmate.env` and runtime data in
   `/var/lib/groupmate`. Never copy these into the GitHub checkout.
3. Schedule a quiet period. Stop the service before taking a restricted backup of the complete
   runtime directory (including uploads and SQLite sidecars). Keep a copy of the old code release.
4. Stage the new source at a known commit. This release does not change the database schema.
   Preserve the existing service working directory, owner secret and XIPU workflow settings.
5. Run tests in staging, then restart the service only after the operator authorizes the update.
   Check `/`, `/teacher`, login, student joining, message persistence and teacher publication.
   Use a designated test group for an authenticated XIPU call; never publish test feedback to a real class.
6. If checks fail, stop the service and restore the recorded old code checkout, then restart.
   Keep the current runtime database when rolling back this UI-only release. Restore a database
   backup only after assessing new submissions: restoring an older database discards newer records.

The original `deploy/update.sh` is retained for compatibility. It pulls main and restarts;
review its scope before use. It is not an automatic rollback system. Do not run install/update
scripts merely to preview the UI. GitHub Pages cannot execute this Python backend.
