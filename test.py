import unittest
from tests import setup_django


def test():
    setup_django()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    test()
