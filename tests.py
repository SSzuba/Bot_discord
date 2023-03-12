from main import *
import pytest

def test_check_for_type_sport() -> None:
  assert check_for_type("sport")

def test_check_for_type_moto() -> None:
  assert check_for_type("moto")

def test_check_for_type_biznes() -> None:
  assert check_for_type("biznes")

def test_check_for_type_non_exist() -> None:
  with pytest.raises(AssertionError):
    assert check_for_type("wiadomosci")

def test_count_New() -> None:
  assert count("sport", "New") > 0
  assert count("moto", "New") > 0
  assert count("biznes", "New") > 0

def test_count_Update() -> None:
  assert count("sport", "Update") > 0
  assert count("moto", "Update") > 0
  assert count("biznes", "Update") > 0

def test_count_wrong_params() -> None:
  with pytest.raises(AssertionError):
    assert count("sport", "nowe") > 0
    assert count("motorowe", "nowe") > 0
    assert count("biznes", "nowe") > 0
    assert count("sportowe", "Update") > 0
    assert count("moto", "aktualizacja") > 0
    assert count("biznesowe", "zmiana") > 0

def test_geters() -> None:
  assert get_sites()
  assert get_types()

def test_check_site() -> None:
  assert check_site("https://www.onet.pl/") == True
  assert check_site("https://www.onet.pl/sportowe/wiadomosci") != True
  assert check_site("https://www.jakas.tam.strona.pl/") != True

