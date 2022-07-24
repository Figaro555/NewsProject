import unittest


def main():
    loader = unittest.TestLoader()
    start_dir = 'test'
    suite = loader.discover(start_dir, pattern="*_test.py")

    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    main()
