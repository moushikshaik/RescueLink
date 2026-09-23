import streamlit as st
import boto3
import requests
import json
import base64
import pandas as pd

from botocore.exceptions import ClientError


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RescueLink",
    page_icon="🍱",
    layout="wide"
)


# ============================================================
# CONFIGURATION
# ============================================================

AWS_REGION = "ap-south-2"

LOCATION_REGION = "ap-south-1"

COGNITO_USER_POOL_ID = "ap-south-2_mt0ZbL7A3"

COGNITO_CLIENT_ID = "1f547lkj8l8am7cna8hmglulbl"

API_BASE_URL = (
    "https://p71vlw2xf6.execute-api.ap-south-2.amazonaws.com"
)


# ============================================================
# AMAZON LOCATION API KEY
# ============================================================

try:

    LOCATION_API_KEY = st.secrets[
        "AWS_LOCATION_API_KEY"
    ]

except Exception:

    LOCATION_API_KEY = ""


# ============================================================
# COGNITO CLIENT
# ============================================================

cognito = boto3.client(
    "cognito-idp",
    region_name=AWS_REGION
)


# ============================================================
# SESSION STATE
# ============================================================

default_session_values = {

    "logged_in": False,

    "id_token": None,

    "access_token": None,

    "refresh_token": None,

    "user_role": None,

    "user_id": None,

    "user_email": None,

    "challenge_name": None,

    "challenge_session": None,

    "challenge_username": None
}


for key, value in default_session_values.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# JWT DECODER
# ============================================================

def decode_jwt_payload(token):

    try:

        if not token:

            return {}

        parts = token.split(".")

        if len(parts) != 3:

            return {}

        payload = parts[1]

        padding = "=" * (
            -len(payload) % 4
        )

        decoded = base64.urlsafe_b64decode(
            payload + padding
        )

        return json.loads(
            decoded.decode("utf-8")
        )

    except Exception:

        return {}


# ============================================================
# AUTH HEADERS
# ============================================================

def auth_headers():

    token = st.session_state.get(
        "id_token"
    )

    return {

        "Authorization":
            f"Bearer {token}",

        "Content-Type":
            "application/json"
    }


# ============================================================
# API GET
# ============================================================

def api_get(
    endpoint,
    authenticated=True
):

    try:

        if authenticated:

            headers = auth_headers()

        else:

            headers = {}

        return requests.get(

            f"{API_BASE_URL}{endpoint}",

            headers=headers,

            timeout=15
        )

    except requests.exceptions.RequestException as e:

        st.error(
            "❌ API connection failed."
        )

        st.code(
            str(e)
        )

        return None


# ============================================================
# API POST
# ============================================================

def api_post(
    endpoint,
    payload=None,
    authenticated=True
):

    try:

        if authenticated:

            headers = auth_headers()

        else:

            headers = {}

        return requests.post(

            f"{API_BASE_URL}{endpoint}",

            headers=headers,

            json=payload or {},

            timeout=15
        )

    except requests.exceptions.RequestException as e:

        st.error(
            "❌ API connection failed."
        )

        st.code(
            str(e)
        )

        return None


# ============================================================
# API PATCH
# ============================================================

def api_patch(
    endpoint,
    payload=None
):

    try:

        return requests.patch(

            f"{API_BASE_URL}{endpoint}",

            headers=auth_headers(),

            json=payload or {},

            timeout=15
        )

    except requests.exceptions.RequestException as e:

        st.error(
            "❌ API connection failed."
        )

        st.code(
            str(e)
        )

        return None


# ============================================================
# ADMIN REPORTS
# ============================================================

def get_admin_reports():

    response = api_get(
        "/admin/reports",
        authenticated=True
    )

    if response is None:

        return None

    print(
        "======================================"
    )

    print(
        "ADMIN REPORTS STATUS:",
        response.status_code
    )

    print(
        "ADMIN REPORTS RESPONSE:"
    )

    print(
        response.text
    )

    print(
        "======================================"
    )

    if response.status_code == 200:

        try:

            return response.json()

        except Exception as e:

            st.error(
                "❌ Could not parse Admin Reports response."
            )

            st.code(
                response.text
            )

            st.code(
                str(e)
            )

            return None

    elif response.status_code == 401:

        st.error(
            "🔐 Authentication failed."
        )

        st.code(
            response.text
        )

        return None

    elif response.status_code == 403:

        st.error(
            "🚫 ADMIN permission required."
        )

        st.code(
            response.text
        )

        return None

    else:

        st.error(
            f"❌ Admin Reports API error: "
            f"{response.status_code}"
        )

        st.code(
            response.text
        )

        return None


# ============================================================
# ADMIN DONATIONS
# ============================================================

def get_admin_donations():

    response = api_get(
        "/admin/donations"
    )

    if response is None:

        return []

    if response.status_code == 200:

        try:

            data = response.json()

            return data.get(
                "donations",
                []
            )

        except Exception as e:

            st.error(
                "❌ Invalid Admin Donations response."
            )

            st.code(
                str(e)
            )

            return []

    st.error(
        f"❌ Admin Donations error: "
        f"{response.status_code}"
    )

    st.code(
        response.text
    )

    return []


# ============================================================
# ADMIN USERS
# ============================================================

def get_admin_users():

    response = api_get(
        "/admin/users"
    )

    if response is None:

        return []

    if response.status_code == 200:

        try:

            data = response.json()

            return data.get(
                "users",
                []
            )

        except Exception as e:

            st.error(
                "❌ Invalid Admin Users response."
            )

            st.code(
                str(e)
            )

            return []

    st.error(
        f"❌ Admin Users error: "
        f"{response.status_code}"
    )

    st.code(
        response.text
    )

    return []


# ============================================================
# GET USER ROLE
# ============================================================

def get_user_role():

    existing_role = st.session_state.get(
        "user_role"
    )

    if existing_role:

        return existing_role

    response = api_get(
        "/dashboard"
    )

    if response is not None:

        if response.status_code == 200:

            try:

                data = response.json()

                role = data.get(
                    "role"
                )

                if role:

                    st.session_state[
                        "user_role"
                    ] = role

                    return role

            except Exception:

                pass

    return "UNKNOWN"


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state["logged_in"]:

    st.title(
        "🍱 RescueLink"
    )

    st.subheader(
        "Food Redistribution Platform"
    )

    st.write(
        "Connecting surplus food with communities. 🤝"
    )

    st.divider()

    st.subheader(
        "🔐 Login"
    )

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        if not email or not password:

            st.error(
                "Please enter email and password."
            )

        else:

            try:

                response = cognito.initiate_auth(

                    ClientId=COGNITO_CLIENT_ID,

                    AuthFlow="USER_PASSWORD_AUTH",

                    AuthParameters={

                        "USERNAME":
                            email,

                        "PASSWORD":
                            password
                    }
                )

                # ==========================================
                # NORMAL LOGIN
                # ==========================================

                if "AuthenticationResult" in response:

                    auth = response[
                        "AuthenticationResult"
                    ]

                    st.session_state[
                        "id_token"
                    ] = auth[
                        "IdToken"
                    ]

                    st.session_state[
                        "access_token"
                    ] = auth[
                        "AccessToken"
                    ]

                    st.session_state[
                        "refresh_token"
                    ] = auth.get(
                        "RefreshToken"
                    )

                    st.session_state[
                        "logged_in"
                    ] = True

                    st.session_state[
                        "user_email"
                    ] = email

                    payload = decode_jwt_payload(
                        auth["IdToken"]
                    )

                    st.session_state[
                        "user_id"
                    ] = payload.get(
                        "sub"
                    )

                    st.session_state[
                        "user_role"
                    ] = None

                    st.success(
                        "✅ Login successful!"
                    )

                    st.rerun()

                # ==========================================
                # NEW PASSWORD REQUIRED
                # ==========================================

                elif response.get(
                    "ChallengeName"
                ) == "NEW_PASSWORD_REQUIRED":

                    st.session_state[
                        "challenge_name"
                    ] = "NEW_PASSWORD_REQUIRED"

                    st.session_state[
                        "challenge_session"
                    ] = response.get(
                        "Session"
                    )

                    st.session_state[
                        "challenge_username"
                    ] = email

                    st.rerun()

            except ClientError as e:

                error = e.response.get(
                    "Error",
                    {}
                )

                st.error(
                    error.get(
                        "Message",
                        "Login failed."
                    )
                )

            except Exception as e:

                st.error(
                    "Unexpected login error."
                )

                st.code(
                    str(e)
                )


    # ========================================================
    # NEW PASSWORD
    # ========================================================

    if st.session_state[
        "challenge_name"
    ] == "NEW_PASSWORD_REQUIRED":

        st.divider()

        st.subheader(
            "🔑 Set New Password"
        )

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        name = st.text_input(
            "Name",
            value="Samo"
        )

        if st.button(
            "Set New Password",
            use_container_width=True
        ):

            if not new_password:

                st.error(
                    "Please enter a new password."
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                try:

                    response = (
                        cognito.respond_to_auth_challenge(

                            ClientId=
                                COGNITO_CLIENT_ID,

                            ChallengeName=
                                "NEW_PASSWORD_REQUIRED",

                            Session=
                                st.session_state[
                                    "challenge_session"
                                ],

                            ChallengeResponses={

                                "USERNAME":
                                    st.session_state[
                                        "challenge_username"
                                    ],

                                "NEW_PASSWORD":
                                    new_password,

                                "name":
                                    name
                            }
                        )
                    )

                    auth = response[
                        "AuthenticationResult"
                    ]

                    st.session_state[
                        "id_token"
                    ] = auth[
                        "IdToken"
                    ]

                    st.session_state[
                        "access_token"
                    ] = auth[
                        "AccessToken"
                    ]

                    st.session_state[
                        "refresh_token"
                    ] = auth.get(
                        "RefreshToken"
                    )

                    st.session_state[
                        "logged_in"
                    ] = True

                    st.session_state[
                        "user_email"
                    ] = st.session_state[
                        "challenge_username"
                    ]

                    payload = decode_jwt_payload(
                        auth["IdToken"]
                    )

                    st.session_state[
                        "user_id"
                    ] = payload.get(
                        "sub"
                    )

                    st.session_state[
                        "challenge_name"
                    ] = None

                    st.session_state[
                        "challenge_session"
                    ] = None

                    st.session_state[
                        "challenge_username"
                    ] = None

                    st.session_state[
                        "user_role"
                    ] = None

                    st.success(
                        "✅ Password changed successfully!"
                    )

                    st.rerun()

                except ClientError as e:

                    error = e.response.get(
                        "Error",
                        {}
                    )

                    st.error(
                        error.get(
                            "Message",
                            "Password change failed."
                        )
                    )

                except Exception as e:

                    st.error(
                        "Unexpected password change error."
                    )

                    st.code(
                        str(e)
                    )

    st.stop()


# ============================================================
# USER ROLE
# ============================================================

user_role = get_user_role()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "🍱 RescueLink"
)

st.sidebar.success(
    f"Role: {user_role}"
)

if st.session_state.get(
    "user_email"
):

    st.sidebar.caption(
        st.session_state[
            "user_email"
        ]
    )

st.sidebar.divider()

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    for key in default_session_values:

        st.session_state[
            key
        ] = default_session_values[key]

    st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

st.title(
    "🍱 RescueLink"
)

st.caption(
    "Food Redistribution Platform"
)


# ============================================================
# USER DASHBOARD
# ============================================================

if user_role != "ADMIN":

    response = api_get(
        "/dashboard"
    )

    if response is not None:

        if response.status_code == 200:

            dashboard = response.json()

            st.divider()

            st.subheader(
                "📊 Dashboard"
            )

            c1, c2, c3, c4 = st.columns(4)

            with c1:

                st.metric(
                    "Total Donations",
                    dashboard.get(
                        "totalDonations",
                        0
                    )
                )

            with c2:

                st.metric(
                    "Available",
                    dashboard.get(
                        "available",
                        dashboard.get(
                            "availableDonations",
                            0
                        )
                    )
                )

            with c3:

                st.metric(
                    "Completed",
                    dashboard.get(
                        "completed",
                        dashboard.get(
                            "completedDonations",
                            0
                        )
                    )
                )

            with c4:

                st.metric(
                    "Food Rescued",
                    dashboard.get(
                        "foodPortionsRescued",
                        0
                    )
                )


# ============================================================
# DONOR
# ============================================================

if user_role == "DONOR":

    st.divider()

    st.subheader(
        "🍱 Create a Donation"
    )

    with st.form(
        "create_donation"
    ):

        food_type = st.text_input(
            "Food Type",
            placeholder="Prepared Meals"
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            step=1
        )

        pickup_location = st.text_input(
            "Pickup Location",
            placeholder="Tirupati Central Market"
        )

        pickup_time = st.text_input(
            "Pickup Time",
            placeholder="2026-12-10T18:00:00Z"
        )

        description = st.text_area(
            "Description"
        )

        submit = st.form_submit_button(
            "Create Donation",
            use_container_width=True
        )

    if submit:

        payload = {

            "foodType":
                food_type,

            "quantity":
                quantity,

            "pickupLocation":
                pickup_location,

            "pickupTime":
                pickup_time,

            "description":
                description
        }

        response = api_post(
            "/donations",
            payload
        )

        if response is not None:

            if response.status_code in [
                200,
                201
            ]:

                st.success(
                    "🎉 Donation created successfully!"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Failed to create donation."
                )

                st.code(
                    response.text
                )


# ============================================================
# AVAILABLE DONATIONS
# ============================================================

st.divider()

st.subheader(
    "📦 Available Donations"
)

response = api_get(
    "/donations",
    authenticated=False
)

if response is not None:

    if response.status_code == 200:

        data = response.json()

        donations = data.get(
            "donations",
            []
        )

        if donations:

            st.write(
                f"**{len(donations)} "
                f"available donation(s)**"
            )

            for donation in donations:

                donation_id = donation.get(
                    "donationId"
                )

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### 🍱 "
                        f"{donation.get('foodType', '-')}"
                    )

                    c1, c2, c3 = st.columns(3)

                    with c1:

                        st.write(
                            f"**Quantity:** "
                            f"{donation.get('quantity', '-')}"
                        )

                    with c2:

                        st.write(
                            f"**Location:** "
                            f"{donation.get('pickupLocation', '-')}"
                        )

                    with c3:

                        st.write(
                            f"**Status:** "
                            f"{donation.get('status', '-')}"
                        )

                    st.write(
                        f"**Pickup:** "
                        f"{donation.get('pickupTime', '-')}"
                    )

                    if user_role == "RECEIVER":

                        if st.button(
                            "🤝 Claim Donation",
                            key=f"claim_{donation_id}",
                            use_container_width=True
                        ):

                            claim = api_post(
                                f"/donations/{donation_id}/claim"
                            )

                            if claim is not None:

                                if claim.status_code == 200:

                                    st.success(
                                        "✅ Donation claimed!"
                                    )

                                    st.rerun()

                                else:

                                    st.error(
                                        "❌ Unable to claim donation."
                                    )

                                    st.code(
                                        claim.text
                                    )

        else:

            st.info(
                "No available donations."
            )


# ============================================================
# MY DONATIONS
# ============================================================

if user_role in [
    "DONOR",
    "RECEIVER"
]:

    st.divider()

    st.subheader(
        "🤝 My Donations"
    )

    response = api_get(
        "/my-donations"
    )

    if response is not None:

        if response.status_code == 200:

            data = response.json()

            my_donations = data.get(
                "donations",
                []
            )

            if my_donations:

                for donation in my_donations:

                    donation_id = donation.get(
                        "donationId"
                    )

                    status = donation.get(
                        "status"
                    )

                    with st.container(
                        border=True
                    ):

                        st.markdown(
                            f"### 🍱 "
                            f"{donation.get('foodType', '-')}"
                        )

                        st.write(
                            f"**Quantity:** "
                            f"{donation.get('quantity', '-')}"
                        )

                        st.write(
                            f"**Location:** "
                            f"{donation.get('pickupLocation', '-')}"
                        )

                        st.write(
                            f"**Status:** "
                            f"{status}"
                        )

                        # ==================================
                        # PICKED UP
                        # ==================================

                        if (
                            user_role == "RECEIVER"
                            and status == "CLAIMED"
                        ):

                            if st.button(
                                "🚚 Mark as Picked Up",
                                key=f"pickup_{donation_id}",
                                use_container_width=True
                            ):

                                result = api_patch(

                                    f"/donations/"
                                    f"{donation_id}/status",

                                    {
                                        "status":
                                            "PICKED_UP"
                                    }
                                )

                                if result is not None:

                                    if result.status_code == 200:

                                        st.success(
                                            "✅ Marked as picked up!"
                                        )

                                        st.rerun()

                                    else:

                                        st.error(
                                            "❌ Unable to update status."
                                        )

                                        st.code(
                                            result.text
                                        )

                        # ==================================
                        # COMPLETED
                        # ==================================

                        if (
                            user_role == "RECEIVER"
                            and status == "PICKED_UP"
                        ):

                            if st.button(
                                "✅ Mark as Completed",
                                key=f"complete_{donation_id}",
                                use_container_width=True
                            ):

                                result = api_patch(

                                    f"/donations/"
                                    f"{donation_id}/status",

                                    {
                                        "status":
                                            "COMPLETED"
                                    }
                                )

                                if result is not None:

                                    if result.status_code == 200:

                                        st.success(
                                            "🎉 Donation completed!"
                                        )

                                        st.rerun()

                                    else:

                                        st.error(
                                            "❌ Unable to update status."
                                        )

                                        st.code(
                                            result.text
                                        )

            else:

                st.info(
                    "No donations found."
                )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

if user_role == "ADMIN":

    st.divider()

    st.header(
        "🛠️ Admin Dashboard"
    )

    # ========================================================
    # REPORTS
    # ========================================================

    st.subheader(
        "📊 Reports & Statistics"
    )

    reports = get_admin_reports()

    # ========================================================
    # DEBUG RESPONSE
    # ========================================================

    with st.expander(
        "🔧 Debug: Admin Reports API Response"
    ):

        if reports is not None:

            st.json(
                reports
            )

        else:

            st.error(
                "No report data returned."
            )

    # ========================================================
    # ADMIN REPORT DATA
    # ========================================================

    if reports:

        # IMPORTANT:
        #
        # API returns:
        #
        # {
        #     "summary": {
        #         "totalDonations": 26,
        #         "available": 2,
        #         "claimed": 5,
        #         ...
        #     },
        #
        #     "statusBreakdown": {...},
        #
        #     "foodTypeBreakdown": {...}
        # }
        #
        # Therefore summary MUST be extracted.

        summary = reports.get(
            "summary",
            {}
        )

        # ====================================================
        # SUMMARY VALUES
        # ====================================================

        total_donations = summary.get(
            "totalDonations",
            0
        )

        available = summary.get(
            "available",
            0
        )

        claimed = summary.get(
            "claimed",
            0
        )

        picked_up = summary.get(
            "pickedUp",
            0
        )

        completed = summary.get(
            "completed",
            0
        )

        expired = summary.get(
            "expired",
            0
        )

        cancelled = summary.get(
            "cancelled",
            0
        )

        total_food = summary.get(
            "totalFoodPortions",
            0
        )

        completed_food = summary.get(
            "completedFoodPortions",
            0
        )

        completion_rate = summary.get(
            "completionRate",
            0
        )

        active_donors = summary.get(
            "activeDonors",
            0
        )

        active_receivers = summary.get(
            "activeReceivers",
            0
        )

        # ====================================================
        # MAIN SUMMARY CARDS
        # ====================================================

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Total Donations",
                total_donations
            )

        with c2:

            st.metric(
                "Completed",
                completed
            )

        with c3:

            st.metric(
                "Food Rescued",
                total_food
            )

        with c4:

            st.metric(
                "Completion Rate",
                f"{completion_rate}%"
            )

        # ====================================================
        # STATUS CARDS
        # ====================================================

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Available",
                available
            )

        with c2:

            st.metric(
                "Claimed",
                claimed
            )

        with c3:

            st.metric(
                "Picked Up",
                picked_up
            )

        with c4:

            st.metric(
                "Expired",
                expired
            )

        # ====================================================
        # ADDITIONAL CARDS
        # ====================================================

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Cancelled",
                cancelled
            )

        with c2:

            st.metric(
                "Completed Food",
                completed_food
            )

        with c3:

            st.metric(
                "Donors",
                active_donors
            )

        with c4:

            st.metric(
                "Receivers",
                active_receivers
            )

        # ====================================================
        # STATUS BREAKDOWN
        # ====================================================

        st.subheader(
            "📊 Status Breakdown"
        )

        status_breakdown = reports.get(
            "statusBreakdown",
            {}
        )

        if status_breakdown:

            status_df = pd.DataFrame(
                {
                    "Status":
                        list(
                            status_breakdown.keys()
                        ),

                    "Count":
                        list(
                            status_breakdown.values()
                        )
                }
            )

            st.bar_chart(
                status_df.set_index(
                    "Status"
                )
            )

            st.dataframe(
                status_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No status breakdown available."
            )

        # ====================================================
        # FOOD TYPE BREAKDOWN
        # ====================================================

        st.subheader(
            "🍱 Food Type Breakdown"
        )

        food_breakdown = reports.get(
            "foodTypeBreakdown",
            {}
        )

        if food_breakdown:

            food_df = pd.DataFrame(
                {
                    "Food Type":
                        list(
                            food_breakdown.keys()
                        ),

                    "Count":
                        list(
                            food_breakdown.values()
                        )
                }
            )

            st.bar_chart(
                food_df.set_index(
                    "Food Type"
                )
            )

            st.dataframe(
                food_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No food type breakdown available."
            )

    else:

        st.error(
            "❌ Admin Reports returned no data."
        )

    # ========================================================
    # ALL DONATIONS
    # ========================================================

    st.divider()

    st.subheader(
        "📋 All Donations"
    )

    admin_donations = get_admin_donations()

    if admin_donations:

        statuses = [

            "ALL",

            "AVAILABLE",

            "CLAIMED",

            "PICKED_UP",

            "COMPLETED",

            "EXPIRED",

            "CANCELLED"
        ]

        selected_status = st.selectbox(
            "Filter by status",
            statuses
        )

        if selected_status == "ALL":

            filtered_donations = (
                admin_donations
            )

        else:

            filtered_donations = [

                donation

                for donation in admin_donations

                if donation.get(
                    "status"
                ) == selected_status
            ]

        st.write(
            f"Showing "
            f"**{len(filtered_donations)}** "
            f"donations"
        )

        for donation in filtered_donations:

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### 🍱 "
                    f"{donation.get('foodType', '-')}"
                )

                st.write(
                    f"**Donation ID:** "
                    f"{donation.get('donationId', '-')}"
                )

                st.write(
                    f"**Quantity:** "
                    f"{donation.get('quantity', '-')}"
                )

                st.write(
                    f"**Status:** "
                    f"{donation.get('status', '-')}"
                )

                st.write(
                    f"**Donor:** "
                    f"{donation.get('donorEmail', 'N/A')}"
                )

                st.write(
                    f"**Donor Role:** "
                    f"{donation.get('donorRole', 'N/A')}"
                )

                st.write(
                    f"**Receiver:** "
                    f"{donation.get('receiverEmail', '-')}"
                )

                st.write(
                    f"**Receiver Role:** "
                    f"{donation.get('receiverRole', '-')}"
                )

                st.write(
                    f"**Pickup Location:** "
                    f"{donation.get('pickupLocation', '-')}"
                )

                st.write(
                    f"**Pickup Time:** "
                    f"{donation.get('pickupTime', '-')}"
                )

                if donation.get(
                    "description"
                ):

                    st.write(
                        f"**Description:** "
                        f"{donation.get('description')}"
                    )

    else:

        st.info(
            "No donations found."
        )

    # ========================================================
    # DONATION STATUS MANAGEMENT
    # ========================================================

    st.divider()

    st.subheader(
        "⚙️ Donation Status Management"
    )

    if admin_donations:

        donation_options = {}

        for donation in admin_donations:

            donation_id = donation.get(
                "donationId"
            )

            label = (

                f"{donation.get('foodType', '-')}"
                f" | "
                f"{donation.get('status', '-')}"
                f" | "
                f"{donation_id}"
            )

            donation_options[
                label
            ] = donation

        selected_donation_label = st.selectbox(

            "Select donation",

            list(
                donation_options.keys()
            )
        )

        selected_donation = (
            donation_options[
                selected_donation_label
            ]
        )

        donation_id = (
            selected_donation.get(
                "donationId"
            )
        )

        current_status = (
            selected_donation.get(
                "status"
            )
        )

        st.write(
            f"**Food:** "
            f"{selected_donation.get('foodType', '-')}"
        )

        st.write(
            f"**Current Status:** "
            f"{current_status}"
        )

        new_status = st.selectbox(

            "New Status",

            [
                "AVAILABLE",
                "CLAIMED",
                "PICKED_UP",
                "COMPLETED",
                "EXPIRED",
                "CANCELLED"
            ]
        )

        if st.button(
            "Update Donation Status",
            use_container_width=True
        ):

            if new_status == current_status:

                st.warning(
                    "Donation is already in this status."
                )

            else:

                result = api_patch(

                    f"/donations/"
                    f"{donation_id}/status",

                    {
                        "status":
                            new_status
                    }
                )

                if result is not None:

                    if result.status_code == 200:

                        st.success(
                            "✅ Donation status updated!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "❌ Status update failed."
                        )

                        st.code(
                            result.text
                        )

    # ========================================================
    # USER MANAGEMENT
    # ========================================================

    st.divider()

    st.subheader(
        "👥 User Management"
    )

    users = get_admin_users()

    if users:

        for user in users:

            with st.container(
                border=True
            ):

                st.write(
                    f"**Email:** "
                    f"{user.get('email', 'N/A')}"
                )

                st.write(
                    f"**Role:** "
                    f"{user.get('role', 'N/A')}"
                )

                st.write(
                    f"**User ID:** "
                    f"{user.get('userId', 'N/A')}"
                )

    else:

        st.info(
            "No users found."
        )

    # ========================================================
    # CSV EXPORT
    # ========================================================

    st.divider()

    st.subheader(
        "📥 Export Donation Report"
    )

    if admin_donations:

        df = pd.DataFrame(
            admin_donations
        )

        csv = df.to_csv(
            index=False
        ).encode(
            "utf-8"
        )

        st.download_button(

            "📥 Download Donations CSV",

            data=csv,

            file_name=
                "rescueLink_donations.csv",

            mime=
                "text/csv",

            use_container_width=True
        )


# ============================================================
# AMAZON LOCATION GEOCODING
# ============================================================

def geocode_location(
    location
):

    if not LOCATION_API_KEY:

        st.error(
            "❌ Amazon Location API key is missing."
        )

        return None

    if not location:

        return None

    location = location.strip()

    if not location:

        return None

    try:

        url = (

            f"https://places.geo."
            f"{LOCATION_REGION}"
            f".amazonaws.com/v2/geocode"
        )

        params = {

            "key":
                LOCATION_API_KEY
        }

        body = {

            "QueryText":
                location,

            "MaxResults":
                5
        }

        response = requests.post(

            url,

            params=params,

            json=body,

            timeout=15
        )

        print(
            "Amazon Location status:",
            response.status_code
        )

        print(
            "Amazon Location response:",
            response.text
        )

        if response.status_code != 200:

            return None

        data = response.json()

        results = data.get(
            "ResultItems",
            []
        )

        if not results:

            return None

        result = results[0]

        position = result.get(
            "Position"
        )

        if not position:

            return None

        if len(position) < 2:

            return None

        longitude = position[0]

        latitude = position[1]

        address = result.get(
            "Address",
            {}
        )

        label = address.get(
            "Label"
        )

        if not label:

            label = result.get(
                "Title",
                location
            )

        return {

            "latitude":
                latitude,

            "longitude":
                longitude,

            "label":
                label,

            "place_id":
                result.get(
                    "PlaceId"
                ),

            "place_type":
                result.get(
                    "PlaceType"
                )
        }

    except requests.exceptions.Timeout:

        st.error(
            "⏱️ Amazon Location request timed out."
        )

        return None

    except requests.exceptions.RequestException as e:

        st.error(
            "❌ Amazon Location request failed."
        )

        st.code(
            str(e)
        )

        return None

    except Exception as e:

        st.error(
            "❌ Geocoding error."
        )

        st.code(
            str(e)
        )

        return None


# ============================================================
# PICKUP MAP
# ============================================================

st.divider()

st.subheader(
    "📍 RescueLink Pickup Map"
)

st.write(
    "Search for a pickup location and display it on the map."
)

map_location = st.text_input(

    "Pickup Location",

    placeholder=(
        "Tirupati Central Market, "
        "Tirupati, Andhra Pradesh, India"
    )
)

if st.button(
    "📍 Find Location",
    use_container_width=True
):

    if not map_location:

        st.warning(
            "Please enter a location."
        )

    else:

        result = geocode_location(
            map_location
        )

        if result:

            st.success(
                "📍 Location found!"
            )

            st.write(
                f"**Address:** "
                f"{result['label']}"
            )

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "Latitude",
                    round(
                        result["latitude"],
                        6
                    )
                )

            with c2:

                st.metric(
                    "Longitude",
                    round(
                        result["longitude"],
                        6
                    )
                )

            map_df = pd.DataFrame(

                {
                    "latitude": [
                        result["latitude"]
                    ],

                    "longitude": [
                        result["longitude"]
                    ]
                }
            )

            st.map(

                map_df,

                latitude="latitude",

                longitude="longitude",

                zoom=13
            )

        else:

            st.warning(
                "⚠️ Unable to find this location."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "RescueLink • Connecting surplus food with communities 🤝"
)