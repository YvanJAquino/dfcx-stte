from fastapi import FastAPI

from modules.models import WebhookRequest
from modules.whr_client import WebhookResponse
from modules.matcher import NameMatcher

matcher = NameMatcher.from_file('ai-models/matcher.mdl')

app = FastAPI()

@app.post('/name-provided')
async def name_provided(webhook: WebhookRequest):
    parameters = webhook.sessionInfo.parameters
    response = WebhookResponse()

    name = parameters.get('caller-name').get('name')
    if not name:
        response.add_text_response(['caller-name was not found within the session parameters.'])
    else:
        matches = matcher.match(name)
        best_match = matches[0]
        response.add_text_response([f'caller-name: {name}.  Matching Algorithm: {best_match}'])

    return response


