from devpi_server.views import url_for_entrypath
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
    projects = set()
    for stage, names in context.stage.op_sro("list_projects_perstage"):
        if stage.ixconfig["type"] == "mirror":
            continue
        projects.update(names)
    all_links = []
    basenames = set()
    for project in sorted(projects):
        for stage, res in context.stage.op_sro_check_mirror_whitelist(
                "get_releaselinks_perstage", project=project):
            if stage.ixconfig["type"] == "mirror":
                continue
            for link in res:
                if getattr(link, 'eggfragment', None):
                    key = link.eggfragment
                else:
                    key = link.basename
                if key not in basenames:
                    basenames.add(key)
                    all_links.append(link)
    links = []
    for link in sorted(all_links, key=attrgetter('basename')):
        href = url_for_entrypath(request, link.entrypath)
        entry = link.entry
        if getattr(entry, 'eggfragment', None):
            href += "#egg=%s" % entry.eggfragment
        elif entry.hash_spec:
            href += "#%s" % entry.hash_spec
        links.extend([
            "/".join(link.entrypath.split("/", 2)[:2]) + " ",
            html.a(link.basename, href=href),
            html.br(), "\n"])
    if not links:
        links = [html.p('No releases.')]
    return Response(html.html(
        html.head(
            html.title(title)),
        html.body(
            html.h1(title), "\n",
            links)).unicode(indent=2))
