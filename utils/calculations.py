# ---------------------------------------------------
# CALCULATE REVENUE SHARE
# ---------------------------------------------------

def calculate_revenue_share(price, total_price):

    if total_price == 0:
        return 0

    return price / total_price


# ---------------------------------------------------
# CALCULATE REVENUE ALLOCATION
# ---------------------------------------------------

def calculate_allocated_revenue(
        yearly_target,
        revenue_share
):

    return yearly_target * revenue_share


# ---------------------------------------------------
# CALCULATE ENROLLMENTS NEEDED
# ---------------------------------------------------

def calculate_enrollments_needed(
        allocated_revenue,
        course_price
):

    if course_price == 0:
        return 0

    return allocated_revenue / course_price


# ---------------------------------------------------
# CALCULATE REQUIRED LEADS
# ---------------------------------------------------

def calculate_required_leads(
        enrollments_needed,
        conversion_rate=0.05
):

    if conversion_rate == 0:
        return 0

    return enrollments_needed / conversion_rate