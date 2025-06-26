FROM python:3.13

ENV PATH="/.venv/bin:$PATH"

WORKDIR /final_project/
COPY . /final_project/

RUN pip3 install poetry


COPY poetry.toml ./
COPY poetry.lock ./
RUN poetry install --no-root

EXPOSE 8000

#
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]