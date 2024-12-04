FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

COPY lambda_function.py ${LAMBDA_TASK_ROOT}

COPY templates ${LAMBDA_TASK_ROOT}/templates

COPY assets ${LAMBDA_TASK_ROOT}/assets

CMD [ "lambda_function.handler" ]
