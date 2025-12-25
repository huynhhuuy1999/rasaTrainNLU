import os
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv
import requests

from actions.db import get_driver
load_dotenv()  


NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
GPT4ALL_API = "http://127.0.0.1:8000/chat"

class toChucNghiLeAction(Action):

    def name(self) -> str:
        return "toChucNghiLeAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            print("ok ne")
            
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run("MATCH (a:Answer)-[:BELONG_TO]->(i:Intent {name:\"ToChucNghiLe\"}) return a;").data()
            if result:
                answers = [record['a']['answer'] for record in result]
                dispatcher.utter_message(text=', '.join(answers))
            else:
                dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
        # drv.close()
        return []
class trachNhiemVaQuyenHanAction(Action):

    def name(self) -> str:
        return "trachNhiemVaQuyenHanAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            entities = tracker.latest_message['entities']
            giangVien = next((e['value'] for e in entities if e['entity'] == 'GiangVien'), None)
            CBCS = next((e['value'] for e in entities if e['entity'] == 'CBCS'), None)
            giangVienThinhGiang = next((e['value'] for e in entities if e['entity'] == 'GiangVienThinhGiang'), None)
            answers = None
            entity = ""
            
            if giangVien:
                entity = "GiangVien"
            elif CBCS:
                entity = "CBCS"
            elif giangVienThinhGiang:
                entity = "GiangVienThinhGiang"
            if entity:
                result = session.run(f"MATCH (a:Answer {{entity:\"{entity}\"}})-[:BELONG_TO]->(i:Intent {{name:\"TrachNhiemVaQuyenHan\"}}) return a.answer LIMIT 1;").data()
                if result:
                    answers = [record['a.answer'] for record in result]
            if answers:
                dispatcher.utter_message(text=', '.join(answers))
            else:
                dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
            drv.close()
        return []

class NguyenTacLamViecAction(Action):

    def name(self) -> str:
        return "nguyenTacLamViecAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run("MATCH (a:Answer)-[:BELONG_TO]->(i:Intent {name:\"NguyenTacLamViec\"}) return a;").data()
            if result:
                answers = [record['a']['answer'] for record in result]
                dispatcher.utter_message(text=', '.join(answers))
            else:
                dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
        # drv.close()
        return []

class ThamQuyenPheDuyetCuocHopAction(Action):

    def name(self) -> str:
        return "thamQuyenPheDuyetCuocHopAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run("MATCH (a:Answer)-[:BELONG_TO]->(i:Intent {name:\"ThamQuyenPheDuyetHop\"}) return a;").data()
            if result:
                answers = [record['a']['answer'] for record in result]
                dispatcher.utter_message(text=', '.join(answers))
            else:
                dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
        # drv.close()
        return []
class TrachNhiemThuTruongTrongTiepCBCSAction(Action):

    def name(self) -> str:
        return "trachNhiemThuTruongTrongTiepCBCSAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run("MATCH (a:Answer)-[:BELONG_TO]->(i:Intent {name:\"TrachNhiemThuTruongTrongTiepCBCS\"}) return a;").data()
            if result:
                answers = [record['a']['answer'] for record in result]
                dispatcher.utter_message(text=', '.join(answers))
            else:
                dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
        # drv.close()
        return []
class LoaiHoiNghiVaHopAction(Action):

    def name(self) -> str:
        return "loaiHoiNghiVaHopAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run("MATCH (a:Answer)-[:BELONG_TO]->(i:Intent {name:\"LoaiHoiNghiVaHop\"}) return a;").data()
            if result:
                answers = [record['a']['answer'] for record in result]
                dispatcher.utter_message(text=', '.join(answers))
            else:
                dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
        # drv.close()
        return []
class LoaiChuongTrinhCongTacAction(Action):

    def name(self) -> str:
        return "loaiChuongTrinhCongTacAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run("MATCH (a:Answer)-[:BELONG_TO]->(i:Intent {name:\"LoaiChuongTrinhCongTac\"}) return a;").data()
            if result:
                answers = [record['a']['answer'] for record in result]
                dispatcher.utter_message(text=', '.join(answers))
            else:
                dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
        # drv.close()
        return []
class PhamViGiaiQuyetCongViecAction(Action):

    def name(self) -> str:
        return "phamViGiaiQuyetCongViecAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            entities = tracker.latest_message['entities']
            thuTruong = next((e['value'] for e in entities if e['entity'] == 'ThuTruong'), None)
            phoThuTruong = next((e['value'] for e in entities if e['entity'] == 'PhoThuTruong'), None)
            answers = None
            entity = ""
            print('entity', entities)
            if thuTruong:
                entity = "ThuTruong"
            elif phoThuTruong:
                entity = "PhoThuTruong"
            if entity:
                result = session.run(f"MATCH (a:Answer {{entity:\"{entity}\"}})-[:BELONG_TO]->(i:Intent {{name:\"PhamViGiaiQuyetCongViec\"}}) return a.answer LIMIT 1;").data()
                if result:
                    answers = [record['a.answer'] for record in result]
            if answers:
                dispatcher.utter_message(text=', '.join(answers))
            else:
                dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
            drv.close()
        return []
class TrinhTuToChucCuocHopHoiNghiAction(Action):

    def name(self) -> str:
        return "trinhTuToChucCuocHopHoiNghiAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run("MATCH (a:Answer)-[:BELONG_TO]->(i:Intent {name:\"TrinhTuToChucHop\"}) return a;").data()
            if result:
                answers = [record['a']['answer'] for record in result]
                dispatcher.utter_message(text=', '.join(answers))
            else:
                dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
        # drv.close()
        return []
class QuyTrinhXayDungChuongTrinhCongTacAction(Action):

    def name(self) -> str:
        return "quyTrinhXayDungChuongTrinhCongTacAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            entities = tracker.latest_message['entities']
            nam = next((e['value'] for e in entities if e['entity'] == 'Nam'), None)
            hocKy = next((e['value'] for e in entities if e['entity'] == 'HocKy'), None)
            thang = next((e['value'] for e in entities if e['entity'] == 'Thang'), None)
            quy = next((e['value'] for e in entities if e['entity'] == 'Quy'), None)
            tuan = next((e['value'] for e in entities if e['entity'] == 'Tuan'), None)
            print('entity', nam)
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
                result = session.run(f"MATCH (a:Answer {{entity:\"{entity}\"}})-[:BELONG_TO]->(i:Intent {{name:\"QuyTrinhXayDungChuongTrinhCongTac\"}}) return a.answer LIMIT 1;").data()
                if result:
                    answers = [record['a.answer'] for record in result]
            if answers:
                dispatcher.utter_message(text=', '.join(answers))
            else:
                dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
            drv.close()
        return []
class NguyenTacToChucCuocHopAction(Action):

    def name(self) -> str:
        return "nguyenTacToChucCuocHopAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            session = drv.session(database=NEO4J_DATABASE)
            result = session.run("MATCH (a:Answer)-[:BELONG_TO]->(i:Intent {name:\"NguyenTacToChucHop\"}) return a;").data()
            if result:
                answers = [record['a']['answer'] for record in result]
                dispatcher.utter_message(text=', '.join(answers))
            else:
                dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
        # drv.close()
        return []

class ActionFallbackHandler(Action):
    def name(self) -> Text:
        return "action_fallback_handler"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if intent == 'nlu_fallback':
            dispatcher.utter_message("Xin lỗi tôi không thể hiểu ý định của bạn! Bạn có thể thử hỏi lại hoặc liên hệ với bộ phận hỗ trợ để được giúp đỡ.")
        else:
            dispatcher.utter_message("Xin lỗi, có vẻ như tôi không thể giúp bạn với điều đó.")
        return []
    
class ActionPhoGPTFallback(Action):

    def name(self) -> Text:
        return "action_phogpt_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get("text")

        try:
            response = requests.post(
                GPT4ALL_API,
                json={"message": user_message},
                timeout=20
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