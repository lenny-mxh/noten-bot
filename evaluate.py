def evaluate(fach):
    if 'eng' in fach:
        fach = 'Englisch'
        return fach
    elif 'Amat' in fach:
        fach = 'Akzentfach A-Mat'
        return fach
    elif 'bio' in fach:
        fach = 'Biologie'
        return fach
    elif 'che' in fach:
        fach = 'Chemie'
        return fach
    elif 'deu' in fach:
        fach = 'Deutsch'
        return fach
    elif 'fra' in fach:
        fach = 'Französisch'
        return fach
    elif 'geo' in fach:
        fach = 'Geografie'
        return fach
    elif 'gsc' in fach:
        fach = 'Geschichte'
        return fach
    elif 'inf' in fach:
        fach = 'Informatik'
        return fach
    elif 'mat' in fach:
        fach = 'Mathematik'
        return fach
    elif 'mus' in fach:
        fach = 'Musik'
        return fach
    elif 'phy' in fach:
        fach = 'Physik'
        return fach
    elif 'spm' in fach:
        fach = 'Sport'
        return fach
    elif 'TroMa' in fach:
        fach = 'Gitarre (-n Unterricht)'
        return fach
    elif 'wir' in fach:
        fach = 'Wirtschaft'
        return fach

