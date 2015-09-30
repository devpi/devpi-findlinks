from test_devpi_server.conftest import gentmp, httpget, makemapp  # noqa
from test_devpi_server.conftest import maketestapp, makexom, mapp  # noqa
from test_devpi_server.conftest import pypiurls, testapp, pypistage  # noqa
from test_devpi_server.conftest import proxymock, mock  # noqa
import pytest


(makexom,)  # shut up pyflakes


@pytest.fixture
def xom(request, makexom):
    import devpi_findlinks.main
    xom = makexom(plugins=[(devpi_findlinks.main, None)])
    from devpi_server.main import set_default_indexes
    with xom.keyfs.transaction(write=True):
        set_default_indexes(xom.model)
    return xom
