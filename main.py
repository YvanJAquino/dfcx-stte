from fastapi import FastAPI

from modules.models import WebhookRequest
from modules.whr_client import WebhookResponse
from modules.matcher import NameMatcher

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import joblib

matcher = NameMatcher(source_file='data/full_names.json')

app = FastAPI()

@app.post('/name-provided')
async def name_provided(webhook: WebhookRequest):
    parameters = webhook.sessionInfo.parameters
    response = WebhookResponse()

    name = parameters.get('caller-name').get('name')
    print("name:", name)
    if not name:
        response.add_text_response('caller-name was not found within the session parameters.')

    else:
        matches = matcher.match(name)
        best_match = matches[0]
        response.add_text_response(f'caller-name: {name}.  Matching Algorithm: {best_match}')

    return response


