# from django.shortcuts import redirect
# from django.urls import reverse

# # 로그인 여부 check

# def login_required(function):
#     def wrap(request, *args, **kwargs):
#         user = request.session.get('user')
#         if not user:
#             return redirect (reverse('account:login'))

#         return function(request, *args, **kwargs)

#     return wrap