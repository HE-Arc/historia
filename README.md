<img src="https://user-images.githubusercontent.com/91063762/163147512-7689ed6c-385b-4609-ac62-bc7e61623027.svg" width="100" height="100">

# Historia

A web app challenging your historical characters knowledges.

## Server address
https://historia.srvz-webapp.he-arc.ch/

It is not necessary to create an account to try this application, a sample quiz is available. To do so, click on the yellow ["try"](https://historia.srvz-webapp.he-arc.ch/try/) button. 

## Documentation
- [Statement of work](https://github.com/HE-Arc/historia/wiki/Cahier-des-charges)
- [Models](https://github.com/HE-Arc/historia/wiki/Maquettes)
- [Diagrams](https://github.com/HE-Arc/historia/wiki/Diagrammes)

## Requirements

Django highly recommends using python versions 3.8+ but support Python 3.6 and 3.7. [See more informations on Django doc.](https://docs.djangoproject.com/en/4.0/releases/4.0/#python-compatibility)

## Description

Historia is a project developed during the 3rd year of the Bachelor in Computer Science course at the Haute école Arc Ingenierie. It is an application allowing users to test their knowledge via quizzes on important characters in the history of humanity. For each correct answer obtained by the user, cards on the historical figure in question are displayed. The user then has the opportunity to consult this character. There are different quizzes on different themes. The quizzes are sorted into 4 categories (art, history, geography and science & inventions). When a user completes a quiz, he/she gets a score on it. This score is available in a general and a personal ranking.

## Installation

1. Clone the repository 
```
git clone git@github.com:HE-Arc/historia.git
```
2. Create a virtual environment
```
$ python3 -m venv <Project name> <Folder in which the venv is stored>
```
3. Activate the virtual env
```
source .venv/bin/activate
```
4. Install all the dependances in the requirements.txt file
```
pip install -r requirements.txt
```
5. Run the server
```
cd historiaproject
python manage.py runserver
```

6. Database - migration
```
cd historiaproject
python manage.py makemigrations
python manage.py migrate
```
7. (Optional) Load data

It is necessary to add the data in order as in this section.
This dataset consists of approximately 50 characters with just under 50 questions, 4 categories and 11 quizzes.

- load the cards of the historical figures
 ```
 python manage.py loaddata cards.json
 ```

- loads the categories for the quizzes
```
python manage.py loaddata category.json
```

- loads the questions available in the quizzes
```
python manage.py loaddata questions.json
```

- load the quizzes 
```
python manage.py loaddata quizzes.json
```


8. Compte administrateur
Nous avons créé en amont un compte administrateur pour vous permettre de tester les fonctionnalités dans ce mode :
__**user:** Admin__
__**mdp:** k3yb0ard__




## Continuous Deployment

Historia uses [Capistrano](https://capistranorb.com/) for continuous deployment. 

## Examples

![image](https://user-images.githubusercontent.com/91063762/163145001-4e501920-6e41-46cc-af6a-59e1f976b55e.png)
![image](https://user-images.githubusercontent.com/91063762/163145073-5446f5a8-257c-4883-8a19-7a4b18ffcadf.png)
![image](https://user-images.githubusercontent.com/91063762/163145228-10dad566-8ba7-4bd5-9099-7a1ad39048d9.png)
![image](https://user-images.githubusercontent.com/91063762/163145335-38fcffc6-600e-43e2-be09-7d7b37faaaa3.png)
![image](https://user-images.githubusercontent.com/91063762/163145509-2f6ce022-f430-4fe4-9083-57c35155b7a4.png)
![image](https://user-images.githubusercontent.com/91063762/163145645-4eef0ae0-5ca9-4bef-9886-06d0125d2c70.png)

## Authors
* Alex Mozerski (@alex.mozerski)
* Yasmine Margueron (@yasmine.margueron)
* Simon Meier (@simon.meier)






