def collect_all():
    # 1. 뉴스/기사 수집
    news_results = get_google_news("AI 교육")
    
    # 2. 학술/논문 수집
    paper_results = get_google_news("AI 리터러시 교육 논문")
    for p in paper_results:
        p["category"] = "paper"
        p["type"] = "paper"

    # 3. 도서 정보 (구글 뉴스로 대체하거나 샘플 제공)
    book_results = get_google_news("인공지능 교육 도서 신간")
    for b in book_results:
        b["category"] = "book"
        b["type"] = "book"

    # --- 각 항목별 안전장치 (데이터가 0건일 때) ---

    # 기사 안내문
    if not news_results:
        news_results.append({
            "title": "최신 AI 교육 기사를 찾고 있습니다",
            "date": datetime.now().strftime("%Y.%m.%d"),
            "source": "시스템 알림",
            "summary": "현재 새로운 교육 기사를 수집 중입니다. 잠시 후 다시 확인해 주세요.",
            "link": "#", "category": "article", "type": "article"
        })

    # 논문 안내문
    if not paper_results:
        paper_results.append({
            "title": "관련 학술 논문을 분석 중입니다",
            "date": datetime.now().strftime("%Y.%m.%d"),
            "source": "시스템 알림",
            "summary": "AI 리터러시 및 교육 관련 최신 논문을 라이브러리에 업데이트 중입니다.",
            "link": "#", "category": "paper", "type": "paper"
        })

    # 도서 안내문
    if not book_results:
        book_results.append({
            "title": "추천 도서 목록을 준비하고 있습니다",
            "date": datetime.now().strftime("%Y.%m.%d"),
            "source": "시스템 알림",
            "summary": "예비 교사를 위한 AI 교육 필독서 정보를 정리 중입니다.",
            "link": "#", "category": "book", "type": "book"
        })

    # 최종 데이터 구조 생성
    data = {
        "article": news_results,
        "news": news_results, 
        "paper": paper_results,
        "book": book_results
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"업데이트 완료! 기사:{len(news_results)}, 논문:{len(paper_results)}, 도서:{len(book_results)}")
