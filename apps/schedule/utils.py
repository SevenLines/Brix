def kont_obozn_process(title):
    return title.replace('(И,О)', '').strip() if title else ""
