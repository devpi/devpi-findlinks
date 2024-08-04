from devpi_common.metadata import parse_version
from devpi_server import __version__ as _devpi_server_version
import pytest


devpi_server_version = parse_version(_devpi_server_version)


if devpi_server_version < parse_version("6.9.3dev"):
    from test_devpi_server.conftest import gentmp, httpget, makemapp  # noqa
    from test_devpi_server.conftest import maketestapp, makexom, mapp  # noqa
    from test_devpi_server.conftest import pypiurls, testapp, pypistage  # noqa
    from test_devpi_server.conftest import storage_info  # noqa
    from test_devpi_server.conftest import mock  # noqa
    (makexom,)  # shut up pyflakes
else:
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
