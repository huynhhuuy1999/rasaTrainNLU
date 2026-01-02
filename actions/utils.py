def format_answer(law, answers):
    try:
        # check answers hợp lệ
        if not answers or not isinstance(answers, (list, tuple)):
            raise ValueError

        answer_text = answers[0]

        # nếu có law thì thêm "Căn cứ ..."
        if law and isinstance(law, (list, tuple)) and len(law) > 0:
            return f"Căn cứ {law[0].lower()}:\n{answer_text}"

        # không có law → chỉ trả về answer
        return answer_text

    except Exception:
        return "Xin lỗi tôi không thể trả lời câu hỏi của bạn"
