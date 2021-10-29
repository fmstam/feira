FROM python:3.9.7

WORKDIR /feira

COPY requirements.txt ./

RUN pip install --ignore-installed  --no-cache-dir -r requirements.txt

# copy everything
COPY . .


# expose the 8000 port 

EXPOSE 8000

# run the server
CMD [ "./feira/manage.py", "runserver", "127.0.0.1:8000" ]