# Job Description AI

> By [MEOK AI Labs](https://meok.ai) — Generate, analyze, and optimize job descriptions with bias checking

## Installation

```bash
pip install job-description-ai-mcp
```

## Usage

```bash
python server.py
```

## Tools

### `generate_job_description`
Generate a complete job description for a given role and level.

**Parameters:**
- `title` (str): Job title
- `level` (str): Seniority level: junior, mid, senior, lead, principal (default: "mid")
- `company` (str): Company name (default: "Our company")
- `remote` (bool): Whether the role is remote (default: True)
- `skills` (list[str]): Required skills list

### `analyze_requirements`
Analyze a job description text and extract structured requirements.

**Parameters:**
- `description` (str): Full job description text

### `suggest_salary_range`
Suggest a competitive salary range based on role, level, and region.

**Parameters:**
- `title` (str): Job title
- `level` (str): Seniority level (default: "mid")
- `region` (str): Region code: US, UK, EU, AU, CA, LATAM, IN, SEA (default: "US")

### `check_bias`
Check a job description for biased or non-inclusive language and suggest alternatives.

**Parameters:**
- `text` (str): Job description text to analyze

## Authentication

Free tier: 15 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
