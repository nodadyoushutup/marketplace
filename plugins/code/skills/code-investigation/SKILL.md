---
name: code-investigation
description: Performs efficient, evidence-driven codebase investigations, behavior tracing, legacy-code analysis, and technical-debt discovery. Use when locating implementations, answering how code works, assessing whether code is unused, tracing cross-runtime contracts, or gathering evidence for debugging and technical planning.
---

# Code Investigation

Use this workflow to answer the specific question with the smallest investigation that produces defensible evidence.

## 1. Define the target

Restate internally:

- the exact question or decision
- likely entry points, symbols, routes, UI text, errors, configuration keys, or data shapes
- what evidence would confirm the answer
- what evidence would disprove the leading explanation
- explicit boundaries and unresolved assumptions

Do not begin with a repository-wide read.

Keep a lightweight evidence ledger while investigating:

- **Observed:** directly supported by code, configuration, tests, history, or runtime output.
- **Inferred:** the smallest conclusion that follows from observations.
- **Unknown:** unresolved assumptions that could change the answer.

Resolve unknowns by reading code, tests, or runtime evidence. Do not ask the
user to fill investigation gaps unless execute-first names a blocker.

Do not let an early inference silently become an observation.

## 2. Build a fast repository map

Check high-signal metadata first:

- workspace instructions and relevant nested guidance
- manifests, lockfiles, build configuration, and platform configuration
- top-level source, test, script, migration, and deployment directories
- package boundaries and generated/vendor exclusions

Search filenames before contents when the likely artifact name is known. Use exact symbols and distinctive literals before broad concepts.

For an unfamiliar repository or broad question, execute the repository mapper:

```bash
python3 .cursor/skills/code-investigation/scripts/repo_map.py . --limit 12
```

Use `--json` when structured output is easier to process. Skip the script when the relevant package and files are already known. Treat its output as leads, not proof.

## 3. Search in narrowing passes

Run independent searches in parallel when possible:

1. **Definition:** exact class, function, component, hook, route, schema, or configuration key.
2. **References:** imports, calls, renders, registrations, exports, re-exports, tests, mocks, fixtures, and documentation.
3. **Runtime wiring:** routers, dependency injection, plugin registries, runtime auto-discovery, dynamic imports, reflection, string-based lookup, environment variables, jobs, and CLI entry points.
4. **History only if needed:** commits, blame, removals, and migration context when current code cannot explain intent.

Narrow by language and directory. Avoid dumping large files; read focused regions around matches, then expand along the call graph.

For a named symbol or distinctive literal, execute the evidence search:

```bash
python3 .cursor/skills/code-investigation/scripts/symbol_evidence.py 'SymbolName' . --word
```

Useful options:

- `--glob '*.py'` or repeated `--glob` arguments to constrain scope.
- `--regex` for a deliberate pattern instead of a literal.
- `--history` only when current code cannot explain intent or replacement.
- `--json` for structured output.

The script groups likely definitions, tests, runtime wiring, documentation, and ordinary references. Verify its heuristic categories by reading the relevant files. Execute these scripts as utilities; do not read their source unless modifying or debugging them.

## 4. Trace behavior end to end

Follow the minimum complete path:

`entry point → orchestration → domain logic → persistence/external boundary → returned or rendered result`

Also inspect:

- error and fallback paths
- state ownership and lifecycle
- async/concurrency boundaries
- validation and authorization
- feature flags and environment-specific behavior
- tests that define expected behavior

For Python, check decorators, package exports, dependency injection, task/command registration, metaprogramming, and import side effects.

For React JSX, check component composition, props, hooks and effects, context/store ownership, routing, data fetching, memoization boundaries, event flow, and server/client rendering boundaries.

For bugs or regressions, also:

- reproduce or identify the exact failing observation before proposing a cause
- inspect recent changes only after locating the affected path
- find one comparable working path and enumerate meaningful differences
- state one falsifiable hypothesis at a time

Use a debugging skill alongside this one when the request requires diagnosing or fixing unexpected behavior. In a repository that ships its own debugging skill, follow that one for runtime-specific playbooks.

## 5. Analyze legacy code and technical debt

Do not equate “no textual references” with “unused.” Before calling code dead, check:

- dynamic or string-based references
- runtime conventions and auto-registration
- public APIs and downstream consumers
- templates, serialized data, database records, and configuration
- scripts, jobs, tests, migrations, deployments, and feature flags
- duplicate or replacement implementations

Classify findings:

- **Verified:** direct evidence establishes the claim.
- **Probable:** multiple signals support it, but a runtime or external dependency remains possible.
- **Suspected:** worth investigating; evidence is insufficient for action.

For each debt item, report evidence, impact, removal/refactor risk, dependencies, and the safest validation step. Prioritize by risk and value, not aesthetics.

Actively seek contradictory evidence before making a negative claim such as “unused,” “unreachable,” “never persisted,” or “not registered.” A search with no matches is weak evidence unless all plausible dynamic and external paths were checked.

## 6. Research uncertain best practices

Research externally only when the answer depends on current library behavior, security guidance, compatibility, or disputed practice.

Source priority:

1. official documentation or standards
2. source code, release notes, and maintainer-owned repositories
3. maintainer issue/discussion threads
4. reputable technical analysis
5. community discussions, including Reddit, as leads or corroboration only

Check publication/version context. Compare advice with the versions and constraints found locally. Cite links and identify conflicting or weak evidence.

## 7. Stop and report

Stop when the central question is supported by a definition, its relevant references or runtime wiring, and one corroborating source such as a test, configuration path, or call-site trace.

Before stopping:

- re-check the original question and boundaries
- separate verified facts from probable interpretations
- confirm cited line ranges still match the latest file contents
- identify the cheapest runtime check when static evidence is insufficient

Report:

- direct conclusion
- evidence with file paths, symbols, and line ranges where available
- concise behavior trace
- risks or debt with confidence labels
- recommendation and trade-offs
- unknowns plus the cheapest verification step

Do not write code or expand into unrelated cleanup.
