FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV PORT=8080

# --target must match the Python function name, NOT the decorator name.
# @functions_framework.cloud_event is just a decorator; the callable is handle_contact_message.
CMD exec functions-framework \
      --target=handle_contact_message \
      --signature-type=http \
      --port=$PORT
