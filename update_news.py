import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import urllib.parse

def get_google_news(keyword):
    """구글 뉴스 RSS를 통해 키워드 검색 결과를 가져옵니다."""
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ko&gl=KR&ceid=KR:ko"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []

    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'xml') 
        items = soup.find_all('item')

        for item in items[:8]: 
            title = item.title.text
            link = item.link.text
            source = item.source.text if item.source else "Google News"
            clean_title = title.split(' - ')[0]

            results.append({
                "title": clean_title,
                "date": datetime.now().strftime("%Y.%m.%d"),
                "source": source,
                "summary": f"'{keyword}'와(과) 관련된 최신 소식입니다.",
                "link": link,
                "category": "article",
                "type": "article"
            })
    except Exception as e:
        print(f"수집 중 오류 ({keyword}): {e}")
    
    return results

def collect_all():
    # 1. 뉴스/기사 수집
    news_results = get_google_news("AI 교육")
    
    # 2. 학술/논문 수집
    paper_results = get_google_news("AI 리터러시 교육 논문")
    for p in paper_results:
        p["category"] = "paper"
        p["type"] = "paper"

    # 3. 도서 정보 수집
    book_results = get_google_news("인공지능 교육 도서 신간")
    for b in book_results:
        b["category"] = "book"
        b["type"] = "book"

    # --- 각 항목별 안전장치 (데이터가 0건일 때) ---
    if not news_results:
        news_results.append({
            "title": "최신 AI 교육 기사를 찾고 있습니다",
            "date": datetime.now().strftime("%Y.%m.%d"),
            "source": "시스템 알림",
            "summary": "현재 새로운 교육 기사를 수집 중입니다. 잠시 후 다시 확인해 주세요.",
            "link": "#", "category": "article", "type": "article"
        })

    if not paper_results:
        paper_results.append({
            "title": "관력 학술 논문을 분석 중입니다",
            "date": datetime.now().strftime("%Y.%m.%d"),
            "source": "시스템 알림",
            "summary": "AI 리터러시 및 교육 관련 최신 논문을 라이브러리에 업데이트 중입니다.",
            "link": "#", "category": "paper", "type": "paper"
        })

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

if __name__ == "__main__":
    collect_all()
