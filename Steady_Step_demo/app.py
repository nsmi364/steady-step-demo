"""
Steady Step - demo artefact (Streamlit)
INFOMGMT 399 Group 2 (The Big 4) - Proposal 2: Student Dropout Risk

Flow:  synthetic CSVs -> rules.py (day-21 indicators -> status + reasons)
       Student:  Overview · Weekly check-in · My progress · Find support (booking)
       Adviser:  Learners to check in with · Fairness check · How it works
Run:   streamlit run app.py
"""

from datetime import date, timedelta

import altair as alt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import rules
import ui
from booking import ADVISERS, TIME_SLOTS, make_booking
from fairness import FAIRNESS_FIELDS, flag_rates

st.set_page_config(page_title="Steady Step", page_icon="🌱", layout="wide", initial_sidebar_state="expanded")
ui.inject_css()

# Always open the sidebar when the page first loads (Streamlit otherwise remembers it was closed)
components.html("""<script>
const doc = window.parent.document;
if (!window.parent.__ssSidebarOpened) {
  window.parent.__ssSidebarOpened = true;
  setTimeout(() => {
    const btn = doc.querySelector('[data-testid="stExpandSidebarButton"] button, [data-testid="stExpandSidebarButton"]');
    if (btn && btn.offsetParent !== null) btn.click();
  }, 400);
}
</script>""", height=0)


# ---------------- DATA (input) ----------------
@st.cache_data
def get_data():
    data = rules.load_data()
    return data, rules.build_checkpoint_features(data)


data, features = get_data()
results = rules.apply_rules(features)                 # default rule: bottom 25%, 2+ indicators

for key, default in {"bookings": [], "decisions": {}, "checkins": [], "spage": "Overview",
                     "ci_step": 0, "ci_answers": {}, "ci_result": None, "just_booked": None}.items():
    st.session_state.setdefault(key, default)


def go(page):
    """Button callback: jump to another sidebar page."""
    st.session_state.spage = page


STUDENT_PAGES = {"Overview": ":material/grid_view:", "Weekly check-in": ":material/check_circle:",
                 "My progress": ":material/monitoring:", "Find support": ":material/calendar_month:"}
ADVISER_PAGES = {"Learners to check in with": ":material/group:", "Fairness check": ":material/balance:",
                 "How it works": ":material/account_tree:"}

# ---------------- SIDE MENU ----------------
ui.sidebar_logo()
nav = st.sidebar.container(key="nav")
with nav:
    if st.session_state.get("view", "Student") == "Student":
        ui.side_label("YOUR SPACE", st)
        page = st.radio("Menu", list(STUDENT_PAGES), key="spage", label_visibility="collapsed",
                        format_func=lambda p: f"{STUDENT_PAGES[p]}  {p}")
    else:
        ui.side_label("ADVISER TOOLS", st)
        page = st.radio("Menu", list(ADVISER_PAGES), key="apage", label_visibility="collapsed",
                        format_func=lambda p: f"{ADVISER_PAGES[p]}  {p}")
ui.side_card()
st.sidebar.write("")
ui.side_label("SIGNED IN AS (TEST ACCOUNT)")
view = st.sidebar.radio("View", ["Student", "Adviser"], key="view", horizontal=True, label_visibility="collapsed")
if view == "Student":
    learner_id = st.sidebar.selectbox("Learner", features.learner_id, label_visibility="collapsed")
st.sidebar.caption("Checkpoint: end of Week 3 (day 21) · synthetic data")


# =====================================================================
# STUDENT PAGES
# =====================================================================
def top_bar(label):
    left, right = st.columns([5, 1])
    with left:
        ui.crumb(f"{label} &nbsp;/&nbsp; 2026S2")
    with right:
        st.button("＋ Check in", type="primary", on_click=go, args=("Weekly check-in",), key=f"top_{page}")


if view == "Student":
    me = results[results.learner_id == learner_id].iloc[0]            # own record only
    my_checkins = [c for c in st.session_state.checkins if c["learner_id"] == learner_id]
    my_bookings = [b for b in st.session_state.bookings if b["learner_id"] == learner_id]
    top_bar("STUDENT DASHBOARD")

    # ------------------------------------------------------------ Overview
    if page == "Overview":
        green = {"On track": "You're doing more right than you think.",
                 "Worth keeping an eye on": "You're closer than you think.",
                 "Suggested check-in": "Let's find your footing together."}[me.status]
        h, b = st.columns([3, 1.1])
        with h:
            ui.heading("", f"Hey, {learner_id}.", green,
                       f"Here's your steady view of {me.course_code}. No judgement, just useful next steps.")
        with b:
            st.write("")
            st.write("")
            st.button("✓ Do this week's check-in ↗", type="primary", on_click=go, args=("Weekly check-in",),
                      use_container_width=True)

        c1, c2 = st.columns([1.35, 1])
        with c1:
            pct = min(100, round(100 * rules.CHECKPOINT_DAY / 84))
            ui.md(f'<div class="ss-dark"><div class="ss-bubble"><b>{len(my_checkins)}</b><small>CHECK-INS</small></div>'
                  f'<span class="ss-mono" style="color:#9DA1BC">YOUR MOMENTUM</span><br><br>'
                  f'<span class="ss-big">{me.active_days_to_day21}</span> <span>days active</span><br>'
                  f'<small style="color:#B9BCD0">on Canvas in your first three weeks</small>'
                  f'<div class="ss-bar"><div style="width:{pct}%"></div></div>'
                  f'<small style="color:#B9BCD0">Keep the rhythm going</small>'
                  f'<span class="ss-mono" style="float:right;color:#9DA1BC">CHECKPOINT · DAY 21</span></div>')
        with c2:
            msg = ui.STATUS[me.status][4]
            ui.md(f'<div class="ss-card"><span class="ss-mono">A QUICK READ</span>'
                  f'<span style="float:right">{ui.pill(me.status)}</span><br><br>'
                  f'{ui.ring(int(me.indicator_count), me.status)}'
                  f'<div style="font-size:1.15rem;font-weight:500">{me.status}</div>'
                  f'<div style="color:#6B6F80;font-size:.92rem">{msg}</div><div style="clear:both"></div></div>')
            st.button("Complete your weekly check-in ↗", on_click=go, args=("Weekly check-in",), key="qr")

        s1, s2, s3 = st.columns(3)
        s1.markdown(ui.stat("🖱️", "Canvas interactions (to day 21)", me.interactions_to_day21), unsafe_allow_html=True)
        s2.markdown(ui.stat("📝", "First quiz", me.first_quiz_status.capitalize(), "#FDEBDD"), unsafe_allow_html=True)
        s3.markdown(ui.stat("💗", "Next best action",
                            "Book a chat" if me.flagged else "Weekly check-in", "#FBE3EC"), unsafe_allow_html=True)

        g1, g2 = st.columns([1.35, 1])
        with g1:
            with st.container(border=True):
                ui.md('<div class="ss-eyebrow">Signal, not scorekeeping</div><div class="ss-h2">Your progress at a glance</div>')
                act = data["learning_activity"]
                act = act[(act.learner_id == learner_id) & act.activity_day.between(0, rules.CHECKPOINT_DAY)]
                weekly = (act.assign(week=act.activity_day // 7 + 1).groupby("week").interaction_count.sum()
                          .reindex([1, 2, 3], fill_value=0).reset_index())
                weekly["week"] = "Week " + weekly.week.astype(str)
                st.altair_chart(alt.Chart(weekly).mark_bar(color=ui.GREEN, cornerRadiusTopLeft=4,
                                                           cornerRadiusTopRight=4, size=46)
                                .encode(x=alt.X("week", title=None, axis=alt.Axis(labelAngle=0)), y=alt.Y("interaction_count", title="Canvas interactions"))
                                .properties(height=230), use_container_width=True)
        with g2:
            with st.container(border=True):
                ui.md('<div class="ss-eyebrow">A gentle look back</div><div class="ss-h2">Recent check-ins</div>')
                if my_checkins:
                    rows = "".join(f'<div class="ss-row"><div><b>{c["date"]:%d %b}</b><br><small>{c["result"]}</small></div>'
                                   f'<small>avg {c["average"]}/5</small></div>' for c in my_checkins[::-1][:4])
                    ui.md(rows)
                else:
                    st.caption("Your check-ins will show here.")
                if me.student_reasons:
                    ui.md('<div class="ss-eyebrow" style="margin-top:12px">What we noticed by Week 3</div>')
                    for r in me.student_reasons:
                        st.caption("• " + r)

        with st.container(border=True):
            a, b = st.columns([3, 1])
            with a:
                ui.md('<div class="ss-eyebrow">Support, when you want it</div>'
                      '<div class="ss-h2">You don\'t have to solve the whole semester today.</div>'
                      '<span class="ss-mono">Talk through a plan with someone who knows the terrain.</span>')
            with b:
                st.write("")
                st.button("Meet an advisor ↗", type="primary", on_click=go, args=("Find support",), key="meet")

    # ------------------------------------------------------- Weekly check-in
    elif page == "Weekly check-in":
        QUESTIONS = [
            ("01 · Classes", "How well did you keep up with classes?",
             ["Fell behind", "Missed a few", "Mostly there", "Kept up", "All in"]),
            ("02 · Feeling", "How are you feeling about your study?",
             ["Overwhelmed", "Stretched", "Okay", "Pretty good", "Great"]),
            ("03 · Confidence", "How confident are you about your grades?",
             ["Not confident", "A few worries", "Finding my feet", "Feeling good", "I know my stuff"]),
        ]
        step, answers = st.session_state.ci_step, st.session_state.ci_answers

        if st.session_state.ci_result:                                      # ----- result screen
            low = st.session_state.ci_result == "Seek support"
            _, mid, _ = st.columns([1, 2.2, 1])
            with mid, st.container(border=True):
                ui.md(f'<div style="text-align:center;padding:20px 0 6px">'
                      f'<div style="font-size:2.4rem">{"🤝" if low else "🌿"}</div>'
                      f'<div class="ss-eyebrow">Your weekly read</div>'
                      f'<div class="ss-title" style="font-size:2.4rem">'
                      f'{"You deserve some backup." if low else "You&#39;re finding your rhythm."}</div>'
                      f'<div class="ss-sub" style="margin:auto">'
                      f'{"You do not need to wait for things to get worse. A friendly chat can help you find your next step." if low else "That is a strong week. Keep choosing the next small thing - it is adding up."}'
                      f'</div></div>')
                b1, b2 = st.columns(2)
                b1.button("Find an advisor →" if low else "See my progress →", type="primary",
                          on_click=go, args=("Find support" if low else "My progress",), use_container_width=True)
                if b2.button("Done for now", use_container_width=True):
                    st.session_state.ci_result = None
                    st.rerun()
                st.caption("✓ Saved to your weekly list")
        else:                                                               # ----- questionnaire
            h, d = st.columns([4, 1])
            with h:
                ui.heading("Weekly reset · 2 min", "A quick check-in,", "just for you.",
                           "Three honest taps help turn a busy week into a clearer next step.")
            with d:
                dashes = "".join(f'<span style="background:{ui.GREEN if i < step else (ui.ORANGE if i == step else "#E5E0D5")}"></span>'
                                 for i in range(3))
                ui.md(f'<div class="ss-dashes" style="text-align:right;margin-top:70px">{dashes}</div>'
                      f'<div class="ss-mono" style="text-align:right">{step + 1} of 3</div>')

            q, side = st.columns([1.6, 1])
            with q, st.container(border=True):
                tag, question, labels = QUESTIONS[step]
                ui.md(f'<div class="ss-mono" style="color:{ui.GREEN}">{tag.upper()}</div>'
                      f'<div style="font-size:1.7rem;font-weight:500;margin-top:6px">{question}</div>'
                      f'<div style="color:#6B6F80">Not a prediction - just your current sense of things.</div><br>')
                for i, col in enumerate(st.columns(5)):
                    with col.container(key=f"opt{step}_{i}"):
                        chosen = answers.get(step) == i + 1
                        if st.button(f"{'✓ ' if chosen else ''}{i + 1}\n\n{labels[i]}", key=f"q{step}_{i}",
                                     type="primary" if chosen else "secondary", use_container_width=True):
                            answers[step] = i + 1
                            st.rerun()
                back, _, nxt = st.columns([1, 1, 1.6])
                if step > 0 and back.button("‹ Back"):
                    st.session_state.ci_step -= 1
                    st.rerun()
                last = step == 2
                if nxt.button("See my weekly read →" if last else "Next →", type="primary",
                              disabled=step not in answers, use_container_width=True):
                    if last:
                        avg = round(sum(answers.values()) / 3, 1)
                        result = "Seek support" if avg <= 2.5 else "Keep going"
                        st.session_state.checkins.append({
                            "learner_id": learner_id, "date": date.today(), "classes": answers[0],
                            "feeling": answers[1], "confidence": answers[2], "average": avg, "result": result,
                            "note": st.session_state.get("ci_note", "")})
                        st.session_state.ci_result, st.session_state.ci_step = result, 0
                        st.session_state.ci_answers = {}
                    else:
                        st.session_state.ci_step += 1
                    st.rerun()
            with side:
                ui.md('<div class="ss-dark"><div style="color:#F2884B;font-size:1.3rem">♡</div>'
                      '<div class="ss-quote">"The point is not to measure yourself. It\'s to notice yourself."</div>'
                      '<br><span class="ss-mono" style="color:#9DA1BC">- your future self</span></div>')
                with st.container(border=True):
                    st.markdown("**📝 Anything else on your mind?**")
                    st.text_area("note", key="ci_note", placeholder="Optional - a sentence is enough.",
                                 label_visibility="collapsed")
            st.caption("Self-reported and private to you. The weekly check-in is NOT used in the early-support flag.")

        ui.md('<div class="ss-eyebrow" style="margin-top:20px">Your rhythm</div><div class="ss-h2">Previous check-ins</div>')
        if my_checkins:
            for col, c in zip(st.columns(3), my_checkins[::-1][:3]):
                col.markdown(f'<div class="ss-card"><span class="ss-mono">Week of {c["date"]:%d %b}</span><br>'
                             f'<b style="font-size:1.1rem">{c["result"]}</b><br>'
                             f'<span class="ss-mono">average {c["average"]} / 5</span></div>', unsafe_allow_html=True)
        else:
            st.caption("No check-ins yet - your first one will show here.")

    # ----------------------------------------------------------- My progress
    elif page == "My progress":
        ui.heading("Your rhythm", "My progress,", "week by week.",
                   "Signal, not scorekeeping. This is what we can see up to the Week 3 checkpoint.")
        s1, s2, s3 = st.columns(3)
        s1.markdown(ui.stat("🖱️", "Canvas interactions", me.interactions_to_day21), unsafe_allow_html=True)
        s2.markdown(ui.stat("📆", "Active days (of 22)", me.active_days_to_day21, "#FDEBDD"), unsafe_allow_html=True)
        s3.markdown(ui.stat("🗂️", "Registered", "On time" if me.registration_day <= 0
                            else f"Day {int(me.registration_day)}", "#E8E6F8"), unsafe_allow_html=True)

        act = data["learning_activity"]
        act = act[(act.course_code == me.course_code) & act.activity_day.between(0, rules.CHECKPOINT_DAY)]
        act = act.assign(week="Week " + (act.activity_day // 7 + 1).astype(str))
        n_class = int((results.course_code == me.course_code).sum())
        mine = act[act.learner_id == learner_id].groupby("week").interaction_count.sum()
        cls = act.groupby("week").interaction_count.sum() / n_class
        chart = pd.DataFrame({"Me": mine, "Class average": cls.round(1)}).reindex(
            ["Week 1", "Week 2", "Week 3"]).fillna(0).reset_index(names="week").melt("week", var_name="who")
        with st.container(border=True):
            ui.md('<div class="ss-eyebrow">Signal, not scorekeeping</div><div class="ss-h2">Canvas activity vs your class</div>')
            st.altair_chart(alt.Chart(chart).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
                            .encode(x=alt.X("week", title=None, axis=alt.Axis(labelAngle=0)), xOffset="who",
                                    y=alt.Y("value", title="Interactions"),
                                    color=alt.Color("who", title=None, scale=alt.Scale(
                                        domain=["Me", "Class average"], range=[ui.GREEN, "#C9C3B6"])))
                            .properties(height=260), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1, st.container(border=True):
            ui.md('<div class="ss-eyebrow">What we noticed by Week 3</div>')
            if me.student_reasons:
                for r in me.student_reasons:
                    st.write("• " + r)
            else:
                st.write("Nothing to worry about - you're engaging well. 🎉")
        with c2, st.container(border=True):
            ui.md('<div class="ss-eyebrow">Your check-ins</div>')
            if my_checkins:
                ci = pd.DataFrame(my_checkins)
                st.dataframe(ci[["date", "classes", "feeling", "confidence", "average", "result"]],
                             hide_index=True, use_container_width=True)
            else:
                st.caption("No check-ins yet.")
                st.button("Do a check-in →", on_click=go, args=("Weekly check-in",))

    # ---------------------------------------------------------- Find support
    elif page == "Find support":

        @st.dialog("Book a conversation")
        def booking_dialog(adviser):
            st.caption("Choose a time that suits you. Bring as much or as little as you like.")
            st.markdown(f"**{adviser}**  \n{ADVISERS[adviser].split(' - ')[0]}")
            c1, c2 = st.columns(2)
            day = c1.date_input("Date", value=date.today() + timedelta(days=1), min_value=date.today())
            time = c2.selectbox("Time", TIME_SLOTS)
            note = st.text_area("What would you like to talk about?", placeholder="e.g. Study and life balance")
            if st.button("Confirm booking", type="primary", use_container_width=True):
                ok, msg = make_booking(st.session_state.bookings, learner_id, adviser, day, time, note)
                if ok:
                    st.session_state.just_booked = adviser
                    st.rerun()
                st.error(msg)

        h, badge = st.columns([3.2, 1])
        with h:
            ui.heading("Find support · no wrong door", "People in your corner,", "when you need them.",
                       "A conversation can be practical, personal, or somewhere in between. You choose the topic.")
        with badge:
            ui.md('<div class="ss-card" style="margin-top:110px;text-align:center">'
                  f'<span class="ss-mono" style="color:{ui.GREEN}">STUDENT-FIRST</span><br><b>SUPPORT TEAM</b></div>')
        if st.session_state.just_booked:
            ui.md(f'<div class="ss-chip">✓ Booked with {st.session_state.just_booked}. '
                  f'(Simulated: a confirmation email would be sent.)</div>')
            st.session_state.just_booked = None

        ui.md(f'<div class="ss-eyebrow">Your calendar</div><div class="ss-h2">Upcoming conversations '
              f'<span class="ss-mono" style="float:right">{len(my_bookings)} BOOKED</span></div>')
        if not my_bookings:
            st.caption("No conversations booked yet.")
        for i, bk in enumerate(sorted(my_bookings, key=lambda x: (x["date"], x["time"]))):
            with st.container(border=True):
                a, b, c = st.columns([6, 1.2, 0.6])
                a.markdown(f'<div class="ss-date"><b>{bk["date"].day}</b><small>{bk["date"]:%b}</small></div>'
                           f'<b>{bk["note"] or "A conversation"}</b><br>'
                           f'<span class="ss-mono">📅 {bk["date"]:%d %b %Y} · 🕒 {bk["time"]} · with {bk["adviser"]}</span>',
                           unsafe_allow_html=True)
                b.markdown('<br><span class="ss-pill" style="background:#E3F4EC;color:#1F7A5C">Confirmed</span>',
                           unsafe_allow_html=True)
                if c.button("🗑", key=f"del{i}", help="Cancel"):
                    st.session_state.bookings.remove(bk)
                    st.rerun()

        ui.md('<div class="ss-eyebrow" style="margin-top:18px">Meet the team</div><div class="ss-h2">Who can help?</div>')
        colours = ["#F2884B", "#E58BE0", "#F1EEE6"]
        openings = ["Today, 3:30 PM", "Tomorrow, 10:00 AM", "Thu, 1:00 PM"]
        for col, (name, role), colour, opening in zip(st.columns(3), ADVISERS.items(), colours, openings):
            with col, st.container(border=True):
                title, focus = role.split(" - ")
                st.markdown(f'<div class="ss-avatar" style="background:{colour}">{ui.initials(name)}</div>'
                            f'<div style="font-size:1.2rem">{name}</div><div style="color:#6B6F80;font-size:.9rem">{title}</div>'
                            f'<div style="color:#6B6F80;font-size:.85rem;margin:6px 0">{focus}</div>'
                            f'<div class="ss-mono"><span style="color:{ui.GREEN}">●</span> Next opening <b>{opening}</b></div>',
                            unsafe_allow_html=True)
                if st.button("＋ Book a conversation", key=f"book_{name}", use_container_width=True):
                    booking_dialog(name)
                st.caption("✉️ Replies within 2 working days")


# =====================================================================
# ADVISER PAGES
# =====================================================================
else:
    ui.crumb("ADVISER DASHBOARD &nbsp;/&nbsp; 2026S2")

    if page == "Learners to check in with":
        ui.heading("End of Week 3 · day 21", "Learners to", "check in with.",
                   "Suggestions only, each with a plain reason. You decide what happens next.")
        c1, c2 = st.columns(2)
        pct = c1.slider("Low activity = bottom X% of course", 10, 50, 25, 5)
        min_ind = c2.slider("Flag when at least N indicators are true", 1, 3, 2)
        results = rules.apply_rules(features, activity_percentile=pct, min_indicators=min_ind)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Learners", len(results))
        m2.metric("Suggested check-in", int(results.flagged.sum()))
        m3.metric("Keep an eye on", int((results.status == "Worth keeping an eye on").sum()))
        m4.metric("Flag rate", f"{100 * results.flagged.mean():.1f}%")

        with st.container(border=True):
            ui.md('<div class="ss-eyebrow">Suggested check-ins</div>')
            flagged = results[results.flagged].copy()
            flagged["decision"] = flagged.learner_id.map(st.session_state.decisions).fillna("Not reviewed")
            edited = st.data_editor(
                flagged[["learner_id", "course_code", "indicator_count", "reasons", "decision"]],
                column_config={
                    "learner_id": "Learner", "course_code": "Course", "indicator_count": "Indicators",
                    "reasons": st.column_config.TextColumn("Reason", width="large"),
                    "decision": st.column_config.SelectboxColumn(
                        "Your decision", options=["Not reviewed", "Contact learner", "Monitor", "No action"])},
                disabled=["learner_id", "course_code", "indicator_count", "reasons"],
                hide_index=True, use_container_width=True, key="editor")
            st.session_state.decisions.update(dict(zip(edited.learner_id, edited.decision)))
            done = sum(v != "Not reviewed" for v in st.session_state.decisions.values())
            st.caption(f"Reviewed {done} of {len(flagged)} suggestions")

        with st.container(border=True):
            ui.md('<div class="ss-eyebrow">Learner detail</div>')
            pick = st.selectbox("Choose a learner", results.learner_id)
            row = results[results.learner_id == pick].iloc[0]
            ui.md(f'<b style="font-size:1.2rem">{pick}</b> · {row.course_code} &nbsp; {ui.pill(row.status)}')
            st.table(pd.DataFrame({
                "Indicator": ["Low Canvas activity", "First quiz late / missing", "Late registration"],
                "Value": [f"{row.interactions_to_day21} interactions (percentile {row.activity_percentile})",
                          row.first_quiz_status, f"day {int(row.registration_day)}"],
                "Triggered": ["Yes" if row.low_activity else "No", "Yes" if row.first_quiz_issue else "No",
                              "Yes" if row.late_registration else "No"]}).set_index("Indicator"))
            bks = [b for b in st.session_state.bookings if b["learner_id"] == pick]
            st.caption(f"Booked conversations: {len(bks)}")

    elif page == "Fairness check":
        ui.heading("Light subgroup check", "Is the flag", "fair across groups?",
                   "Flag rate for each group compared with the overall rate. "
                   "Protected attributes are used here only - never in the flag rule.")
        field = st.selectbox("Compare by", FAIRNESS_FIELDS)
        table, overall = flag_rates(results, data["learners"], field)
        with st.container(border=True):
            st.metric("Overall flag rate", f"{overall}%")
            bars = alt.Chart(table).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, size=50).encode(
                x=alt.X(field, title=None, axis=alt.Axis(labelAngle=0)), y=alt.Y("flag_rate_%", title="Flag rate (%)"),
                color=alt.Color("result", scale=alt.Scale(domain=["OK", "Review", "Too small to judge"],
                                                          range=[ui.GREEN, "#E06666", "#C9C3B6"])))
            rule = alt.Chart(pd.DataFrame({"y": [overall]})).mark_rule(strokeDash=[4, 4]).encode(y="y")
            st.altair_chart((bars + rule).properties(height=280), use_container_width=True)
            st.dataframe(table, hide_index=True, use_container_width=True)
            st.caption("Review = more than 10 points from overall (dashed line). Too small = fewer than 30 learners.")
        if (table.result == "Review").any():
            st.warning("A group needs review. Team response: find which indicator causes the gap, adjust its "
                       "threshold or wording, re-run, and record the change.")

    elif page == "How it works":
        ui.heading("Input → processing → output", "How it", "works.",
                   "Rule-based and explainable: every flag comes with its reasons.")
        with st.container(border=True):
            st.graphviz_chart("""
digraph {
  rankdir=LR; bgcolor="transparent"; node [shape=box style="rounded,filled" fillcolor="#FFFDF9" color="#2F9E7B" fontname="Helvetica"];
  edge [color="#252A47" fontname="Helvetica" fontsize=10];
  csv  [label="Synthetic CSVs\\n(generate_data.py)" fillcolor="#FFF4D6"];
  feat [label="build_checkpoint_features\\nkeep data <= day 21"];
  rule [label="apply_rules\\n3 indicators -> status + reason"];
  fair [label="fairness.py\\nflag rate by group"];
  stu  [label="Student pages" fillcolor="#E3F4EC"];
  adv  [label="Adviser pages\\n(adviser decides)" fillcolor="#E3F4EC"];
  book [label="make_booking\\n-> confirmation" fillcolor="#FDEBDD"];
  csv -> feat -> rule;
  rule -> stu [label="status + reasons"];
  rule -> adv [label="flags + reasons"];
  rule -> fair -> adv;
  stu -> book;
}""")
        c1, c2 = st.columns(2)
        with c1, st.container(border=True):
            ui.md('<div class="ss-eyebrow">The rule</div>')
            st.write("Flag for a check-in when **2 or more** are true by **day 21**:\n"
                     "1. Low Canvas activity - bottom 25% of the course\n"
                     "2. First quiz late or not submitted\n"
                     "3. Registered after the course started (day 0)")
            st.caption("Never used in the flag: final outcome, data after day 21, gender, age, deprivation, "
                       "accessibility, and the weekly check-in.")
        with c2, st.container(border=True):
            ui.md('<div class="ss-eyebrow">Build status</div>')
            st.table(pd.DataFrame({
                "Feature": ["Synthetic dataset, day-21 rule, reasons", "Adviser list, decisions, fairness",
                            "Student pages, check-in, booking", "Login", "Email / saved storage", "Real Canvas data"],
                "Status": ["Working", "Working", "Working", "Simulated (test accounts)",
                           "Simulated (resets on restart)", "Planned"]}).set_index("Feature"))
