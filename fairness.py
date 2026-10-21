"""
Steady Step - fairness check
============================
Compares each group's flag rate with the overall flag rate.
  - gap more than 10 percentage points  -> "Review"
  - fewer than 30 learners in the group -> "Too small to judge"
Protected attributes are only used HERE, never in the flag rule (rules.py).

If a group needs review, the team would: find which indicator causes the gap,
adjust that indicator's threshold or wording, re-run, and record the change.
"""

FAIRNESS_FIELDS = ["gender_group", "age_group", "area_deprivation_band",
                   "accessibility_support_flag", "learner_region"]
GAP_LIMIT = 10        # percentage points
MIN_GROUP = 30        # learners


def flag_rates(results, learners, field):
    df = results[["learner_id", "flagged"]].merge(learners[["learner_id", field]], on="learner_id")
    overall = df.flagged.mean() * 100

    table = df.groupby(field).agg(learners=("flagged", "size"), flagged=("flagged", "sum")).reset_index()
    table["flag_rate_%"] = (table.flagged / table.learners * 100).round(1)
    table["gap_vs_overall"] = (table["flag_rate_%"] - overall).round(1)
    table["result"] = "OK"
    table.loc[table.gap_vs_overall.abs() > GAP_LIMIT, "result"] = "Review"
    table.loc[table.learners < MIN_GROUP, "result"] = "Too small to judge"
    return table, round(overall, 1)
