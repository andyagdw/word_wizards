# Word Wizards ⚡

A dynamic Django-based web application that brings the magic of words to your fingertips👐.
Whether you're a word enthusiast, a student, or simply someone who loves to expand their
vocabulary, Word Wizards provides a delightful experience with a variety of word-related
features. Leveraging the power of the [WordsAPI](https://www.wordsapi.com/), the platform offers users the ability to
explore the word of the day, discover random words, and curate a personalised list of
favourite words. Additionally, users can upgrade their accounts to access enhanced features
and enjoy a richer experience free of cost ❗.

## Features ✨

* **Word of the Day**: <br> Stay inspired and learn something new every day with the 'Word of the Day'
 feature, providing you with a fresh word and its details daily
* **Random Word**: <br> Discover new words at random and expand your vocabulary with just a click
* **Favourites**: <br> Keep track of the words you love by adding them to your favourites list for easy
 access and review
* **Account Upgrades**: <br> Upgrade your account to unlock 'Plus' or 'Pro' features, enhancing your word
 discovery experience with additional functionalities

## Light and Dark Mode 🌓

Word Wizards offers a seamless experience with both light and dark modes. Choose the theme that suits your preference
and enjoy the interface in any lighting condition 😄.

### Light Mode (Plus account)

![Light Mode](https://github.com/andyagdw/words_wizards/assets/138252680/c4e1d9e1-e7f5-4482-9eae-792053c3a875)

### Dark Mode (Plus account)

![Dark Mode](https://github.com/andyagdw/words_wizards/assets/138252680/d75d19d5-e1d3-48ff-b99e-143b965036b2)

## Getting started ✅

Follow these simple steps to get started with Word Wizards:

### Prerequisite
- Ensure that Python and Pip are installed on your machine

1. Create a free account with RapidAPI:
* Go to the [WordsAPI RapidAPI page](https://rapidapi.com/dpventures/api/wordsapi/pricing).
* Sign up for a free basic plan, which provides access to 2,500 requests per day.
* After subscribing to the WordsAPI, you should be redirected to a page where you can view your X-RapidAPI-Key.
* If you are not automatically redirected, navigate to the workspace by clicking on the "Workspace" button on the
  left sidebar, then scroll down to "My Subscriptions" and select "WordsAPI" to view your API key.
* Copy your X-RapidAPI-Key for later use.

2. Clone the repository to your local machine: <br>
   `git clone https://github.com/andyagdw/word_wizards.git`
3. Navigate to the project directory: <br>
   `cd word_wizards`
4. Set up a virtual environment: <br>

   Using venv:

   `python -m venv venv` <br>
   For Python 3.3 or newer: <br>
   `python3 -m venv venv`

   Using virtualenv:

   ```
   pip install virtualenv
   virtualenv venv
   ```

5. Activate the virtual environment:

   Using venv:

   Windows: <br>
   `venv\Scripts\activate` <br>
   Unix\Mac: <br>
   `source venv/bin/activate`

   Using virtualenv: <br>

   Windows: <br>
   `venv\Scripts\activate` <br>
   Unix\Mac: <br>
   `source venv/bin/activate`

6. Ensure project dependencies are installed: <br>
   ```pip install -r requirements.txt```

7. Create a `.env` file from the example template `.env.example`:

   Windows: <br>
   `copy .env.example .env` <br>
   Unix\Mac: <br>
   `cp .env.example .env`
   
   Then, open the `.env` file and replace `your_api_key_here` with your actual WordsAPI key. For example:

   WORDS_API_KEY = 'ABCDE'

8. In the project directory, start the server: <br>
   `python manage.py runserver`

9. Click the link that shows in the terminal 🚀.

## Upcoming Features 🎆

1. **Interactive Games**: <br> Add a variety of word-related games, including both single-player and
 multiplayer options, to make learning new words fun and engaging 😁.
2. **Personal Vocabulary Notes**: <br> Introduce a feature that allows users to add personal notes and insights
 about words, creating a personalised vocabulary journal 📖.

## Credits
### Contact

If you have any questions or just want to connect, you can reach me on
[LinkedIn](https://www.linkedin.com/in/andyagyeidwumah/) 👍.
