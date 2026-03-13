from urllib.parse import quote


def test_unregister_from_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "daniel@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in participants


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    encoded_activity_name = quote(activity_name, safe="")
    email = "daniel@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_nonexistent_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "not.registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"
