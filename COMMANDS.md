# Stobo MCP Commands

## User-facing (11)

| Command | What it does | Free? |
|---------|-------------|-------|
| `audit_site` | Analyze a website's SEO performance and AI visibility | Yes |
| `audit_article` | Analyze a single blog post or article | Yes |
| `generate_llms_txt` | Create an llms.txt file to help AI assistants understand your site | No |
| `generate_robots_txt` | Create a robots.txt that welcomes AI crawlers | Yes |
| `generate_sitemap` | Create a sitemap.xml by crawling your website | Yes |
| `generate_freshness_code` | Create date markup so AI knows your content is fresh | Yes |
| `rewrite_article` | Rewrite an existing article for better SEO and AI visibility | No |
| `extract_tone` | Analyze your brand's writing style from blog posts | No |
| `audit_freshness` | Check how many blog posts have proper date markup | Yes |
| `get_credits` | Check how many credits you have left | No |
| `check_connection` | Verify API connectivity (diagnostic) | Yes |

## Admin-facing (13) — removed from MCP, still available via CLI/API

| Command | What it does | Why removed |
|---------|-------------|-------------|
| `audit_seo` | SEO-only audit on an article | Redundant with `audit_article` |
| `audit_aeo` | AEO-only audit on an article | Redundant with `audit_article` |
| `get_audit` | Fetch a past audit by ID | CRUD — users just re-run the audit |
| `list_audits` | List recent audits | CRUD |
| `get_tone` | Fetch a stored tone profile | CRUD — `extract_tone` returns it directly |
| `list_tone_profiles` | List all tone profiles | CRUD |
| `delete_tone` | Delete a tone profile | CRUD |
| `get_job` | Poll optimization job status | `optimize` now returns results directly (sync) |
| `get_job_preview` | Get before/after preview of a job | Same — included in sync response |
| `list_jobs` | List optimization jobs | CRUD |
| `get_freshness` | Fetch a past freshness audit by ID | CRUD — users just re-run the audit |
| `export_report` | Generate a markdown report | Niche — Claude formats results itself |
| `get_export` | Fetch a cached export | CRUD |
