import pytest
from main import get_playlist, runner_main
from pathlib import Path

playlist_path = Path('playlist_test')
visual_path = Path('visual_test\\video_test.mp4')
@pytest.mark.unit
def test_get_playlist():
    playlist = get_playlist(playlist_path)
    assert len(playlist) == 3, 'get_playlist function can not read correctly the files in: {}.'.format(path2test)

def test_runner_main():
    runner_main(playlist_path=playlist_path, video_path=visual_path, shutdown=False)


