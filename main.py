"""Show who is available on the helpdesk right now.

Usage: python3 main.py agents.csv [--now 10:30]
CSV columns: agent,shift_start,shift_end,status. Status is
available, on-break or busy. An agent is ON SHIFT when --now
falls inside shift_start..shift_end (an end time at or before
the start time means an overnight shift, e.g. 22:00-06:00).
The board groups agents into AVAILABLE, ON BREAK, BUSY and
OFF SHIFT, and names the next agent due on shift.
"""
import argparse, csv, sys

def to_minutes(value):
    hours, minutes = value.strip().split(":")
    return int(hours) * 60 + int(minutes)

def on_shift(start, end, now):
    if end <= start:
        return now >= start or now < end
    return start <= now < end

def board(rows, now="10:30"):
    now_minutes = to_minutes(now)
    groups = {"AVAILABLE": [], "ON BREAK": [], "BUSY": [], "OFF SHIFT": []}
    next_on = None
    for row in rows:
        agent = row["agent"].strip()
        start = to_minutes(row["shift_start"])
        end = to_minutes(row["shift_end"])
        status = row["status"].strip().lower()
        if on_shift(start, end, now_minutes):
            if status == "available":
                groups["AVAILABLE"].append((agent, row["shift_start"], row["shift_end"]))
            elif status == "on-break":
                groups["ON BREAK"].append((agent, row["shift_start"], row["shift_end"]))
            else:
                groups["BUSY"].append((agent, row["shift_start"], row["shift_end"]))
        else:
            groups["OFF SHIFT"].append((agent, row["shift_start"], row["shift_end"]))
            if start > now_minutes:
                if next_on is None or start < next_on[1]:
                    next_on = (agent, start, row["shift_start"])
    return groups, next_on

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--now", default=None,
                        help="current time HH:MM (default: current time)")
    args = parser.parse_args(argv)
    from datetime import datetime
    now = args.now or datetime.now().strftime("%H:%M")
    with open(args.path, newline="", encoding="utf-8") as f:
        groups, next_on = board(list(csv.DictReader(f)), now)
    for label in ("AVAILABLE", "ON BREAK", "BUSY", "OFF SHIFT"):
        print(f"{label}:")
        for agent, start, end in groups[label]:
            print(f"  {agent} ({start}-{end})")
    total = sum(len(v) for v in groups.values())
    print(f"{len(groups['AVAILABLE'])} available, "
          f"{len(groups['ON BREAK'])} on break, "
          f"{len(groups['BUSY'])} busy, "
          f"{len(groups['OFF SHIFT'])} off shift out of {total} agent(s).", end="")
    if next_on is not None:
        print(f" Next on shift: {next_on[0]} at {next_on[2]}.")
    else:
        print()
    return 0

if __name__ == "__main__":
    sys.exit(main())
