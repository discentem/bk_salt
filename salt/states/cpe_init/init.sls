#!py

def run():

    config = {}
    config['sync all'] = {
        'module.run': [
            {'name': 'saltutil.sync_all'},
            {'kwargs': {'refresh': True}}
        ]
    }
    config['manage hosts file'] = {
        'cpe_hosts.managed': []
    }
    config['enable touchid'] = {
        'cpe_touchid.managed': []
    }
    
    if __grains__['os_family'] == 'Windows':
        config['disable touchid'] = {
            'cpe_touchid.managed': [
                {'enabled': False}
            ]
        }

    return config