import streamlit as st

st.set_page_config(
    page_title="StrongTies: Professional Social Graph",
    layout="wide",
    page_icon=":handshake:"
)

def main():
    st.markdown(
        """
        <style>
        .center-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 70vh;
        }
        .main-title {
            font-size: 3em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 0.2em;
            text-align: center;
        }
        .subtitle {
            font-size: 1.3em;
            color: #34495e;
            margin-bottom: 1em;
            text-align: center;
        }
        .info-box {
            background-color: #f4f6f8;
            border-radius: 8px;
            padding: 1em 2em;
            margin-bottom: 1em;
            border-left: 6px solid #2980b9;
            text-align: left;
            max-width: 500px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="center-container">
            <div class="main-title">StrongTies</div>
            <div class="subtitle">
                Analyze your professional network and discover high-potential introduction paths.<br>
                <span style="font-size:0.95em;">All processing is local; your data stays on your device.</span>
            </div>
            <div class="info-box">
                <b>Step 1:</b> Upload your LinkedIn-style CSV file to begin.<br>
                <b>Step 2:</b> Explore your professional social graph (coming soon).
            </div>
            <div class="info-box">
                <b>Note:</b> Graph analysis features will be available soon.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()