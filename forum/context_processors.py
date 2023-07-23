from accounts.models import Alert

def alerts_count(request):
    if request.user.is_authenticated:
        alerts_count = Alert.objects.filter(user=request.user, is_read=False).count()
    else:
        alerts_count = 0
    
    return {'alerts_count': alerts_count}