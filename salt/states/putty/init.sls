#!py

'''Configure Putty'''

# pylint: disable= C0111
def run():
    config = {}
    hive = "HKEY_CURRENT_USER\\"
    key = "Software\\SimonTatham\\PuTTY\\Sessions\\Default%20Settings"

    config[hive + key] = {
        'reg.present': [
            {'vname': 'FontHeight'},
            {'vdata': "25"},
            {'vtype': 'REG_DWORD'}
        ]
    }

    return config
