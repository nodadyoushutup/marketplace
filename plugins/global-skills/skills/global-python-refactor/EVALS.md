# Python Refactor Evaluation Scenarios

A strong response protects behavior before proposing structure and refuses
unnecessary scope.

## 1. Transaction extraction

Prompt: extract persistence from a request handler that flushes for an ID,
emits an external event, and commits.

Pass criteria:

- identifies flush, commit, rollback, object-lifetime, and side-effect ordering
- preserves transaction ownership and exception behavior
- does not silently reorder the event as part of structural work
- requires focused success and failure-path tests

## 2. Discovered class move

Prompt: move a dynamically registered class to a new module.

Pass criteria:

- checks defining module, class identity, decorators, imports, registration, and
  persisted references
- does not assume a re-export preserves introspection-based discovery
- requires registration or runtime integration verification

## 3. Entrypoint decomposition

Prompt: split a large entrypoint without changing behavior.

Pass criteria:

- preserves arguments, exit codes, signals, environment validation, errors, and
  startup ordering
- avoids circular imports and hidden import-time effects
- verifies actual entrypoint behavior, not only imports

## 4. Tiny local edit

Prompt: rename one local variable in a short private helper.

Pass criteria:

- performs only the narrow rename
- adds no abstraction, module, dependency, or tooling
- runs validation proportional to risk
