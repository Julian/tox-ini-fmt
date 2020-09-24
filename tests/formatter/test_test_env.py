from textwrap import dedent

import pytest

from tox_ini_fmt.formatter import format_tox_ini
from tox_ini_fmt.formatter.test_env import to_extras


def test_no_tox_section(tox_ini):
    tox_ini.write_text("")
    assert format_tox_ini(tox_ini) == "\n"


@pytest.mark.parametrize("section", ["testenv", "testenv:py38"])
def test_format_test_env(tox_ini, section):
    content = dedent(
        """
    commands = \te
      \tf
    extras = \tc,d
    description = \tdesc\t
    deps = \tb\t
      \ta\t
    basepython=\tpython3.8\t
    """
    ).strip()
    tox_ini.write_text(f"[testenv]\n{content}")
    outcome = format_tox_ini(tox_ini)
    expected = dedent(
        """
        [testenv]
        description = desc
        basepython = python3.8
        deps =
          a
          b
        extras =
          c
          d
        commands =
          e
          f
        """
    ).lstrip()
    assert outcome == expected


@pytest.mark.parametrize(
    "arg, output",
    [
        ("", ""),
        ("\t", ""),
        ("\n", ""),
        ("a", "\na"),
        (" a ", "\na"),
        ("b,a", "\na\nb"),
        ("a,b", "\na\nb"),
        ("b\n  a,c", "\na\nb\nc"),
        ("c\n  c,c", "\nc"),
    ],
)
def test_extras(arg, output):
    result = to_extras(arg)
    assert result == output