# pdfly CLI Skill for AI Agents

pdfly provides a skill package at ``skills/pdfly-cli/`` designed for AI agents to understand and correctly use all pdfly CLI commands.

## Skill Structure

```
skills/pdfly-cli/
├── SKILL.md                    # Main skill file (quick reference)
└── references/
    ├── sign.md               # PDF signing workflow
    ├── rotate.md             # Rotate command details
    ├── cat.md                # Extract/merge operations
    └── page-ranges.md        # Page range syntax
```

## Quick Reference

.. list-table::
   :header-rows: 1
   :widths: 30 50

   * - Command
     - Description
   * - ``pdfly compress IN OUT``
     - Lossless compression
   * - ``pdfly cat IN [PAGES]... -o OUT``
     - Merge/split pages
   * - ``pdfly rm IN [PAGES]... -o OUT``
     - Remove pages
   * - ``pdfly rotate -o OUT IN DEG [PGRGS]``
     - Rotate pages (note: -o must come before positional args)
   * - ``pdfly sign IN --p12 CERT [-o OUT]``
     - Sign PDF with PKCS12
   * - ``pdfly check-sign IN --pem CERT``
     - Verify signature
   * - ``pdfly meta IN [-o FORMAT]``
     - Show metadata (text/json/yaml)
   * - ``pdfly pagemeta IN IDX [-o FORMAT]``
     - Page details (0-based index)
   * - ``pdfly extract-images IN``
     - Extract images
   * - ``pdfly extract-text IN``
     - Extract text
   * - ``pdfly extract-annotated-pages IN [-o OUT]``
     - Extract annotated pages
   * - ``pdfly uncompress IN OUT``
     - Decompress PDF streams
   * - ``pdfly update-offsets IN [-o OUT]``
     - Fix PDF offsets
   * - ``pdfly 2-up IN OUT``
     - 2-up page layout
   * - ``pdfly booklet IN OUT [-b FILE] [-c FILE]``
     - Booklet printing layout
   * - ``pdfly x2pdf [FILES]... -o OUT``
     - Convert files to PDF

## Key Points for AI Agents

1. **Page indexing is 0-based** - First page is index 0, not 1
2. **Rotate command argument order** - ``-o/--output`` is **required** and must come **before** positional arguments
3. **Sign uses --p12 option** - Certificate is passed via ``--p12``, not as positional argument
4. **Check-sign uses --pem option** - Certificate is passed via ``--pem``, not as positional argument
5. **Page ranges use Python slice notation** - ``0:3`` means pages 0, 1, 2

## Using the Skill

When working with pdfly, load the skill to get accurate command syntax and examples. The skill includes:

- Verified command syntax (all commands tested against source code)
- Common usage patterns and examples
- Page range syntax with negative indices
- PDF signing workflow with certificate conversion
- Exit codes and error handling
