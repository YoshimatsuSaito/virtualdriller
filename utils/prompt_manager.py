import os
from typing import Optional

import openai
from dotenv import load_dotenv

load_dotenv(".env")
openai.api_key = os.getenv("OPENAI_API_KEY")


class Driller:
    """Drill users presentation"""
    def __init__(self, client_information: str, model_name: str="gpt-3.5-turbo") -> None:
        self.model_name = model_name
        self.list_message: list[dict[str, str]] = []
        self.client_information = client_information
        self.set_system_message()

    def set_system_message(self) -> None:
        """set the system message"""
        system_message = f"""
        あなたは、下記のような立場に置かれているクライアントとして提案者の提案を検討します。

        {self.client_information}

        提案者は、下記の形式であなたに提案を行います。
        【提案者】
        '提案内容'

        あなたは、下記の観点で、上記の提案内容を可能な限り厳しく検討します。
        ・不明瞭・情報不足な点があれば、その旨を指摘します
        ・論理の飛躍や抜け漏れがあれば、その旨を指摘します
        ・追加の要望があれば、その旨を指摘します

        あなたの返答はできるだけ短く簡潔でなければなりません。
        あなたの返答は以下の形式をとります。

        【クライアント】
        '指摘の番号'. 'あなたの指摘内容'
        """
        self.list_message.append(
            {
                "role": "system", "content": system_message
            }
        )
    
    def drill(self) -> None:
        """drill the text"""
        res = openai.ChatCompletion.create(
            model=self.model_name,
            messages=self.list_message,
            max_tokens=1048,
        )
        assistant_message = res["choices"][0]["message"]["content"]
        self.list_message.append(
            {
                "role": "assistant", "content": assistant_message
            }
        )

    def hear(self, message: str) -> None:
        """hear explanation from the presentor"""
        message = "【提案者】\n" + message
        self.list_message.append(
            {
                "role": "user", "content": message
            }
        )
    