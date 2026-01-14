import os
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv
import requests

from actions.db import get_driver
from actions.utils import format_answer

load_dotenv()


NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
GPT4ALL_API = "http://127.0.0.1:8000/chat"
MESSAGE_FAILURE_RESPONSE = "Xin lỗi tôi không thể trả lời câu hỏi của bạn"
OLLAMA_URL = "http://localhost:11434/api/generate"


class customActionBase(Action):

    def name(self) -> str:
        return "customActionBase"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            intentName = tracker.latest_message["intent"].get("name")
            print("intentName", intentName)
            result = session.run(
                f'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent {{name:"{intentName}"}})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
            ).data()
            if result:
                answers = [record["a"]["answer"] for record in result]
                law = [
                    {"name": record["di"]["name"], "content": record["di"]["content"]}
                    for record in result
                ]
                documents = [record["do"]["text"] for record in result]
                dispatcher.utter_message(text=format_answer(law, answers, documents))
            else:
                dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
        # drv.close()
        return []
