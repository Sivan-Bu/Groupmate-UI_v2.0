# v2.0 integration and acceptance

This release starts from the supplied groupmate-classroom-main.zip. API contracts, database schema and the original live JavaScript handlers are preserved.
Python changes are limited to explicit UTF-8 file reads and serving the new stylesheet.
The supplied v1.2 HTML is a visual reference, not the runtime application: its hard-coded
groups, simulated posts, approval booleans and sample AI messages are not imported.

`static/lm-v2.css` applies its purple #7423b5, white panels, grey sidebar, navigation,
typography, forms and mobile layout to both live entry points. This is a theme and layout
integration into the existing frontend, not a pixel-identical rewrite of every prototype screen.
Existing classroom navigation and field structures are retained to preserve working workflows.

| Prototype workflow | Live implementation |
| --- | --- |
| Course / case / activity preparation | `/` teacher login, teaching studio, source selection, generation, confirmations |
| Group monitor / assessment / reports | `/teacher`, real sessions, evidence, teacher review and publication |
| Student classroom / case | `/`, join code and pseudonym, published packet |
| Discussion / AI | Existing message submission and role orchestration; server-side XIPU client |
| Reflection / feedback | Existing individual reflection and teacher-published outcomes |

## Demonstration to a teacher

Run the Python server. Use two separate browser profiles for teacher and student.
Create a sample activity, review and confirm all required sections, publish and open a group.
Join using its code, contribute, invite an AI role, submit the required work and reflection.
Return as teacher, review evidence and feedback, approve/publish, then inspect the student outcome.
Only generated output received from XIPU is live AI output. An absent key must show a configuration
error rather than invented replies. Do not use `/demo-guide` as proof of a live AI call.

No production credentials are included. Live XIPU access requires the original approved workflow,
valid server-side key, campus/network access and its published input/output contract. Automated
transport tests use fixtures; they do not certify the current remote service or account permissions.

## Release data boundaries

Keep `groupmate/sample*.json` and test/native fixtures: these are bundled case/template inputs,
not a database of classroom sessions. Review their case content for your intended publication.
Runtime databases, uploads, .env files, logs, caches and local test output are excluded by the
source allowlist packager. Credential-pattern scanning supplements that exclusion but cannot
prove the absence of every possible confidential string.
