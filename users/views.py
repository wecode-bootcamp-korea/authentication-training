import json, bcrypt, re, jwt

from django.http            import JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError
from django.conf            import settings

from users.models       import User
from users.validation   import validate_email, validate_password

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)

            email        = data['email']
            password     = data['password']

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message" : "EMAIL_ALREADY_EXISTS"}, status=409)

            validate_email(email)
            validate_password(password)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email     = email,
                password  = hashed_password
            )

            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        except ValidationError as error:
            return JsonResponse({"message": error.message}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = User.objects.get(email=data['email'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status=401)

            access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({
                 "message"      : "SUCCESS",
                 "access_token" : access_token
            }, status=200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        except ValueError:
            return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_EMAIL"}, status=401)