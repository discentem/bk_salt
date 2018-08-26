#!py

def run():
    pillar = {}
    pillar['apm_packages'] = [
        'language-terraform'
    ]

    apm_packages = list(__salt__['pillar.get']('apm_packages'))
    pillar['apm_packages'].append('apm_packages')

    return pillar
