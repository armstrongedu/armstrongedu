from django.shortcuts import redirect


def email_checker(get_response):
    def middleware(request):
        response = get_response(request)
        user = request.user
        if (user.is_authenticated
            and request.path not in ['/authorization/confirm-email-start/',
                                     '/authorization/confirm-email',
                                     '/authorization/email-confirmed',]
            and not user.is_confirmed
            and not user.is_staff):
            return redirect('authorization:confirm-email-start')
        return response
    return middleware


def std_checker(get_response):
    def middleware(request):
        response = get_response(request)
        user = request.user
        if (user.is_authenticated
            and user.is_member()
            and not user.has_students()
            and request.path not in ['/authorization/add-students/',
                                     '/payment/subscribe-done/',]
            and not user.is_staff):
            return redirect('authorization:add-students')
        return response
    return middleware
