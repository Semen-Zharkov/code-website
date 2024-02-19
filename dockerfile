FROM python:3.11.4

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean

WORKDIR /code_website
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code_website

EXPOSE 5000

ENTRYPOINT ["python3", "main.py"] 
CMD ["runserver", "0.0.0.0:5000"]
