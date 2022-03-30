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

from json import dumps
from typing import Any, List, Dict, Optional, Union
from pydantic import BaseModel


class SessionInfo(BaseModel):
    session: str
    parameters: Optional[Dict[str, Any]]


class WebhookRequest(BaseModel):
    detectIntentResponseId: str
    languageCode: str
    text: Optional[Union[str, List[str]]]
    fuilfillmentInfo: Optional[Dict[str, Any]]
    intentInfo: Optional[Dict[str, Any]]
    pageInfo: Optional[Dict[str, Any]]
    sessionInfo: Optional[SessionInfo]
    messages: Optional[List[Dict[str, Any]]]
    payload: Optional[Dict[str, Any]]
    sentimentAnalysisResult: Optional[Dict[str, Any]]
    query: Optional[Dict[str, Any]]
    triggerEvent: Optional[str]
