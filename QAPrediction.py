import json
import boto3

def lambda_handler(event, context):
    try:
        region = "us-east-1"
        endpoint_name = "huggingface-question-answering"

        runtime = boto3.client("sagemaker-runtime", region_name=region)

        body = event.get("body", {})

        if isinstance(body, str):
            body = json.loads(body)

        context_text = body.get("context")
        question_text = body.get("question")

        if not context_text or not question_text:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps({
                    "error": "Se requieren 'context' y 'question'"
                })
            }

        payload = {
            "inputs": {
                "context": context_text,
                "question": question_text
            }
        }

        response = runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType="application/json",
            Body=json.dumps(payload)
        )

        result = response["Body"].read().decode("utf-8")
        parsed_result = json.loads(result)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(parsed_result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }
