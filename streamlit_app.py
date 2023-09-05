import streamlit as st
from get_response_func import get_response_url, get_response_single_prompt
import ast
import pandas as pd
from text_extractor import WebpageTextExtractor

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
    st.markdown("Note: The information reliability must be verified (AI can get creative)")
    st.markdown("**Your feedback is appreciated!** At the bottom you will find a CSV template, download it and fill in the following: \n")
    st.markdown("like_or_dislike \n")
    st.markdown("comments: comments you have about the tool outputs \n")
    st.markdown("suggestion: suggestions for prompt improvement")
    st.markdown("Upload the CSV file to: https://drive.google.com/drive/folders/17TlhsWgsRqcForpTxrxosWLGd5BrZRF1?usp=drive_link")

    st.text_input("URL", key="URL")
    st.text_input("Terms URL", key="terms_url")

    # access the value
    url = st.session_state.URL
    terms_url = st.session_state.terms_url

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
        extractor = WebpageTextExtractor(terms_url)
        extracted_text = extractor.extract_text()

        responses, questions = get_response_url(url, extracted_text)

        st.subheader(f"**URL:** {url}")
        print("------responses: ", responses)
        merchant_name = responses[0]["company"] if responses[0] is not None else "Information not found"
        description = responses[1]["description"] if responses[1] is not None else "Information not found"
        industry = responses[2]["industry"] if responses[2] is not None else "Information not found"
        channels = responses[3]["channels"] if responses[3] is not None else "Information not found"
        billings = responses[4]["billings"] if responses[4] is not None else "Information not found"
        email_address = responses[5]["emailAddress"] if responses[5] is not None else "Information not found"
        customer_support = responses[6]["customer_support"] if responses[6] is not None else "Information not found"
        cancellation = responses[6]["cancellation"] if responses[6] is not None else "Information not found"
        refund_policy = responses[6]["refund_policy"] if responses[6] is not None else "Information not found"
        delivery_methods = responses[7]["delivery_methods"] if responses[7] is not None else "Information not found"
        liability = responses[7]["liability"] if responses[7] is not None else "Information not found"
        if len(responses) == 9:
            crypto_transfers = responses[8]["crypto_transfers"] if responses[8] is not None else "Information not found"
        else:
            crypto_transfers = "Information not found"

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

        st.subheader("customer_support")
        if customer_support != "NULL" and customer_support != "Information not found":
            st.write(f"**timeframe:** {customer_support['timeframe']}")
            st.write(f"**summary:** {customer_support['summary']}")
            st.write(f"**quote:** {customer_support['quote']}")
            st.write(f"**specificConditions:** {customer_support['specificConditions']}")
            st.write(f"**source:** {customer_support['source']}")
        else:
            st.write(f"Information not found")
            customer_support = "Information not found"

        st.subheader("cancellation")
        if cancellation != "NULL" and cancellation != "Information not found":
            st.write(f"**timeframe:** {cancellation['timeframe']}")
            st.write(f"**summary:** {cancellation['summary']}")
            st.write(f"**quote:** {cancellation['quote']}")
            st.write(f"**specificConditions:** {cancellation['specificConditions']}")
            st.write(f"**source:** {cancellation['source']}")
        else:
            st.write(f"Information not found")
            cancellation = "Information not found"

        st.subheader("refund_policy")
        if refund_policy != "NULL" and refund_policy != "Information not found":
            st.write(refund_policy)
        else:
            st.write(f"Information not found")
            refund_policy = "Information not found"

        st.subheader("delivery_methods")
        st.write(delivery_methods)

        st.subheader("liability")
        st.write(liability)

        st.subheader("crypto_transfers")
        st.write(crypto_transfers)

        st.divider()
        df = pd.DataFrame({"question": pd.Series(["merchant_name", "description", "industry", "channels",
                                                  "billings", "email_address", "customer_support", "cancellation",
                                                  "refund_policy", "delivery_methods", "liability", "crypto_transfers"]),
                           "response": pd.Series([merchant_name, description, industry, channels,
                                                  billings, email_address, customer_support, cancellation,
                                                  refund_policy, delivery_methods, liability, crypto_transfers]),
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

        # st.divider()
        #
        #
        # for i in range(len(questions)):
        #     st.divider()
        #     st.write(f"**Prompt**")
        #     st.write(f"{questions[i]}")
        #     st.write(f"**response**")
        #     st.write(f"{responses[i]}")

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
        single_response = get_response_single_prompt(st.session_state.prompt)
        st.write(f"**prompt**")
        st.write(st.session_state.prompt)
        st.write(f"**response**")
        st.write(single_response)
