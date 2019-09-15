import os
from subprocess import Popen
import pytest

CONTENT_DIR_NAME = 'content'
BUILD_DIR_NAME = 'build'


@pytest.fixture
def content_directory(tmpdir):
    test_content_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'test_content')
    current_dir = str(tmpdir)
    copy_test_dir_process = Popen("rsync -avu %s/ %s" % (test_content_dir, current_dir),
                                  shell=True)
    std_out, std_err = copy_test_dir_process.communicate()
    assert std_out is None
    assert std_err is None
    yield tmpdir


def test_build(content_directory):
    content_dir = os.path.join(content_directory, CONTENT_DIR_NAME)
    build_dir = os.path.join(content_directory, BUILD_DIR_NAME)
    build_command_str = "python pystatic build %s %s" % (content_dir, build_dir)
    build_process = Popen(build_command_str, shell=True)
    std_out, std_err = build_process.communicate()
    assert len(os.listdir(build_dir)) > 1
