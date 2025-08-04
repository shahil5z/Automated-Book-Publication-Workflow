import streamlit as st
import os
from scraper.scraper import scrape_content_and_screenshot
from ai_agents.writer import generate_content
from ai_agents.reviewer import review_content
from ai_agents.editor import edit_content
from storage.version_control import store_version, search_versions
from rl_model.reward_model import calculate_reward
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()

# CSS for UI
st.markdown("""
    <style>
    .main { max-width: 900px; margin: 0 auto; padding: 20px; }
    .stButton>button {
        background-color: #005670;
        color: white;
        border-radius: 4px;
        padding: 8px 16px;
        font-size: 14px;
        margin: 5px 0;
    }
    .stTextInput, .stTextArea { border-radius: 4px; padding: 8px; }
    h2 { color: #333333; font-family: 'Arial', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'content' not in st.session_state:
    st.session_state.content = ""
if 'version_history' not in st.session_state:
    st.session_state.version_history = []
if 'current_version' not in st.session_state:
    st.session_state.current_version = 0
if 'screenshot_file' not in st.session_state:
    st.session_state.screenshot_file = None

# Content Acquisition Section
st.header("Content Acquisition")
st.write("Enter a URL to acquire source content and take a screenshot.")
url = st.text_input("Source URL", "", placeholder="Enter URL", key="url_input")
if st.button("Acquire Content", key="acquire_button"):
    content, screenshot_file = scrape_content_and_screenshot(url)
    if content:
        st.session_state.content = content
        st.session_state.screenshot_file = screenshot_file
        st.session_state.version_history.append({"version": 0, "content": content, "type": "original", "screenshot": screenshot_file})
        store_version(content, 0, "original", screenshot_file)
        st.write("Acquired Content Preview:")
        st.write(content[:500] + "..." if content else "No content acquired.")

# Display the screenshot if it exists
if st.session_state.screenshot_file:
    st.image(st.session_state.screenshot_file, caption="Webpage Screenshot", use_container_width=True)

# Content Processing Section
if st.session_state.content:
    st.header("Content Processing")
    st.write("Process content using AI-driven tools.")

    # Content Generation
    st.subheader("Generate Content")
    st.write("Create a rewritten version.")
    if st.button("Generate Content", key="generate_button"):
        generated_content = generate_content(st.session_state.content)
        reward = calculate_reward(st.session_state.content, generated_content)
        st.session_state.current_version += 1
        st.session_state.version_history.append({"version": st.session_state.current_version, "content": generated_content, "type": "generated", "reward": reward})
        store_version(generated_content, st.session_state.current_version, "generated", st.session_state.screenshot_file)
        st.write(f"Generated Content (Version {st.session_state.current_version}):")
        st.write(generated_content[:500] + "..." if generated_content else "Generation failed.")
        st.write(f"Quality Score: {reward}")

    # Content Review
    st.subheader("Review Content")
    st.write("Refine the latest content.")
    if st.button("Review Content", key="review_button"):
        reviewed_content = review_content(st.session_state.version_history[-1]["content"])
        reward = calculate_reward(st.session_state.version_history[-1]["content"], reviewed_content)
        st.session_state.current_version += 1
        st.session_state.version_history.append({"version": st.session_state.current_version, "content": reviewed_content, "type": "reviewed", "reward": reward})
        store_version(reviewed_content, st.session_state.current_version, "reviewed", st.session_state.screenshot_file)
        st.write(f"Reviewed Content (Version {st.session_state.current_version}):")
        st.write(reviewed_content[:500] + "..." if reviewed_content else "Review failed.")
        st.write(f"Quality Score: {reward}")

    # Human Editing
    st.header("Edit Manually")
    st.write("Manually edit the latest content.")

    # Increase the height parameter for a larger text area
    edited_content = st.text_area("Edit Content", st.session_state.version_history[-1]["content"], height=400, key="edit_content")

    if st.button("Save Edited Content", key="save_edit_button"):
        reward = calculate_reward(st.session_state.version_history[-1]["content"], edited_content)
        st.session_state.current_version += 1
        st.session_state.version_history.append({"version": st.session_state.current_version, "content": edited_content, "type": "edited", "reward": reward})
        store_version(edited_content, st.session_state.current_version, "edited", st.session_state.screenshot_file)
        st.success(f"Edited Content Saved (Version {st.session_state.current_version})")
        st.write(f"Quality Score: {reward}")

    # Version History Search
    st.header("Version History Search")
    st.write("Search through saved content versions.")
    search_query = st.text_input("Search Versions", key="search_input")
    if st.button("Search Versions", key="search_button"):
        results = search_versions(search_query)
        if results:
            st.write("Search Results:")
            for result in results:
                st.write(f"Version {result['version']}: {result['content'][:200]}... (Type: {result['type']}, Quality Score: {result.get('reward', 'N/A')})")
        else:
            st.info("No results found.")
