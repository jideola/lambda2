resource "aws_iam_role" "lambda_role2" {
name   = "lambda_role2"
assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "sts:AssumeRole",
     "Principal": {
       "Service": "lambda.amazonaws.com"
     },
     "Effect": "Allow",
     "Sid": ""
   }
 ]
}
EOF
}

resource "aws_iam_policy" "iam_policy_for_lambda2" {

 name         = "aws_iam_policy_for_terraform_aws_lambda_role"
 path         = "/"
 description  = "AWS IAM Policy for managing aws lambda role"
 policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": [
       "logs:CreateLogGroup",
       "logs:CreateLogStream",
       "logs:PutLogEvents"
     ],
     "Resource": "arn:aws:logs:*:*:*",
     "Effect": "Allow"
   },
   {
    "Effect": "Allow",
    "Action": [
                "secretsmanager:GetSecretValue"
            ],
    "Sid": "AllowGetSecretValueOnSlackToken",
    "Resource": "arn:aws:secretsmanager:us-east-1:951708231033:secret:slack-token-cp14Ku"
   }
 ]
}
EOF
}
resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
 role        = aws_iam_role.lambda_role2.name
 policy_arn  = aws_iam_policy.iam_policy_for_lambda2.arn
}


data "archive_file" "zip_the_python_code" {
type        = "zip"
source_dir  = "cloudwatch_lambda"
output_path = var.output_path
}


resource "aws_lambda_function" "cw_lambda2" {
  filename                       = var.output_path
  function_name                  = var.function_name
  role                           = aws_iam_role.lambda_role2.arn
  handler                        = "lambda_function.lambda_handler"
  runtime                        = "python3.9"
  depends_on                     = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
}

resource "aws_sns_topic" "guardian2" {
  name = "guardian2"
}

resource "aws_sns_topic_subscription" "sns_topic_subscription_to_lambda2" {
  topic_arn = aws_sns_topic.guardian2.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.cw_lambda2.arn
}

resource "aws_lambda_permission" "lambda_trigger" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cw_lambda2.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.guardian2.arn
}