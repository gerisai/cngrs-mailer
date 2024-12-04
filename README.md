# CNGRS Mailer

Lambda function to send mails triggered by SQS

##  Test
1. Copy env file and fill with custom values
```shell
$ cp .env .env.local
```

2. Log in using CLI
```shell
$ aws sso login
```

3. Run test script with an event type
```shell
./test.sh user
```