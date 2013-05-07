#! /bin/sh
# Collect all the static files, ignoring things which never need
# to be collected and clearing old things
foreman run ./manage.py collectstatic --noinput --clear --ignore *.scss --ignore CHANGELOG.md --ignore README.md --ignore component.json --ignore LICENSE --ignore CONTRIBUTING.md