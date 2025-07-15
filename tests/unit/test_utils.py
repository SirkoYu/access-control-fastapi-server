import pytest

from src.utils.case_converter import camel_case_to_snake_case


@pytest.mark.parametrize("input_str, expected", [
    ("simpleTest", "simple_test"),
    ("SimpleTest", "simple_test"),
    ("testCaseExample", "test_case_example"),
    ("Test", "test"),
    ("T", "t"),
    ("", ""),
    ("test", "test"),
    ("XMLHttpRequest", "xml_http_request"),
    ("JSONData", "json_data"),
    ("HTTPRequest", "http_request"),
    ("HTML", "html"),
    ("MyBIGNumber", "my_big_number"),
    ("BigUSACompany", "big_usa_company"),
    ("camelCaseToSnakeCase", "camel_case_to_snake_case"),
])
def test_camel_case_to_snake_case(input_str, expected):
    assert camel_case_to_snake_case(input_str) == expected