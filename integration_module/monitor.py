from queue_manager import queue

def show_monitor():
    print("\n=== MONITOR DASHBOARD ===")
    print(f"Total patients: {len(queue)}")

    critical = sum(1 for p in queue if p["severity"] == "Critical")
    urgent = sum(1 for p in queue if p["severity"] == "Urgent")
    normal = sum(1 for p in queue if p["severity"] == "Normal")

    print(f"Critical: {critical}")
    print(f"Urgent: {urgent}")
    print(f"Normal: {normal}")