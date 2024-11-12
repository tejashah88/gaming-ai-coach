from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.language_models.chat_models import BaseChatModel
from modules.ai_chatbot.messages import UserTextMessage, UserImageMessage

class LLMChatbot:
    def __init__(self, chat_model: BaseChatModel, system_message: str):
        self.chat_model: BaseChatModel = chat_model
        self.system_message: str = system_message


    def send_message(self, user_msgs: list[UserTextMessage | UserImageMessage], configurable_settings={}):
        input_messages = []

        if self.system_message:
            input_messages += [
                SystemMessage(
                    content=self.system_message
                )
            ]


        input_messages += [
            HumanMessage(
                content=[msg.as_msg_entry() for msg in user_msgs]
            )
        ]


        bot_response = self.chat_model.invoke(
            input_messages,
            config = {'configurable': configurable_settings}
        )

        return bot_response
