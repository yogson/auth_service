FROM python:3.11
WORKDIR /code
VOLUME /data
ENV USER_DATA_STORE="/data/user_data"
ENV USERS_STORE="/data/users"
COPY ./requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./ /code
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
