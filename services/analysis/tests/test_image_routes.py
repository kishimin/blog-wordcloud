from main import app
from analysis.routes.image_by_entity import WORD_CLOUD_FONT_PATH
from analysis.routes.image_by_frame_file import (
    WORD_CLOUD_FONT_PATH as FRAME_FILE_WORD_CLOUD_FONT_PATH,
)


def test_entity_image_route_is_registered():
    assert "get" in app.openapi()["paths"]["/images/{entity_id}"]


def test_frame_file_image_route_is_registered():
    assert "post" in app.openapi()["paths"]["/images/frame-file/{entity_id}"]


def test_entity_image_route_uses_the_service_font():
    from pathlib import Path

    assert Path(WORD_CLOUD_FONT_PATH).is_file()


def test_frame_file_image_route_uses_the_service_font():
    from pathlib import Path

    assert Path(FRAME_FILE_WORD_CLOUD_FONT_PATH).is_file()


def test_frame_file_upload_is_required():
    operation = app.openapi()["paths"]["/images/frame-file/{entity_id}"]["post"]

    assert operation["requestBody"]["required"] is True
