# https://stackoverflow.com/questions/54327005/installing-pdftotext-library-on-heroku
heroku buildpacks:add  -a textstudio-api heroku-community/apt
heroku buildpacks:add  -a textstudio-api heroku/python
