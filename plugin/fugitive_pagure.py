def pagure_url(path=None, remote=None, commit=None, line1=None, line2=None, **kwargs):
    if not is_pagure(remote):
        # It is very strange to return an empty string, I would expect
        # returning the URL unchanged, but this is how the other plugins do it
        return ""

    # Special case for generating commit URLs instead of file URLs, e.g.
    # :Gbrowse 460eae630
    if kwargs["type"] == "commit":
        url = "{remote}/c/{commit}"

    else:
        url = "{remote}/{type}/{commit}/f/{path}"
        if is_markup(path):
            url += "?text=True"
        if line1 and line1 != "0":
            url += "#_{line1}"
        if line2 and line2 != "0" and line2 != line1:
            url += "-{line2}"

    return url.format(
        remote=remote2http(remote),
        type=kwargs["type"],
        commit=commit,
        path=path,
        line1=line1,
        line2=line2)


def is_pagure(remote):
    domains = ["pagure.io", "src.fedoraproject.org"]
    return any(d in remote for d in domains)


def is_fork(remote):
    token = remote.rsplit("/")[3]
    return (token == 'forks')


def is_markup(path):
    ext = path[path.rfind("."):]
    return ext in (".rst", ".mk", ".md", ".markdown")


def remote2http(remote):
    url = remote
    if is_fork(remote):
        url = remote.replace('/forks/', '/fork/', 1)
    url = url.rsplit(".git")[0]
    if remote.startswith("ssh://"):
        url = url.split("@", 1)[1]
        url = "https://" + url
    return url


def main():
    import vim
    # An `a:opts` example:
    #   'path': 'frontend/coprs_frontend/commands/update_indexes_quick.py'
    #   'remote': 'ssh://git@pagure.io/copr/copr.git'
    #   'type': 'blob'
    #   'commit': 'master'
    #   'line1': 0
    #   'line2' can be missing or int
    opts = vim.eval('a:opts')

    url = pagure_url(**opts)
    vim.command("let s:url = '{0}'".format(url))
