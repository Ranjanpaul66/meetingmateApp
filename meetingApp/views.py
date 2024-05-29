from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from meetingApp.services import google_get_user_info
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework.views import APIView
from meetingApp.utils import save_events, get_calendar_events


class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/"
    client_class = OAuth2Client

class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter


class Get_user(APIView):
    def post(self, request):
        access_token = request.data["access_token"]

        if not access_token:
            return JsonResponse({'error': 'No access token provided'}, status=400)

        try:
            user_info = google_get_user_info(access_token)
            email = user_info.get('email')

            if not email:
                return JsonResponse({'error': 'No email found in user info'}, status=400)

            # Check if user exists
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # If user does not exist, create a new user
               user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=user_info.get('given_name', ''),
                    last_name=user_info.get('family_name', ''),
                    password=User.objects.make_random_password()
                )

            calendar_events = get_calendar_events(access_token)
            save_events(user, calendar_events)
            return JsonResponse({
                'user_info': user_info,
                'calendar_events': calendar_events,
            })
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



