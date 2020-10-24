from .rocketchat import RocketChat
from django.conf import settings


class ChatMixin(object):
    @property
    def chat_user_name(self):
        if self.email.split("@")[0] == settings.CHAT_SERVICE_ADMIN:
            return self.email.split("@")[0]
        username = self.email.replace("@", '-')
        return username

    def is_chat_registration_done(self, password):
        userQuery = (
            RocketChat().users_info(username=self.chat_user_name).json()
        )
        if userQuery['success']:
            return True
        else:
            return self.register_user(password)

    def do_chat_login(self, password):
        if self.is_chat_registration_done(password):
            response = (
                RocketChat()
                .users_create_token(username=self.chat_user_name)
                .json()
            )
            if response['success']:
                chat_user_id = response["data"]["userId"]
                authToken = response["data"]["authToken"]
                if self.chat_user_id is None:
                    self.chat_user_id = chat_user_id
                    return True, authToken
                else:
                    return False, authToken
            else:
                return False, False

    def register_user(self, password):
        creation_repsone = (
            RocketChat()
            .users_create(
                email=self.email,
                name=self.full_name,
                password=password,
                username=self.chat_user_name,
            )
            .json()
        )
        return creation_repsone

    def update_chat_user_info(self, password):
        creation_repsone = (
            RocketChat()
            .users_update(
                user_id=self.chat_user_id,
                email=self.email,
                name=self.full_name,
                password=password,
                username=self.chat_user_name,
            )
            .json()
        )
        return creation_repsone
