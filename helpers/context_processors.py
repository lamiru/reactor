from config import env
from accounts.models import Notification

def default(request):
    return {
        'ENV': env.ENV,
    }

def notifications(request):
    if request.user.is_authenticated:
        notification_list = Notification.objects.filter(user=request.user).order_by('-id')[:10]
    else:
        notification_list = None
    return {
        'notification_list': notification_list,
    }
