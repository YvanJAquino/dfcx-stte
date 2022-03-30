# Copyright 2022 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi import FastAPI

from modules.models import WebhookRequest
from modules.whr_client import WebhookResponse
from modules.matcher import NameMatcher

matcher = NameMatcher(source_file='data/full_names.json')

app = FastAPI()


@app.post('/retry-full-name')
async def name_provided(webhook: WebhookRequest):
    # Get session parameters, get the retry_full_name, and prepare a response.
    parameters = webhook.sessionInfo.parameters
    name = parameters.get('retry_full_name')
    response = WebhookResponse()

    # If the name is missing, return a text response indicating not retry name
    # was not found within the session parameters.
    if not name:
        response.add_text_response('retry_full_name was not found within the session parameters.')
    else:
        matches = matcher.match(name)
        best_match = matches[0] # matches are sorted by scoring.
        best_match_name = best_match['source']
        response.add_text_response(f'Okay. I heard {best_match_name}. Did I get it right this time?')

    return response


