#!/usr/bin/env python3
"""
Specstory Yak Shave Analyzer

Analyzes .specstory/history files to detect when coding sessions
drifted off track from their original goal.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


@dataclass
class DomainShift:
    """Represents a detected shift in topic/domain during a session."""
    from_domain: str
    to_domain: str
    trigger_line: int
    signal: str  # "file_ref_change", "tool_type_change", "goal_replacement"


@dataclass
class SessionAnalysis:
    """Analysis results for a single specstory session."""
    filename: str
    session_id: str
    timestamp: str
    title: str

    # Initial intent
    initial_message: str
    initial_message_summary: str
    detected_goal: str

    # Metrics
    user_message_count: int = 0
    agent_message_count: int = 0
    file_refs: list = field(default_factory=list)
    tool_calls: dict = field(default_factory=dict)
    domain_shifts: list = field(default_factory=list)

    # Scoring
    yak_shave_score: int = 0
    score_breakdown: dict = field(default_factory=dict)

    # Summary
    started_with: str = ""
    ended_with: str = ""
    is_yak_shave: bool = False

    # Author (from git blame)
    author: str = "unknown"


def find_specstory_path() -> Optional[Path]:
    """Auto-detect .specstory/history path by searching up from cwd."""
    current = Path.cwd()
    for _ in range(10):  # Max 10 levels up
        specstory = current / ".specstory" / "history"
        if specstory.exists():
            return specstory
        if current.parent == current:
            break
        current = current.parent
    return None


def get_git_author(filepath: Path) -> str:
    """Get the git author who committed this file using git blame."""
    try:
        # Get the author of the first line (file creator)
        result = subprocess.run(
            ["git", "blame", "-p", "-L", "1,1", str(filepath)],
            capture_output=True,
            text=True,
            cwd=filepath.parent,
            timeout=5
        )
        if result.returncode == 0:
            # Parse porcelain output for author
            for line in result.stdout.split("\n"):
                if line.startswith("author "):
                    return line[7:].strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        pass
    return "unknown"


# Funny descriptions for different score ranges
SCORE_DESCRIPTIONS = {
    (0, 10): [
        "Surgical precision. In and out, no casualties.",
        "Like a ninja: swift, silent, done.",
        "You actually finished what you started. Rare.",
    ],
    (11, 30): [
        "Minor detours. Scenic route, but you got there.",
        "A few side quests, but the main quest prevailed.",
        "Only slightly distracted by shiny objects.",
    ],
    (31, 50): [
        "Started strong, got a bit... curious.",
        "The rabbit hole called. You answered.",
        "Scope creep is a feature, not a bug, right?",
    ],
    (51, 70): [
        "What started as a button fix became a journey.",
        "You touched files you didn't know existed.",
        "Your past self would not recognize this PR.",
    ],
    (71, 85): [
        "This was supposed to be a 5-minute fix.",
        "You've gone full yak. Never go full yak.",
        "At some point, you forgot what you came here for.",
    ],
    (86, 100): [
        "LEGENDARY yak shave. Bards will sing of this.",
        "You started fixing a typo and rewrote the universe.",
        "This session needs its own postmortem.",
        "The yak is fully shaved, groomed, and styled.",
    ],
}


def get_score_quip(score: int) -> str:
    """Get a funny description for a score."""
    import random
    for (low, high), quips in SCORE_DESCRIPTIONS.items():
        if low <= score <= high:
            return random.choice(quips)
    return "Impressive... in a concerning way."


def get_leaderboard_title(avg_score: float) -> str:
    """Get a funny title based on average yak shave score."""
    if avg_score >= 80:
        return "Legendary Yak Whisperer"
    elif avg_score >= 65:
        return "Chief Yak Shaver"
    elif avg_score >= 50:
        return "Senior Rabbit Hole Explorer"
    elif avg_score >= 35:
        return "Tangent Enthusiast"
    elif avg_score >= 20:
        return "Mostly On Track"
    else:
        return "Laser-Focused Legend"


def detect_platform() -> str:
    """Detect the user's platform for installation instructions."""
    import platform
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "linux":
        # Check for WSL
        try:
            with open("/proc/version", "r") as f:
                if "microsoft" in f.read().lower():
                    return "wsl"
        except:
            pass
        return "linux"
    return "unknown"


def get_install_instructions() -> str:
    """Return platform-specific installation instructions for SpecStory."""
    platform = detect_platform()

    instructions = """
No .specstory/history directory found.

SpecStory automatically saves your AI coding conversations to .specstory/history/
You need to install SpecStory to start capturing sessions.

"""

    if platform == "macos":
        instructions += """FOR CLAUDE CODE (macOS - Homebrew):
    brew tap specstoryai/tap
    brew update
    brew install specstory
    specstory run claude        # Run Claude Code with auto-save
    specstory sync claude       # Sync existing sessions

"""
    elif platform in ("linux", "wsl"):
        instructions += """FOR CLAUDE CODE (Linux/WSL):
    # Download from: https://github.com/specstoryai/getspecstory/releases
    tar -xzf SpecStoryCLI_Linux_x86_64.tar.gz
    sudo mv specstory /usr/local/bin/
    sudo chmod +x /usr/local/bin/specstory
    specstory run claude        # Run Claude Code with auto-save
    specstory sync claude       # Sync existing sessions

"""
    else:
        instructions += """FOR CLAUDE CODE:
    # macOS: brew tap specstoryai/tap && brew install specstory
    # Linux: Download from https://github.com/specstoryai/getspecstory/releases
    specstory run claude        # Run Claude Code with auto-save
    specstory sync claude       # Sync existing sessions

"""

    instructions += """FOR CURSOR / VS CODE:
    1. Open Cursor or VS Code
    2. Press Ctrl/Cmd+Shift+X (Extensions)
    3. Search "SpecStory" and click Install
    4. Start chatting - sessions auto-save to .specstory/history/

MORE INFO: https://docs.specstory.com/docs/quickstart

TIP: Use --path to analyze a specific .specstory/history location:
    python analyze.py --path /path/to/.specstory/history
"""
    return instructions


def parse_date_from_filename(filename: str) -> Optional[datetime]:
    """Extract date from specstory filename format: YYYY-MM-DD_HH-MM-SSZ-title.md"""
    match = re.match(r"(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2})", filename)
    if match:
        date_str = match.group(1)
        time_str = match.group(2).replace("-", ":")
        try:
            return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            pass
    return None


def extract_title_from_filename(filename: str) -> str:
    """Extract human-readable title from filename."""
    # Remove date prefix and extension
    match = re.match(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(?:-\d{2})?Z?-?(.*)\.md", filename)
    if match and match.group(1):
        return match.group(1).replace("-", " ").strip()
    return filename


def extract_session_id(content: str) -> str:
    """Extract session UUID from specstory header."""
    match = re.search(r"Session\s+([a-f0-9-]{36})", content)
    return match.group(1) if match else "unknown"


def extract_messages(content: str) -> list[tuple[str, str, str]]:
    """
    Extract user/agent messages from specstory content.
    Returns list of (role, timestamp, message_text)
    """
    messages = []

    # Pattern for message headers: _**User (timestamp)**_ or _**Agent (...)**_
    pattern = r"_\*\*(\w+)(?:\s+\([^)]*\))?\s*\(([^)]+)\)\*\*_\s*(?:<!--[^>]+-->)?\s*(.*?)(?=_\*\*(?:User|Agent|Assistant)|$)"

    for match in re.finditer(pattern, content, re.DOTALL):
        role = match.group(1).lower()
        timestamp = match.group(2)
        text = match.group(3).strip()

        # Clean up the text - remove trailing ---
        text = re.sub(r"\n---\s*$", "", text).strip()

        if role in ("user", "agent", "assistant"):
            messages.append((role, timestamp, text))

    return messages


def extract_file_refs(content: str) -> list[str]:
    """Extract @file references from content."""
    # Match @path/to/file or @filename patterns
    refs = re.findall(r"@([\w./\-]+(?:\.\w+)?)", content)
    return list(set(refs))


def extract_tool_calls(content: str) -> dict[str, int]:
    """Extract tool call counts from content."""
    tools = {}

    # Pattern 1: Tool use: **ToolName**
    for match in re.finditer(r"Tool use:\s*\*\*(\w+)\*\*", content):
        tool = match.group(1)
        tools[tool] = tools.get(tool, 0) + 1

    # Pattern 2: <tool-use data-tool-name="ToolName">
    for match in re.finditer(r'data-tool-name="(\w+)"', content):
        tool = match.group(1)
        tools[tool] = tools.get(tool, 0) + 1

    return tools


def infer_domain(file_ref: str) -> str:
    """Infer the domain/area from a file reference."""
    ref_lower = file_ref.lower()

    if any(x in ref_lower for x in ["test", "spec", "__test__"]):
        return "testing"
    if any(x in ref_lower for x in ["doc", "readme", "md", "changelog"]):
        return "documentation"
    if any(x in ref_lower for x in ["ci", "github", "workflow", "jenkins", "docker", "k8s"]):
        return "devops"
    if any(x in ref_lower for x in ["config", "env", "settings", "yaml", "json", "toml"]):
        return "configuration"
    if any(x in ref_lower for x in ["ui", "component", "page", "view", "css", "style", "tsx", "jsx"]):
        return "frontend"
    if any(x in ref_lower for x in ["api", "server", "route", "controller", "handler"]):
        return "backend"
    if any(x in ref_lower for x in ["db", "model", "schema", "migration", "sql"]):
        return "database"
    if any(x in ref_lower for x in ["auth", "login", "session", "token"]):
        return "auth"
    if any(x in ref_lower for x in ["script", "bin", "tool", "cli"]):
        return "tooling"

    return "code"


def detect_domain_shifts(file_refs: list[str], messages: list) -> list[DomainShift]:
    """Detect when the session shifted domains based on file references."""
    shifts = []

    if not file_refs:
        return shifts

    # Track domains in order of appearance
    seen_domains = []
    for ref in file_refs:
        domain = infer_domain(ref)
        if not seen_domains or seen_domains[-1] != domain:
            if seen_domains:
                shifts.append(DomainShift(
                    from_domain=seen_domains[-1],
                    to_domain=domain,
                    trigger_line=0,  # Would need more parsing for exact line
                    signal="file_ref_change"
                ))
            seen_domains.append(domain)

    return shifts


def summarize_message(msg: str, max_len: int = 100) -> str:
    """Create a short summary of a message."""
    # Take first line or first N chars
    first_line = msg.split("\n")[0].strip()
    if len(first_line) > max_len:
        return first_line[:max_len-3] + "..."
    return first_line


def detect_goal(initial_message: str) -> str:
    """Extract the likely goal from the initial message."""
    msg_lower = initial_message.lower()

    # Look for explicit goal indicators
    patterns = [
        r"(?:help me|i want to|i need to|let's|please)\s+(.{10,80})",
        r"(?:fix|add|create|build|implement|update|refactor)\s+(.{10,80})",
        r"^(.{10,80})\?",  # Questions
    ]

    for pattern in patterns:
        match = re.search(pattern, msg_lower)
        if match:
            return match.group(1).strip()[:80]

    return summarize_message(initial_message, 80)


def compute_yak_shave_score(analysis: SessionAnalysis) -> tuple[int, dict]:
    """
    Compute yak shave score (0-100) based on various factors.
    Returns (score, breakdown_dict)
    """
    breakdown = {}

    # Factor 1: Domain shifts (40% weight)
    num_shifts = len(analysis.domain_shifts)
    shift_score = min(100, num_shifts * 25)  # Each shift adds 25 points
    breakdown["domain_shifts"] = {"raw": num_shifts, "score": shift_score, "weight": 0.4}

    # Factor 2: Session length vs initial message complexity (20% weight)
    initial_words = len(analysis.initial_message.split())
    total_messages = analysis.user_message_count + analysis.agent_message_count

    # Simple request + long session = high yak shave
    if initial_words < 20 and total_messages > 10:
        length_score = min(100, (total_messages - 10) * 10)
    elif initial_words < 50 and total_messages > 20:
        length_score = min(100, (total_messages - 20) * 5)
    else:
        length_score = 0
    breakdown["length_ratio"] = {"raw": f"{initial_words}w/{total_messages}m", "score": length_score, "weight": 0.2}

    # Factor 3: Tool type cascade (15% weight)
    # Read -> Edit -> Create is more escalation than just Read
    tool_types = set(analysis.tool_calls.keys())
    escalation_levels = {
        "Read": 1, "Grep": 1, "Glob": 1,
        "Edit": 2, "Write": 3,
        "Bash": 3, "shell": 3,
        "WebFetch": 4, "WebSearch": 4,
        "Task": 5,
    }
    max_escalation = max((escalation_levels.get(t, 2) for t in tool_types), default=1)
    tool_score = (max_escalation - 1) * 25
    breakdown["tool_cascade"] = {"raw": list(tool_types), "score": tool_score, "weight": 0.15}

    # Factor 4: File reference diversity (25% weight)
    domains = set(infer_domain(ref) for ref in analysis.file_refs)
    domain_score = min(100, (len(domains) - 1) * 25) if domains else 0
    breakdown["domain_diversity"] = {"raw": list(domains), "score": domain_score, "weight": 0.25}

    # Weighted total
    total = (
        shift_score * 0.4 +
        length_score * 0.2 +
        tool_score * 0.15 +
        domain_score * 0.25
    )

    return int(total), breakdown


def analyze_session(filepath: Path) -> Optional[SessionAnalysis]:
    """Analyze a single specstory session file."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
        return None

    filename = filepath.name
    messages = extract_messages(content)

    if not messages:
        return None

    # Get initial user message
    initial_msg = ""
    for role, _, text in messages:
        if role == "user":
            initial_msg = text
            break

    if not initial_msg:
        return None

    # Count messages by role
    user_count = sum(1 for r, _, _ in messages if r == "user")
    agent_count = sum(1 for r, _, _ in messages if r in ("agent", "assistant"))

    # Extract file refs and tool calls
    file_refs = extract_file_refs(content)
    tool_calls = extract_tool_calls(content)

    # Detect domain shifts
    domain_shifts = detect_domain_shifts(file_refs, messages)

    # Get last message for "ended with"
    last_agent_msg = ""
    for role, _, text in reversed(messages):
        if role in ("agent", "assistant"):
            last_agent_msg = text
            break

    analysis = SessionAnalysis(
        filename=filename,
        session_id=extract_session_id(content),
        timestamp=str(parse_date_from_filename(filename) or "unknown"),
        title=extract_title_from_filename(filename),
        initial_message=initial_msg,
        initial_message_summary=summarize_message(initial_msg),
        detected_goal=detect_goal(initial_msg),
        user_message_count=user_count,
        agent_message_count=agent_count,
        file_refs=file_refs,
        tool_calls=tool_calls,
        domain_shifts=[asdict(s) for s in domain_shifts],
        started_with=summarize_message(initial_msg, 300),
        ended_with=summarize_message(last_agent_msg, 300) if last_agent_msg else "",
    )

    # Compute score
    score, breakdown = compute_yak_shave_score(analysis)
    analysis.yak_shave_score = score
    analysis.score_breakdown = breakdown
    analysis.is_yak_shave = score > 40

    return analysis


def format_report(analyses: list[SessionAnalysis], args) -> str:
    """Format the analysis results as a human-readable report."""
    if not analyses:
        return "No sessions found in the specified date range. Your yaks remain unshaved."

    # Sort by yak shave score descending
    sorted_analyses = sorted(analyses, key=lambda a: a.yak_shave_score, reverse=True)

    # Compute stats
    avg_score = sum(a.yak_shave_score for a in analyses) / len(analyses)
    max_score = sorted_analyses[0].yak_shave_score if sorted_analyses else 0
    total_shifts = sum(len(a.domain_shifts) for a in analyses)

    # Check for multiple authors
    authors = defaultdict(list)
    for a in analyses:
        if a.author and a.author != "unknown":
            authors[a.author].append(a)

    # Header with flair
    if avg_score < 25:
        verdict = "Remarkably focused. Are you even human?"
    elif avg_score < 45:
        verdict = "Mostly on track. Room for more adventure."
    elif avg_score < 65:
        verdict = "Classic developer behavior detected."
    elif avg_score < 80:
        verdict = "You came for a bug fix, stayed for the refactor."
    else:
        verdict = "This is art. Chaotic, beautiful art."

    lines = [
        "=" * 60,
        "  YAK SHAVE REPORT",
        "  " + verdict,
        "=" * 60,
        "",
        f"  Sessions analyzed:    {len(analyses)}",
        f"  Average yak score:    {avg_score:.0f}/100",
        f"  Peak yak achieved:    {max_score}/100",
        f"  Total domain shifts:  {total_shifts}",
        "",
    ]

    # Calculate author stats (used in leaderboard and summary)
    author_stats = []
    for author, sessions in authors.items():
        avg = sum(s.yak_shave_score for s in sessions) / len(sessions)
        peak = max(s.yak_shave_score for s in sessions)
        author_stats.append((author, avg, peak, len(sessions)))
    # Sort by average score descending
    author_stats.sort(key=lambda x: x[1], reverse=True)

    # Leaderboard for multiple authors
    if len(authors) > 1:
        lines.append("TEAM YAK LEADERBOARD")
        lines.append("-" * 40)

        for rank, (author, avg, peak, count) in enumerate(author_stats[:5], 1):
            title = get_leaderboard_title(avg)
            # Truncate author name if too long
            display_name = author[:20] + "..." if len(author) > 20 else author
            lines.append(f"  {rank}. {display_name}")
            lines.append(f"     {title}")
            lines.append(f"     Avg: {avg:.0f}/100 | Peak: {peak}/100 | Sessions: {count}")
            lines.append("")

    # Dynamic sizing based on total sessions
    num_sessions = len(analyses)
    if num_sessions > 100:
        hall_of_fame_count = max(args.top, 7)
        hall_of_discipline_count = 5
    elif num_sessions > 50:
        hall_of_fame_count = max(args.top, 5)
        hall_of_discipline_count = 4
    else:
        hall_of_fame_count = args.top
        hall_of_discipline_count = 3

    # Top yak shaves
    lines.append("HALL OF FAME (Top Yak Shaves)")
    lines.append("-" * 60)

    for i, a in enumerate(sorted_analyses[:hall_of_fame_count], 1):
        domains = [s["to_domain"] for s in a.domain_shifts]

        # Truncate domain chain if too long
        if len(domains) > 5:
            domain_str = " -> ".join(domains[:3]) + f" -> ... -> {domains[-1]} ({len(domains)} total)"
        else:
            domain_str = " -> ".join(domains) if domains else "stayed focused"

        author_str = f" by {a.author}" if a.author and a.author != "unknown" else ""

        lines.append(f"{i}. [{a.yak_shave_score}/100] {a.timestamp[:10]}{author_str}")
        lines.append(f"   Session: \"{a.title or 'untitled'}\"")
        lines.append(f"   Filename: {a.filename}")
        lines.append(f"   ")
        lines.append(f"   Started with: \"{a.started_with}\"")
        if a.ended_with and a.ended_with != a.started_with:
            # Clean up ended_with - remove tool tags
            ended_clean = re.sub(r'<[^>]+>', '', a.ended_with).strip()
            lines.append(f"   Ended up at:  \"{ended_clean}\"")
        lines.append(f"   ")
        lines.append(f"   Domain journey: {domain_str}")
        lines.append(f"   Messages: {a.user_message_count} user / {a.agent_message_count} agent")
        if a.tool_calls:
            top_tools = sorted(a.tool_calls.items(), key=lambda x: x[1], reverse=True)[:4]
            tool_str = ", ".join(f"{t}({c})" for t, c in top_tools)
            lines.append(f"   Top tools: {tool_str}")
        lines.append(f"   ")
        lines.append(f"   \"{get_score_quip(a.yak_shave_score)}\"")
        lines.append("")

    # Most focused sessions (the heroes)
    focused = [a for a in sorted_analyses if a.yak_shave_score < 25]
    if focused:
        lines.append("HALL OF DISCIPLINE (Most Focused)")
        lines.append("-" * 60)
        lines.append("These developers stayed on target. Learn from them.")
        lines.append("")

        for a in list(reversed(focused))[:hall_of_discipline_count]:
            author_str = f" by {a.author}" if a.author and a.author != "unknown" else ""
            lines.append(f"  [{a.yak_shave_score}/100] {a.timestamp[:10]}{author_str}")
            lines.append(f"    Session: \"{a.title or 'untitled'}\"")
            lines.append(f"    Filename: {a.filename}")
            lines.append(f"    Goal: \"{a.started_with}\"")
            lines.append(f"    Messages: {a.user_message_count} user / {a.agent_message_count} agent | Domain shifts: {len(a.domain_shifts)}")
            lines.append(f"    \"{get_score_quip(a.yak_shave_score)}\"")
            lines.append("")

    # Fun stats
    if total_shifts > 0:
        most_common_domains = defaultdict(int)
        for a in analyses:
            for shift in a.domain_shifts:
                most_common_domains[shift["to_domain"]] += 1
        top_domain = max(most_common_domains.items(), key=lambda x: x[1])

        lines.append("FUN FACTS")
        lines.append("-" * 40)
        lines.append(f"  Most visited domain: {top_domain[0]} ({top_domain[1]} visits)")
        lines.append(f"  Avg shifts per session: {total_shifts / len(analyses):.1f}")

        # Find the biggest single-session journey
        biggest_journey = max(analyses, key=lambda a: len(a.domain_shifts))
        if len(biggest_journey.domain_shifts) > 3:
            lines.append(f"  Longest journey: {len(biggest_journey.domain_shifts)} domains in one session")
        lines.append("")

    # Score guide with personality
    lines.append("SCORE GUIDE")
    lines.append("-" * 40)
    lines.append("   0-20  Laser focused (teach us your ways)")
    lines.append("  21-40  Minor tangents (happens to the best)")
    lines.append("  41-60  Moderate drift (the spice of coding)")
    lines.append("  61-80  Significant yak (you're in deep now)")
    lines.append("  81-100 LEGENDARY (they'll write songs about this)")
    lines.append("")

    # Summary at the end
    lines.append("=" * 60)
    lines.append("SUMMARY")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"  Total sessions:       {num_sessions}")
    lines.append(f"  Average yak score:    {avg_score:.0f}/100")
    lines.append(f"  Peak yak achieved:    {max_score}/100")
    lines.append(f"  Total domain shifts:  {total_shifts}")
    lines.append("")

    # Compact leaderboard summary
    if len(authors) > 1:
        lines.append("  TEAM RANKINGS:")
        for rank, (author, avg, peak, count) in enumerate(author_stats[:5], 1):
            display_name = author[:25] + "..." if len(author) > 25 else author
            title = get_leaderboard_title(avg)
            lines.append(f"    {rank}. {display_name:<28} {avg:.0f}/100 avg  ({count} sessions) - {title}")
        lines.append("")

    # Quick stats
    yak_sessions = len([a for a in analyses if a.yak_shave_score >= 50])
    focused_sessions = len([a for a in analyses if a.yak_shave_score < 25])
    legendary_sessions = len([a for a in analyses if a.yak_shave_score >= 85])

    lines.append(f"  Legendary yak shaves (85+):  {legendary_sessions}")
    lines.append(f"  Significant yak shaves (50+): {yak_sessions}")
    lines.append(f"  Focused sessions (<25):       {focused_sessions}")
    lines.append("")
    lines.append(f"  Verdict: {verdict}")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze specstory sessions for yak shaving patterns"
    )
    parser.add_argument("--days", type=int, default=7, help="Analyze last N days (default: 7)")
    parser.add_argument("--from", dest="from_date", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--to", dest="to_date", help="End date (YYYY-MM-DD)")
    parser.add_argument("--path", help="Path to .specstory/history directory")
    parser.add_argument("--top", type=int, default=5, help="Show top N worst yak shaves")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", action="store_true", help="Show detailed analysis")
    parser.add_argument("--by-mtime", action="store_true", help="Filter by file modification time instead of filename date")
    parser.add_argument("-o", "--output", help="Write report to markdown file (e.g., yak-report.md)")

    args = parser.parse_args()

    # Find specstory path
    if args.path:
        history_path = Path(args.path)
    else:
        history_path = find_specstory_path()

    if not history_path or not history_path.exists():
        print(get_install_instructions(), file=sys.stderr)
        sys.exit(1)

    # Determine date range
    if args.from_date:
        start_date = datetime.strptime(args.from_date, "%Y-%m-%d")
    else:
        start_date = datetime.now() - timedelta(days=args.days)

    if args.to_date:
        end_date = datetime.strptime(args.to_date, "%Y-%m-%d")
    else:
        end_date = datetime.now()

    # Find matching files
    analyses = []
    for filepath in sorted(history_path.glob("*.md")):
        # Determine file date based on filter mode
        if args.by_mtime:
            file_date = datetime.fromtimestamp(filepath.stat().st_mtime)
        else:
            file_date = parse_date_from_filename(filepath.name)

        if file_date and start_date <= file_date <= end_date:
            analysis = analyze_session(filepath)
            if analysis:
                # Get git author for this file
                analysis.author = get_git_author(filepath)
                analyses.append(analysis)

    # Generate output
    if args.json:
        output_content = json.dumps({
            "date_range": {"from": start_date.isoformat(), "to": end_date.isoformat()},
            "sessions_analyzed": len(analyses),
            "average_score": sum(a.yak_shave_score for a in analyses) / len(analyses) if analyses else 0,
            "sessions": [asdict(a) for a in sorted(analyses, key=lambda x: x.yak_shave_score, reverse=True)]
        }, indent=2, default=str)
    else:
        output_content = format_report(analyses, args)

    # Write to file or stdout
    if args.output:
        output_path = Path(args.output)
        # Add .md extension if not present and not JSON
        if not args.json and not output_path.suffix:
            output_path = output_path.with_suffix(".md")
        elif args.json and not output_path.suffix:
            output_path = output_path.with_suffix(".json")

        output_path.write_text(output_content, encoding="utf-8")
        print(f"Report written to: {output_path}", file=sys.stderr)
        print(output_path)  # Print path to stdout for easy piping/capture
    else:
        print(output_content)


if __name__ == "__main__":
    main()
