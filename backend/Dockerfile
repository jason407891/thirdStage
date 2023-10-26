# Start your image with a node base image
FROM python:3.8

# The /app directory should act as the main application directory
WORKDIR /app

# Copy the app package and package-lock.json file
COPY requirements.txt ./
COPY app.py ./
COPY static ./static
COPY templates ./templates

# Install node packages, install serve, build the app, and remove dependencies at the end
RUN pip install -r requirements.txt

EXPOSE 3000

# Start the app using serve command
CMD [ "python", "app.py"]