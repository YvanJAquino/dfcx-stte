from fastapi import FastAPI

from modules.models import WebhookRequest
from modules.whr_client import WebhookResponse
from modules.matcher import NameMatcher

matcher = NameMatcher(source_file='data/full_names.json')
# matcher = NameMatcher.from_file('ai-models/matcher.mdl')

app = FastAPI()

@app.post('/retry-full-name')
async def name_provided(webhook: WebhookRequest):
    parameters = webhook.sessionInfo.parameters
    response = WebhookResponse()

    name = parameters.get('retry_full_name')
    print("name:", name)
    if not name:
        response.add_text_response('retry_full_name was not found within the session parameters.')

    else:
        matches = matcher.match(name)
        best_match = matches[0]
        response.add_text_response(f'Okay. I heard {best_match}. Did I get it right this time?')

    return response


