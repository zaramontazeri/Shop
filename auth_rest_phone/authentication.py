from django.contrib.auth.models import AnonymousUser
from auth_rest_phone.conf import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .serializers import phoneAndOTPSerializer
import uuid

uid = uuid.uuid4().hex
UserModel = get_user_model()

class CsrfExemptSessionAuthentication(BasicAuthentication):
    def enforce_csrf(self, request):
        print("heeeellllooooo")
        return  # To not perform the csrf check previously happening
class MobileOtpModelBackend(ModelBackend):
    def authenticate(self, request, phone=None, otp_sent=None, **kwargs):
        if phone :
            phoneAndOTPSerializer().validate(attrs={"phone":phone,"otp_sent":otp_sent})
            try:
                user = UserModel._default_manager.get_by_natural_key(phone)
                if self.user_can_authenticate(user):
                    user.register =False
                    return user
            except UserModel.DoesNotExist:
                password=uuid.uuid4().hex
                user = UserModel(phone=phone)
                user.set_password(password)
                user.is_active = True
                user.save()
                user.register =True
                return user
            else :
                return AnonymousUser()
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
