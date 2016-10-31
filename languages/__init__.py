import os, yaml
from django.conf import settings


def trans(keyword):
    try:
        file_path = os.path.join(settings.BASE_DIR, 'languages', 'keywords.yaml')
        f = open(file_path)
        keywords = yaml.safe_load(f)
        f.close()
        sp = keyword.split('.')

        if len(sp) == 1:
            return keywords[settings.LANGUAGE_CODE][sp[0]]
        elif len(sp) == 2:
            return keywords[settings.LANGUAGE_CODE][sp[0]][sp[1]]
        elif len(sp) == 3:
            return keywords[settings.LANGUAGE_CODE][sp[0]][sp[1]][sp[2]]
    except:
        return keyword
