FROM python:3.10 
# Or any preferred Python version.
ADD main.py .
RUN mkdir -p ./dropzone
RUN pip install requests watchdog
CMD ["python", "-u", "./main.py"] 
# Or enter the name of your unique directory and parameter set.