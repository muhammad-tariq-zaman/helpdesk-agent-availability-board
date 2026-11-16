# helpdesk-agent-availability-board

Show who is available on the helpdesk right now: the input CSV lists agent, shift_start, shift_end and status (available, on-break or busy) — an agent is ON SHIFT when --now falls inside shift_start..shift_end (an end time at or before the start time means an overnight shift, e.g. 22:00–06:00). The board groups agents into AVAILABLE, ON BREAK, BUSY and OFF SHIFT, and names the next agent due on shift.

Sample input is included (sample.csv with six agents).

## How to run

```sh
python3 main.py sample.csv --now 10:30
```

## Example output

```
AVAILABLE:
  Ayesha Khan (08:00-16:00)
  Sara Malik (09:00-17:00)
ON BREAK:
  Hina Raza (08:00-12:00)
BUSY:
  Bilal Ahmed (08:00-16:00)
OFF SHIFT:
  Omar Farooq (14:00-22:00)
  Danish Ali (22:00-06:00)
2 available, 1 on break, 1 busy, 2 off shift out of 6 agent(s). Next on shift: Omar Farooq at 14:00.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
