Project overview
"Your ultimate real-time gaming deal discovery platform."

DealFinder AI is a web-based price comparison tool designed to help video game enthusiasts discover the best deals on their favorite games across multiple platforms and vendors. The platform leverages real-time web scraping, intelligent data aggregation, and an interactive user interface to provide users with the most accurate and up-to-date pricing information. Whether you're hunting for the latest blockbuster or a hidden indie gem, DealFinder AI makes gaming more affordable and accessible.

Architecture Overview
User Interaction:
Users input a game title, select the platform(s), and optionally apply filters like price range, region, or edition.
Scraping Trigger:
The Python script runs immediately when the user submits the search. It fetches data from all configured vendors in real-time.
Data Aggregation:
The script consolidates results from various vendors, organizes them into a structured format (e.g., JSON or Pandas DataFrame), and filters out duplicates or irrelevant data.
Display Results:
Streamlit takes the processed data and renders it in a clean, scrollable list or grid view with optional sorting (e.g., by price, vendor).
