def pagure_url(path=None, remote=None, commit=None, line1=None, line2=None, **kwargs):
    url = "{remote}/{type}/{commit}/f/{path}"
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


def remote2http(remote):
    url = remote
    if remote.startswith("ssh://"):
        url = url.split("@", 1)[1]
        url = url.rsplit(".git")[0]
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
