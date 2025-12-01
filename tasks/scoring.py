from datetime import date

def calculate_task_score(task_data):
    """
    Calculates a priority score.
    Higher score = Higher priority.
    """
    score = 0
    today = date.today()

    # Handle date object/string
    due = task_data["due_date"]
    if isinstance(due, str):
        due = date.fromisoformat(due)

    days_until_due = (due - today).days

    # 1. Urgency
    if days_until_due < 0:
        score += 100  # Overdue
    elif days_until_due <= 3:
        score += 50   # Very urgent

    # 2. Importance
    score += (task_data["importance"] * 5)

    # 3. Effort (quick wins)
    if task_data["estimated_hours"] < 2:
        score += 10

    # 4. Dependencies
    dep_count = len(task_data.get("dependencies", []))
    if dep_count > 0:
        score -= dep_count * 2  # Slight penalty

    return score
