# Chatbot System Overview
## Introduction
This document provides a high-level overview of the chatbot system, detailing its key components and functionalities.

## Endpoints
The chatbot system comprises three primary endpoints, each serving a distinct purpose:

- **/ci-agent**: Handles configuration item queries.
- **/rca**: Manages root cause analysis requests.
- **/troubleshoot**: Addresses troubleshooting queries.
## Context Management
- **Session Storage**: Previous user messages are stored in session storage to maintain context across interactions. This provides context awareness functionality to the chatbot. Further we will be integrating this with a enterprise level session storage like redis session so that more number of chat details can be stored.
## Autoprompt Functionality
- **Role**: Each endpoint has a unique autoprompt that serves as the initial instruction to the LLM model. It guides the model in selecting the appropriate actions or sequences of actions to retrieve necessary data.
## External API Integrations
- At present we are making calls to a google cloud datastore where each of the mock data is being stored. The system makes firestore API calls to the following external systems for data retrieval and updation as required:
    - ServiceNow
    - Grafana
    - Confluence
- Future on gaining the enterprise API access we will be replacing the datastore API with the actual API calls.
## Computational Process
The chatbot's response generation involves a computational loop that iterates three times to ensure accuracy and relevance. Each loop follows these sequential steps:

1. **Thought**: Initial analysis and planning by the LLM.
2. **Action**: Execution of API calls to gather data.
3. **Action Response**: Evaluation of the data retrieved.
4. **Answer**: Formulation of a response to the user's query.
## Conclusion
This overview provides insight into the functional structure and operational flow of the chatbot system, highlighting its core components and processes.



