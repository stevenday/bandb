bandb
=====

Make a website for your B&B in 15 minutes

Installation
------------
- Requires sass, yuglify (as well as postgres etc for Django)
- Create a virtualenv
- Create a postgres user with db create permissions and a database for them
- `pip install -r requirements.txt` in your virtualenv
- Add the following settings into a local `.env` file in the project root:
    - CLOUDMADE_API_KEY- For the maps
    - STRIPE_SECRET_KEY - Should be your test key
    - STRIPE_PUBLIC_KEY - Should be your test key
    - AWS_ACCESS_KEY_ID - Only needed to push static files to S3
    - AWS_SECRET_ACCESS_KEY - Only needed to push static files to S3
    - AWS_STORAGE_BUCKET_NAME - Only needed to push static files to S3
    - DJANGO_SECRET_KEY
    - Debug (only set if you want to be in debug mode)

Running
-------
Use foreman to set environment variables from `.env` when running things:
`foreman run ./manage.py runserver <ip>:<port>`

Testing
-------
Use foreman to set environment variables from `.env` when running things:
`foreman run ./manage.py test bookings`

Note only `bookings` app has tests.

Deploying
---------
To deploy the site do the following:
- Remove the `Debug=True` setting in your `.env`
- Run `foreman run ./manage.py collectstatic --noinput`
- `git rm --cached static_cache` - to remove old static files cache
- `git add static_cache` - to add the new static files cache
- `git commit`
- `git push heroku master`
- Add `Debug=True` back into your `.env`
