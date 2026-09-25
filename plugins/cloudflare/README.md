# cloudflare

Cloudflare DNS craft — record changes with destructive gates. Install when
Cloudflare MCP is available.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `cloudflare-dns` | List / create / update |
| `cloudflare-safety` | Delete / bulk risk gates |

## Skills

| Skill | Purpose |
| --- | --- |
| `cloudflare` | Index / gate |

## Commands

- `/cloudflare` → DNS craft

## Pairing

- `global-mcp-first` — Cloudflare MCP before raw API
- `global-host-url` — user-facing hosts after DNS changes
