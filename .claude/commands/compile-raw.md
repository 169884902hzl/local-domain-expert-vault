Read all files in the raw/ directory. For each file, extract the core concepts, entities, and topics following the SCHEMA.md specification.

For each extracted item:
1. Check if a corresponding wiki page already exists in wiki/concepts/, wiki/entities/, or wiki/topics/
2. If it exists, append new information and update the `updated` field
3. If it doesn't exist, create a new wiki page with proper frontmatter, [[wikilinks]] to related pages, and update wiki/INDEX.md

Use the type required by the destination:
- `type: literature` for `wiki/topics/`
- `type: concept` for `wiki/concepts/`
- `type: entity` for `wiki/entities/`

Include [[cross-references]] between related articles and run `python .claude/scripts/audit_kb.py` when done.

When done, output a summary of what was created/updated.
