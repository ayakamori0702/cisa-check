import feedparser
from datetime import datetime, timedelta, timezone
import time

def fetch_last_24h_news():
    # CISAのフィード（NISTが空の時のための確実なソース）
    rss_url = "https://www.cisa.gov/cybersecurity-advisories/all.xml"
    feed = feedparser.parse(rss_url)
    
    # 現在時刻（UTC）と24時間前のしきい値を取得
    now = datetime.now(timezone.utc)
    time_threshold = now - timedelta(hours=24)

    print(f"--- 24時間以内の新着情報をチェック中 ---")
    print(f"基準時刻: {time_threshold.strftime('%Y-%m-%d %H:%M:%S')} UTC\n")
    
    new_entries = []
    for entry in feed.entries:
        # RSSの公開日時をパースしてUTCに変換
        published_time = datetime.fromtimestamp(time.mktime(entry.published_parsed), timezone.utc)
        
        # 24時間以内か判定
        if published_time > time_threshold:
            new_entries.append(entry)

    if not new_entries:
        print("過去24時間以内に新着記事はありませんでした。")
        return

    print(f"合計 {len(new_entries)} 件の新着記事が見つかりました。\n")

    for i, entry in enumerate(new_entries, 1):
        print(f"[{i}] {entry.title}")
        print(f"    Link: {entry.link}")
        print(f"    Date: {entry.published}")
        print("-" * 50)

if __name__ == "__main__":
    fetch_last_24h_news()