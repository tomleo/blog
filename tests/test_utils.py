import pytest


# TODO: should be testing against pip package?
import os
import sys
sys.path.insert(0, os.path.join(os.path.abspath('..'), 'blog'))

from blog import utils  # noqa E402


@pytest.mark.parametrize(
    'quote_variation',
    ['test{}slug{}'.format(char, index)
     for index, char
     in enumerate(utils.unicode_quote_chars)])
def test_slugify_quote_variations(quote_variation):
    generaged_slug = utils.slugify(quote_variation)
    assert quote_variation not in generaged_slug


@pytest.mark.parametrize(
    'dash_variation,expected_slug',
    [('test{}slug{}'.format(char, index), 'test-slug{}'.format(index))
     for (index, char)
     in enumerate(utils.unicode_dash_chars)])
def test_slugify_dash_variations(dash_variation, expected_slug):
    generaged_slug = utils.slugify(dash_variation)
    assert dash_variation not in generaged_slug
    assert generaged_slug == expected_slug


unwated_chars_list = [
    ',',
    ':',
    '?',
    '(',
    ')',
    '\'',
    '!',
    '<',
    '>',
]


@pytest.mark.parametrize(
    'slug_variation,expected_slug',
    [('test{}slug{}'.format(char, index), 'testslug{}'.format(index))
     for (index, char)
     in enumerate(unwated_chars_list)])
def test_slugify_unwanted_chars(slug_variation, expected_slug):
    generaged_slug = utils.slugify(slug_variation)
    assert generaged_slug == expected_slug


@pytest.mark.parametrize(
    'input_val,expected_output',
    [
        ('test&', 'testand'),
        ('test%', 'testpercent'),
        ('foo bar', 'foo-bar'),
        ('test.', 'test'),
        ('TEST', 'test')
    ]
)
def test_misc_transforms(input_val, expected_output):
    generaged_slug = utils.slugify(input_val)
    assert generaged_slug == expected_output
