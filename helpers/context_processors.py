from config import env
from accounts.models import Notification

def default(request):
    return {
        'ENV': env.ENV,
    }

def notifications(request):
    notification_list = Notification.objects.filter(user=request.user).order_by('-id')[:10]
    return {
        'notification_list': notification_list,
    }
