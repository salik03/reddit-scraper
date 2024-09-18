import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st

def setup_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scroll_down(driver, timeout):
    """
    Scroll down the page until the timeout occurs.
    """
    scroll_pause_time = 2  # Seconds to wait between scrolls
    last_height = driver.execute_script("return document.body.scrollHeight")

    end_time = time.time() + timeout
    while time.time() < end_time:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for page to load
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # If scroll height didn't change, we've reached the bottom
            break
        last_height = new_height

def scrape_reddit(driver, url, timeout=30, post_count_container=None):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="search-post"]')))

    scroll_down(driver, timeout)  # Scroll the page for a set time or until it can't scroll anymore

    posts = driver.find_elements(By.CSS_SELECTOR, '[data-testid="search-post"]')
    post_data = []

    for idx, post in enumerate(posts):
        try:
            # Extract the title
            title = post.find_element(By.CSS_SELECTOR, 'a.no-underline.text-sm.font-semibold').text
            
            # Extract post link
            post_link = post.find_element(By.CSS_SELECTOR, 'a.no-underline').get_attribute('href')

            # Attempt to find video or media URL
            media_url = None
            media_type = None
            try:
                img_element = post.find_element(By.CSS_SELECTOR, 'img')
                media_url = img_element.get_attribute('src')
                media_type = 'image'
            except Exception:
                try:
                    video_element = post.find_element(By.TAG_NAME, 'source')
                    media_url = video_element.get_attribute('src')
                    media_type = 'video'
                except Exception:
                    media_type = 'none'

            # Collect author id (username will need to be fetched via API or from post)
            try:
                author_id = post.get_attribute('data-faceplate-tracking-context')
                username = extract_author_id_from_json(author_id)  # Custom method to parse author_id
            except Exception:
                username = 'Unknown'

            post_data.append({
                "Label": title,
                "Username": username,
                "Link": post_link,
                "Media URL": media_url,
                "Media Type": media_type
            })

            # Update the real-time post count in the Streamlit UI
            if post_count_container:
                post_count_container.progress((idx + 1) / len(posts))

        except Exception as e:
            print(f"Error scraping post: {e}")

    return post_data

def extract_author_id_from_json(json_data):
    import json
    try:
        json_obj = json.loads(json_data)
        return json_obj.get('post', {}).get('author_id', 'Unknown')
    except Exception:
        return 'Unknown'

def streamlit_app():
    st.title("📋 Reddit Scraper - r/IndianDankMemes")

    st.write("This tool allows you to scrape posts from the specified Reddit page. Simply enter the URL and click start to begin scraping.")

    # Add an instruction section
    st.markdown("### 🔗 Input Reddit URL")
    st.write("Example: https://www.reddit.com/r/IndianDankMemes/")

    # Create an empty DataFrame to hold the scraped data
    scraped_data_df = pd.DataFrame()

    # URL to scrape
    reddit_url = st.text_input("Enter the Reddit URL you want to scrape:", placeholder="Paste the link here...")

    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("Start Scraping"):
            with st.spinner("Scraping posts..."):
                driver = setup_selenium()

                # Create an empty container to hold the real-time post count
                post_count_container = st.empty()

                # Scrape Reddit and pass the post count container to update real-time post count
                posts = scrape_reddit(driver, reddit_url, timeout=60, post_count_container=post_count_container)
                driver.quit()

                if posts:
                    scraped_data_df = pd.DataFrame(posts)

                    st.success("Scraping complete! Displaying results below.")
                    for post in posts:
                        # Show posts in a card-like structure
                        with st.expander(f"🔗 {post['Label']}", expanded=True):
                            st.write(f"👤 **Posted by**: {post['Username']}")
                            st.write(f"🔗 [Link to post]({post['Link']})")
                            if post["Media Type"] == 'image' and post["Media URL"]:
                                st.image(post["Media URL"])
                            elif post["Media Type"] == 'video' and post["Media URL"]:
                                st.video(post["Media URL"])
                            else:
                                st.write(f"Media URL: {post['Media URL']}")
                else:
                    st.write("No posts found.")
    
    # If the data has been scraped, show the download button in the sidebar
    if not scraped_data_df.empty:
        st.sidebar.markdown("### 📥 Download the Scraped Data")
        # Convert the DataFrame to CSV format
        csv_data = scraped_data_df.to_csv(index=False)

        # Create a green download button for the CSV file
        st.sidebar.download_button(
            label="Download data as CSV",
            data=csv_data,
            file_name='reddit_scraped_data.csv',
            mime='text/csv',
            key="download_csv",
            help="Click to download the scraped data"
        )

if __name__ == "__main__":
    streamlit_app()
