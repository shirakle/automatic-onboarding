import streamlit as st
# from get_response_func import get_questionnaire_responses, get_response_single_prompt
import pandas as pd
from get_links import get_links
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from llm_responses_extractor import LlmResponsesExtractor#get_questionnaire_responses, get_response_single_prompt

st.header("AI-BOARDING :scream_cat: :100:")

st.radio(
    "",
    ["Get response by URL", "Try it yourself"],
    key="mode",
    label_visibility='hidden',
    horizontal=True,
)

if st.session_state.mode == "Get response by URL":

    st.markdown("Use this tool to collect information about the merchant as part of the onboarding research. "
             "Just fill in the merchant's website and click go! \n")
    st.markdown("**Your feedback is appreciated!** At the bottom you will find a CSV template, download it and fill in the following: \n")
    st.markdown("like_or_dislike \n")
    st.markdown("comments: comments you have about the tool outputs \n")
    st.markdown("suggestion: suggestions for prompt improvement")
    st.markdown("Upload the CSV file to: https://drive.google.com/drive/folders/17TlhsWgsRqcForpTxrxosWLGd5BrZRF1?usp=drive_link")

    st.text_input("URL", key="URL")
    st.markdown(
        "**The tool will automatically search for informative sub-URLS to scrape. For example: T&Cs, refund policy, about us etc.**")

    # access the value
    url = st.session_state.URL

    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            width: 300px;
            height: 50px;
            font-size: 40px;
            display: flex;
            margin: auto;
            background-color: #2E8B57;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if st.button('GO!'):

        # sub URLs
        with st.spinner('Looking for sub URLs...'):

            urls, source = get_links(url)
            st.success('Finished URLs search', icon="✅")
            st.write(f"URLs to scrape: {[url_dict['url'] for url_dict in urls]}")

        # LLM
        with st.spinner('Sending data to LLM...'):
            responses = LlmResponsesExtractor.get_questionnaire_responses(url, urls)

            st.success('Done!', icon="✅")

            st.subheader(f"**URL:** {url}")
            merchant_name = responses["merchant_name"]
            description = responses["description"]
            offerings = responses["offerings"]
            industry = responses["industry"]
            channels = responses["channels"]
            billings = responses["billings"]
            email_address = responses["emailAddress"]
            cancellation = responses["cancellation"]
            refund_policy = responses["refund_policy"]
            return_policy = responses["return_policy"]
            delivery_methods = responses["delivery_methods"]
            liability = responses["liability"]

            st.subheader("Merchant name")
            st.write(merchant_name)

            st.subheader("Merchant description")
            st.write(description)

            st.subheader("Industry")
            st.write(industry)

            st.subheader("channels")
            st.write(channels)

            st.subheader("billings")
            st.write(billings)

            st.subheader("email_address")
            st.write(email_address)

            st.subheader("offerings")
            st.write(offerings)

            st.subheader("cancellation")
            st.write(cancellation)

            st.subheader("refund_policy")
            st.write(refund_policy)

            st.subheader("return_policy")
            st.write(return_policy)

            st.subheader("delivery_methods")
            st.write(delivery_methods)

            st.subheader("liability")
            st.write(liability)

            st.divider()
            df = pd.DataFrame({"question": pd.Series(["merchant_name", "description", "industry", "channels",
                                                      "billings", "email_address", "offerings", "cancellation",
                                                      "refund_policy", "return_policy", "delivery_methods",
                                                      "liability", "url", "urls", "source"]),
                               "response": pd.Series([merchant_name, description, industry, channels,
                                                      billings, email_address, offerings, cancellation,
                                                      refund_policy, return_policy, delivery_methods, liability, url,
                                                    urls, source]),
                               "like_or_dislike": None,
                               "comments": None,
                               "suggestion": None})

            st.download_button(
                "Download as a CSV",
                df.to_csv(index=False).encode('utf-8'),
                "file.csv",
                "text/csv",
                key='download-csv'
            )
            st.dataframe(df)


if st.session_state.mode == "Try it yourself":
    st.write(f"We welcome new prompt suggestions :blush:, feel free to post them here: https://drive.google.com/drive/folders/1kv4nwb49IhfOl6-SHu-sBZjCH7mtLs3A?usp=drive_link")
    st.text_input("Prompt", key="prompt")
    st.markdown(
            """
            <style>
            div.stButton > button:first-child {
                width: 300px;
                height: 50px;
                font-size: 40px;
                display: flex;
                margin: auto;
                background-color: #2E8B57;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    if st.button('Try it yourself!'):
        single_response = LlmResponsesExtractor.get_response_single_prompt(st.session_state.prompt)
        st.write(f"**prompt**")
        st.write(st.session_state.prompt)
        st.write(f"**response**")
        st.write(single_response)
