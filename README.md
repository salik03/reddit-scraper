# Reddit Scraper

## Description

Reddit Scraper is a Streamlit-based web application designed to scrape posts from Reddit. It uses Selenium for automated browsing and scraping, allowing users to extract titles, links, media URLs, and more from a specified subreddit. The application is particularly tailored for scraping meme posts from subreddits like r/IndianDankMemes.

## Features

- **Automated Scraping:** Utilizes Selenium to navigate and scroll through Reddit pages.
- **Real-time Progress:** Displays real-time progress updates while scraping.
- **Media Extraction:** Extracts and displays images and videos from posts.
- **Data Download:** Allows users to download scraped data in CSV format.

## Installation

To get started with Reddit Scraper, follow these steps:

1. **Clone the Repository**

   ```sh
   git clone https://github.com/salik03/reddit-scraper.git
   ```

2. **Navigate to the Project Directory**

   ```sh
   cd reddit-scraper
   ```

3. **Set Up a Virtual Environment**

   Create and activate a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install the Required Packages**

   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit Application**

   ```sh
   streamlit run reddit.py
   ```

2. **Input Reddit URL**

   Open the application in your browser. Enter the Reddit URL of the subreddit you want to scrape, for example: `https://www.reddit.com/r/IndianDankMemes/`.

3. **Start Scraping**

   Click the "Start Scraping" button. The application will begin scraping posts and display them in real-time. You can see media content directly in the app and download the results as a CSV file from the sidebar.

## Code Overview

- `app.py`: The main Streamlit application file.
- `requirements.txt`: Lists all Python packages required for the project.
- `reddit.py`: Contains the scraping logic using Selenium.

## Dependencies

- **Selenium:** For automating browser actions.
- **Streamlit:** For creating the web application interface.
- **Pandas:** For data handling and CSV export.
- **WebDriver Manager:** For managing ChromeDriver installations.

## Contribution

If you would like to contribute to this project, please fork the repository, make your changes, and submit a pull request. For any issues or feature requests, please open an issue on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Selenium Documentation](https://www.selenium.dev/documentation/en/)
- [Streamlit Documentation](https://docs.streamlit.io/)
```
