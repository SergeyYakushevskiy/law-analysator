import pytest
from src.storage.services.position_service import LexPositionService
from src.storage.exceptions import PositionOverflow

@pytest.fixture
def lex_service():
    return LexPositionService()

def test_new_position_after(lex_service):
    pos = lex_service.new_position_after("a")
    assert pos > "a"
    assert isinstance(pos, str)

def test_new_position_before(lex_service):
    pos = lex_service.new_position_before("m")
    assert pos < "m"
    assert isinstance(pos, str)

def test_new_position_between_basic(lex_service):
    pos = lex_service.new_position_between("a", "c")
    assert "a" < pos < "c"

def test_new_position_between_edge_cases(lex_service):
    # prev пустая, next "b"
    pos = lex_service.new_position_between("", "b")
    assert pos < "b"
    assert pos >= ""

    # prev "y", next пустая
    pos = lex_service.new_position_between("y", "")
    assert pos > "y"

def test_mid_string_monotonic(lex_service):
    s1 = "abc"
    s2 = "abd"
    mid = lex_service.mid_string(s1, s2)
    assert s1 < mid < s2

def test_position_ordering_multiple_steps(lex_service):
    # Проверяем что последовательные позиции остаются отсортированы
    prev = ""
    positions = []
    for _ in range(10):
        next_pos = lex_service.new_position_after(prev)
        assert next_pos > prev
        positions.append(next_pos)
        prev = next_pos

    # Проверка, что все позиции уникальны и отсортированы
    assert positions == sorted(positions)
    assert len(set(positions)) == len(positions)

def test_max_char_boundary(lex_service):
    # Проверяем, что возвращаемые позиции не превышают MAX_CHAR
    pos = lex_service.new_position_after(chr(0x10FFFE))
    assert all(ord(c) <= lex_service.MAX_CHAR for c in pos)
