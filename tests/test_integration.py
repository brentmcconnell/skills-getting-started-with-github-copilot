from urllib.parse import quote


def test_signup_then_unregister_flow(client):
    # Arrange
    activity_name = "Math Olympiad"
    encoded_activity_name = quote(activity_name, safe="")
    email = "flow.student@mergington.edu"

    # Act
    signup_response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )
    activities_after_signup = client.get("/activities").json()

    unregister_response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )
    activities_after_unregister = client.get("/activities").json()

    # Assert
    assert signup_response.status_code == 200
    assert email in activities_after_signup[activity_name]["participants"]
    assert unregister_response.status_code == 200
    assert email not in activities_after_unregister[activity_name]["participants"]
