FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Install system dependencies
RUN apt-get update && apt-get install -y nginx

# Create a work dir
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

#COPY Models /app/Models
COPY app_enum.py /app/app_enum.py
COPY ChromaDBRepository.py /app/ChromaDBRepository.py
COPY main.py /app/main.py
# Set up Nginx
# Remove default Nginx configuration
RUN rm /etc/nginx/nginx.conf

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

ENV PYTHONUNBUFFERED 1

#RUN python build_downloader.py
#CMD ["uvicorn", "--workers", "1","main:app", "--host", "0.0.0.0", "--port", "8000"]
# Start Nginx and Uvicorn server
CMD service nginx start  && uvicorn main:app --host 0.0.0.0 --port 8000