import streamlit as st
import pandas as pd
from io import BytesIO

from utils.helpers import format_indian_currency

from utils.calculations import (
    calculate_allocated_revenue,
    calculate_enrollments_needed,
    calculate_required_leads
)

from utils.charts import (
    create_monthly_leads_chart,
    create_monthly_enrollments_chart,
    create_revenue_distribution_chart
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="EdTech Revenue Planner",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
}

div[data-baseweb="tag"] {
    background-color: #E8F0FE !important;
    color: black !important;
    border-radius: 8px !important;
}

div[data-baseweb="select"] {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD COURSE MASTER DATA
# ---------------------------------------------------

course_df = pd.read_csv("data/course_master.csv")

courses = course_df["Course Name"].tolist()

# ---------------------------------------------------
# MONTH LIST
# ---------------------------------------------------

all_months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

# ---------------------------------------------------
# SLOT CONFIGURATION
# ---------------------------------------------------

slots_per_month = 4

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Revenue Planning Controls")

# ---------------------------------------------------
# MONTH SELECTION
# ---------------------------------------------------

selected_months = st.sidebar.multiselect(
    "Select Planning Months",
    options=all_months,
    default=["January", "February", "March"],
    help="Select the months you want to plan for"
)

# ---------------------------------------------------
# VALIDATION
# ---------------------------------------------------

if len(selected_months) == 0:

    st.warning("Please select at least one month.")

    st.stop()

# ---------------------------------------------------
# TARGET MODE
# ---------------------------------------------------

target_mode = st.sidebar.radio(
    "Target Distribution Mode",
    [
        "Auto Distribution",
        "Manual Monthly Targets"
    ]
)

# ---------------------------------------------------
# MONTHLY TARGET STORAGE
# ---------------------------------------------------

monthly_targets = {}

# ---------------------------------------------------
# AUTO DISTRIBUTION MODE
# ---------------------------------------------------

if target_mode == "Auto Distribution":

    yearly_target = st.sidebar.number_input(
        "Enter Yearly Revenue Target (₹)",
        min_value=100000,
        value=50000000,
        step=100000
    )

    auto_monthly_target = yearly_target / len(selected_months)

    for month in selected_months:

        monthly_targets[month] = auto_monthly_target

# ---------------------------------------------------
# MANUAL TARGET MODE
# ---------------------------------------------------

else:

    st.sidebar.divider()

    st.sidebar.subheader("Monthly Target Inputs")

    calculated_yearly_target = 0

    for month in selected_months:

        month_target = st.sidebar.number_input(
            f"{month} Target (₹)",
            min_value=0,
            value=5000000,
            step=100000,
            key=f"{month}_target"
        )

        monthly_targets[month] = month_target

        calculated_yearly_target += month_target

    yearly_target = calculated_yearly_target

# ---------------------------------------------------
# MAIN TITLE
# ---------------------------------------------------

st.title("EdTech Revenue Planning System")

st.subheader("Strategic Course Planning & Lead Forecasting")

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:

    st.metric(
        label="Yearly Revenue Target",
        value=format_indian_currency(yearly_target)
    )

with kpi2:

    st.metric(
        label="Selected Months",
        value=len(selected_months)
    )

with kpi3:

    st.metric(
        label="Conversion Rate",
        value="5%"
    )

with kpi4:

    st.metric(
        label="Target Mode",
        value=target_mode
    )

# ---------------------------------------------------
# STORAGE OBJECTS
# ---------------------------------------------------

planning_data = {}

grand_total_enrollments = 0
grand_total_leads = 0

monthly_leads_data = {}
monthly_enrollments_data = {}

# ---------------------------------------------------
# MONTH LOOP
# ---------------------------------------------------

for month in selected_months:

    planning_data[month] = {}

    month_total_enrollments = 0
    month_total_leads = 0

    monthly_target = monthly_targets[month]

    with st.expander(f"{month} Planning", expanded=False):

        st.write(
            f"Monthly Revenue Target: "
            f"{format_indian_currency(monthly_target)}"
        )

        month_columns = st.columns(slots_per_month)

        default_shares = [40, 30, 20, 10]

        for slot_index in range(slots_per_month):

            with month_columns[slot_index]:

                slot_number = slot_index + 1

                st.markdown(f"### Slot {slot_number}")

                selected_course = st.selectbox(
                    "Select Course",
                    courses,
                    key=f"{month}_slot_{slot_number}_course"
                )

                course_price = st.number_input(
                    "Course Price (₹)",
                    min_value=1000,
                    value=50000,
                    step=1000,
                    key=f"{month}_slot_{slot_number}_price"
                )

                revenue_share = st.slider(
                    "Revenue Share %",
                    min_value=0,
                    max_value=100,
                    value=default_shares[slot_index],
                    step=1,
                    key=f"{month}_slot_{slot_number}_share"
                )

                allocated_revenue = calculate_allocated_revenue(
                    monthly_target,
                    revenue_share / 100
                )

                enrollments_needed = calculate_enrollments_needed(
                    allocated_revenue,
                    course_price
                )

                required_leads = calculate_required_leads(
                    enrollments_needed
                )

                planning_data[month][f"Slot {slot_number}"] = {
                    "course": selected_course,
                    "price": course_price,
                    "share": revenue_share,
                    "allocated_revenue": allocated_revenue,
                    "enrollments": enrollments_needed,
                    "leads": required_leads
                }

                st.divider()

                st.write("Revenue Allocation")

                st.success(
                    format_indian_currency(allocated_revenue)
                )

                st.write("Enrollments Needed")

                st.info(
                    f"{enrollments_needed:.0f}"
                )

                st.write("Required Leads")

                st.warning(
                    f"{required_leads:.0f}"
                )

                month_total_enrollments += enrollments_needed
                month_total_leads += required_leads

        month_total_share = sum([
            planning_data[month][f"Slot {i+1}"]["share"]
            for i in range(slots_per_month)
        ])

        st.divider()

        if month_total_share != 100:

            st.error(
                f"Revenue Share Total = "
                f"{month_total_share}% "
                f"(Must equal 100%)"
            )

        else:

            st.success(
                "Revenue Allocation Valid"
            )

        sum1, sum2 = st.columns(2)

        with sum1:

            st.metric(
                "Total Enrollments Needed",
                f"{month_total_enrollments:.0f}"
            )

        with sum2:

            st.metric(
                "Total Leads Needed",
                f"{month_total_leads:.0f}"
            )

    grand_total_enrollments += month_total_enrollments
    grand_total_leads += month_total_leads

    monthly_leads_data[month] = month_total_leads
    monthly_enrollments_data[month] = month_total_enrollments

# ---------------------------------------------------
# FINAL SUMMARY
# ---------------------------------------------------

st.divider()

st.header("Overall Operational Requirements")

final1, final2 = st.columns(2)

with final1:

    st.metric(
        "Total Enrollments Needed",
        f"{grand_total_enrollments:.0f}"
    )

with final2:

    st.metric(
        "Total Leads Needed",
        f"{grand_total_leads:.0f}"
    )

# ---------------------------------------------------
# ANALYTICS DASHBOARD
# ---------------------------------------------------

st.divider()

st.header("Analytics Dashboard")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    leads_chart = create_monthly_leads_chart(
        monthly_leads_data
    )

    st.plotly_chart(
        leads_chart,
        use_container_width=True
    )

with chart_col2:

    enrollments_chart = create_monthly_enrollments_chart(
        monthly_enrollments_data
    )

    st.plotly_chart(
        enrollments_chart,
        use_container_width=True
    )

revenue_chart = create_revenue_distribution_chart(
    planning_data
)

st.plotly_chart(
    revenue_chart,
    use_container_width=True
)

# ---------------------------------------------------
# EXPORT DATAFRAME
# ---------------------------------------------------

export_rows = []

for month in planning_data:

    for slot in planning_data[month]:

        slot_data = planning_data[month][slot]

        export_rows.append({

            "Month": month,

            "Slot": slot,

            "Course": slot_data["course"],

            "Course Price": slot_data["price"],

            "Revenue Share %": slot_data["share"],

            "Revenue Allocation": slot_data["allocated_revenue"],

            "Enrollments Needed": slot_data["enrollments"],

            "Required Leads": slot_data["leads"]
        })

export_df = pd.DataFrame(export_rows)

# ---------------------------------------------------
# EXCEL EXPORT FUNCTION
# ---------------------------------------------------

def generate_excel_download(dataframe):

    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:

        dataframe.to_excel(
            writer,
            index=False,
            sheet_name='Planning Report'
        )

    processed_data = output.getvalue()

    return processed_data

excel_data = generate_excel_download(export_df)

# ---------------------------------------------------
# DOWNLOAD SECTION
# ---------------------------------------------------

st.divider()

st.header("Export Planning Report")

st.download_button(
    label="⬇ Download Excel Report",
    data=excel_data,
    file_name="edtech_revenue_planning_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)