import feedparser
from datetime import datetime, timedelta, timezone
import time

def fetch_news():
    # ターゲットリスト（CISAとJPCERT）
    sources = [
        {"name": "🇺🇸 CISA (Cybersecurity Advisories)", "url": "https://www.cisa.gov/cybersecurity-advisories/all.xml"},
        {"name": "🇯🇵 JPCERT/CC (Alerts & Reports)", "url": "https://www.jpcert.or.jp/rss/jpcert.rdf"}
    ]
    
    # 現在時刻と、30日前（720時間）のしきい値を設定
    now = datetime.now(timezone.utc)
    time_threshold = now - timedelta(hours=720)

    print(f"==========================================")
    print(f"   SECURITY ADVISORY MONITOR (Last 30 Days)")
    print(f"   Check Time: {now.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"==========================================\n")

    for source in sources:
        print(f"--- {source['name']} ---")
        feed = feedparser.parse(source['url'])
        entries_found = 0

        for entry in feed.entries:
            # 日時情報の取得（published_parsed または updated_parsed を使用）
            pub_struct = getattr(entry, 'published_parsed', None) or getattr(entry, 'updated_parsed', None)
            
            if pub_struct:
                # 構造体から日時に変換
                pub_time = datetime.fromtimestamp(time.mktime(pub_struct), timezone.utc)
                
                # 30日以内か判定
                if pub_time > time_threshold:
                    entries_found += 1
                    print(f"[{entries_found}] {entry.title}")
                    print(f"    Link: {entry.link}")
                    print(f"    Date: {pub_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
                    print()

        if entries_found == 0:
            print("過去30日間に新着記事はありませんでした。")
        
        print("\n" + "-"*40 + "\n")

if __name__ == "__main__":
    fetch_news()
