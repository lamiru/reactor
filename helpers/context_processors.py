from config import env

def default(request):
    return {
        'ENV': env.ENV,
    }
