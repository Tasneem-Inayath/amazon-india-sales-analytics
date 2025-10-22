import streamlit as st
import os
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Amazon India Analytics", layout="wide")

# --- TITLE ---
st.sidebar.title("📊 Amazon India Analytics Dashboard")
page = st.sidebar.radio(
    "Go to:",
    ["Dashboard 1 (Q1–Q5)", "Dashboard 2 (Q6–Q30)", "EDA Explorer"]
)

# --- PAGE 1: DASHBOARD 1 ---
if page == "Dashboard 1 (Q1–Q5)":
    st.title("📈 Dashboard 1 – Overview (Questions 1–5)")
    st.markdown("""
    This dashboard covers key insights such as:
    - Revenue trends
    - Category performance
    - Growth analytics
    - Customer segmentation
    - Retention metrics
    """)
    st.markdown("---")
    st.markdown("### 🔗 Embedded Power BI Dashboard")
    st.components.v1.iframe("https://app.powerbi.com/reportEmbed?reportId=7e9a3033-3241-4330-bc07-f50dde7b62a6&autoAuth=true&ctid=a5bd300c-c3b3-41d8-87e0-1f5c8d364af3", height=750, width=1300) #type:ignore

# --- PAGE 2: DASHBOARD 2 ---
elif page == "Dashboard 2 (Q6–Q30)":
    st.title("📊 Dashboard 2 – Deep Dive (Questions 6–30)")
    st.markdown("""
    This dashboard includes:
    - Payment trends  
    - Delivery performance  
    - Brand market share  
    - Product lifecycle  
    - Prime member analytics and more  
    """)
    st.markdown("---")
    st.markdown("### 🔗 Embedded Power BI Dashboard")
    st.components.v1.iframe("https://app.powerbi.com/reportEmbed?reportId=fcef32d4-aa65-4f49-8deb-b0d3641e0279&autoAuth=true&ctid=a5bd300c-c3b3-41d8-87e0-1f5c8d364af3", height=750, width=1300) #type:ignore

# --- PAGE 3: EDA EXPLORER ---
elif page == "EDA Explorer":
    st.title("🔍 Exploratory Data Analysis (EDA) Viewer")

    # Root EDA folder
    eda_root = r"c:\Projects\amazonanalytics\EDA\eda_results"

    # Get all category folders dynamically
    categories = [f for f in os.listdir(eda_root) if os.path.isdir(os.path.join(eda_root, f))]
    categories.sort()

    selected_category = st.selectbox("Select Analysis Category:", categories)

    category_path = os.path.join(eda_root, selected_category)
    files = sorted(os.listdir(category_path))

    st.markdown(f"### 📂 {selected_category.replace('_', ' ').title()} Results")

    # Create a scrollable container for visuals
    with st.container():
        for file in files:
            file_path = os.path.join(category_path, file)

            if file.endswith(".png"):
                st.image(file_path, caption=file, use_column_width=True)
                st.markdown("---")
            elif file.endswith(".csv"):
                st.markdown(f"**📄 Summary Data – {file}**")
                try:
                    df = pd.read_csv(file_path)
                    st.dataframe(df.head(10))
                except Exception as e:
                    st.warning(f"Could not read {file}: {e}")
                st.markdown("---")
            elif file.endswith(".html"):
                st.components.v1.html(open(file_path, 'r', encoding='utf-8').read(), height=600, scrolling=True) #type:ignore
                st.markdown("---")

    st.info("Use the sidebar to explore other dashboards.")

