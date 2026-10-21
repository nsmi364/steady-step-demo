"""
Steady Step - test scenarios for the demo video
Each test records: input, expected result, actual result, pass/fail.
They call the real functions in rules.py and booking.py.
"""

from datetime import date, timedelta

import pandas as pd

from booking import make_booking
from rules import apply_rules


def one_learner(percentile, quiz, reg_day):
    """A hand-made day-21 record for one fictional learner."""
    return pd.DataFrame([{"learner_id": "TEST01", "course_code": "INF200",
                          "interactions_to_day21": 0, "active_days_to_day21": 0,
                          "activity_percentile": percentile, "first_quiz_status": quiz,
                          "registration_day": reg_day}])


def t1_normal():
    r = apply_rules(one_learner(10, "not submitted", -5)).iloc[0]
    return {"id": "T1", "type": "Normal case",
            "input": "Activity percentile 10, first quiz not submitted, registered day -5",
            "expected": "Flagged, with 2 reasons (low activity + first quiz)",
            "actual": f"Flagged = {r.flagged}; reasons: {r.reasons}",
            "passed": bool(r.flagged and r.indicator_count == 2)}


def t2_boundary():
    r = apply_rules(one_learner(10, "on time", -5)).iloc[0]
    return {"id": "T2", "type": "Boundary case - only 1 indicator",
            "input": "Activity percentile 10, first quiz on time, registered day -5",
            "expected": "NOT flagged; status 'Worth keeping an eye on'",
            "actual": f"Flagged = {r.flagged}; status '{r.status}'",
            "passed": bool(not r.flagged and r.status == "Worth keeping an eye on")}


def t3_error_double_booking():
    bookings, day = [], date.today() + timedelta(days=2)
    ok1, _ = make_booking(bookings, "L0001", "Mia Chen", day, "10:00")
    ok2, msg2 = make_booking(bookings, "L0002", "Mia Chen", day, "10:00")
    return {"id": "T3", "type": "Error case - double booking",
            "input": "Two learners book Mia Chen for the same date at 10:00",
            "expected": "First booking confirmed; second rejected with a message",
            "actual": f"First ok = {ok1}; second ok = {ok2} ('{msg2}')",
            "passed": bool(ok1 and not ok2 and len(bookings) == 1)}


ALL_SCENARIOS = [t1_normal, t2_boundary, t3_error_double_booking]


def run_all():
    return pd.DataFrame([s() for s in ALL_SCENARIOS])
