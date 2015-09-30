import pytest


def test_importable():
    import devpi_findlinks
    assert devpi_findlinks.__version__


@pytest.mark.with_notifier
def test_findlinks(mapp, pypistage, testapp):
    mapp.create_and_login_user("user1", "1")
    mapp.create_index("dev", indexconfig=dict(bases=["root/pypi"]))
    mapp.use("user1/dev")
    pypistage.mock_simple("pkg1", text='''
            <a href="../../pkg1/pkg1-2.6.zip" />
        ''', pypiserial=10)
    pypistage.mock_simple("pkg2", text='''
            <a href="../../pkg2/pkg2-1.0.zip" />
        ''', pypiserial=11)
    mapp.upload_file_pypi(
        "pkg1-2.7.tgz", b"123", "pkg1", "2.7", code=200, waithooks=True)
    r = testapp.xget(200, 'http://localhost/user1/dev/+findlinks',
                     headers=dict(accept="text/html"))
    links = r.html.select('a')
    # only the package from the index itself should show up, nothing from pypi
    assert [(l.text, l.attrs['href']) for l in links] == [
        ('pkg1-2.7.tgz', 'http://localhost/user1/dev/+f/a66/5a45920422f9d/pkg1-2.7.tgz#sha256=a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3')]
    body, = [body.text for body in r.html.select('body')]
    assert list(filter(None, (x.strip() for x in body.split('\n')))) == [
        'user1/dev: all package links without root/pypi',
        'user1/dev pkg1-2.7.tgz']


@pytest.mark.with_notifier
def test_findlinks_inherited(mapp, pypistage, testapp):
    mapp.create_and_login_user("user1", "1")
    mapp.create_index("prod", indexconfig=dict(bases=["root/pypi"]))
    mapp.create_index("dev", indexconfig=dict(bases=["user1/prod"]))
    mapp.use("user1/prod")
    mapp.upload_file_pypi(
        "pkg1-2.6.tgz", b"123", "pkg1", "2.6", code=200)
    mapp.use("user1/dev")
    pypistage.mock_simple("pkg1", text='''
            <a href="../../pkg1/pkg1-2.6.zip" />
        ''', pypiserial=10)
    pypistage.mock_simple("pkg2", text='''
            <a href="../../pkg2/pkg2-1.0.zip" />
        ''', pypiserial=11)
    mapp.upload_file_pypi(
        "pkg1-2.7.tgz", b"1234", "pkg1", "2.7", code=200, waithooks=True)
    r = testapp.xget(200, 'http://localhost/user1/dev/+findlinks',
                     headers=dict(accept="text/html"))
    links = r.html.select('a')
    # only the package from the index itself and it's base should show up, nothing from pypi
    assert [(l.text, l.attrs['href']) for l in links] == [
        ('pkg1-2.6.tgz', 'http://localhost/user1/prod/+f/a66/5a45920422f9d/pkg1-2.6.tgz#sha256=a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'),
        ('pkg1-2.7.tgz', 'http://localhost/user1/dev/+f/03a/c674216f3e15c/pkg1-2.7.tgz#sha256=03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4')]
    body, = [body.text for body in r.html.select('body')]
    assert list(filter(None, (x.strip() for x in body.split('\n')))) == [
        'user1/dev: all package links without root/pypi',
        'user1/prod pkg1-2.6.tgz',
        'user1/dev pkg1-2.7.tgz']


def test_findlinks_empty(mapp, pypistage, testapp):
    mapp.create_and_login_user("user1", "1")
    mapp.create_index("dev", indexconfig=dict(bases=["root/pypi"]))
    mapp.use("user1/dev")
    pypistage.mock_simple("pkg1", text='''
            <a href="../../pkg1/pkg1-2.6.zip" />
        ''', pypiserial=10)
    r = testapp.xget(200, 'http://localhost/user1/dev/+findlinks',
                     headers=dict(accept="text/html"))
    links = r.html.select('a')
    # the index is empty, so nothing should show up
    assert [(l.text, l.attrs['href']) for l in links] == []
    body, = [body.text for body in r.html.select('body')]
    assert list(filter(None, (x.strip() for x in body.split('\n')))) == [
        'user1/dev: all package links without root/pypi',
        'No releases.']


@pytest.mark.with_notifier
def test_findlinks_empty_inherited(mapp, pypistage, testapp):
    mapp.create_and_login_user("user1", "1")
    mapp.create_index("prod", indexconfig=dict(bases=["root/pypi"]))
    mapp.create_index("dev", indexconfig=dict(bases=["user1/prod"]))
    mapp.use("user1/prod")
    mapp.upload_file_pypi(
        "pkg1-2.6.tgz", b"123", "pkg1", "2.6", code=200)
    mapp.use("user1/dev")
    pypistage.mock_simple("pkg1", text='''
            <a href="../../pkg1/pkg1-2.6.zip" />
        ''', pypiserial=10)
    pypistage.mock_simple("pkg2", text='''
            <a href="../../pkg2/pkg2-1.0.zip" />
        ''', pypiserial=11)
    r = testapp.xget(200, 'http://localhost/user1/dev/+findlinks',
                     headers=dict(accept="text/html"))
    links = r.html.select('a')
    # the index is empty, but uploads in it's base should show up, nothing from pypi
    assert [(l.text, l.attrs['href']) for l in links] == [
        ('pkg1-2.6.tgz', 'http://localhost/user1/prod/+f/a66/5a45920422f9d/pkg1-2.6.tgz#sha256=a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3')]
    body, = [body.text for body in r.html.select('body')]
    assert list(filter(None, (x.strip() for x in body.split('\n')))) == [
        'user1/dev: all package links without root/pypi',
        'user1/prod pkg1-2.6.tgz']
