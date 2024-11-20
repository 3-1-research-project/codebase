import requests
import time
import pandas as pd
from host_sequence.const_data import register_data_dummie, login_data_dummie, message_data
from utils import print_info_call

BASE_URL = "http://10.7.7.144:5000"
BASE_DELAY = 1.8
ITER_NUM = 20  # iteration number for each endpoint call has to be <= 400

session = requests.Session()

# Store sessions for each user
user_sessions = {}


def request_endpoint(path, method="get", data=None, user_session=None):
    url = f"{BASE_URL}{path}"
    start = time.time()
    response = (user_session or session).request(method=method, url=url, data=data)
    end = time.time()
    print(f"Request to {url:<50} | Status: {response.status_code:<3}  | start: {start:<20.6f} | end: {end:<20.6f}")
    return {"endpoint": path, "response": response.status_code, "start": start, "end": end,
            "delta": end - start}


def sequential_interval_scenario(service, start, iter):
    # set main user
    main_user = register_data_dummie(0)["username"]

    # 1. Access Public Timeline
    print_info_call("Page", service, "Public Timeline", ITER_NUM)
    public_page_response = [request_endpoint("/public") for _ in range(ITER_NUM)]
    time.sleep(BASE_DELAY)

    # 2. Register all 400 users
    print_info_call("Page", service, "Register", ITER_NUM)
    register_response = []
    for i in range(ITER_NUM):
        user = register_data_dummie(i)
        response = request_endpoint("/register", method="post", data=user)
        register_response.append(response)
        # Create a session for each user after registration
        user_sessions[user["username"]] = requests.Session()
    time.sleep(BASE_DELAY)

    # 3. Login with all 400 users
    print_info_call("Page", service, "Login", ITER_NUM)
    login_response = []
    for i in range(ITER_NUM-1, -1, -1):
        user = login_data_dummie(i)
        user_session = user_sessions[user["username"]]
        response = request_endpoint("/login", method="post", data=user, user_session=user_session)
        login_response.append(response)
    time.sleep(BASE_DELAY)

    # 4. main user follows all other users
    print_info_call("Page", service, "Follow", ITER_NUM)
    follow_response = []
    main_user_session = user_sessions[main_user]
    for i in range(1, ITER_NUM):  # Start from the second user to avoid self-following
        user = login_data_dummie(i)
        whom_username = user["username"]
        response = request_endpoint(f"/{whom_username}/follow", user_session=main_user_session)
        follow_response.append(response)
    time.sleep(BASE_DELAY)

    # 5. User 1 posts a message
    print_info_call("Page", service, "Post Message", ITER_NUM)
    message_response = [
        request_endpoint("/add_message", method="post", data=message_data, user_session=main_user_session) for _ in
        range(ITER_NUM)]
    time.sleep(BASE_DELAY)

    # 6. Access public timeline
    print_info_call("Page", service, "Public Timeline Redirect", ITER_NUM)
    public_timeline_redirect_response = [request_endpoint("/public") for _ in range(ITER_NUM)]
    time.sleep(BASE_DELAY)

    # 7. Access user timeline
    print_info_call("Page", service, "User Timeline", ITER_NUM)
    user_timeline_response = [request_endpoint(f"/{main_user}", user_session=main_user_session) for _ in range(ITER_NUM)]
    time.sleep(BASE_DELAY)

    # 8. Unfollow all users
    print_info_call("Page", service, "Unfollow", ITER_NUM)
    unfollow_response = []
    for i in range(ITER_NUM):
        user = login_data_dummie(i)
        whom_username = user["username"]
        response = request_endpoint(f"/{whom_username}/unfollow", user_session=main_user_session)
        unfollow_response.append(response)
    time.sleep(BASE_DELAY)

    # 9. Logout all users
    print_info_call("Page", service, "Logout", ITER_NUM)
    logout_response = []
    for i in range(ITER_NUM):
        user = login_data_dummie(i)
        user_session = user_sessions[user["username"]]
        response = request_endpoint("/logout", user_session=user_session)
        logout_response.append(response)
    time.sleep(BASE_DELAY)

    print(f"Finished page sequence for service {service} - iteration {iter}!", flush=True)

    return [f"{service}-page-{start}-{iter}",
            public_page_response,
            register_response,
            login_response,
            follow_response,
            message_response,
            public_timeline_redirect_response,
            user_timeline_response,
            unfollow_response,
            logout_response]


def run_page_seq_scenario(service, start):
    data = [sequential_interval_scenario(service, start, 0)]
    df = pd.DataFrame(data, columns=[
        "ExperimentID",
        "PublicPageResponse",
        "RegisterResponse",
        "LoginResponse",
        "FollowResponse",
        "AddMessageResponse",
        "PublicTimelineRedirectResponse",
        "UserTimelineResponse",
        "UnfollowResponse",
        "LogoutResponse"
    ])
    return df