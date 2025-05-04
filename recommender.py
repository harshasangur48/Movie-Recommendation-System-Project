print("Starting script...")
# Imports
try:
    import pandas as pd
    import tkinter as tk
    from tkinter import ttk, messagebox
    from surprise import SVD, Dataset, Reader
    from surprise.model_selection import train_test_split
    import random
    print(" All imports successful.")
except ImportError as e:
    print(f" Import error: {e}")
    exit(1)
# Load Data and Train Model
model_trained = False
try:
    print(" Loading ratings and movies data...")
    ratings = pd.read_csv("ml-20m/ratings.csv")[['userId', 'movieId', 'rating']]
    movies = pd.read_csv("ml-20m/movies.csv")
    print(" CSVs loaded.")
    ratings['userId'] = ratings['userId'].astype(str)
    ratings['movieId'] = ratings['movieId'].astype(str)
    movies['movieId'] = movies['movieId'].astype(str)
    reader = Reader(rating_scale=(0.5, 5.0))
    data = Dataset.load_from_df(ratings, reader)
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)
    print("Training SVD model...")
    model = SVD()
    model.fit(trainset)
    model_trained = True
    print(" Model training complete.")
except FileNotFoundError:
    print(" 'ratings.csv' or 'movies.csv' not found.")
except Exception as e:
    print(f"Error during loading or training: {e}")
# Genre + Indian Movie Filters
def extract_genres(movies_df):
    all_genres = set()
    for genres in movies_df['genres']:
        if isinstance(genres, str):
            all_genres.update(genres.split('|'))
    return sorted(list(all_genres - {'(no genres listed)'}))
GENRES = extract_genres(movies) if 'movies' in locals() else []
INDIAN_KEYWORDS = ['india', 'bollywood', 'hindi', 'tamil', 'telugu', 'bolly', 'kollywood', 'mollywood']
def is_indian_movie(title):
    return isinstance(title, str) and any(keyword in title.lower() for keyword in INDIAN_KEYWORDS)
# Recommendation Logic
def recommend_movies_by_genre(genre, prioritize_indian=False, n=5):
    if not model_trained or 'movies' not in globals() or 'ratings' not in globals():
        return [("Error: Model not trained or data not loaded.", 0.0)]
    try:
        user_id = random.choice(ratings['userId'].unique())
    except KeyError:
        return [("Error: No valid userId found.", 0.0)]
    genre_movies = movies[movies['genres'].str.contains(genre, na=False)]
    if prioritize_indian:
        genre_movies = genre_movies[genre_movies['title'].apply(is_indian_movie)]
    genre_movies = genre_movies[~genre_movies['movieId'].isin(ratings[ratings['userId'] == user_id]['movieId'])]
    predictions = []
    for _, m in genre_movies.iterrows():
        try:
            predictions.append((m['title'], model.predict(user_id, m['movieId']).est))
        except Exception as e:
            print(f"Prediction error for {m['title']}: {e}")
            continue
    top_n = sorted(predictions, key=lambda x: x[1], reverse=True)[:n]
    return [(title, round(score, 2)) for title, score in top_n]
# GUI Setup
root = tk.Tk()
root.title("🎬 MovieLens 20M Recommender")
root.geometry("720x500")
root.configure(bg="#f9f9ff")
FONT_TITLE = ("Helvetica", 18, "bold")
FONT_LABEL = ("Helvetica", 12, "bold")
FONT_TEXT = ("Helvetica", 11)
tk.Label(root, text="🎥 MovieLens 20M Recommender", bg="#2e86c1", fg="white", font=FONT_TITLE, pady=15).pack(fill='x')
# Input Frame (Name + Genre + Checkbox)
input_frame = tk.Frame(root, bg="white", pady=15, padx=15, relief=tk.RIDGE, borderwidth=2)
input_frame.pack(padx=30, pady=20, fill='x')
# User name input
tk.Label(input_frame, text="🧑 Your Name:", font=FONT_LABEL, bg="white").grid(row=0, column=0, sticky='w')
name_var = tk.StringVar()
name_entry = tk.Entry(input_frame, textvariable=name_var, font=FONT_TEXT)
name_entry.grid(row=0, column=1, sticky='ew', padx=10)
# Genre dropdown
tk.Label(input_frame, text="🎭 Choose Genre:", font=FONT_LABEL, bg="white").grid(row=1, column=0, sticky='w', pady=10)
genre_var = tk.StringVar()
genre_menu = ttk.Combobox(input_frame, textvariable=genre_var, values=GENRES, state='readonly', font=FONT_TEXT)
genre_menu.grid(row=1, column=1, padx=10, sticky='ew')
if GENRES:
    genre_menu.set(GENRES[0])
else:
    genre_menu['values'] = ["No Genres Available"]
    genre_menu.set("No Genres Available")
# Indian movie checkbox
prioritize_var = tk.BooleanVar()
prioritize_check = tk.Checkbutton(input_frame, text="Prioritize Indian Movies", variable=prioritize_var, font=FONT_LABEL, bg="white")
prioritize_check.grid(row=2, column=0, columnspan=2, pady=10)

def on_recommend():
    name = name_var.get().strip()
    genre = genre_var.get()
    prioritize = prioritize_var.get()
    result_text.config(state='normal')
    result_text.delete("1.0", tk.END)

    if not name:
        result_text.insert(tk.END, "⚠️ Please enter your name first.\n")
        result_text.config(state='disabled')
        return

    if genre == "No Genres Available":
        result_text.insert(tk.END, "⚠️ Genre list could not be loaded.\n")
        result_text.config(state='disabled')
        return

    recs = recommend_movies_by_genre(genre, prioritize)
    if recs and recs[0][0].startswith("Error"):
        result_text.insert(tk.END, f"⚠️ Error: {recs[0][0]}\n")
    elif recs:
        result_text.insert(tk.END, f"🎬 {name}'s Top {genre} Recommendations:\n\n")
        for title, score in recs:
            result_text.insert(tk.END, f"• {title} - ⭐ {score}\n")
    else:
        result_text.insert(tk.END, "No recommendations found for the selected genre.\n")

    result_text.config(state='disabled')
# Button to get recommendations
recommend_btn = ttk.Button(input_frame, text="🎯 Get Recommendations", command=on_recommend)
recommend_btn.grid(row=3, column=0, columnspan=2, pady=15)
input_frame.grid_columnconfigure(1, weight=1)
# Output Frame
output_frame = tk.Frame(root, bg="white", padx=15, pady=10, relief=tk.GROOVE, borderwidth=2)
output_frame.pack(fill='both', expand=True, padx=30)
tk.Label(output_frame, text="📋 Recommendations", font=FONT_LABEL, bg="white").pack(anchor='w')
result_text = tk.Text(output_frame, height=12, font=FONT_TEXT, wrap='word', bg="#fdfdfd", fg="#333333")
result_text.pack(fill='both', expand=True)
result_text.config(state='disabled')
# Start App
root.mainloop()
