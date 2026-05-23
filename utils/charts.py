import plotly.express as px
import pandas as pd


# ---------------------------------------------------
# PROFESSIONAL COLOR PALETTE
# ---------------------------------------------------

professional_colors = [
    "#1F77B4",
    "#FF7F0E",
    "#2CA02C",
    "#D62728",
    "#9467BD",
    "#8C564B",
    "#E377C2",
    "#7F7F7F",
    "#BCBD22",
    "#17BECF",
    "#003F5C",
    "#58508D",
    "#BC5090",
    "#FF6361",
    "#FFA600"
]


# ---------------------------------------------------
# FORMAT REVENUE LABELS
# ---------------------------------------------------

def format_revenue_short(value):

    if value >= 10000000:

        return f"₹ {value / 10000000:.2f} Cr"

    elif value >= 100000:

        return f"₹ {value / 100000:.2f} L"

    else:

        return f"₹ {value:,.0f}"


# ---------------------------------------------------
# MONTHLY LEADS CHART
# ---------------------------------------------------

def create_monthly_leads_chart(monthly_leads_data):

    df = pd.DataFrame({
        "Month": list(monthly_leads_data.keys()),
        "Leads": list(monthly_leads_data.values())
    })

    fig = px.bar(
        df,
        x="Month",
        y="Leads",
        title="Monthly Leads Requirement",
        text_auto=True,
        color="Month",
        color_discrete_sequence=professional_colors
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Required Leads",
        height=500,
        showlegend=False
    )

    return fig


# ---------------------------------------------------
# MONTHLY ENROLLMENTS CHART
# ---------------------------------------------------

def create_monthly_enrollments_chart(monthly_enrollments_data):

    df = pd.DataFrame({
        "Month": list(monthly_enrollments_data.keys()),
        "Enrollments": list(monthly_enrollments_data.values())
    })

    fig = px.line(
        df,
        x="Month",
        y="Enrollments",
        markers=True,
        title="Monthly Enrollment Requirement"
    )

    fig.update_traces(
        line=dict(color="#6A0DAD", width=4),
        marker=dict(size=10, color="#FF7F0E")
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Required Enrollments",
        height=500
    )

    return fig


# ---------------------------------------------------
# REVENUE DISTRIBUTION CHART
# ---------------------------------------------------

def create_revenue_distribution_chart(planning_data):

    labels = []
    revenues = []

    for month in planning_data:

        for slot in planning_data[month]:

            course = planning_data[month][slot]["course"]

            revenue = planning_data[month][slot]["allocated_revenue"]

            label = (
                f"{course} ({month})"
                f" - {format_revenue_short(revenue)}"
            )

            labels.append(label)

            revenues.append(revenue)

    df = pd.DataFrame({
        "Course Launch": labels,
        "Revenue": revenues
    })

    fig = px.pie(
        df,
        names="Course Launch",
        values="Revenue",
        title="Revenue Contribution by Course Launch",
        color_discrete_sequence=professional_colors
    )

    fig.update_layout(
        height=700
    )

    return fig