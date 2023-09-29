import pandas as pd
import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet
import requests
import os

# Create the ./data directory if it doesn't exist.
os.makedirs("./data", exist_ok=True)

def save_uploadedfile(uploadedfile):
  """Uploads a file to the ./data directory.

  Args:
    file: The file object to upload.
  """

  # Save the file to the ./data directory.
  with open(f"./data/{uploadedfile.name}", "wb") as f:
    f.write(uploadedfile.read())
  
  return st.success('Upload Completed')

def download_file_and_rename(url, file_path):
  """Downloads a file from a URL and renames it.

  Args:
    url: The URL of the file to download.
    file_path: The path to save the downloaded file.
  """

  # Split the URL into its components.
  url_parts = url.split("/")

  # Get the file name from the URL.
  file_name = url_parts[-1]

  # Download the file to the specified file path.
  response = requests.get(url)

  with open(file_path + file_name, "wb") as f:
    f.write(response.content)
  
  return st.success('Upload Completed')


st.set_page_config(layout="wide")
st.title('Data Preparation and Analysis with Mito')
st.caption('Created by Bayhaqy :sunglasses:')

option_rd = st.radio(
  "Choose option to upload your data",
  ["Upload via Direct File", "Upload via Link"],
  captions = ["If you have files", "If you only have link to file"])

if option_rd == 'Upload via Direct File':
  st.write('Please Upload the data')

  # Add a file uploader to the Streamlit app.
  uploadedfiles = st.file_uploader("Upload a file:",accept_multiple_files=True)

  for file in uploadedfiles:
    if uploadedfiles is not None:
      save_uploadedfile(file)

      # Display a message to the user.
      st.write("File uploaded successfully!")
else:
  st.write('Upload the data via Link')

  # Get the file URL from the user.
  file_url = st.text_input("Enter the URL of the file to download:")
  
  if file_url:
    # Download the file to the data directory.
    download_file_and_rename(file_url, "./data/")

    # Display a message to the user.
    st.write("File downloaded successfully!")

new_dfs, code = spreadsheet(import_folder='./data')
st.write(new_dfs)
st.code(code)

# If the user has not yet imported data, prompt them to do so.
if len(new_dfs) == 0:
  st.info("Please import a file to begin. Click **Import** > **Import Files** and select a file from the `data` folder.")
