---
name: global-standing-orders
description: >-
  Always-on portable agent postures: execute-first, MCP-first, and no-localhost
  URLs. Use at session start. Claude Code loads this as a skill; Cursor also
  ships matching alwaysApply rules. Coding standards, secure coding, and
  Conventional Commits live in the sibling `code` plugin; BA/planner agents
  live in `business-analyst`; other optional stacks are sibling plugins too.
---

# Standing orders (portable)

Apply these postures for the whole session unless the user overrides them.

## Execute first

Do the work. Do not ask permission to edit, run commands, or verify. Ask at
most one question, and only for irreversible data loss, a missing secret,
incompatible product outcomes with no safe default, or a broad ask with no
success criteria. Tracker create-only asks: file the issue and stop.

See also: `global-action-first`.

## MCP first

When a ready MCP covers the external service, use it. Do not prefer CLI,
curl, or ad-hoc SDKs for the same action. No matching MCP → use the normal
CLI/SDK immediately.

## No localhost for the user

Never put `localhost` or `127.0.0.1` in a URL shown to the user. Resolve a
machine-reachable `$HOST` (project env → detect → optional memory preference)
and build `http://$HOST:<port>`.

## Sibling plugins

| Plugin | When |
| --- | --- |
| `code` | Language standards, secure coding, Conventional Commits, coding workflow, worktrees/merge, coding agents |
| `business-analyst` | Business analysis, ambiguous multi-step planning, external research |
| `agentmemory` | AgentMemory MCP connected |
| `atlassian` | Unified Jira + Confluence craft |
| `github` | GitHub PR checks/comments + Actions CI |
| `jenkins` | Jenkins builds + pipeline CI |
| `framework` | Framework monorepo craft (this marketplace) |
| `homelab` | Homelab infra repo (from **marketplace-private**) |
| `browser` | Browser QA / IDE browser → CLI |
| `drawio` | `.drawio` author/repair + editor false alarms |
| `lucidchart` | Lucidchart Standard Import author/repair + `.lucid` packaging |
| `google-workspace` | Gmail + Drive + Calendar + Docs/Sheets |
| `google-cloud` | GCP projects + Compute/GKE + GCS |
| `freshservice` | Freshservice ITSM tickets |
| `vault` | Vault secrets/PKI |
| `grafana` | Dashboards / Explore / alerting |
| `cloudflare` | DNS with destructive gates |
| `compose` | Docker Compose layout/ops + destructive gates |
| `kubernetes` | Pod/event/log triage |
| `proxmox` | Proxmox VE inventory + gated VM ops |
| `argocd` | Argo CD apps + gated sync |
| `prometheus` | PromQL discover/query |
| `graylog` | Graylog search + redaction |
| `minio` | MinIO/S3 buckets/objects |
| `velero` | Velero backups/restores |
| `fortigate` | FortiGate inventory + gated policies |
| `yarr` | *arr / Plex / qBit / Seerr fleet |
