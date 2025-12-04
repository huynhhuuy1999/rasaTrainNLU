import os
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from dotenv import load_dotenv

from actions.db import get_driver
load_dotenv()  


NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class toChucNghiLeAction(Action):

    def name(self) -> str:
        return "toChucNghiLeAction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[str, Any]):
        drv = get_driver()
        with drv.session() as session:
            print("abc",tracker.latest_message)
            
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
            
            
        #     result = session.run("MATCH (a:Answer)-[:BELONG_TO]->(i:Intent {name:\"QuyTrinhXayDungChuongTrinhCongTac\"}) return a;").data()
        #     if result:
        #         answers = [record['a']['answer'] for record in result]
        #         dispatcher.utter_message(text=', '.join(answers))
        #     else:
        #         dispatcher.utter_message(text="Xin lỗi tôi không thể trả lời câu hỏi của bạn")
        # # drv.close()
        return []