tasks = [
    {"name": "Fix Linux Drivers", "priority": 1, "status": "Complete"},
    {"name": "Master Git", "priority": 2, "status": "Complete"},
    {"name": "Learn Python Async", "priority": 3, "status": "In Progress"},
]

print("---Current Project Status ---")

for t in tasks: 
    if t["status"] == "Complete":
        checkmark = "✅"
    else: checkmark = "⏳"

    print(f"{checkmark} {t['name']} (Priority: {t['priority']})")