import json
import re

input_file = 'a.txt'
output_file = 'log.json'

events = []

with open(input_file, 'r') as f:
    lines = f.readlines()

time = None
for line in lines:
    line = line.strip()
    # Match tuple lines like (1, 0, 1)
    m = re.match(r'\((\d+),\s*(\d+),\s*(\d+)\)', line)
    if m:
        time, process, page = map(int, m.groups())
        event = {
            "time": time,
            "process": process,
            "page": page,
            "event": "request"
        }
        events.append(event)
    else:
        # Match Page Fault lines like: Page Fault: (0, 1)
        m_fault = re.match(r'Page Fault:\s*\((\d+),\s*(\d+)\)', line)
        if m_fault:
            process, page = map(int, m_fault.groups())
            # Use the last time + 0.5 to place fault event immediately after request
            fault_time = time + 0.5 if time is not None else 0
            event = {
                "time": fault_time,
                "process": process,
                "page": page,
                "event": "page_fault"
            }
            events.append(event)

with open(output_file, 'w') as f:
    json.dump(events, f, indent=2)

print(f"Converted {input_file} to {output_file} with {len(events)} events.")

