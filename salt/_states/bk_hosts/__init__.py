def managed(name):

    ret = {
        'name': name,
        'changes': {},
        'result': True,
        'comment': '',
        'pchanges': {},
    }

    hosts_path = __salt__['grains.filter_by']({
        'default': '/etc/hosts',
        'Windows': 'C:\Windows\System32\drivers\etc\hosts'
        },
        grain='os_family'
    )

    lines = []
    line_marker = " # Salt Managed"
    with open(hosts_path, 'r') as hosts_file:
        for line in hosts_file:
            line = line.rstrip()
            if line.endswith(line_marker):
                pass
            else:
                lines.append(line)

    extra_entries = __salt__['pillar.get']('bk_hosts:extra_entries', None)
    if extra_entries:
        extra_entries = {k: v for k, v in extra_entries.items() if v}
        for ip, urls in extra_entries.items():
            entry = "{0} {1}".format(ip, ' '.join(urls))
            entry = entry.replace('\n', '')
            entry += line_marker
            lines.append(entry)

    if __opts__['test'] == True:
        final_hosts_file = __states__['file.managed'](hosts_path,
                                                      contents=lines, test=True)
        ret['changes'] = final_hosts_file['changes']
        if 'diff' in ret['changes']:
            ret['result'] = None
            ret['comment'] = "{0} would have been updated. See diff.".format(hosts_path)
        else:
            ret['result'] = True
            ret['comment'] = "No changes would have occurred".format(hosts_path)
            ret['comment'] += "\n{0} is in the correct state.".format(hosts_path)
    else:
        final_hosts_file = __states__['file.managed'](hosts_path,
                                                  contents=lines)
        ret['changes'] = final_hosts_file['changes']
        if 'diff' in ret['changes']:
            ret['comment'] = "{0} was updated. See diff.".format(hosts_path)
        else:
            ret['comment'] = "{0} is in the correct state.".format(hosts_path)

    if __salt__['pillar.get']('bk_hosts:extra_entries', None) is None:
        ret['comment'] += "\npillar['bk_hosts']['extra_entries'] is empty."

    return ret
