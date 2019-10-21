def handler(event, context):
    import cfnresponse
    import boto3, os, json
    from botocore.vendored import requests

    ssm_cl = boto3.client('ssm')
    req_type = event['RequestType']
    print(event)

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    def start_ssmautomation(event):
        doc_name = event['ResourceProperties']['DocumentName']
        ecr_repo = event['ResourceProperties']['ECRRepoName']
        stack_name = event['ResourceProperties']['StackName']
        qs_bucket = event['ResourceProperties']['QSS3BucketName']
        qs_bucket_prefix = event['ResourceProperties']['QSS3KeyPrefix']

        start_automation = ssm_cl.start_automation_execution(
            DocumentName= doc_name,
            Parameters={
                'ECRRepoName': [
                    ecr_repo
                ],
                'StackName': [
                    stack_name
                ],
                'QSS3BucketName': [
                    qs_bucket
                ],
                'QSS3KeyPrefix': [
                    qs_bucket_prefix
                ]
            },
        )

        cfnresponse.send(event, context, SUCCESS, start_automation, start_automation['AutomationExecutionId'])
    
    def delete_automation():
        cfnresponse.send(event, context, SUCCESS, 'delete', 'nothingtodo')

    actions = {
        'Create': start_ssmautomation,
        'Delete': delete_automation,
        'Update': start_ssmautomation
    }

    try:
        actions.get(req_type)(event)    
    except Exception as exc:
        error_msg = {'Error': '{}'.format(exc)}
        print(error_msg)
        cfnresponse.send(event, context, FAILED, error_msg)