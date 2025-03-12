import os
import pytest

from playwright.sync_api import Page, expect
from helpers.postgres_helper import (
    User,
    create_user_using_psql,
    execute_postgres_query,
    fetch_postgres_query,
    follow_user_using_psql,
    tweet_using_psql,
)
from helpers.test_helper import (
    BASE_URL,
    generate_random_email,
    generate_random_password,
    generate_random_username,
)

MY_TIMELINE_URL = f"{BASE_URL}/"
PUBLIC_TIMELINE_URL = f"{BASE_URL}/public"
SIGN_UP_URL = f"{BASE_URL}/register"
SIGN_IN_URL = f"{BASE_URL}/login"
SIGN_OUT_URL = f"{BASE_URL}/logout"
USER_TIMELINE_URL = f"{BASE_URL}/user"


def sign_in_using_playwrght(page: Page, useTestUser=True):
    if not useTestUser:
        page.goto(SIGN_UP_URL)
        global username, email, password

        username = generate_random_username()
        email = generate_random_email()
        password = generate_random_password()

        page.locator("input[name='username']").fill(username)
        page.locator("input[name='email']").fill(email)
        page.locator("input[name='password']").fill(password)
        page.locator("input[name='password2']").fill(password)
        page.locator("input[type='submit']").click()

    page.goto(SIGN_IN_URL)

    page.locator("input[name='username']").fill(
        test_username if useTestUser else username
    )
    page.locator("input[name='password']").fill(
        test_password if useTestUser else password
    )
    page.locator("input[type='submit']").click()


def sign_in_user_using_playwright(page: Page, user: User):
    page.goto(SIGN_IN_URL)

    page.locator("input[name='username']").fill(user.username)
    page.locator("input[name='password']").fill(user.password)
    page.locator("input[type='submit']").click()


test_username = "test"
test_email = "test@test.test"
test_password = "test"

execute_postgres_query("truncate table users, followers, messages, latest;")
execute_postgres_query(
    f"do $$ begin IF NOT EXISTS (SELECT 1 FROM users WHERE username = '{test_username}') THEN INSERT INTO users (username, email, pw_hash) VALUES ('{test_username}', '{test_email}', '{test_password}'); END IF; end $$;"
)


def tweet_box_visible_test(page: Page):
    expect(page.get_by_text(f"What's on your mind {test_username}?"))
    expect(page.locator("input[name='text']")).to_be_visible()
    expect(page.locator("input[value='Share']")).to_be_visible()


def tweet_list_visible_test(page: Page):
    tweet_list_count = page.get_by_text("There's no message so far.").count()

    if tweet_list_count > 1:
        pytest.fail("Too many tweet lists")
    elif tweet_list_count == 0:
        assert page.locator("img").count() > 0


def test_root_redirect_to_public_timeline(page: Page):
    page.goto(MY_TIMELINE_URL)

    expect(page).to_have_url(PUBLIC_TIMELINE_URL)


def test_public_timeline_header_and_tweet_list_show(page: Page):
    page.goto(PUBLIC_TIMELINE_URL)

    expect(page.locator("h2").filter(has_text="Public Timeline")).to_be_visible()


def test_public_timeline_user_can_tweet_and_is_shown(page: Page):
    sign_in_using_playwrght(page)

    page.goto(PUBLIC_TIMELINE_URL)

    tweet = generate_random_username()
    page.locator("input[name='text']").fill(tweet)
    page.locator("input[type='submit']").click

    expect(page.get_by_text(tweet)).to_be_visible()


def test_public_timeline_shows_all_tweets(page: Page):
    user = create_user_using_psql()
    user2 = create_user_using_psql()

    tweet_using_psql(user.user_id)
    tweet_using_psql(user2.user_id)

    follow_user_using_psql(user.user_id, user2.user_id)

    page.goto(PUBLIC_TIMELINE_URL)

    assert page.get_by_text(user.username).count() >= 1
    assert page.get_by_text(user2.username).count() >= 1


def test_register_required_fields_and_buttons(page: Page):
    page.goto(SIGN_UP_URL)

    expect(page.get_by_text("Username:")).to_be_visible()
    expect(page.get_by_text("E-Mail:")).to_be_visible()
    expect(page.get_by_text("Password:")).to_be_visible()
    expect(page.get_by_text("Password (repeat):")).to_be_visible()

    expect(page.locator("input[name='username']")).to_be_visible()
    expect(page.locator("input[name='email']")).to_be_visible()
    expect(page.locator("input[name='password']")).to_be_visible()
    expect(page.locator("input[name='password2']")).to_be_visible()
    expect(page.locator("input[type='submit']")).to_be_visible()


def test_register_works_redirects_to_sign_in(page: Page):
    page.goto(SIGN_UP_URL)

    username = generate_random_username()
    email = generate_random_email()
    password = generate_random_password()

    page.locator("input[name='username']").fill(username)
    page.locator("input[name='email']").fill(email)
    page.locator("input[name='password']").fill(password)
    page.locator("input[name='password2']").fill(password)
    page.locator("input[type='submit']").click()

    does_user_exist_in_db = fetch_postgres_query(
        f"SELECT count(*) FROM users WHERE username = '{username}'"
    )
    assert does_user_exist_in_db[0][0] == 1


def test_sign_in_fields_and_buttons(page: Page):
    page.goto(SIGN_IN_URL)

    expect(page.get_by_text("Username:")).to_be_visible()
    expect(page.get_by_text("Password:")).to_be_visible()

    expect(page.locator("input[name='username']")).to_be_visible()
    expect(page.locator("input[name='password']")).to_be_visible()


def test_sign_in_works_redirects_to_my_timeline(page: Page):
    page.goto(SIGN_IN_URL)

    page.locator("input[name='username']").fill(test_username)
    page.locator("input[name='password']").fill(test_password)
    page.locator("input[type='submit']").click()

    page.wait_for_url(MY_TIMELINE_URL)

    assert page.url == MY_TIMELINE_URL


def test_my_timeline_tweet_box_and_message_list(page: Page):
    sign_in_using_playwrght(page)

    page.goto(MY_TIMELINE_URL)

    expect(page.get_by_text("My Timeline", exact=True)).to_be_visible()
    tweet_box_visible_test(page)
    tweet_list_visible_test(page)


def test_my_timeline_user_can_tweet_and_message_is_shown(page: Page):
    sign_in_using_playwrght(page)

    page.goto(MY_TIMELINE_URL)
    page.wait_for_url(MY_TIMELINE_URL)

    tweet = generate_random_username()
    page.locator("input[name='text']").fill(tweet)
    page.locator("input[type='submit']").click()

    expect(page.get_by_text(tweet)).to_be_visible()


def test_my_timeline_shows_followed_tweets_and_my_own_tweets(page: Page):
    user = create_user_using_psql()
    user2 = create_user_using_psql()

    tweet_using_psql(user.user_id)
    tweet_using_psql(user2.user_id)

    follow_user_using_psql(user.user_id, user2.user_id)

    sign_in_user_using_playwright(page, user)

    page.goto(MY_TIMELINE_URL)

    assert page.get_by_text(user.username).count() >= 1
    assert page.get_by_text(user2.username).count() >= 1


def test_logout_logs_out_user_and_redirects_to_public_timeline(page: Page):
    sign_in_using_playwrght(page)

    page.goto(SIGN_OUT_URL)

    assert page.url == PUBLIC_TIMELINE_URL

    page.goto(f"{USER_TIMELINE_URL}/{test_username}")

    assert page.get_by_text("This is you!").count() == 0


def test_follow_and_unfollow(page: Page):
    sign_in_using_playwrght(page, useTestUser=False)

    page.goto(f"{USER_TIMELINE_URL}/{test_username}")

    not_following_text = "You are not yet following this user"

    expect(page.get_by_text(not_following_text)).to_be_visible()
    page.get_by_text("Follow user").click()

    expect(page.get_by_text("You are currently following this user")).to_be_visible()
    page.get_by_text("Unfollow user").click()

    expect(page.get_by_text(not_following_text)).to_be_visible()


def test_user_timeline_user_own_timeline_only_shows_users_tweets(page: Page):
    user = create_user_using_psql()
    user2 = create_user_using_psql()

    tweet_using_psql(user.user_id)
    tweet_using_psql(user2.user_id)

    sign_in_user_using_playwright(page, user)

    page.goto(f"{USER_TIMELINE_URL}/{user.username}")

    assert page.get_by_text(user.username).count() >= 1
    assert page.get_by_text(user2.username).count() >= 0
