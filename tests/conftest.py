import pytest


pytest_plugins = ["pytest_devpi_server", "test_devpi_server.plugin"]


def write_transaction(keyfs):
    if hasattr(keyfs, 'write_transaction'):
        return keyfs.write_transaction()
    return keyfs.transaction(write=True)


@pytest.fixture
def xom(request, makexom):
    import devpi_findlinks.main
    xom = makexom(plugins=[(devpi_findlinks.main, None)])
    from devpi_server.main import set_default_indexes
    with write_transaction(xom.keyfs):
        set_default_indexes(xom.model)
    return xom
