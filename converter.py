import json

# Input data
input_data = [
     {
        "movie_name": "Black Panther: Wakanda Forever",
        "review": "**Title:**\n\"Black Panther: Wakanda Forever (2022) \u2013 A Tribute to Chadwick Boseman's Legacy and Marvel's Cultural Impact\"\n\n**General Information:**\n- **Release Year:** 2022\n- **Genre:** Superhero, Action, Adventure\n- **Runtime:** 2 hours 26 minutes\n- **IMDb Rating:** TBA\n- **MPAA Rating:** TBA\n- **Language:** English\n- **Country of Origin:** USA\n- **Filming Locations:** Atlanta, Georgia; Puerto Rico; South Korea\n- **Box Office Information:** TBA\n\n**Director and Crew:**\n- **Director:** Ryan Coogler (\"Black Panther,\" \"Creed\")\n- **Writers:** Ryan Coogler, Joe Robert Cole\n- **Producers:** Kevin Feige, Louis D'Esposito, Victoria Alonso\n\n**Main Cast:**\n- **Chadwick Boseman as T'Challa / Black Panther:** The late actor's portrayal brought depth and charisma to the character.\n- **Letitia Wright as Shuri:** Known for her intelligence and wit, a pivotal character in Wakanda.\n- **Angela Bassett as Ramonda:** The regal presence as the Queen Mother of Wakanda.\n- **Supporting Cast:** Lupita Nyong'o, Winston Duke, Danai Gurira, Martin Freeman, Daniel Kaluuya\n\n**Plot Summary:**\nIn \"Black Panther: Wakanda Forever,\" the kingdom of Wakanda faces new challenges as it mourns the loss of King T'Challa. With the throne in question and enemies at the gates, the Wakandan people must come together to defend their nation and honor their fallen hero.\n\n**Taglines:**\n- \"Long live the king.\"\n- \"A nation under threat. A hero's legacy.\"\n\n**Themes & Symbolism:**\n- **Legacy and Leadership:** Exploring the weight of legacy and the responsibilities of leadership.\n- **Unity and Tradition:** Balancing tradition with the need for change and adaptation.\n- **Identity and Sacrifice:** Delving into the sacrifices made for the greater good and the essence of identity.\n\n**Character Development:**\n- **Main Character Arcs:** Witness the evolution of characters as they navigate loss, duty, and honor.\n- **Supporting Character Development:** Discover how supporting characters play crucial roles in shaping the narrative.\n- **Psychological Insights:** Unravel the characters' motivations, fears, and growth throughout the film.\n\n**Directorial Vision:**\n- **Directorial Style:** Ryan Coogler's distinct vision brings a blend of heart, action, and social commentary.\n- **Cinematography:** Stunning visuals capture the beauty and power of Wakanda and its people.\n- **Use of Space:** The film utilizes space to convey intimacy, grandeur, and cultural richness.\n\n**Soundtrack & Music:**\n- **Original Score:** The score enhances the emotional depth and cultural resonance of the film.\n- **Soundtrack and Songs:** Infused with African influences, the music elevates the viewing experience.\n- **Sound Design:** Immersive soundscapes create a vibrant and dynamic world.\n\n**Production Design:**\n- **Set Design:** Intricate sets immerse viewers in the futuristic and traditional landscapes of Wakanda.\n- **Costume and Makeup:** Vibrant costumes and makeup reflect the rich culture and heritage of Wakanda.\n- **Special Effects:** Seamless visual effects blend technology and tradition to create a visually stunning world.\n\n**Pacing and Structure:**\n- **Pacing:** The film's pacing builds tension and emotional resonance, keeping audiences engaged.\n- **Narrative Structure:** A non-linear narrative adds depth and complexity to the story.\n- **Editing:** Precise editing enhances the film's emotional impact and narrative flow.\n\n**Cultural, Social, or Historical Context:**\n- **Context:** \"Black Panther: Wakanda Forever\" continues to celebrate African culture and representation in mainstream media.\n- **Impact at Time of Release:** Anticipated to be a cultural milestone, honoring Chadwick Boseman's legacy.\n- **Influence on Future Works:** Expected to inspire future films with diverse representation and strong cultural themes.\n\n**Audience Reception & Critical Acclaim:**\n- **Critical Consensus:** TBA\n- **Audience Reception:** Fans eagerly anticipate this sequel, honoring the beloved character of T'Challa.\n- **Awards & Nominations:** TBA\n- **Viewer Feedback:** Social media buzz reflects excitement and reverence for the film's significance.\n\n**Trivia and Fun Facts:**\n- Details about the film's tribute to Chadwick Boseman.\n- Easter eggs and references to Marvel lore and African culture.\n\n**Quotes & Dialogue:**\n- \"Wakanda forever.\"\n- \"In times of crisis, the wise build bridges, while the foolish build barriers.\"\n\n**Legacy and Impact:**\n- **Cultural Legacy:** The film's impact extends beyond entertainment, fostering representation and empowerment.\n- **Quotes and References:** \"Wakanda forever\" has become a rallying cry for diversity and unity.\n- **Future Adaptations:** Speculation on how the film will shape future Marvel projects and representation in cinema.\n\n**Criticism:**\n- **Weaknesses:** Potential challenges in honoring Boseman's legacy while moving the narrative forward.\n- **Room for Improvement:** Balancing action with emotional depth and thematic exploration.\n\n**Conclusion:**\n\"Black Panther: Wakanda Forever\" stands as a testament to Chadwick Boseman's legacy and the cultural significance of the Black Panther franchise. With its rich themes, vibrant world-building, and compelling characters, this film is poised to be a fitting tribute to a beloved hero. Fans of superhero epics and those seeking powerful storytelling with a message of unity and strength will find \"Wakanda Forever\" a must-watch.\n\n**Overall Rating:** TBA\n\n**Meta Title:**\n\"Black Panther: Wakanda Forever \u2013 A Tribute to Chadwick Boseman's Legacy\"\n\n**Meta Description:**\n\"Explore the world of Wakanda in 'Black Panther: Wakanda Forever' as it honors Chadwick Boseman's legacy. A superhero sequel with cultural impact and emotional resonance.\""
    }
    
]

# Define a function to extract details and structure them
def process_review_data(movie_data):
    extracted_data = []
    for entry in movie_data:
        review_text = entry["review"]
        print(f"Processing review for: {entry['movie_name']}")  # Debugging line
        print(f"Review Text:\n{review_text}\n")  # Debugging line

        # Extract fields using updated extract_value function
        movie_name = entry["movie_name"]
        release_year = extract_value("Release Year", review_text)
        rating = extract_value("MPAA Rating", review_text)
        runtime = extract_value("Runtime", review_text)
        imdb_rating = extract_value("IMDb Rating", review_text)
        genre = extract_value("Genre", review_text)
        plot_summary = extract_value("Plot Summary", review_text)
        director = extract_value("Director", review_text)
        writers = extract_value("Writers", review_text)
        
        # Handle 'Main Cast' extraction safely
        stars_raw = extract_value("Main Cast", review_text)
        stars = stars_raw.split("\n") if stars_raw else []  # Only split if stars_raw is not None

        extracted_data.append({
            "movie_name": movie_name,
            "release_year": release_year,
            "rating": rating,
            "runtime": runtime,
            "imdb_rating": imdb_rating,
            "genre": genre,
            "plot_summary": plot_summary,
            "director": director,
            "writers": writers.split(",") if writers else [],
            "stars": [star.split(" as ")[0].strip() for star in stars]
        })
    return extracted_data



def extract_value(field_name, text):
    # Look for the line starting with "**<field_name>**:" in the text
    for line in text.splitlines():
        if line.strip().startswith(f"**{field_name}**:"):
            field_line = line.strip()
            if ": " in field_line:
                return field_line.split(": ", 1)[1].strip()
            else:
                return field_line.split(":", 1)[1].strip()
    
    # Handle bullet points and other list-based formats
    for line in text.splitlines():
        if line.strip().startswith("- **" + field_name + "**:"):
            field_line = line.strip()
            return field_line.split(": ", 1)[1].strip()
    
    # If not found directly, look for the first bullet point after "General Information" or similar section
    # to extract data related to that section
    if field_name == "Genre":
        # Search within the general information block
        general_info_section = text.split("**General Information:**")[1]  # Capture all after "General Information"
        for line in general_info_section.splitlines():
            if line.strip().startswith("- **" + field_name + "**:"):
                field_line = line.strip()
                return field_line.split(": ", 1)[1].strip()

    print(f"Field not found: {field_name}")  # Debugging line
    return None



# Process input data and output result
output_data = process_review_data(input_data)

# Print the structured output
print(json.dumps(output_data, indent=4))
