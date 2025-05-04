Movie-Recommendation-System-Project
This is a Tkinter-based movie recommendation system built using the MovieLens 20M dataset and the SVD algorithm from the Surprise library. The application offers a simple graphical interface where users can receive personalized movie recommendations by selecting their favorite genre.

💡 Features
Genre-Based Recommendations: Choose from a wide range of movie genres.

User-Friendly Input: Enter your name for a personalized experience.

Top-N Prediction: Displays top-rated unseen movies for a simulated user.

Trained on MovieLens 20M: Uses real-world data to provide meaningful recommendations.

Simple GUI: Built using Python’s Tkinter library for desktop use.

🧪 Tech Stack
Python 3.x

Pandas for data manipulation

Surprise (Scikit-Surprise) for the movie recommendation algorithm

Tkinter for creating the graphical user interface (GUI)

📁 Files Required
This project requires the following two CSV files from the MovieLens 20M dataset:

ratings.csv

movies.csv

You can download the dataset from: MovieLens 20M Dataset

Place these CSV files in a folder named ml-20m/ in the project directory.

🚀 How to Run
Clone the repository:
Open your terminal or command prompt and run the following command:
git clone : https://github.com/harshasangur48/Movie-Recommendation-System-Project.git
cd movie-recommender

Install required dependencies:
You need to install some Python libraries to run the project. In the terminal, run the following command:
pip install pandas scikit-surprise
Ensure the dataset files are in place:
Make sure that the ml-20m/ folder contains the required CSV files, ratings.csv and movies.csv.

Run the Python script:
To start the recommender system, run the following command:
python recommender.py
This will open a Tkinter window where you can input your name, select a genre, and get movie recommendations.

📌 Future Improvements
Here are some potential future features you could add to improve this project:

Add user authentication to save and load user preferences.

Allow users to input their past ratings to make the recommendations more personalized.

Deploy the application as a web application using Flask or Streamlit.

Add search and filter options for users to refine the recommendations.

💬 Contributing
Feel free to fork the repository, create issues, and submit pull requests. Contributions are welcome!

👀 License
This project is open-source and available under the MIT License.

