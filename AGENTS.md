# AGENTS.md

1. Commit Messages:
    1. AI-Disclosure: The last line of a commit message should be `Co-authored-by: {model_name} <{model_email}>`
    2. Format: `{PREFIX}: {DESCRIPTION}\n\n{BODY}`, where PREFIX is the first that applies:
        * SEC: Security improvements. Typically, an infinite loop that was possible. Usually only used by the maintainers - others should report possible issues in this category privately first and only push a public change if told so.
        * BUG: A bug was fixed. Likely there are one or multiple issues. Then write in the BODY: Closes #123 where 123 is the issue number on GitHub. It would be absolutely amazing if you could write a regression test in those cases. That is a test that would fail without the fix. A bug is always an issue for users - test code or CI that was fixed is not considered a bug here.
        * ENH: A new feature! Describe in the body what it can be used for.
        * DEP: Deprecation. Either marking something as “this is going to be removed” or actually removing it.
        * PI: A performance improvement. DESCRIPTION must contain a benchmark section.
        * ROB: A robustness change, e.g. dealing better with broken PDF files.
        * DOC: A documentation change.
        * TST: Adding or adjusting tests.
        * DEV: Developer experience improvements, e.g., pre-commit or setting up CI.
        * MAINT: Quite a lot of different stuff. Performance improvements are, for sure, the most interesting changes in here. Refactorings as well.
        * STY: A style change. Something that makes code more consistent. Typically, a small change. It could also be better error messages for end users.
2. Project Language: (American) English must be used for all communication, including variable names, code comments, commit messages and documentation.
3. Use `assert` only within tests. It is fine to use assert in the "arrange" step of a test to show which preconditions are expected before executing the code under test.
4. Tests should have 3 sections: Arrange (setup data), Act (execute code under test), Assert (verify results). They do not need to have explicit comments separating the sections, but if the blocks get longer and more complex, it's appreciated.
