from fixture.application import Application
import pytest

fixture = None


@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    base_url = request.config.getoption("--base_url")
    base_password = request.config.getoption("--base_password")
    if fixture is None:
        fixture = Application(browser=browser, base_url=base_url, base_password=base_password)
    else:
        if not fixture.is_valid():
            fixture = Application(browser=browser, base_url=base_url, base_password=base_password)
    fixture.session.ensure_login(username="admin", password=base_password)
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--base_url", action="store", default="http://localhost/addressbook/addressbook/")
    parser.addoption("--base_password", action="store", default="secret")

