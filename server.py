#!/usr/bin/env python3
"""MEOK AI Labs — job-description-ai-mcp MCP Server. Generate and optimize job descriptions for any role."""

import json
import re
from datetime import datetime, timezone
from collections import defaultdict

from mcp.server.fastmcp import FastMCP
import sys, os
sys.path.insert(0, os.path.expanduser("~/clawd/meok-labs-engine/shared"))
from auth_middleware import check_access

FREE_DAILY_LIMIT = 15
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day"})
    _usage[c].append(now); return None

LEVEL_REQUIREMENTS = {
    "junior": {"years": "0-2", "prefix": "Entry-level", "skills_count": 3},
    "mid": {"years": "2-5", "prefix": "Mid-level", "skills_count": 5},
    "senior": {"years": "5-8", "prefix": "Senior", "skills_count": 7},
    "lead": {"years": "7-10", "prefix": "Lead", "skills_count": 8},
    "principal": {"years": "10+", "prefix": "Principal/Staff", "skills_count": 10},
}

SALARY_RANGES = {
    "software engineer": {"junior": (55, 80), "mid": (80, 120), "senior": (120, 170), "lead": (150, 200), "principal": (180, 250)},
    "product manager": {"junior": (60, 85), "mid": (90, 130), "senior": (130, 175), "lead": (160, 210), "principal": (190, 260)},
    "data scientist": {"junior": (60, 85), "mid": (85, 125), "senior": (125, 170), "lead": (155, 205), "principal": (185, 255)},
    "designer": {"junior": (45, 65), "mid": (65, 95), "senior": (95, 135), "lead": (120, 165), "principal": (150, 200)},
    "default": {"junior": (40, 60), "mid": (60, 90), "senior": (90, 130), "lead": (120, 170), "principal": (150, 210)},
}

BIASED_TERMS = {
    "ninja": "specialist", "rockstar": "expert", "guru": "experienced professional",
    "young": "early-career", "manpower": "workforce", "chairman": "chairperson",
    "aggressive": "ambitious", "dominate": "lead", "man-hours": "person-hours",
    "he/she": "they", "mankind": "humanity", "salesman": "sales representative",
    "fireman": "firefighter", "policeman": "police officer", "waitress": "server",
}

COMMON_SKILLS = {
    "software engineer": ["Python", "JavaScript", "SQL", "Git", "REST APIs", "CI/CD", "Docker", "AWS", "System Design", "Testing"],
    "product manager": ["Roadmap Planning", "User Research", "A/B Testing", "SQL", "Agile/Scrum", "Stakeholder Management", "Data Analysis", "PRD Writing", "Market Analysis", "OKRs"],
    "data scientist": ["Python", "SQL", "Machine Learning", "Statistics", "TensorFlow/PyTorch", "Data Visualization", "Feature Engineering", "A/B Testing", "NLP", "MLOps"],
    "designer": ["Figma", "User Research", "Wireframing", "Prototyping", "Design Systems", "Typography", "Accessibility", "Interaction Design", "Visual Design", "Usability Testing"],
}

mcp = FastMCP("job-description-ai", instructions="Generate, analyze, and optimize job descriptions with bias checking.")


@mcp.tool()
def generate_job_description(title: str, level: str = "mid", company: str = "Our company", remote: bool = True, skills: list[str] = [], api_key: str = "") -> str:
    """Generate a complete job description for a given role and level."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err

    lvl = LEVEL_REQUIREMENTS.get(level, LEVEL_REQUIREMENTS["mid"])
    title_lower = title.lower()

    # Get relevant skills
    role_skills = skills if skills else COMMON_SKILLS.get(title_lower, ["Communication", "Problem Solving", "Teamwork", "Attention to Detail", "Time Management"])
    selected_skills = role_skills[:lvl["skills_count"]]

    location = "Remote" if remote else "On-site"
    salary_key = title_lower if title_lower in SALARY_RANGES else "default"
    salary = SALARY_RANGES[salary_key].get(level, (60, 90))

    responsibilities = [
        f"Design, develop, and maintain {title_lower} solutions",
        f"Collaborate with cross-functional teams to define and ship features",
        f"Write clean, maintainable, and well-documented code/deliverables",
        f"Participate in code reviews, design discussions, and team planning",
        f"Mentor {'junior team members' if level in ('senior', 'lead', 'principal') else 'peers'} and contribute to best practices",
    ]
    if level in ("lead", "principal"):
        responsibilities.append("Drive technical/strategic direction and architecture decisions")
        responsibilities.append("Represent the team in cross-org planning and leadership forums")

    return json.dumps({
        "title": f"{lvl['prefix']} {title}",
        "company": company,
        "location": location,
        "experience": f"{lvl['years']} years",
        "salary_range": f"${salary[0]}k - ${salary[1]}k USD",
        "description": f"{company} is looking for a {lvl['prefix'].lower()} {title} to join our team. "
                       f"You will work on impactful projects in a collaborative, {location.lower()} environment.",
        "responsibilities": responsibilities,
        "required_skills": selected_skills,
        "nice_to_have": ["Open source contributions", "Public speaking experience", "Relevant certifications"],
        "benefits": ["Competitive salary", "Health insurance", "Flexible PTO", "Learning budget", "Equity/stock options"],
    }, indent=2)


@mcp.tool()
def analyze_requirements(description: str, api_key: str = "") -> str:
    """Analyze a job description text and extract structured requirements."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err

    lower = description.lower()
    # Detect experience level
    years_match = re.search(r'(\d+)\+?\s*(?:years?|yrs?)', lower)
    exp_years = int(years_match.group(1)) if years_match else None
    level = "junior" if exp_years and exp_years < 2 else "mid" if exp_years and exp_years < 5 else "senior" if exp_years and exp_years < 8 else "lead" if exp_years else "unknown"

    # Extract skills
    all_skills = set()
    for skills_list in COMMON_SKILLS.values():
        for skill in skills_list:
            if skill.lower() in lower:
                all_skills.add(skill)

    # Detect requirements vs nice-to-haves
    has_remote = any(w in lower for w in ["remote", "work from home", "wfh", "distributed"])
    has_degree = any(w in lower for w in ["bachelor", "master", "degree", "phd", "bs ", "ms "])
    word_count = len(description.split())

    return json.dumps({
        "estimated_level": level,
        "experience_years": exp_years,
        "detected_skills": sorted(all_skills),
        "requires_degree": has_degree,
        "remote_friendly": has_remote,
        "word_count": word_count,
        "readability": "good" if 200 <= word_count <= 800 else "too short" if word_count < 200 else "too long",
    }, indent=2)


@mcp.tool()
def suggest_salary_range(title: str, level: str = "mid", region: str = "US", api_key: str = "") -> str:
    """Suggest a competitive salary range based on role, level, and region."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err

    region_multipliers = {"US": 1.0, "UK": 0.85, "EU": 0.80, "AU": 0.90, "CA": 0.88, "LATAM": 0.45, "IN": 0.30, "SEA": 0.35}
    multiplier = region_multipliers.get(region.upper(), 0.75)

    salary_key = title.lower() if title.lower() in SALARY_RANGES else "default"
    base = SALARY_RANGES[salary_key].get(level, (60, 90))
    low = round(base[0] * multiplier)
    high = round(base[1] * multiplier)
    median = round((low + high) / 2)

    return json.dumps({
        "title": title,
        "level": level,
        "region": region.upper(),
        "salary_range": {"low": f"${low}k", "median": f"${median}k", "high": f"${high}k"},
        "currency": "USD equivalent",
        "region_multiplier": multiplier,
        "note": "Based on market data estimates. Actual ranges vary by company size, industry, and location.",
    }, indent=2)


@mcp.tool()
def check_bias(text: str, api_key: str = "") -> str:
    """Check a job description for biased or non-inclusive language and suggest alternatives."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl(): return err

    lower = text.lower()
    issues = []
    for biased, alternative in BIASED_TERMS.items():
        if biased in lower:
            issues.append({"term": biased, "suggestion": alternative, "severity": "high" if biased in ("ninja", "rockstar", "guru") else "medium"})

    # Check for excessive requirements
    word_count = len(text.split())
    warnings = []
    years_matches = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)', lower)
    if years_matches and max(int(y) for y in years_matches) > 10:
        warnings.append("Experience requirement over 10 years may unnecessarily limit candidate pool")
    if lower.count("must") > 3:
        warnings.append("Excessive use of 'must' - consider softer language for some requirements")
    if "culture fit" in lower:
        warnings.append("'Culture fit' can be exclusionary - consider 'culture add' instead")

    score = max(0, 100 - len(issues) * 15 - len(warnings) * 5)

    return json.dumps({
        "inclusivity_score": score,
        "biased_terms_found": len(issues),
        "issues": issues,
        "warnings": warnings,
        "recommendation": "Excellent - inclusive language" if score >= 90 else "Good - minor improvements suggested" if score >= 70 else "Needs revision - several biased terms detected",
    }, indent=2)


if __name__ == "__main__":
    mcp.run()
