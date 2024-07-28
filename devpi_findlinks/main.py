from devpi_server.views import url_for_entrypath
from html import escape
from operator import attrgetter
from pluggy import HookimplMarker
from pyramid.response import Response
from pyramid.view import view_config


server_hookimpl = HookimplMarker("devpiserver")


def get_entry_hash_spec(entry):
    return (
        entry.best_available_hash_spec
        if hasattr(entry, 'best_available_hash_spec') else
        entry.hash_spec)


def includeme(config):
    config.add_route(
        "findlinks",
        "/{user}/{index}/+findlinks")
    config.scan()


@server_hookimpl
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
        elif get_entry_hash_spec(entry):
            href += "#%s" % get_entry_hash_spec(entry)
        relpath = "/".join(link.entrypath.split("/", 2)[:2])
        links.append(
            f'{escape(relpath)} <a href="{escape(href)}">{escape(link.basename)}</a><br/>\n')
    links = (
        ''.join(str(x) for x in links)
        if links else
        '\n    <p>No releases.</p>')
    body = (
        f"<html>\n"
        f"  <head>\n"
        f"    <title>{escape(title)}</title></head>\n"
        f"  <body>\n"
        f"    <h1>{escape(title)}</h1>\n"
        f"{links}</body></html>")
    return Response(body)
