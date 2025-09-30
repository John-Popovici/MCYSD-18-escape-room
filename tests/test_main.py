from main import square, square_wrong


def test_square():
    Integer = 5
    assert square(Integer) == 25
    assert square(1) == 1
    assert square(-5) == 25
    assert square(0) != "hello"
    
def test_square_wrong():
    assert square_wrong(5) == 25
    assert square_wrong(1) == 1
    assert square_wrong(-5) == 25
    
def test_square_wrong_2():
    assert square_wrong(2) == 4