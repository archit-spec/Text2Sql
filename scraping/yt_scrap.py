from playwright.sync_api import sync_playwright
import json

class YouTubeScraper:
    FILTERS = {
        "creative_commons": "sp=EgIwAQ%3D%3D",
        "short_duration": "sp=EgIQAQ%3D%3D",
        "long_duration": "sp=EgIQAw%3D%3D",
        "last_hour": "sp=EgQIARAB",
        "today": "sp=EgQIAhAB",
        "this_week": "sp=EgQIAxAB",
        "this_month": "sp=EgQIBBAB",
        "this_year": "sp=EgQIBRAB"
    }

    def __init__(self):
        self.video_data = []

    def scrape_youtube(self, query, filter_name=None):
        filter_param = self.FILTERS.get(filter_name, "")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                # Go to YouTube search results page with filter
                search_url = f"https://www.youtube.com/results?search_query={query}&{filter_param}"
                page.goto(search_url)
                page.wait_for_selector("ytd-video-renderer")

                # Scroll to load more videos
                for _ in range(50):  # Adjust the range for more or fewer scrolls
                    page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                    page.wait_for_timeout(2000)  # Wait for more videos to load

                # Extract video data
                videos = page.query_selector_all("ytd-video-renderer")
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

                    self.video_data.append({
                        "title": title,
                        "link": link,
                        "channel_name": channel_name,
                        "channel_link": channel_link,
                        "views": views,
                        "upload_date": upload_date
                    })
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                browser.close()

    def save_to_json(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.video_data, f, ensure_ascii=False, indent=4)
        print(f"Data has been scraped and saved to {filename}")

    def get_video_data(self):
        return self.video_data


# Example usage:
if __name__ == "__main__":
    scraper = YouTubeScraper()
    filter_name = "creative_commons"  # Use one of the predefined filters
    scraper.scrape_youtube("Python programming", filter_name)
    scraper.save_to_json("youtube_data.json")
    data = scraper.get_video_data()
    print(data)