# Static Evolution public data

This public repository mirrors published content from [staticevolution.com](https://staticevolution.com), following the backup/Datasette architecture of Simon Willison's blog.

The scheduled workflow reads the production PostgreSQL database, selects publishing tables, removes drafts, future/unlisted content and operational fields, and stores a diffable JSON history under `data/`. Railway builds an immutable, public read-only Datasette instance from that history.

No users, permissions, admin logs, sessions, credentials, private bucket keys or draft records belong in this repository.
