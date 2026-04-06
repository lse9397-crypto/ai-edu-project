import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_data_from_site(name, url, selector, title_tag, source_name, is_paper=False):
    """사이트별 맞춤 수집 함수"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 기사/논문 영역 찾기
        item = soup.select_one(selector)
        if not item: return None

        title = item.select_one(title_tag).text.strip()
        # 링크 처리 (상대경로 방지)
        link_tag = item.select_one('a')
        link = link_tag['href'] if link_tag else url
        if not link.startswith('http'):
            link = f"{url.split('.com')[0]}.com{link}" if '.com' in url else f"{url.split('.co.kr')[0]}.co.kr{link}"

        return {
            "title": title,
            "date": datetime.now().strftime("%Y.%m.%d"),
            "source": source_name,
            "summary": f"{source_name}에서 제공하는 최신 정보입니다.",
            "link": link,
            "category": "paper" if is_paper else "news"
        }
    except:
        return None

def collect_all():
    # 1. 뉴스 사이트 설정 (한겨레, 중앙일보, 마이니치, BBC 등)
    news_targets = [
        {"name": "연합뉴스", "url": "https://www.yna.co.kr/it/sci", "selector": ".list-type03 li", "tag": ".tit-news"},
        {"name": "한겨레", "url": "https://www.hani.co.kr/arti/economy/it", "selector": ".article-interface", "tag": ".article-title"},
        {"name": "중앙일보", "url": "https://www.joongang.co.kr/it", "selector": ".story_list li", "tag": ".headline"},
        {"name": "마이니치(日)", "url": "https://mainichi.jp/it/", "selector": ".articlelist li", "tag": ".articletitle"},
        {"name": "BBC(World)", "url": "https://www.bbc.com/innovation", "selector": "[data-testid='anchor-inner-wrapper']", "tag": "h2"}
    ]

    # 2. 학술 사이트 설정 (RISS, ERIC 등) - 검색 결과 페이지 기준
    paper_targets = [
        {"name": "RISS(학술)", "url": "http://www.riss.kr/search/Search.do?query=AI교육", "selector": ".numAndTitle", "tag": ".title"},
        {"name": "DBpia(학술)", "url": "https://www.dbpia.co.kr/search/search?query=AI교육", "selector": ".item", "tag": ".tit"},
        {"name": "ERIC(Global)", "url": "https://eric.ed.gov/?q=AI+education", "selector": ".eric_result", "tag": ".eric_rtitle"}
    ]

    news_results = []
    paper_results = []

    # 뉴스 수집
    for t in news_targets:
        res = get_data_from_site(t['name'], t['url'], t['selector'], t['tag'], t['name'])
        if res: news_results.append(res)

    # 논문 수집
    for t in paper_targets:
        res = get_data_from_site(t['name'], t['url'], t['selector'], t['tag'], t['name'], is_paper=True)
        if res: paper_results.append(res)

    # 데이터 저장 (기존 구조 유지)
    data = {
        "news": news_results,
        "paper": paper_results,
        "book": []
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"업데이트 완료: 뉴스 {len(news_results)}건, 논문 {len(paper_results)}건")

if __name__ == "__main__":
    collect_all()
