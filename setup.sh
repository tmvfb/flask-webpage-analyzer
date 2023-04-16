#!/bin/zsh

echo "Generating the SECRET_KEY environment variable..."
echo "SECRET_KEY=$(python3 -c 'import os; print(os.urandom(16))')" > secret.env

echo 'Done.'

echo "Please enter the value for the DATABASE_URL environment variable (format is {provider}://{user}:{password}@{host}:{port}/{db}):"
read DATABASE_URL
echo "DATABASE_URL=$DATABASE_URL" >> secret.env

echo 'Setup complete'

chmod 600 secret.env