from main import app


def test_entity_image_route_is_registered():
    assert "get" in app.openapi()["paths"]["/images/{entity_id}"]


def test_frame_file_image_route_is_registered():
    assert "post" in app.openapi()["paths"]["/images/frame-file/{entity_id}"]
