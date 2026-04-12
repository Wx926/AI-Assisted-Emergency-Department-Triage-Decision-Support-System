queue = []

def add_patient(patient, severity):
    patient["severity"] = severity

    if severity == "Critical":
        queue.insert(0, patient)
    elif severity == "Urgent":
        if len(queue) > 0:
            queue.insert(1, patient)
        else:
            queue.append(patient)
    else:
        queue.append(patient)

def show_queue():
    print("\n=== CURRENT QUEUE ===")
    for i, p in enumerate(queue):
        print(f"{i+1}. {p['symptoms']} - {p['severity']}")