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


class toChucNghiLeAction(Action):

    def name(self) -> str:
        return "toChucNghiLeAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)

            result = session.run(
                'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent {name:"ToChucNghiLe"})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
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


class trachNhiemVaQuyenHanAction(Action):

    def name(self) -> str:
        return "trachNhiemVaQuyenHanAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            entities = tracker.latest_message["entities"]
            giangVien = next(
                (e["value"] for e in entities if e["entity"] == "GiangVien"), None
            )
            CBCS = next((e["value"] for e in entities if e["entity"] == "CBCS"), None)
            giangVienThinhGiang = next(
                (e["value"] for e in entities if e["entity"] == "GiangVienThinhGiang"),
                None,
            )
            answers = None
            entity = ""

            if giangVien:
                entity = "GiangVien"
            elif CBCS:
                entity = "CBCS"
            elif giangVienThinhGiang:
                entity = "GiangVienThinhGiang"
            if entity:
                result = session.run(
                    f'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer {{entity:"{entity}"}})-[:BELONG_TO]->(i:Intent {{name:"TrachNhiemVaQuyenHan"}})<-[:HAS_INTENT]-(do:DOCUMENT)'
                    f" return a,do,di LIMIT 1;"
                ).data()
                if result:
                    answers = [record["a"]["answer"] for record in result]
                    law = [
                        {
                            "name": record["di"]["name"],
                            "content": record["di"]["content"],
                        }
                        for record in result
                    ]
                    documents = [record["do"]["text"] for record in result]
            if answers:
                dispatcher.utter_message(text=format_answer(law, answers, documents))
            else:
                dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
            drv.close()
        return []


class NguyenTacLamViecAction(Action):

    def name(self) -> str:
        return "nguyenTacLamViecAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            a = tracker.latest_message["intent"]
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run(
                'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent {name:"NguyenTacLamViec"})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
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


class ThamQuyenPheDuyetCuocHopAction(Action):

    def name(self) -> str:
        return "thamQuyenPheDuyetCuocHopAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run(
                'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent {name:"ThamQuyenPheDuyetHop"})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
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


class TrachNhiemTiepCBCSAction(Action):

    def name(self) -> str:
        return "trachNhiemTiepCBCSAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            entities = tracker.latest_message["entities"]

            hieuTruong = next(
                (e["entity"] for e in entities if e["entity"] == "HieuTruong"), None
            )
            thuTruong = next(
                (e["entity"] for e in entities if e["entity"] == "ThuTruong"), None
            )

            if hieuTruong or thuTruong:
                result = session.run(
                    f'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer {{entity:"{hieuTruong or thuTruong}"}})-[:BELONG_TO]->(i:Intent {{name:"TrachNhiemTiepCBCS"}})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
                ).data()
                if result:
                    answers = [record["a"]["answer"] for record in result]
                    documents = [record["do"]["text"] for record in result]
                    law = [
                        {
                            "name": record["di"]["name"],
                            "content": record["di"]["content"],
                        }
                        for record in result
                    ]
                    dispatcher.utter_message(
                        text=format_answer(law, answers, documents)
                    )
                else:
                    dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
            else:
                dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
        # drv.close()
        return []


class LoaiHoiNghiVaHopAction(Action):

    def name(self) -> str:
        return "loaiHoiNghiVaHopAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run(
                'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent {name:"LoaiHoiNghiVaHop"})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
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


class LoaiChuongTrinhCongTacAction(Action):

    def name(self) -> str:
        return "loaiChuongTrinhCongTacAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run(
                'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent {name:"LoaiChuongTrinhCongTac"})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
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


class PhamViGiaiQuyetCongViecAction(Action):

    def name(self) -> str:
        return "phamViGiaiQuyetCongViecAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            entities = tracker.latest_message["entities"]

            thuTruong = next(
                (e["value"] for e in entities if e["entity"] == "ThuTruong"), None
            )
            phoThuTruong = next(
                (e["value"] for e in entities if e["entity"] == "PhoThuTruong"), None
            )
            answers = None
            entity = ""

            if thuTruong:
                entity = "ThuTruong"
            elif phoThuTruong:
                entity = "PhoThuTruong"
            if entity:
                result = session.run(
                    f'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer {{entity:"{entity}"}})-[:BELONG_TO]->(i:Intent {{name:"PhamViGiaiQuyetCongViec"}})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
                ).data()
                if result:
                    answers = [record["a"]["answer"] for record in result]
                    law = [
                        {
                            "name": record["di"]["name"],
                            "content": record["di"]["content"],
                        }
                        for record in result
                    ]
                    documents = [record["do"]["text"] for record in result]
            if answers:
                dispatcher.utter_message(text=format_answer(law, answers, documents))
            else:
                dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
            drv.close()
        return []


class TrinhTuToChucCuocHopHoiNghiAction(Action):

    def name(self) -> str:
        return "trinhTuToChucCuocHopHoiNghiAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run(
                'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent {name:"TrinhTuToChucHop"})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
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


class QuyTrinhXayDungChuongTrinhCongTacAction(Action):

    def name(self) -> str:
        return "quyTrinhXayDungChuongTrinhCongTacAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            entities = tracker.latest_message["entities"]
            nam = next((e["value"] for e in entities if e["entity"] == "Nam"), None)
            hocKy = next((e["value"] for e in entities if e["entity"] == "HocKy"), None)
            thang = next((e["value"] for e in entities if e["entity"] == "Thang"), None)
            quy = next((e["value"] for e in entities if e["entity"] == "Quy"), None)
            tuan = next((e["value"] for e in entities if e["entity"] == "Tuan"), None)

            answers = None
            entity = ""

            if nam:
                entity = "Nam"
            elif hocKy:
                entity = "HocKy"
            elif thang:
                entity = "Thang"
            elif quy:
                entity = "Quy"
            elif tuan:
                entity = "Tuan"
            if entity:
                result = session.run(
                    f'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer {{entity:"{entity}"}})-[:BELONG_TO]->(i:Intent {{name:"QuyTrinhXayDungChuongTrinhCongTac"}})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
                ).data()

                if result:
                    # answers = [record["a.answer"] for record in result]
                    answers = [record["a"]["answer"] for record in result]
                    law = [
                        {
                            "name": record["di"]["name"],
                            "content": record["di"]["content"],
                        }
                        for record in result
                    ]
                    documents = [record["do"]["text"] for record in result]
                    khoan = [record["a"]["khoan"] for record in result]
            if answers:
                dispatcher.utter_message(
                    text=format_answer(law, answers, documents, khoan)
                )
            else:
                dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
            drv.close()
        return []


class NguyenTacToChucCuocHopAction(Action):

    def name(self) -> str:
        return "nguyenTacToChucCuocHopAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run(
                'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent {name:"NguyenTacToChucHop"})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
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


class CanCuXayDungChuongTrinhCongTacAction(Action):

    def name(self) -> str:
        return "canCuXayDungChuongTrinhCongTacAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run(
                'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent {name:"CanCuXayDungChuongTrinhCongTac"})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
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


class TrinhVaKyVanBanAction(Action):

    def name(self) -> str:
        return "trinhVaKyVanBanAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run(
                'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent {name:"TrinhVaKyVanBan"})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
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


class ThamQuyenDuyetVaKyVanBanAction(Action):

    def name(self) -> str:
        return "thamQuyenDuyetVaKyVanBanAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run(
                'MATCH (di:DIEU)-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent {name:"ThamQuyenDuyetVaKyVanBan"})<-[:HAS_INTENT]-(do:DOCUMENT) return a,do,di LIMIT 1;'
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


class hoiVeDieuAction(Action):

    def name(self) -> str:
        return "hoiVeDieuAction"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            entities = tracker.latest_message["entities"]
            article_number = next(
                (e["value"] for e in entities if e["entity"] == "article_number"), None
            )
            document_name = next(
                (e["value"] for e in entities if e["entity"] == "document_name"), None
            )

            if article_number and document_name:
                result = session.run(
                    f'MATCH (di:DIEU {{name:"Điều {article_number}"}})-[:HAS_DIEU]->(a:Answer)-[:BELONG_TO]->(i:Intent)<-[:HAS_INTENT]-(do:DOCUMENT)'
                    f' WHERE do.text="{document_name}" ORDER BY a.khoan ASC '
                    f"RETURN a,di,do;"
                ).data()
                if result:

                    answers = [record["a"]["answer"] for record in result]
                    law = [
                        {
                            "name": record["di"]["name"],
                            "content": record["di"]["content"],
                        }
                        for record in result
                    ]
                    document = [record["do"]["text"] for record in result]
                    dispatcher.utter_message(text=format_answer(law, answers, document))
                else:
                    dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)
            else:
                dispatcher.utter_message(text=MESSAGE_FAILURE_RESPONSE)

        return []


class ActionFallbackHandler(Action):
    def name(self) -> Text:
        return "action_fallback_handler"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message["intent"].get("name")
        if intent == "nlu_fallback":
            dispatcher.utter_message(
                "Xin lỗi tôi không thể hiểu ý định của bạn! Bạn có thể thử hỏi lại hoặc liên hệ với bộ phận hỗ trợ để được giúp đỡ."
            )
        else:
            dispatcher.utter_message(
                "Xin lỗi, có vẻ như tôi không thể giúp bạn với điều đó."
            )
        return []


class ActionPhoGPTFallback(Action):

    def name(self) -> Text:
        return "action_phogpt_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get("text")

        try:
            response = requests.post(
                GPT4ALL_API, json={"message": user_message}, timeout=20
            )
            response.raise_for_status()
            print("PhoGPT API response:", response.json())
            answer = response.json().get("text", "")
            if not answer:
                answer = "Mình chưa có đủ thông tin để trả lời câu hỏi này."

        except Exception as e:
            print("Error occurred while calling PhoGPT API", e)
            answer = "Hệ thống AI nâng cao đang tạm thời không khả dụng."

        dispatcher.utter_message(text=answer)
        return []


class ActionAskOllamaPhoGPT(Action):

    def name(self) -> Text:
        return "action_fallback_ollama_phogpt"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # 1. Lấy tin nhắn người dùng
        user_message = tracker.latest_message.get("text")

        print("tracker", tracker.latest_message)

        # 2. Cấu hình API endpoint của Ollama
        ollama_url = "http://localhost:11434/api/generate"

        # 3. Tạo payload
        # Lưu ý: stream=False để Rasa đợi lấy toàn bộ câu trả lời rồi mới hiển thị
        payload = {
            "model": "phogpt",
            "prompt": user_message,
            "stream": False,
            "options": {
                "num_predict": 256,  # Giới hạn độ dài câu trả lời để phản hồi nhanh
                "temperature": 0.2,  # Giữ cho câu trả lời ổn định
                "num_ctx": 2048,  # Độ dài ngữ cảnh
            },
        }

        try:
            # 4. Gửi request
            # Timeout thấp để tránh treo chatbot nếu model xử lý quá lâu
            response = requests.post(ollama_url, json=payload, timeout=30)

            if response.status_code == 200:
                data = response.json()
                bot_response = data.get("response", "")

                # Xử lý làm sạch câu trả lời nếu cần
                if not bot_response.strip():
                    bot_response = "Xin lỗi, tôi chưa nghĩ ra câu trả lời."

                dispatcher.utter_message(text=bot_response)
            else:
                dispatcher.utter_message(text=f"Lỗi kết nối AI: {response.status_code}")

        except Exception as e:
            dispatcher.utter_message(
                text=f"Hệ thống đang bận, vui lòng thử lại sau. ({str(e)})"
            )

        return []
