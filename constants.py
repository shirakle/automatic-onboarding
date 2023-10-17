from dataclasses import dataclass


@dataclass(frozen=True)
class QuestionnairePrompts:
    NAME_DESC_INDUSTRY_OFFERINGS: str = "From the information in this website, answer the following four questions and return a json in the following format: " \
                                        "{'company': answer_to_question_1, " \
                                        "'description': answer_to_question_2, " \
                                        "'industry': answer_to_question_3, " \
                                        "'offerings': answer_to_question_4}. " \
                                        "1. Search the company name. Return the answer as a string. " \
                                        "2. Describe the company in up to five sentences, and no less than three " \
                                        "sentences. Focus on what they do as a company, and what services they offer. " \
                                        "Be neutral and descriptive. Return the answer as a string " \
                                        "3. See this list of one-word industry descriptions: " \
                                        "'Retail, Financial Services, Travel, Gaming, Crypto, Software Subscription, Gambling, Ticketing, Delivery'. " \
                                        "Choose one description that suits the provided company the most. You can " \
                                        "only use the options provided above, don't invent other options. Return the answer as a string." \
                                        "4. See this list of offerings descriptions: " \
                                        "'Physical Goods, Digital Goods, Software, In-Person Services, Personal Banking, Payment Facilitation, Investment Services, Accommodation, Top Up Services, Crypto Currencies, Gaming, Gambling, NFTs, Hotels, Car Rentals, Flights, Tickets'. " \
                                        "What type of offerings does the company sell? Choose only the options that " \
                                        "suits the provided company the most. You can only use the options provided " \
                                        "above, don't invent other options. You can also use your previous knowledge to answer this question. Return the answer as a string."
    CHANNELS_BILLINGS_DELIVERY_EMAIL: str = "From the information in this website, answer the following four questions and return the answers in a json format: " \
                                            "{'channels': answer_to_question_1, " \
                                            "'billings': answer_to_question_2, " \
                                            "'delivery_methods': answer_to_question_3," \
                                            "'emailAddress': answer_to_question_4}. " \
                                            "If the text from the website does not contain required information to answer " \
                                            "the question return 'NULL'. Don't answer based on your previous knowledge. " \
                                            "1. See this list of selling channel options: 'Website, Mobile app, 3rd party, Phone calls'. " \
                                            "Based on the information on the website, choose only the options the provided " \
                                            "company uses to sell their products. You can only choose out the options provided above, " \
                                            "don't invent other options. Return the answer as a list of strings " \
                                            "2. See this list of billing models: 'One time payment, Subscriptions, Installments'. " \
                                            "out of this list, choose only the options the provided company offers. " \
                                            "You can only choose out the options provided above, don't invent other options. " \
                                            "Choose as many answers as applicable, but not options that are not listed. Return the answer as a list of strings. " \
                                            "3. Does the merchant sell physical things? " \
                                            "If the merchant doesn't sell physical things return ['Merchant doesn't sell physical goods']. " \
                                            "If he does, what delivery methods does the seller offer? Shipping, in store pickup or other? " \
                                            "Return the answer as a list of strings. " \
                                            "4. What is the merchant's customer support email? Return the answer as a string."
    POLICIES: str = "From the information in this website, answer the following three questions and return the answers in a json format: " \
                    "{'cancellation': answer_to_question_1, " \
                    "'refund_policy': answer_to_question_2, " \
                    "'return_policy: answer_to_question_3}. " \
                    "If the text from the website does not contain required information to answer the question replace " \
                    "X with 'NULL'. Don't answer based on your previous knowledge. " \
                    "1.Summarize the cancellation policy on the website. Mention the specific conditions for cancellation. " \
                    "Provide the relevant quotes from the website and the URL for the source you use for your answer. " \
                    "Return the answer as a json in this format: {'summary': X, 'quote': X , 'source': X}" \
                    "2. Summarize the exact conditions to get a refund based on the information from the website. return it as a string. " \
                    "3. What is the maximum number of days for return? Summarize the exact conditions based on the information from the website. return it as a string."
    CRYPTO: str = "From the information in this website answer the following question. Does the platform use " \
                 "blockchain to transfer the crypto or the crypto transfer is done on it’s own platform? if the " \
                 "merchant's industry is not crypto return NULL. " \
                 "Return the answer as a json in this format: {'crypto_transfers': blockchain\internal system}"
    LIABILITY: str = "Based on the information on the website, who takes liability on the following topics? " \
                     "Chargebacks (fraud transactions and service), delivery issues and product quality? " \
                     "Return the answer as a json in this format: " \
                     "{'Chargebacks': X, 'delivery_issues': X, 'quality': X}. " \
                     "If this information is missing, replace X with NULL."
