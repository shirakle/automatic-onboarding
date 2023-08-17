import dotenv
import concurrent.futures
from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel
import ast
from google.oauth2 import service_account
import streamlit as st
import logging
import os
import openai
import tiktoken


openai.api_key = st.secrets["openai"]["api_key"]

def trim_prompt(prompt):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(prompt)
    num_tokens = len(tokens)
    if num_tokens > 15000:
        trimmed_prompt = encoding.decode(tokens[0:15000])
        return trimmed_prompt
    return prompt

def process_question(question):
    # trim text since there is a maximum input limit of ~8000 tokens
    trimmed_question = ' '.join(question.split()[:6000])
    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        trimmed_question,
        temperature=0.3,
        max_output_tokens=1024,
    )
    return response.text.strip().strip('`').replace("json", "").replace("\n", "")

def process_question_gpt(question):
    question["terms"] = trim_prompt(question["terms"])
    print("-------terms: ", question["terms"])

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question["prompt"]},
        {"role": "assistant", "content": question["terms"]},
    ]
    chatbot_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
    )
    output = chatbot_response.choices[0].message["content"]

    return output.strip().strip('`').replace("json", "").replace("\n", "")


def get_response_single_prompt(prompt):
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["connections"]
    )
    aiplatform.init(credentials=credentials)
    aiplatform.init(project='datascience-393713')

    return process_question(prompt)

def get_response_url(url, extracted_text):

    print("secrets: ", st.secrets["connections"])
    logging.info(st.secrets["connections"])
    # Create API client.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["connections"]
    )
    print("credentials: ", credentials)
    logging.info(credentials)
    aiplatform.init(credentials=credentials)
    aiplatform.init(project='datascience-393713')

    get_merchant_name = f"Extract the company name from the following website: {url}. Return the answer in a JSON " \
                        f"format of one line, with key='company' and value='RESPONSE'"
    get_description = f"Use the following url: {url}. Describe the company in up to five sentences, and no less than " \
                      f"three sentences. Focus on what they do as a company, and what services they offer. Be neutral " \
                      f"and descriptive. Return the answer in a JSON format of one line, " \
                      f"with key='description' and value='Your RESULT'"
    get_industry = f"Review the following company website: {url}. See this list of one-word industry descriptions: " \
                   f"'Retail, Financial Services, Travel, Gaming, Crypto, Software Subscription, Gambling, " \
                   f"Ticketing, Delivery'. Choose the description that suits the provided company the most. You can " \
                   f"only use the options provided above, don't invent other options. Return the answer in a json " \
                   f"format of one line, with key='industry' and value='Your choice'"
    get_channels = f"Review the following company website: {url}. See this list of selling channel options: " \
                   f"'Website, Mobile app, 3rd party / reseller, Phone calls'. Choose only the options the provided " \
                   f"company uses to sell their products. You can only choose out the options provided above, " \
                   f"don't invent other options. Return the answer in a json format of one line, with key='channels' " \
                   f"and value='Your choices'"
    get_billing = f"Review the following company website: {url}. See this list of billing models: 'One time payment, " \
                  f"Subscriptions, Installments'. out of this list, Choose only the options the provided company " \
                  f"offers. You can only choose out the options provided above, don't show other options. Choose as " \
                  f"many answers as applicable, but not options that are not listed. Return the answer in a json " \
                  f"format of one line, with key='billings' and value='Your choices'"
    get_email_address = f"`Review the following company website: {url}. What is their customer support email? " \
                        f"Return the answer in a json format of one line, with key='emailAddress' " \
                        f"and value='Your choice'"
    get_terms_info = "`From the information in Terms of Service, answer the following three questions and return the " \
                     "answers in a json format: {'customer_support': answer_to_question_1, " \
                     "'cancellation': answer_to_question_2, 'refund_policy': answer_to_question_3}. " \
                     "1. What is the maximal timeframe mentioned " \
                     "per purchase for customer support? Summarize it and also provide the relevant paragraph " \
                     "from the Terms of Service and save it as quote. If there are any specific conditions for " \
                   "it, mention them. Provide URL for the source you use for your answer. Return the answer " \
                   "as a json in this format: {'timeframe': X, 'summary': X, 'quote': X , 'specificConditions': X, 'source': X} " \
                     "If the given information does not contain specific information about customer support replace X with 'NULL'. " \
                     "2. What is the maximal timeframe mentioned per purchase for the cancellation policy? Summarize " \
                     "it and also provide the relevant quotes from the Terms of Service. If there are any specific " \
                     "conditions for it, mention them. Provide URL for the source you use for your answer. " \
                     "Return the answer as a json in this format: {'timeframe': X, 'summary': X, 'quote': X , 'specificConditions': X, 'source': X}" \
                    "If the given information does not contain specific information about cancellation policy replace X with 'NULL'. " \
                     "3. Quote directly from the terms of service and " \
                    "return the refund policy of the company. return it as a json {'refundPolicy': X}. " \
                     "If the given information does not contain specific information about refund policy replace X with 'NULL'."
    get_customer_support = f"`From the information in Terms of Service, What is the maximal timeframe mentioned " \
                           f"per purchase for customer support? Summarize it and also provide the relevant paragraph " \
                           f"from the Terms of Service and save it as quote. If there are any specific conditions for " \
                           f"it, mention them. Provide URL for the source you use for your answer. Return the answer " \
                           f"in a json format of one line, with keys: ['timeframe', 'summary', 'quote' , " \
                           f"'specificConditions', 'source'] and values ['DAYS', 'SUMMARY', 'PARAGRAPH', " \
                           f"'SPECIFIC CONDITIONS', 'SOURCE']. If you do not have an answer to one of the options, " \
                           f"write 'NULL'."
    get_cancellation = f"`From the information in Terms of Service below, What is the maximal timeframe mentioned " \
                       f"per purchase for the cancellation policy? Summarize it and also provide the relevant " \
                       f"quotes from the Terms of Service. If there are any specific conditions for it, mention them. " \
                       f"Provide URL for the source you use for your answer. Return the answer in a json format of " \
                       f"one line, with keys: ['timeframe', 'summary', 'quote' , 'specificConditions', 'source'] " \
                       f"and values ['DAYS', 'SUMMARY', 'QUOTE', 'SPECIFIC CONDITIONS', 'SOURCE']. " \
                       f"If you do not have an answer to one of the options, write 'NULL'. "
    get_refund_policy = f"From the information in Terms of Service, Quote directly from the terms of service and " \
                        f"return the refund policy of the company. return it in a json format with key: 'refundPolicy' " \
                        f"and value: 'your REFUND POLICY'"
    terms = f"Terms of Service: '{extracted_text}'"
    questions_vertax = [get_merchant_name, get_description, get_industry, get_channels, get_billing, get_email_address]
    get_terms_info = {"prompt":get_terms_info, "terms":terms}

    # Using ThreadPoolExecutor to parallelize the processing of questions
    with concurrent.futures.ThreadPoolExecutor() as executor:
        responses_vertax = list(executor.map(process_question, questions_vertax))

    responses_gpt = process_question_gpt(get_terms_info)

    responses = responses_vertax + [responses_gpt]
    questions = questions_vertax + [get_terms_info["prompt"]]

    return responses, questions

