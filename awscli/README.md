Verify Current AWS Identity
(.venv) bijut@b:~/rag_course_catalog/awscli$ aws sts get-caller-identity

Check Bedrock Access
(.venv) bijut@b:~/rag_course_catalog/awscli$ aws bedrock list-foundation-models --region us-east-1

(.venv) bijut@b:~/rag_course_catalog/awscli$ aws bedrock list-foundation-models \
 --region us-east-1 \
 --query "modelSummaries[?starts_with(modelId, 'amazon.titan') && contains(modelName, 'Text')].[modelId, modelName, providerName, modelLifecycle.status]" \
 --output table

---

| ListFoundationModels |
+------------------------------------+------------------------------+---------+---------+
| amazon.titan-tg1-large | Titan Text Large | Amazon | ACTIVE |
| amazon.titan-text-premier-v1:0 | Titan Text G1 - Premier | Amazon | ACTIVE |
| amazon.titan-embed-g1-text-02 | Titan Text Embeddings v2 | Amazon | ACTIVE |
| amazon.titan-text-lite-v1:0:4k | Titan Text G1 - Lite | Amazon | ACTIVE |
| amazon.titan-text-lite-v1 | Titan Text G1 - Lite | Amazon | ACTIVE |
| amazon.titan-text-express-v1:0:8k | Titan Text G1 - Express | Amazon | ACTIVE |
| amazon.titan-text-express-v1 | Titan Text G1 - Express | Amazon | ACTIVE |
| amazon.titan-embed-text-v1:2:8k | Titan Embeddings G1 - Text | Amazon | ACTIVE |
| amazon.titan-embed-text-v1 | Titan Embeddings G1 - Text | Amazon | ACTIVE |
| amazon.titan-embed-text-v2:0:8k | Titan Text Embeddings V2 | Amazon | ACTIVE |
| amazon.titan-embed-text-v2:0 | Titan Text Embeddings V2 | Amazon | ACTIVE |
+------------------------------------+------------------------------+---------+---------+
(.venv) bijut@b:~/rag_course_catalog/awscli$

aws bedrock list-foundation-models \
 --profile ragcli \
 --region us-east-1 \
 --query "modelSummaries[?starts_with(modelId, 'amazon.titan')].[modelId, modelName]" \
 --output table

---

| ListFoundationModels |
+------------------------------------+----------------------------------+
| amazon.titan-tg1-large | Titan Text Large |
| amazon.titan-image-generator-v1:0 | Titan Image Generator G1 |
| amazon.titan-image-generator-v1 | Titan Image Generator G1 |
| amazon.titan-image-generator-v2:0 | Titan Image Generator G1 v2 |
| amazon.titan-text-premier-v1:0 | Titan Text G1 - Premier |
| amazon.titan-embed-g1-text-02 | Titan Text Embeddings v2 |
| amazon.titan-text-lite-v1:0:4k | Titan Text G1 - Lite |
| amazon.titan-text-lite-v1 | Titan Text G1 - Lite |
| amazon.titan-text-express-v1:0:8k | Titan Text G1 - Express |
| amazon.titan-text-express-v1 | Titan Text G1 - Express |
| amazon.titan-embed-text-v1:2:8k | Titan Embeddings G1 - Text |
| amazon.titan-embed-text-v1 | Titan Embeddings G1 - Text |
| amazon.titan-embed-text-v2:0:8k | Titan Text Embeddings V2 |
| amazon.titan-embed-text-v2:0 | Titan Text Embeddings V2 |
| amazon.titan-embed-image-v1:0 | Titan Multimodal Embeddings G1 |
| amazon.titan-embed-image-v1 | Titan Multimodal Embeddings G1 |
+------------------------------------+----------------------------------+
(.venv) bijut@b:~/rag_course_catalog/awscli$

For your RAG setup:
✅ Use Titan Text Embeddings V2 for the retriever/embedding step amazon.titan-embed-text-v2:0
✅ Use Titan Text G1 - Lite for the generator/response step amazon.titan-text-lite-v1:0:4k
amazon.titan-text-lite-v1

(.venv) bijut@b:~/rag_course_catalog/ingestion$ aws iam get-user-policy --user-name rag-cli-user --policy-name rag-cli-user-policy

An error occurred (AccessDenied) when calling the GetUserPolicy operation: User: arn:aws:iam::637423309379:user/rag-cli-user is not authorized to perform: iam:GetUserPolicy on resource: user rag-cli-user because no identity-based policy allows the iam:GetUserPolicy action
(.venv) bijut@b:~/rag_course_catalog/ingestion$

(.venv) bijut@b:~/rag_course_catalog/ingestion$ aws bedrock-runtime invoke-model --model-id amazon.titan-text-lite-v1 --body '{ "inputText": "What is the capital of France?", "textGenerationConfig": { "maxTokenCount": 100, "temperature": 0.5 } }' --region us-east-1 --profile ragcli --cli-binary-format raw-in-base64-out output.json

{
"contentType": "application/json"
}

(.venv) bijut@b:~/rag_course_catalog/ingestion$ cat output.json
{"inputTextTokenCount":7,"results":[{"tokenCount":46,"outputText":"\nParis is the capital of France. France has a total of 13 regions. Paris is the largest city in France. It is also the largest city in the European Union. Paris is the capital of France. ","completionReason":"FINISH"}]}

(.venv) bijut@b:~/rag_course_catalog/ingestion$

====================
(.venv) bijut@b:~/rag_course_catalog/ingestion$ aws bedrock-runtime invoke-model   --model-id amazon.titan-text-lite-v1   --body file://input.json   --content-type application/json   --accept application/json   --region us-east-1   --profile ragcli   --cli-binary-format raw-in-base64-out output.json
{
    "contentType": "application/json"
}
(.venv) bijut@b:~/rag_course_catalog/ingestion$ cat output.json 
{"inputTextTokenCount":7,"results":[{"tokenCount":79,"outputText":"\nParis is the capital of France. France's capital is Paris. It is located in the north-central part of the country. Paris is one of the most visited cities in the world. It is known for its rich history, culture, and architecture. Paris is also home to many famous landmarks, such as the Eiffel Tower, Notre Dame Cathedral, and the Louvre Museum. ","completionReason":"FINISH"}]}

=================================
