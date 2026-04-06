import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_yna_ai_news():
    # 연합뉴스 IT/과학 섹션 (AI 관련 소식이 많음)
    url = "https://www.yna.co.kr/it/sci"
    headers = {"User-Agent": "Mozilla/5.0"} # 차단 방지용
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    news_list = []
    # 기사 목록 추출 (연합뉴스 구조에 맞춤)
    articles = soup.select('.list-type03 li')[:5] # 최신 5개만
    
    for article in articles:
        try:
            title = article.select_one('.tit-news').text.strip()
            link = "https:" + article.select_one('a')['href']
            # 요약문 (보통 기사 리스트의 서브 텍스트)
            summary = article.select_one('.lead').text.strip()[:100] + "..." 
            date = datetime.now().strftime("%Y.%m.%d") # 수집 날짜
            
            news_list.append({
                "title": title,
                "date": date,
                "source": "연합뉴스",
                "summary": summary,
                "link": link,
                "isOverseas": False
            })
        except Exception as e:
            continue
            
    return news_list

# 데이터 저장
latest_news = get_yna_ai_news()
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump({"news": latest_news, "paper": [], "book": []}, f, ensure_ascii=False, indent=4)

print("뉴스 데이터 업데이트 완료!")
