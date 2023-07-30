FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY pineapple/ /app/pineapple/
COPY main.py .
EXPOSE 8501
CMD ["streamlit", "run", "main.py"]
