# --- powerdash_components.py ---
# Chart generators for post-call analytics
# Called from inside analysis_notebook.ipynb
# Uses Altair for clean, readable dashboards

import altair as alt
import pandas as pd

# helper to chart sentiment over time
def sentiment_trend_chart(df: pd.DataFrame) -> alt.Chart:
    # assumes df has 'call_id', 'utterance_index', 'sentiment' columns
    return (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(
            x=alt.X("utterance_index:Q", title="Utterance #"),
            y=alt.Y("sentiment_score:Q", title="Sentiment Score (-1 to +1)"),
            color=alt.Color("call_id:N", title="Call ID"),
            tooltip=["call_id", "utterance_index", "sentiment", "sentiment_score"]
        )
        .properties(title="Sentiment Progression per Call", height=300)
    )

# helper to chart issue category distribution
def issue_category_pie(df: pd.DataFrame) -> alt.Chart:
    # assumes df has 'issue_category' column with values like 'Billing', 'Cancel', etc.
    count_df = df["issue_category"].value_counts().reset_index()
    count_df.columns = ["issue_category", "count"]

    return (
        alt.Chart(count_df)
        .mark_arc(innerRadius=50)
        .encode(
            theta="count:Q",
            color="issue_category:N",
            tooltip=["issue_category", "count"]
        )
        .properties(title="Issue Category Distribution", height=300)
    )

# helper to chart escalation tactic usage
def resolution_tactic_bar(df: pd.DataFrame) -> alt.Chart:
    tactic_df = df["resolution_tactic"].value_counts().reset_index()
    tactic_df.columns = ["resolution_tactic", "count"]

    return (
        alt.Chart(tactic_df)
        .mark_bar()
        .encode(
            x=alt.X("count:Q", title="# of Calls"),
            y=alt.Y("resolution_tactic:N", sort="-x"),
            tooltip=["resolution_tactic", "count"]
        )
        .properties(title="Recommended Resolution Tactics Used", height=300)
    )

# optional: chart satisfaction by agent if present
def satisfaction_by_agent(df: pd.DataFrame) -> alt.Chart:
    if "agent_id" not in df.columns or "satisfaction" not in df.columns:
        return alt.Chart(pd.DataFrame(columns=["x", "y"])).mark_point()  # blank

    return (
        alt.Chart(df)
        .mark_boxplot()
        .encode(
            x="agent_id:N",
            y="satisfaction_score:Q",
            color="agent_id:N",
            tooltip=["agent_id", "satisfaction", "satisfaction_score"]
        )
        .properties(title="Customer Satisfaction by Agent", height=300)
    )
