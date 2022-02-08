# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from typing import List, Optional, Union, Any, Dict
from pydantic import BaseModel, validator

# https://cloud.google.com/dialogflow/cx/docs/reference/rpc/google.cloud.dialogflow.cx.v3#google.cloud.dialogflow.cx.v3.WebhookResponse

# https://googleapis.dev/nodejs/dialogflow-cx/latest/index.html
# https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/Fulfillment#ResponseMessage

class Text(BaseModel):
    text: List[str]
    allowPlaybackInterruption: Optional[bool]


class ConversationSuccess(BaseModel):
    metadata: Dict[Any, str]


class OutputAudioText(BaseModel):
    # conversation_success
    allowPlaybackInterruption: Optional[bool]
    text: Optional[str]
    ssml: Optional[str]

    @validator('ssml')
    def add_speak_tags(cls, ssml: str):
        if not ssml.startswith('<speak>'):
            ssml = '<speak>' + ssml
        if not ssml.endswith('/<speak>'):
            ssml += '</speak>'
        return ssml


class LiveAgentHandoff(BaseModel):
    metadata: Dict[Any, str]


class PlayAudio(BaseModel):
    allowPlaybackInterruption: Optional[bool]
    audioUri: str


class Segment(BaseModel):
    allowPlaybackInterruption: Optional[bool]
    audio: Optional[bytes]
    uri: Optional[str]


class MixedAudio(BaseModel):
    segments: List[Segment]


# class EndInteraction(BaseModel):
#     pass


class ResponseMessage(BaseModel):
    text: Optional[Text]
    payload: Optional[Dict[Any, str]]
    conversationSuccess: Optional[ConversationSuccess]
    outputAudioText: Optional[OutputAudioText]
    liveAgentHandoff: Optional[LiveAgentHandoff]
    playAudio: Optional[PlayAudio]
    mixedAudio: Optional[MixedAudio]
    # endInteraction: Optional[EndInteraction]


class FulfillmentResponse(BaseModel):
    messages: List[ResponseMessage] = []
    mergeBehavior: Optional[str]

    def add_messages(self, *messages):
        for message in messages:
            if isinstance(message, Text):
                self.messages.append(ResponseMessage(text=message))
            elif isinstance(message, OutputAudioText):
                self.messages.append(ResponseMessage(outputAudioText=message))


class WebhookResponse(BaseModel):
    fulfillmentResponse: FulfillmentResponse = FulfillmentResponse()
    # responses: Optional[List[ResponseMessage]] = None

    def to_json(self):
        return json.dumps(
            self.dict(exclude_none=True), 
            indent=2
        )

    def to_dict(self):
        return self.dict(exclude_none=True)

    def add_text_response(self, *texts, allowPlaybackInterruption=None):
        text = Text(text=list(texts), allowPlaybackInterruption=allowPlaybackInterruption)
        message = ResponseMessage(text=text)
        self.fulfillmentResponse.messages.append(message)

    def add_audio_text_response(self, text_or_ssml, ssml=True, allowPlaybackInterruption=None):
        if not ssml:
            output_audio_text = OutputAudioText(text=text_or_ssml, allowPlaybackInterruption=allowPlaybackInterruption)
        else:
            output_audio_text = OutputAudioText(ssml=text_or_ssml, allowPlaybackInterruption=allowPlaybackInterruption)        
        message = ResponseMessage(outputAudioText=output_audio_text)
        self.fulfillmentResponse.messages.append(message)

    def add_responses(self, *responses):
        self.fulfillmentResponse.add_messages(*responses)


