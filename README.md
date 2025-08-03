# Automated Book Publication Workflow

This project provides an automated system designed to streamline the process of acquiring, generating, reviewing, and editing content for book publication. It leverages AI models, web scraping, and a version control system to enhance efficiency and productivity.

## Features

- **Content Acquisition**: Scrape text content and take a screenshot from a specified URL using Playwright and BeautifulSoup.
- **AI-Driven Processing**: Generate, review, and edit content using OpenAI's models.
- **Version Control**: Store and manage different versions of content with metadata, leveraging ChromaDB.
- **Streamlit Interface**: A simple, interactive web application for managing the workflow.

## Technologies Used

- **Python**: The core programming language.
- **Streamlit**: For the web interface.
- **Playwright**: For taking screenshots of web pages.
- **BeautifulSoup**: For web scraping.
- **OpenAI API**: For AI-driven content generation and review.
- **ChromaDB**: Hypothetical database for storing content versions.
- **dotenv**: For environment variable management.

## Setup Instructions

1. **Clone the Repository**

    ```bash
    git clone https://github.com/shahil5z/Automated-Book-Publication-Workflow.git
    cd Automated-Book-Publication-Workflow

2. **Create a Virtual Environment**

python -m venv venv
# Activate it:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

3. **Install Dependencies**

    pip install -r requirements.txt
    playwright install

4. **Set Up Environment Variables**

    OPENAI_API_KEY=your_openai_api_key_here
    CHROMA_DB_PATH=chromadb_path_here

5. **Run the Application**

    streamlit run main.py

## Usage

1. Content Acquisition: Enter a URL in the Streamlit app to scrape text content and capture a screenshot.
2. Content Processing: Use AI tools to generate, review, or manually edit content. Save and track different versions.
3. Version Management: Search and view different versions of content stored in ChromaDB.