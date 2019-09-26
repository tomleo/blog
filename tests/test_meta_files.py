import pytest


# TODO: should be testing against pip package?
import os
import sys
sys.path.insert(0, os.path.join(os.path.abspath('..'), 'blog'))

from blog.meta_files import model  # noqa E402


def test_file_context_meta():
    file_context_meta = model.FileContextMeta()
    assert file_context_meta.template == model.FileContextMeta.DEFAULT_TEMPLATE_STR
    assert file_context_meta['template'] == model.FileContextMeta.DEFAULT_TEMPLATE_STR
    with pytest.raises(KeyError):
        file_context_meta['foo']
    file_context_meta['foo'] = 'foo'
    assert file_context_meta['foo'] == 'foo'
    file_context_meta['template'] = 'template-new'
    assert file_context_meta.template == 'template-new'
    assert file_context_meta['template'] == 'template-new'

    meta_dict = file_context_meta.as_dict()
    assert set(meta_dict.keys()) == {'foo', 'template'}
    assert meta_dict['template'] == 'template-new'
    assert meta_dict['foo'] == 'foo'


def test_file_context_body():
    file_context_body = model.FileContextBody('bar')
    assert file_context_body.content == 'bar'


def test_file_context():
    file_context = model.FileContext(
        meta=model.FileContextMeta(),
        content=model.FileContextBody(content='bar'),
    )
    assert file_context.get_template() == 'default.html'
    assert file_context.get_context()['meta'] == {'template': 'default'}
    assert file_context.get_context()['content'] == 'bar'


def test_md():
    md = model.Md(
        yaml_meta='foo',
        markdown_content='bar'
    )
    assert md.yaml_meta == 'foo'
    assert md.markdown_content == 'bar'


def test_dest_file():
    dest_file = model.DestFile(
        dest_file_name='foo.txt',
        dest_file_folder='/home/',
    )
    assert dest_file.dest_file_name == 'foo.txt'
    assert dest_file.dest_file_folder == '/home/'
    assert dest_file.dest_file_path == '/home/foo.txt'


def test_folder_meta():
    folder_meta = model.FolderMeta(
        dir_path='a',
        files='b',
        has_dirs='c'
    )
    assert folder_meta.dir_path == 'a'
    assert folder_meta.files == 'b'
    assert folder_meta.has_dirs == 'c'
