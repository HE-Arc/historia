# config valid for current version and patch releases of Capistrano
lock "~> 3.16.0"

set :application, "historiaapp"
set :repo_url, "https://github.com/HE-Arc/historia.git"

# Default branch is :master
ask :branch, `git rev-parse --abbrev-ref main`.chomp
# set :branch "main"

# Default deploy_to directory is /var/www/my_app_name
set :deploy_to, "/var/www/#{fetch(:application)}"

after 'deploy:publishing', 'uwsgi:restart'

namespace :uwsgi do
    desc 'Restart application'
    task :restart do
        on roles(:web) do |h|
	    execute :sudo, 'sv reload uwsgi'
	end
    end
end

# Ajouter la tâche de mise à jour du venv python dans config/deploy.rb dans le projet local

after 'deploy:updating', 'python:create_venv'

namespace :python do

    def venv_path
        File.join(shared_path, 'env')
    end

    desc 'Create venv'
    task :create_venv do
        on roles([:app, :web]) do |h|
	    execute "python3.8 -m venv #{venv_path}"
            execute "source #{venv_path}/bin/activate"
            execute "#{venv_path}/bin/pip install -r #{release_path}/requirements.txt"
            execute "cd #{release_path}/historiaproject && #{venv_path}/bin/python3 manage.py makemigrations"
            execute "cd #{release_path}/historiaproject && #{venv_path}/bin/python3 manage.py migrate"
            execute "cd #{release_path}/historiaproject && #{venv_path}/bin/python3 manage.py loaddata cards.json"
            execute "cd #{release_path}/historiaproject && #{venv_path}/bin/python3 manage.py loaddata questions.json"
            execute "cd #{release_path}/historiaproject && #{venv_path}/bin/python3 manage.py loaddata category.json"
            execute "cd #{release_path}/historiaproject && #{venv_path}/bin/python3 manage.py loaddata quizzes.json"
       end
    end
end

# execute "cd #{release_path}/historiaproject && #{venv_path}/bin/python3 manage.py makemigrations"
# execute "cd #{release_path}/historiaproject && #{venv_path}/bin/python3 manage.py migrate"
# execute "cd #{release_path}/historiaproject && #{venv_path}/bin/python3 manage.py loaddata cards.json"
# execute "cd #{release_path}/historiaproject && #{venv_path}/bin/python3 manage.py loaddata questions.json"
# execute "cd #{release_path}/historiaproject && #{venv_path}/bin/python3 manage.py loaddata quizzes.json"

# Default value for :format is :airbrussh.
# set :format, :airbrussh

# You can configure the Airbrussh format using :format_options.
# These are the defaults.
# set :format_options, command_output: true, log_file: "log/capistrano.log", color: :auto, truncate: :auto

# Default value for :pty is false
# set :pty, true

# Default value for :linked_files is []
# append :linked_files, "config/database.yml"

# Default value for linked_dirs is []
# append :linked_dirs, "log", "tmp/pids", "tmp/cache", "tmp/sockets", "public/system"

# Default value for default_env is {}
# set :default_env, { path: "/opt/ruby/bin:$PATH" }

# Default value for local_user is ENV['USER']
# set :local_user, -> { `git config user.name`.chomp }

# Default value for keep_releases is 5
# set :keep_releases, 5

# Uncomment the following to require manually verifying the host key before first deploy.
# set :ssh_options, verify_host_key: :secure
