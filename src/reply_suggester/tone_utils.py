def detect_tone(user_id):
    return "IC" if user_id.startswith("U1") else "Leader"
