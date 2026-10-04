from main import app
from analysis.routes.image_by_entity import WORD_CLOUD_FONT_PATH


def test_entity_image_route_is_registered():
    assert "get" in app.openapi()["paths"]["/images/{entity_id}"]


def test_frame_file_image_route_is_registered():
    assert "post" in app.openapi()["paths"]["/images/frame-file/{entity_id}"]


def test_entity_image_route_uses_the_service_font():
    from pathlib import Path

    assert Path(WORD_CLOUD_FONT_PATH).is_file()
