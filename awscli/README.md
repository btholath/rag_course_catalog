Verify Current AWS Identity
(.venv) bijut@b:~/rag_course_catalog/awscli$ aws sts get-caller-identity

Check Bedrock Access
(.venv) bijut@b:~/rag_course_catalog/awscli$ aws bedrock list-foundation-models --region us-east-1

(.venv) bijut@b:~/rag_course_catalog/awscli$ aws bedrock list-foundation-models \
  --region us-east-1 \
  --query "modelSummaries[?starts_with(modelId, 'amazon.titan') && contains(modelName, 'Text')].[modelId, modelName, providerName, modelLifecycle.status]" \
  --output table
-----------------------------------------------------------------------------------------
|                                 ListFoundationModels                                  |
+------------------------------------+------------------------------+---------+---------+
|  amazon.titan-tg1-large            |  Titan Text Large            |  Amazon |  ACTIVE |
|  amazon.titan-text-premier-v1:0    |  Titan Text G1 - Premier     |  Amazon |  ACTIVE |
|  amazon.titan-embed-g1-text-02     |  Titan Text Embeddings v2    |  Amazon |  ACTIVE |
|  amazon.titan-text-lite-v1:0:4k    |  Titan Text G1 - Lite        |  Amazon |  ACTIVE |
|  amazon.titan-text-lite-v1         |  Titan Text G1 - Lite        |  Amazon |  ACTIVE |
|  amazon.titan-text-express-v1:0:8k |  Titan Text G1 - Express     |  Amazon |  ACTIVE |
|  amazon.titan-text-express-v1      |  Titan Text G1 - Express     |  Amazon |  ACTIVE |
|  amazon.titan-embed-text-v1:2:8k   |  Titan Embeddings G1 - Text  |  Amazon |  ACTIVE |
|  amazon.titan-embed-text-v1        |  Titan Embeddings G1 - Text  |  Amazon |  ACTIVE |
|  amazon.titan-embed-text-v2:0:8k   |  Titan Text Embeddings V2    |  Amazon |  ACTIVE |
|  amazon.titan-embed-text-v2:0      |  Titan Text Embeddings V2    |  Amazon |  ACTIVE |
+------------------------------------+------------------------------+---------+---------+
(.venv) bijut@b:~/rag_course_catalog/awscli$ 
