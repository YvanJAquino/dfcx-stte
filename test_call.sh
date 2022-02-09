#!/bin/bash

curl \
    -d '{
  "detectIntentResponseId": "fbdb34d8-c49e-442e-b14c-2d4c2e86f68b",
  "pageInfo": {
    "currentPage": "projects/oktony-cx/locations/global/agents/fda7e914-cce8-448a-ace7-56c7246eb2d4/flows/00000000-0000-0000-0000-000000000000/pages/ec05703f-b1da-4b0c-b324-4d18270509d3",
    "displayName": "Confirm User information"
  },
  "sessionInfo": {
    "session": "projects/oktony-cx/locations/global/agents/fda7e914-cce8-448a-ace7-56c7246eb2d4/sessions/aefe43-ae0-724-bab-cd999c062",
    "parameters": {
      "caller-name": {
        "name": "Daniel Cormier",
        "original": "Daniel Cormier"
      },
      "ssn": "012345678"
    }
  },
  "fulfillmentInfo": {
    "tag": "fuzzy_test"
  },
  "messages": [{
    "text": {
      "text": ["Great! Let\u0027s make sure i got that right."],
      "redactedText": ["Great! Let\u0027s make sure i got that right."]
    },
    "responseType": "HANDLER_PROMPT",
    "source": "VIRTUAL_AGENT"
  }, {
    "text": {
      "text": ["I have your full name as Daniel Cormier and your social security number as 012345678. Did I get that correct?"],
      "redactedText": ["I have your full name as Daniel Cormier and your social security number as 012345678. Did I get that correct?"]
    },
    "responseType": "ENTRY_PROMPT",
    "source": "VIRTUAL_AGENT"
  }],
  "text": "012345678",
  "languageCode": "en"
}' \
    -H 'Content-Type: application/json' \
    -X POST \
    http://localhost:8081/name-provided




