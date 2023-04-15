FROM python:3.9 
# Or any preferred Python version.
ADD main.py .
RUN pip install requests python-dotenv watchdog
CMD ["python", "./main.py"] 
# Or enter the name of your unique directory and parameter set.