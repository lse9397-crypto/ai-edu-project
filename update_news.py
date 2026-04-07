import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import urllib.parse

def get_google_news(keyword):
    """구글 뉴스 RSS를 통해 키워드 검색 결과를 가져옵니다."""
    encoded_keyword = urllib.parse.quote(keyword)
    # 한국어 뉴스 검색 RSS URL
    url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=ko&gl=KR&ceid=KR:ko"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []

    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'xml') # RSS는 XML 형식이므로 xml 파서 사용
        items = soup.find_all('item')

        for item in items[:8]: # 최신 뉴스 8개만 추출
            title = item.title.text
            link = item.link.text
            pub_date = item.pubDate.text
            source = item.source.text if item.source else "Google News"
            
            # 뉴스 제목에서 신문사 이름 분리 (보통 "제목 - 신문사" 형태)
            clean_title = title.split(' - ')[0]

            results.append({
                "title": clean_title,
                "date": datetime.now().strftime("%Y.%m.%d"), # 수집일 기준
                "source": source,
                "summary": f"'{keyword}'와(과) 관련된 최신 소식입니다.",
                "link": link,
                "category": "article",
                "type": "article"
            })
    except Exception as e:
        print(f"구글 뉴스 수집 중 오류: {e}")
    
    return results

def collect_all():
    # 1. 뉴스/기사 수집 (키워드: AI 교육)
    news_results = get_google_news("AI 교육")
    
    # 2. 학술/논문 수집 (키워드: AI 리터러시 논문)
    # 구글 뉴스에서도 학술 정보를 일부 다루므로 키워드를 달리하여 수집
    paper_raw = get_google_news("AI 리터러시 교육 논문")
    paper_results = []
    for p in paper_raw:
        p["category"] = "paper"
        p["type"] = "paper"
        paper_results.append(p)

    # --- 안전장치 (Dummy Data) ---
    # 수집된 데이터가 하나도 없을 경우 보여줄 기본 카드
    if not news_results:
        news_results.append({
            "title": "새로운 AI 교육 소식을 찾고 있습니다",
            "date": datetime.now().strftime("%Y.%m.%d"),
            "source": "시스템 알림",
            "summary": "현재 새로운 기사를 수집 중이거나 일시적인 연결 지연이 발생했습니다. 잠시 후 다시 확인해 주세요.",
            "link": "#",
            "category": "article",
            "type": "article"
        })

    data = {
        "article": news_results,
        "news": news_results, # index.html 호환용
        "paper": paper_results,
        "book": []
    }

    # 파일 저장
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"업데이트 완료! 기사: {len(news_results)}건, 논문: {len(paper_results)}건")

if __name__ == "__main__":
    collect_all()
