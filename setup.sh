#!/bin/zsh

echo "Please enter the value for the SECRET_KEY environment variable:"
read SECRET_KEY

export SECRET_KEY=$SECRET_KEY

echo "Please enter the value for the DATABASE_URL environment variable:"
read DATABASE_URL

export DATABASE_URL=$DATABASE_URL