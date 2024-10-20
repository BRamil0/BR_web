import fastapi
from main import fast_app_start

from src.tests import test_pages
from src.tests import test_codes
from src.tests import test_background

def tests_start() -> bool | None:
    """
    start of tests
    :return: bool | None
    """
    app: fastapi.FastAPI = fast_app_start()

    tp = test_pages.TestPages(app)
    tc = test_codes.TestCodes(app)
    tb = test_background.TestBackground(app)

    tp.run_tests()
    tc.run_tests()
    tb.run_tests()
    return True