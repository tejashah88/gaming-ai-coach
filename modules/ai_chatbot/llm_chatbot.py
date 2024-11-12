from langchain_core.messages import SystemMessage, HumanMessage

from modules.ai_chatbot.structs import UserTextMessage, UserImageMessage

class LLMChatbot:
    def __init__(self, chat_model, system_message):
        self.chat_model = chat_model
        self.system_message = system_message


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

        response = self.chat_model.invoke(
            input_messages,
            config = {'configurable': configurable_settings}
        )

        return response.content
