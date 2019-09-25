import os
from subprocess import Popen
import pytest

CONTENT_DIR_NAME = 'content'
BUILD_DIR_NAME = 'build'

test_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(test_dir)


@pytest.fixture
def content_directory(tmpdir):
    test_data_dir = os.path.join(
        root_dir,
        'data'
    )
    test_content_dir = os.path.join(
        test_data_dir,
        CONTENT_DIR_NAME,
    )

    current_dir = str(tmpdir)

    tmp_content_dir = os.path.join(
        current_dir,
        CONTENT_DIR_NAME,
    )

    tmp_build_dir = os.path.join(
        current_dir,
        BUILD_DIR_NAME,
    )
    copy_test_dir_process = Popen("rsync -avu %s/ %s/" % (test_content_dir, tmp_content_dir),
                                  shell=True)
    std_out, std_err = copy_test_dir_process.communicate()
    assert std_out is None
    assert std_err is None
    build_dest_folder_process = Popen(f"mkdir -p {tmp_build_dir}", shell=True)
    std_out1, std_err1 = build_dest_folder_process.communicate()
    assert std_out1 is None
    assert std_err1 is None
    assert len(os.listdir(tmp_content_dir)) > 0
    assert len(os.listdir(tmp_build_dir)) == 0

    yield tmpdir


def test_build(content_directory):
    content_dir = os.path.join(content_directory, CONTENT_DIR_NAME)
    build_dir = os.path.join(content_directory, BUILD_DIR_NAME)
    build_command_str = "python -m blog build %s %s" % (content_dir, build_dir)
    build_process = Popen(build_command_str, shell=True)
    std_out, std_err = build_process.communicate()
    assert len(os.listdir(build_dir)) > 1
    # TODO: more comprehensive tests against output