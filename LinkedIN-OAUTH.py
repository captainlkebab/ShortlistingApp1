import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import requests
import os

# LinkedIn OAuth Configuration
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")  # Use an environment variable
LINKEDIN_CLIENT_SECRET = "WPL_AP1.aQwxJD8zvp3kxbP9./5znnA=="  # Use an environment variable
REDIRECT_URI = "http://localhost:8501"  # Replace with deployed app URL if needed

AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
PROFILE_URL = "https://api.linkedin.com/v2/me"
EMAIL_URL = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"

# OAuth Helper Functions
def get_authorization_url():
    oauth = OAuth2Session(client_id=LINKEDIN_CLIENT_ID, redirect_uri=REDIRECT_URI)
    url, state = oauth.create_authorization_url(
        AUTHORIZATION_URL,
        scope=["openid","profile", "email"]
    )
    st.session_state["oauth_state"] = state  # Store state to validate CSRF
    return url

def get_access_token(code):
    oauth = OAuth2Session(
        client_id=LINKEDIN_CLIENT_ID,
        client_secret=LINKEDIN_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI
    )
    token = oauth.fetch_token(
        TOKEN_URL,
        code=code,
        include_client_id=True
    )
    return token

def get_user_profile(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    profile = requests.get(PROFILE_URL, headers=headers).json()
    email_response = requests.get(EMAIL_URL, headers=headers).json()
    email = None
    if "elements" in email_response:
        elements = email_response["elements"]
        if elements:
            email = elements[0]["handle~"]["emailAddress"]

        return profile, email

# Streamlit App
st.title("LinkedIn OAuth Integration")

# Initialize session state variables
if "oauth_state" not in st.session_state:
    st.session_state["oauth_state"] = None
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

# OAuth Flow
if st.session_state["access_token"] is None:
    # Step 1: Display Login Button
    if st.button("Login with LinkedIn"):
        auth_url = get_authorization_url()
        st.write(f"[Click here to log in]({auth_url})")

    # Step 2: Handle Redirect with Authorization Code
    query_params = st.query_params  # Updated for compatibility
    if "code" in query_params:
        code = query_params["code"][0]
        token = get_access_token(code)

        # Validate state parameter (Optional for security)
        if st.session_state["oauth_state"] == query_params.get("state", [None])[0]:
            st.session_state["access_token"] = token["access_token"]
            st.experimental_rerun()
        else:
            st.error("Invalid state parameter. Possible CSRF detected.")
else:
    # Step 3: Fetch and Display User Profile
    access_token = st.session_state["access_token"]
    profile, email = get_user_profile(access_token)

    st.write("### User Profile:")
    st.json(profile)

    st.write("### Email Address:")
    st.json(email)

    # Logout Option
    if st.button("Logout"):
        st.session_state["access_token"] = None
        st.experimental_rerun()
