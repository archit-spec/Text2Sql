from playwright.sync_api import sync_playwright
import json

def scrape_youtube(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Go to YouTube search results page
        page.goto(f"https://www.youtube.com/results?search_query=chip+tune+music&sp=EgIwAQ%253D%253D")
        print(f"https://www.youtube.com/results?search_query={query}")

        # Wait for the search results to load
        page.wait_for_selector("ytd-video-renderer")
        print("ytd-video-renderer")

        # Scroll to load more videos
        for _ in range(50):  # Adjust the range for more or fewer scrolls
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)  # Wait for more videos to load

        # Extract video data
        videos = page.query_selector_all("ytd-video-renderer")
        video_data = []

        for video in videos:
            title_element = video.query_selector("a#video-title")
            link_element = video.query_selector("a#thumbnail")
            channel_name_element = video.query_selector("#channel-info #channel-name a")
            channel_link_element = video.query_selector("#channel-info #channel-name a")
            metadata_elements = video.query_selector_all("span.inline-metadata-item.style-scope.ytd-video-meta-block")

            title = title_element.get_attribute("title").strip() if title_element else "N/A"
            link = "https://www.youtube.com" + link_element.get_attribute("href") if link_element else "N/A"
            channel_name = channel_name_element.inner_text().strip() if channel_name_element else "N/A"
            channel_link = "https://www.youtube.com" + channel_link_element.get_attribute("href") if channel_link_element else "N/A"

            views = metadata_elements[0].inner_text().strip() if len(metadata_elements) > 0 else "N/A"
            upload_date = metadata_elements[1].inner_text().strip() if len(metadata_elements) > 1 else "N/A"

            video_data.append({
                "title": title,
                "link": link,
                "channel_name": channel_name,
                "channel_link": channel_link,
                "views": views,
                "upload_date": upload_date
            })

        browser.close()

        return video_data

# Use the function and save results to a JSON file
query = "react tutorial hindi"
videos = scrape_youtube(query)

with open("youtube_videos2.json", "w", encoding="utf-8") as f:
    json.dump(videos, f, ensure_ascii=False, indent=4)

print("Data has been scraped and saved to youtube_videos.json")
