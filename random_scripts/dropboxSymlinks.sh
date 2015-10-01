

#create symlinks to files in dropbox, allowing for running of files straight from dropbox
#run with:
#	bash dropboxSymlinks.sh

#this file
ln -s ~/Dropbox/COSC280ReadingNetProject/Random_Scripts/dropboxSymlinks.sh ~/readingnet/Random_Scripts/dropboxSymlinks.sh

#readingnet
ln -s ~/Dropbox/COSC280ReadingNetProject/config.py ~/readingnet/config.py
ln -s ~/Dropbox/COSC280ReadingNetProject/db_create.py ~/readingnet/db_create.py
ln -s ~/Dropbox/COSC280ReadingNetProject/db_downgrade.py ~/readingnet/db_downgrade.py
ln -s ~/Dropbox/COSC280ReadingNetProject/db_migrate.py ~/readingnet/db_migrate.py
ln -s ~/Dropbox/COSC280ReadingNetProject/db_upgrade.py ~/readingnet/db_upgrade.py
ln -s ~/Dropbox/COSC280ReadingNetProject/run.py ~/readingnet/run.py
ln -s ~/Dropbox/COSC280ReadingNetProject/manage.py ~/readingnet/manage.py
ln -s ~/Dropbox/COSC280ReadingNetProject/db_init_tables.py ~/readingnet/db_init_tables.py
ln -s ~/Dropbox/COSC280ReadingNetProject/generate_fakes.py ~/readingnet/generate_fakes.py

#readingnet/app
ln -s ~/Dropbox/COSC280ReadingNetProject/app/__init__.py ~/readingnet/app/__init__.py
ln -s ~/Dropbox/COSC280ReadingNetProject/app/forms.py ~/readingnet/app/forms.py
ln -s ~/Dropbox/COSC280ReadingNetProject/app/models.py ~/readingnet/app/models.py
ln -s ~/Dropbox/COSC280ReadingNetProject/app/validators.py ~/readingnet/app/validators.py
ln -s ~/Dropbox/COSC280ReadingNetProject/app/views.py ~/readingnet/app/views.py

#readingnet/app/class_files
ln -s ~/Dropbox/COSC280ReadingNetProject/Class_Files/00ChangeLog ~/readingnet/Class_Files/00ChangeLog
ln -s ~/Dropbox/COSC280ReadingNetProject/Class_Files/00ToDo ~/readingnet/Class_Files/00ToDo

#readingnet/app/templates
ln -s ~/Dropbox/COSC280ReadingNetProject/app/templates/add.html ~/readingnet/app/templates/add.html
ln -s ~/Dropbox/COSC280ReadingNetProject/app/templates/base.html ~/readingnet/app/templates/base.html
ln -s ~/Dropbox/COSC280ReadingNetProject/app/templates/common.html ~/readingnet/app/templates/common.html
ln -s ~/Dropbox/COSC280ReadingNetProject/app/templates/index.html ~/readingnet/app/templates/index.html
ln -s ~/Dropbox/COSC280ReadingNetProject/app/templates/login.html ~/readingnet/app/templates/login.html
ln -s ~/Dropbox/COSC280ReadingNetProject/app/templates/new.html ~/readingnet/app/templates/new.html
ln -s ~/Dropbox/COSC280ReadingNetProject/app/templates/remove.html ~/readingnet/app/templates/remove.html
ln -s ~/Dropbox/COSC280ReadingNetProject/app/templates/search.html ~/readingnet/app/templates/search.html
ln -s ~/Dropbox/COSC280ReadingNetProject/app/templates/genre.html ~/readingnet/app/templates/genre.html

