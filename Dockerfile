FROM python:3.13

WORKDIR /final_project/

RUN pip3 install poetry

COPY . /final_project/

RUN poetry install --no-root

EXPOSE 8000

# ENV PATH="/final_project/.venv/bin:$PATH"
#
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]