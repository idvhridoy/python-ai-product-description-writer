import os
import openai
import json
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# File paths
input_file = "data/movies.txt"  # A notepad file containing movie names
output_file = "output/movie_reviews.json"

# Role prompt and primer
role_prompt = """
    Assume the role of an expert movie reviewer with years of experience and a proven track record.
    You have reviewed thousands of movies across genres and eras. Your reviews are structured, detailed, and SEO-optimized. 
    You are skilled at analyzing film elements, including direction, performances, cinematography, themes, and sound design.
    Your reviews provide insightful critique while being engaging and accessible to a wide audience.
"""

primer = """
Your task is to write a comprehensive, SEO-ready, and structured movie review for the movie {movie_name}. Each review should include the following elements:

1. Title:
   - Create an engaging, SEO-friendly title that includes the film’s name, key genre, and perhaps notable performances.
   Example: "Inception (2010) – A Mind-Bending Sci-Fi Thriller Featuring Leonardo DiCaprio"

2. General Information:
   - Release Year: Include the year the movie was released.
   - Genre: Identify the genre(s) of the film (e.g., Drama, Thriller, Comedy, etc.).
   - Runtime: Mention the duration of the film in hours and minutes.
   - IMDb Rating: Provide the IMDb rating score.
   - MPAA Rating: The official movie rating (PG-13, R, etc.).
   - Language: Primary language of the movie.
   - Country of Origin: Where the movie was produced (e.g., USA, UK, etc.).
   - Filming Locations: Notable filming locations or set designs (if relevant).
   - Box Office Information: Budget, opening weekend, and gross earnings (domestic & worldwide).

3. Director and Crew:
   - Director(s): Name(s) of the director(s) and their previous notable works.
   - Writer(s): Key screenwriters and their previous works.
   - Producers: Notable producers and their contributions to the film.

4. Main Cast:
   - Lead Actors and Characters: Detailed profiles of lead actors and the characters they portray.
   - Supporting Cast: Key supporting actors and the roles they play.

5. Plot Summary:
   - Brief, Spoiler-Free Synopsis: A concise, spoiler-free overview of the plot (1-2 paragraphs).
   - Plot Analysis: In-depth breakdown of the movie's storyline and key events.

6. Taglines:
   - Include memorable or iconic taglines that capture the essence of the movie.
   Example: "Your mind is the scene of the crime."

7. Themes & Symbolism:
   - Key Themes: Discuss the film’s core themes (e.g., love, justice, fate, revenge, etc.).
   - Symbolism: Analysis of how symbolic elements in the movie (visuals, motifs) reflect its themes.
   
8. Character Development:
   - Main Character Arcs: Detailed discussion on the evolution of the lead characters and their arcs.
   - Supporting Character Development: Analysis of key supporting characters and how they contribute to the narrative.
   - Psychological Insights: Explore motivations, struggles, and emotional growth of characters.

9. Directorial Vision:
   - Directorial Style: Insights into the director's unique approach (tone, pacing, visual storytelling).
   - Cinematography: Discuss the visual style (e.g., camera work, shot composition, lighting).
   - Use of Space: How the director uses physical and visual space to enhance storytelling.

10. Soundtrack & Music:
    - Original Score: Analyze how the score elevates the emotional tone of the movie.
    - Soundtrack and Songs: Discuss notable songs and how they enhance the viewing experience.
    - Sound Design: Explore the role of sound effects and ambient noise in creating atmosphere.

11. Production Design:
    - Set Design: Discuss how the sets contribute to the film’s setting, tone, and immersion.
    - Costume and Makeup: How the costumes and makeup design support the story.
    - Special Effects: Analysis of visual effects, CGI, and practical effects, and how they influence the narrative.

12. Pacing and Structure:
    - Pacing: How the pacing of the film impacts engagement and emotional beats.
    - Narrative Structure: Analyze the structure (linear, non-linear) and its effects on the plot.
    - Editing: Discuss how editing techniques (cuts, transitions, timing) contribute to suspense or emotional payoff.

13. Cultural, Social, or Historical Context:
    - Context: How the movie relates to its time, cultural relevance, or historical background.
    - Impact at Time of Release: Discuss how the film was received by audiences and critics at the time of release.
    - Influence on Future Works: Explore the film’s legacy and influence on future films.

14. Audience Reception & Critical Acclaim:
    - Critical Consensus: Summarize the review consensus from major critics and publications.
    - Audience Reception: What general audiences are saying about the film.
    - Awards & Nominations: Mention any awards won or nominations the movie received.
    - Viewer Feedback: Explore fan reactions and feedback on social platforms or forums.

15. Trivia and Fun Facts:
    - Fun behind-the-scenes facts or trivia about the movie.
    - Alternate Versions: Information about alternate or extended versions.
    - Easter Eggs: Hidden details, references, or cameos that are important.

16. Quotes & Dialogue:
    - Memorable or impactful quotes from the film.
    - Discuss how specific lines of dialogue contribute to the film's themes or character development.

17. Legacy and Impact:
    - Cultural Legacy: How the film influenced popular culture, other films, or media.
    - Quotes and References: How the film is referenced or parodied.
    - Future Adaptations: Any plans for sequels, remakes, or other adaptations.

18. Criticism:
    - Weaknesses: Address areas where the film may have faltered (pacing issues, weak character arcs, etc.).
    - Room for Improvement: Offer suggestions or objective points where the movie could have been enhanced.

19. Conclusion:
    - Final thoughts on the film, including a balanced view of strengths and weaknesses.
    - Who Should Watch: Suggest what type of audience would enjoy this film.

20. Overall Rating:
    - Assign an overall score or rating (e.g., 1-10, 5 stars) and explain the rationale behind it.

21. Meta Title:
    - Create a short, SEO-optimized title for the review page (max 60 characters).

22. Meta Description:
    - Provide a concise meta description for SEO purposes (max 160 characters).

Ensure that each section is well-structured, formatted clearly for readability, and maintains a professional yet approachable tone. Your review should offer a comprehensive and in-depth analysis that appeals to both casual viewers and film enthusiasts.
"""

def send_primer():
    """
    Sends the initial primer message to OpenAI API to establish context.
    """
    openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": primer}
        ],
        max_tokens=150,
    )
    print("Primer set successfully.")

def generate_movie_review(movie_name):
    """
    Generates a structured movie review based on the movie name.
    """
    prompt = primer.format(movie_name=movie_name)
    
    # Make a request to the OpenAI ChatCompletion API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4000,
        temperature=0.7
    )
    
    # Extract the text from the API response
    review_content = response['choices'][0]['message']['content'].strip()
    
    # Create a structured review dictionary
    review = {
        "movie_name": movie_name,
        "release_year": 1994,  # Example data, replace with actual data
        "rating": "R",  # Example data, replace with actual data
        "runtime": "2h 22m",  # Example data, replace with actual data
        "imdb_rating": 9.3,  # Example data, replace with actual data
        "your_rating": 8.5,  # Example data, replace with actual data
        "popularity": 85,  # Example data, replace with actual data
        "genre": "Drama",  # Example data, replace with actual data
        "plot_summary": "A banker convicted of uxoricide forms a friendship over a quarter century with a hardened convict, while maintaining his innocence and trying to remain hopeful through simple compassion.",  # Example data, replace with actual data
        "director": "Frank Darabont",  # Example data, replace with actual data
        "writers": [
            "Stephen King",
            "Frank Darabont"
        ],  # Example data, replace with actual data
        "stars": [
            "Tim Robbins",
            "Morgan Freeman",
            "Bob Gunton"
        ],  # Example data, replace with actual data
        "storyline": "Chronicles the experiences of a formerly successful banker as a prisoner in the gloomy jailhouse of Shawshank after being found guilty of a crime he did not commit. The film portrays the man's unique way of dealing with his new, torturous life; along the way he befriends a number of fellow prisoners, most notably a wise long-term inmate named Red.",  # Example data, replace with actual data
        "tagline": "Fear can hold you prisoner. Hope can set you free.",  # Example data, replace with actual data
        "mpaa_rating": "Rated R for language and prison violence",  # Example data, replace with actual data
        "trivia": [
            "Andy and Red's opening chat in the prison yard, in which Red is throwing a baseball, took nine hours to shoot.",
            "Heywood is shown listening to the record '24 of Hank Williams' Greatest Hits', released in 1970."
        ],  # Example data, replace with actual data
        "goofs": [
            "Circa 1963, Heywood is shown listening to the record '24 of Hank Williams' Greatest Hits', released in 1970."
        ],  # Example data, replace with actual data
        "quotes": [
            "Andy Dufresne: I guess it comes down to a simple choice, really. Get busy living, or get busy dying."
        ],  # Example data, replace with actual data
        "crazy_credits": [
            "The man who cried and was beaten when Andy first arrived is listed and credited as 'Fat Ass'."
        ],  # Example data, replace with actual data
        "alternate_versions": [
            "The film was produced independently by Castle Rock Entertainment but distributed by Columbia Pictures."
        ],  # Example data, replace with actual data
        "connections": [
            "Featured in Siskel & Ebert: Why Gump? Why Now? (1994)"
        ],  # Example data, replace with actual data
        "soundtracks": [
            {
                "song_name": "If I Didn't Care",
                "artist": "The Ink Spots",
                "album": "24 of Hank Williams' Greatest Hits",
                "label": "MCA Records"
            }
        ],  # Example data, replace with actual data
        "user_reviews": [
            {
                "rating": 10,
                "title": "This is How Movies Should Be Made",
                "review_text": "This movie is not your ordinary Hollywood flick. It has a great and deep message.",
                "helpful_votes": 997
            }
        ],  # Example data, replace with actual data
        "release_date": "October 14, 1994",  # Example data, replace with actual data
        "country_of_origin": "United States",  # Example data, replace with actual data
        "official_sites": [
            "Official Facebook",
            "Warner Bros. (United States)"
        ],  # Example data, replace with actual data
        "filming_locations": [
            "Mansfield Reformatory - 100 Reformatory Road, Mansfield, Ohio, USA"
        ],  # Example data, replace with actual data
        "production_company": "Castle Rock Entertainment",  # Example data, replace with actual data
        "box_office": {
            "budget": "$25,000,000 (estimated)",
            "gross_us_canada": "$28,767,189",
            "opening_weekend_us_canada": "$727,327 (Sep 25, 1994)",
            "gross_worldwide": "$29,331,700"
        },  # Example data, replace with actual data
        "tech_specs": {
            "runtime": "2 hours 22 minutes",
            "sound_mix": "Dolby Digital",
            "aspect_ratio": "1.85 : 1"
        }  # Example data, replace with actual data
    }
    
    return review

def save_review(review):
    """
    Saves a single movie review to the JSON file.
    """
    try:
        # Load existing reviews
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            with open(output_file, 'r') as f:
                movie_reviews = json.load(f)
        else:
            movie_reviews = []

        # Append the new review
        movie_reviews.append(review)

        # Save back to the file
        with open(output_file, 'w') as outfile:
            json.dump(movie_reviews, outfile, indent=4)
    except Exception as e:
        print(f"Error saving review for {review['movie_name']}: {e}")

def process_movie(movie_name):
    """
    Processes a single movie to generate and save its review.
    """
    try:
        # Generate the review
        review = generate_movie_review(movie_name)
        
        # Save the review
        save_review(review)
        
        # Print progress
        print(f"Review for {movie_name} generated and saved successfully.")
    except Exception as e:
        print(f"Error processing movie {movie_name}: {e}")

def main():
    # Send the primer message to the API
    send_primer()
    
    # Load movie names from the notepad file
    with open(input_file, 'r') as f:
        movie_names = f.readlines()
    
    # Create threads for processing movies
    threads = []
    for movie_name in movie_names:
        movie_name = movie_name.strip()
        thread = threading.Thread(target=process_movie, args=(movie_name,))
        threads.append(thread)
        thread.start()
        
        # Limit the number of concurrent threads
        if len(threads) >= 100:
            for t in threads:
                t.join()
            threads = []
    
    # Wait for all threads to complete
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
