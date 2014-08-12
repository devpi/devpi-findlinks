from devpi_common.url import URL
from operator import attrgetter
from py.xml import html
from pyramid.response import Response
from pyramid.view import view_config


def includeme(config):
    config.add_route(
        "findlinks",
        "/{user}/{index}/+findlinks")
    config.scan()


def devpiserver_pyramid_configure(config, pyramid_config):
    # by using include, the package name doesn't need to be set explicitly
    # for registrations of static views etc
    pyramid_config.include('devpi_findlinks.main')


@view_config(route_name="findlinks", request_method="GET")
def findlinks_view(context, request):
    title = "%s: all package links without root/pypi" % (context.stage.name)
    projectnames = set()
    for stage, names in context.stage.op_sro("list_projectnames_perstage"):
        if stage.ixconfig["type"] == "mirror":
            continue
        projectnames.update(names)
    all_links = []
    basenames = set()
    for projectname in sorted(projectnames):
        for stage, res in context.stage.op_sro_check_pypi_whitelist(
                "get_releaselinks_perstage", projectname=projectname):
            if stage.ixconfig["type"] == "mirror":
                continue
            for link in res:
                if link.eggfragment:
                    key = link.eggfragment
                else:
                    key = link.basename
                if key not in basenames:
                    basenames.add(key)
                    all_links.append(link)
    links = []
    for link in sorted(all_links, key=attrgetter('projectname', 'version')):
        relpath = link.entrypath
        href = "/" + relpath
        href = URL(request.path).relpath(href)
        if link.eggfragment:
            href += "#egg=%s" % link.eggfragment
        elif link.md5:
            href += "#md5=%s" % link.md5
        links.extend([
            "/".join(relpath.split("/", 2)[:2]) + " ",
            html.a(link.basename, href=href),
            html.br(), "\n"])
    return Response(html.html(
        html.head(
            html.title(title)),
        html.body(
            html.h1(title), "\n",
            links)).unicode(indent=2))
