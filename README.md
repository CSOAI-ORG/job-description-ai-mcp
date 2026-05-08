<div align="center">

# Job Description Ai MCP

**MCP server for job description ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-job-description-ai-mcp)](https://pypi.org/project/meok-job-description-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Job Description Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `generate_job_description` | Generate a complete job description for a given role and level. |
| `analyze_requirements` | Analyze a job description text and extract structured requirements. |
| `suggest_salary_range` | Suggest a competitive salary range based on role, level, and region. |
| `check_bias` | Check a job description for biased or non-inclusive language and suggest alterna |

## Installation

```bash
pip install meok-job-description-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "job-description-ai": {
      "command": "python",
      "args": ["-m", "meok_job_description_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
