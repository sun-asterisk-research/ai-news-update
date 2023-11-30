import logging
import openai
from datetime import datetime

# Import const from settings.py
from django.conf import settings

SYSTEM_MESSAGE = """You are an expert in summary the content from a blog. When I give you an raw text from public blog, please summary it in around 5 sentences in VIETNAMESE. Output summaried text must be less than 100 words in total"""

OPENAI_MODEL = "gpt-3.5-turbo"


class Summarizer:
    def __init__(self, retries=3, time_duration=3):
        self.api_key = settings.AZURE_OPENAI_KEY
        self.api_endpoint = settings.AZURE_OPENAI_ENDPOINT
        self.api_version = settings.AZURE_OPENAI_VERSION
        self.gpt_deployment_name = settings.AZURE_OPENAI_GPT_DEPLOYMENT_NAME

        self.system_message = SYSTEM_MESSAGE
        self.retries = retries
        self.time_duration = time_duration
        self.configure_openai()

    def configure_openai(self):
        openai.api_key = self.api_key
        openai.api_base = self.api_endpoint
        openai.api_type = "azure"
        openai.api_version = self.api_version

    def extract_info(self, query):
        for attempt in range(self.retries):
            try:
                res = openai.ChatCompletion.create(
                    engine=self.gpt_deployment_name,
                    temperature=0 + attempt * 0.1,
                    messages=[
                        {"role": "system", "content": self.system_message},
                        {"role": "user", "content": query},
                    ],
                )
                return res["choices"][0]["message"]["content"]

            except TimeoutError:
                # Handle API Timeout
                logging.error("[Summarizer] - OpenAI Timed out")

            except TypeError:
                # Handle API Timeout
                logging.error("[Summarizer] - OpenAI output not qualified")

            except openai.error.APIError as e:
                # Handle API error here, e.g. retry or log
                logging.error(f"[Summarizer] - OpenAI API returned an API Error: {e}")

            except openai.error.ServiceUnavailableError as e:
                # Handle Service Unavailable error
                logging.error(f"[Summarizer] - Service Unavailable: {e}")

            except openai.error.AuthenticationError as e:
                # Handle Authentication error here, e.g. invalid API key
                logging.error(
                    f"[Summarizer] - OpenAI API returned an Authentication Error: {e}"
                )

            except openai.error.APIConnectionError as e:
                # Handle connection error here
                logging.error(f"[Summarizer] - Failed to connect to OpenAI API: {e}")

            except openai.error.InvalidRequestError as e:
                # Handle connection error here
                logging.error(f"[Summarizer] - Invalid Request Error: {e}")

            except openai.error.RateLimitError as e:
                # Handle rate limit error
                logging.error(
                    f"[Summarizer] - OpenAI API request exceeded rate limit: {e}"
                )

            except Exception as e:
                # Handles all other exceptions
                logging.error(f"[Summarizer] - An exception has occurred. {e}")
            finally:
                pass

        return {"message": "Something wrong!"}

    def summary(self, user_query):
        openai_output = self.extract_info(user_query)
        return openai_output
