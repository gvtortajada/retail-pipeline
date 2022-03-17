FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

ENV FLEX_TEMPLATE_PYTHON_PY_FILE="main.py"
ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="./setup.py"

COPY . .

RUN pip install -e .