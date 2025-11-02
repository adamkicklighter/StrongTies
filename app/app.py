import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from data_loader import load_connections

st.set_page_config(
    page_title="StrongTies: Professional Social Graph",
    layout="wide",
    page_icon="🤝"
)

def main():
    st.markdown(
        """
        <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Main container styling */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        
        /* Typography */
        .main-title {
            font-size: 3rem;
            font-weight: 700;
            color: #1a202c;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }
        
        .subtitle {
            font-size: 1.1rem;
            color: #4a5568;
            margin-bottom: 2rem;
            line-height: 1.6;
        }
        
        /* Card styling */
        .card {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
            margin-bottom: 1.5rem;
        }
        
        .info-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .info-card h3 {
            color: white;
            margin-top: 0;
            font-size: 1.2rem;
        }
        
        .info-card p {
            margin: 0.5rem 0;
            opacity: 0.95;
        }
        
        /* Feature list styling */
        .feature-list {
            background: #f7fafc;
            border-radius: 8px;
            padding: 1.5rem;
            border-left: 4px solid #4299e1;
        }
        
        .feature-item {
            padding: 0.5rem 0;
            color: #2d3748;
        }
        
        /* File uploader styling */
        .stFileUploader {
            border: 2px dashed #cbd5e0;
            border-radius: 8px;
            padding: 1rem;
            background: #f7fafc;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: transform 0.2s;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102,126,234,0.4);
        }
        
        /* Input styling */
        .stTextInput>div>div>input {
            border-radius: 8px;
            border: 1px solid #cbd5e0;
            padding: 0.5rem 1rem;
        }
        
        /* Success/Error messages */
        .stSuccess, .stError {
            border-radius: 8px;
            padding: 1rem;
        }
        
        /* Dataframe styling */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header Section
    st.markdown('<div class="main-title">🤝 StrongTies</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">'
        'Analyze your professional network and discover high-potential introduction paths. '
        'All processing happens locally — your data never leaves your device.'
        '</div>',
        unsafe_allow_html=True
    )
    
    st.divider()

    # Main Content
    col1, col2 = st.columns([3, 2], gap="large")
    
    with col1:
        st.markdown("### 📁 Upload Your Data")
        st.markdown("Upload one or more LinkedIn connections CSV files (e.g., alice_connections.csv, bob_connections.csv).")

        uploaded_files = st.file_uploader(
            "Choose your LinkedIn connections CSV files",
            type="csv",
            accept_multiple_files=True,
            help="Upload CSVs named like alice_connections.csv, bob_connections.csv"
        )

        user_id = None
        available_users = []

        if uploaded_files:
            # Extract user identifiers from file name prefixes
            for file in uploaded_files:
                filename = file.name
                if filename.endswith("_connections.csv"):
                    prefix = filename.replace("_connections.csv", "")
                    available_users.append(prefix)
                elif filename.endswith(".csv"):
                    prefix = filename.replace(".csv", "")
                    available_users.append(prefix)
            available_users = list(set(available_users))  # Remove duplicates

            if available_users:
                user_id = st.selectbox(
                    "Your Identifier",
                    options=available_users,
                    help="Select your identifier (from file name prefix) to analyze your network"
                )

        if uploaded_files and user_id:
            st.markdown("")  # spacing
            if st.button("🚀 Analyze Network", use_container_width=True):
                with st.spinner("Processing your network..."):
                    try:
                        # Find the file matching the selected user_id
                        selected_file = None
                        for file in uploaded_files:
                            filename = file.name
                            if filename.startswith(user_id):
                                selected_file = file
                                break
                        if not selected_file:
                            st.error("Could not find a file for the selected identifier.")
                        else:
                            temp_path = os.path.join("temp_uploaded.csv")
                            with open(temp_path, "wb") as f:
                                f.write(selected_file.getbuffer())
                            df = load_connections(temp_path, user_id)

                            st.success(f"✅ Successfully loaded {len(df)} connections for {user_id}!")

                            # Display metrics
                            metric_col1, metric_col2, metric_col3 = st.columns(3)
                            with metric_col1:
                                st.metric("Total Connections", len(df))
                            with metric_col2:
                                st.metric("Network Nodes", "Coming Soon")
                            with metric_col3:
                                st.metric("Introduction Paths", "Coming Soon")

                            st.markdown("### 📊 Your Connections")
                            st.dataframe(df, use_container_width=True, height=400)

                            os.remove(temp_path)
                    except Exception as e:
                        st.error(f"❌ Error loading CSV: {e}")
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
    
    with col2:
        with st.expander("🎯 How It Works", expanded=True):
            st.markdown(
                """
                <div class="info-card">
                    <h3>🎯 How It Works</h3>
                    <p><strong>1.</strong> Upload your LinkedIn connections CSV</p>
                    <p><strong>2.</strong> We build your professional social graph</p>
                    <p><strong>3.</strong> Discover optimal introduction paths</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with st.expander("✨ Features", expanded=False):
            st.markdown(
                """
                <div class="feature-list">
                    <div style="font-weight: 600; margin-bottom: 0.5rem; color: #2d3748;">✨ Features</div>
                    <div class="feature-item">🔒 <strong>100% Private</strong> - All data stays local</div>
                    <div class="feature-item">🎯 <strong>Smart Analysis</strong> - Find the best paths</div>
                    <div class="feature-item">📊 <strong>Visual Insights</strong> - Coming soon</div>
                    <div class="feature-item">📈 <strong>Network Metrics</strong> - Coming soon</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with st.expander("ℹ️ How to export your LinkedIn connections"):
            st.markdown("""
            1. Go to LinkedIn Settings & Privacy
            2. Click on "Data Privacy"
            3. Select "Get a copy of your data"
            4. Choose "Connections" and download
            5. **Only upload the minimum data needed for analysis:** first name, last name, company, and position. Do not include contact details.
            6. Upload the CSV file to StrongTies
            """)

        with st.expander("👥 Who Should Use StrongTies?", expanded=False):
            st.markdown(
                """
                <div class="info-card" style="background: linear-gradient(135deg, #4299e1 0%, #48bb78 100%);">
                    <h3>👥 Who Should Use StrongTies?</h3>
                    <p><strong>•</strong> Small, trusted groups (2–5 people) who know each other well</p>
                    <p><strong>•</strong> Willing to help and make meaningful introductions</p>
                    <p><strong>•</strong> Not for large, anonymous, or commercial use</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with st.expander("🛡️ Ethical Principles", expanded=False):
            st.markdown(
                """
                <div class="info-card" style="background: linear-gradient(135deg, #ed8936 0%, #f6e05e 100%);">
                    <h3>🛡️ Ethical Principles</h3>
                    <p><strong>Privacy First:</strong> Your data stays local—never uploaded or shared externally.</p>
                    <p><strong>Reciprocity:</strong> Built for mutual support, not for exploiting networks.</p>
                    <p><strong>Transparency:</strong> All analysis is explainable and inspectable.</p>
                    <p><strong>Noncommercial Use:</strong> Free for personal and group use only.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with st.expander("🔐 Privacy & Security"):
            st.markdown("""
            - **No data upload**: Everything processes locally
            - **No tracking**: We don't collect any analytics
            - **Open source**: Review the code anytime
            - **Your data, your control**: Delete anytime
            - **Important:** Please do **not** upload contact details (such as emails or phone numbers) for your connections. Only upload the minimum data needed for analysis.
            """)

        # --- New: Link to Full User Guide ---
        st.markdown(
            """
            <div style="margin-top: 1rem; text-align: center;">
                <a href="https://github.com/adamkicklighter/StrongTies/blob/main/user-guide.md" target="_blank" style="color: #4299e1; font-weight: 600;">
                    📖 Read the full StrongTies User Guide
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Footer
    st.divider()
    st.markdown(
        '<div style="text-align: center; color: #718096; font-size: 0.9rem; padding: 1rem 0;">'
        'StrongTies • Licensed under Polyform Noncommercial 1.0.0 • '
        '<a href="https://github.com/adamkicklighter/StrongTies" style="color: #4299e1;">View on GitHub</a>'
        '</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()