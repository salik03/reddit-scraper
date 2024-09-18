import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st
from concurrent.futures import ThreadPoolExecutor

def setup_selenium():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scrape_reddit(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="search-post"]')))

    posts = driver.find_elements(By.CSS_SELECTOR, '[data-testid="search-post"]')
    
    post_data = []
    
    for post in posts:
        try:
            title = post.find_element(By.CSS_SELECTOR, 'a.text-sm.font-semibold').text
            post_link = post.find_element(By.TAG_NAME, 'a').get_attribute('href')
            
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
            
            post_data.append({
                "title": title,
                "link": post_link,
                "media_url": media_url,
                "media_type": media_type
            })
        except Exception as e:
            print(f"Error scraping post: {e}")
    
    return post_data

def scrape_usernames(driver, post_links):
    def fetch_username(link):
        try:
            driver.get(link)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/shreddit-app/div/div[1]/div/main/shreddit-post/div[1]/span[1]/div/div/span[1]/div/faceplate-hovercard/faceplate-tracker/a")))
            
            username_element = driver.find_element(By.XPATH, "/html/body/shreddit-app/div/div[1]/div/main/shreddit-post/div[1]/span[1]/div/div/span[1]/div/faceplate-hovercard/faceplate-tracker/a")
            username = username_element.text
            
            return {
                "link": link,
                "username": username
            }
        except Exception as e:
            print(f"Error finding username on {link}: {e}")
            return {
                "link": link,
                "username": None
            }

    usernames = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_username, post_links)
        usernames.extend(results)
    
    return usernames

def streamlit_app():
    st.title("Reddit Scraper - r/IndianDankMemes")

    reddit_url = "https://www.reddit.com/r/IndianDankMemes/search/?q=transgender&type=media&cId=54ac47e2-a739-4413-927b-349124ed5ffe&iId=2f44d501-024d-4ac9-a3bd-08d9a943e8e1&rdt=64459"
    
    if st.button("Scrape Reddit"):
        with st.spinner("Scraping posts..."):
            driver = setup_selenium()
            posts = scrape_reddit(driver, reddit_url)
            
            if posts:
                post_links = [post['link'] for post in posts]
                
                usernames = scrape_usernames(driver, post_links)
                driver.quit()
                
                for post in posts:
                    st.subheader(post["title"])
                    st.write(f"[Link to post]({post['link']})")
                    
                    if post["media_type"] == 'image' and post["media_url"]:
                        st.image(post["media_url"])
                    elif post["media_type"] == 'video' and post["media_url"]:
                        st.video(post["media_url"])
                    else:
                        st.write(f"Media URL: {post['media_url']}")
                    
                    username_info = next((item for item in usernames if item['link'] == post['link']), None)
                    if username_info:
                        st.write(f"Username: {username_info['username']}")
                    else:
                        st.write("Username not found.")
                
            else:
                st.write("No posts found.")

if __name__ == "__main__":
    streamlit_app()
