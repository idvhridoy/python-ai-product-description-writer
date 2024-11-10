import json
import re

def convert_review_to_dict(review_text):
    # Define key sections to match using regular expressions
    movie_review = {
        "Title": "",
        "General Information": {
            "Release Year": "",
            "Genre": "",
            "Runtime": "",
            "IMDb Rating": "",
            "MPAA Rating": "",
            "Language": "",
            "Country of Origin": "",
            "Filming Locations": "",
            "Box Office Information": {
                "Budget": "",
                "Opening Weekend": "",
                "Gross Earnings": ""
            }
        },
        "Director and Crew": {
            "Director": "",
            "Writer": "",
            "Producers": []
        },
        "Main Cast": {
            "Lead Actors": [],
            "Supporting Cast": []
        },
        "Plot Summary": "",
        "Taglines": [],
        "Themes & Symbolism": {
            "Themes": [],
            "Symbolism": []
        },
        "Character Development": {
            "Ellie": "",
            "Joel": "",
            "Supporting Characters": ""
        },
        "Directorial Vision": "",
        "Soundtrack & Music": {
            "Composer": "",
            "Details": ""
        },
        "Production Design": "",
        "Pacing and Structure": "",
        "Cultural, Social, or Historical Context": "",
        "Audience Reception & Critical Acclaim": "",
        "Trivia and Fun Facts": [],
        "Quotes & Dialogue": [],
        "Legacy and Impact": "",
        "Criticism": "",
        "Conclusion": "",
        "Who Should Watch": "",
        "Overall Rating": "",
        "Meta Title": "",
        "Meta Description": ""
    }

    # Define regex patterns for each section
    sections = {
        "Title": r"\"([^\"]+)\"",
        "General Information": r"\*\*General Information:\*\*(.*?)\*\*Director and Crew:\*\*",
        "Director and Crew": r"\*\*Director and Crew:\*\*(.*?)\*\*Main Cast:\*\*",
        "Main Cast": r"\*\*Main Cast:\*\*(.*?)\*\*Plot Summary:\*\*",
        "Plot Summary": r"\*\*Plot Summary:\*\*(.*?)\*\*Taglines:\*",
        "Taglines": r"\*\*Taglines:\*\*(.*?)\*\*Themes & Symbolism:\*",
        "Themes & Symbolism": r"\*\*Themes & Symbolism:\*\*(.*?)\*\*Character Development:\*",
        "Character Development": r"\*\*Character Development:\*\*(.*?)\*\*Directorial Vision:\*",
        "Directorial Vision": r"\*\*Directorial Vision:\*\*(.*?)\*\*Soundtrack & Music:\*",
        "Soundtrack & Music": r"\*\*Soundtrack & Music:\*\*(.*?)\*\*Production Design:\*",
        "Production Design": r"\*\*Production Design:\*\*(.*?)\*\*Pacing and Structure:\*",
        "Pacing and Structure": r"\*\*Pacing and Structure:\*\*(.*?)\*\*Cultural, Social, or Historical Context:\*",
        "Cultural, Social, or Historical Context": r"\*\*Cultural, Social, or Historical Context:\*\*(.*?)\*\*Audience Reception & Critical Acclaim:\*",
        "Audience Reception & Critical Acclaim": r"\*\*Audience Reception & Critical Acclaim:\*\*(.*?)\*\*Trivia and Fun Facts:\*",
        "Trivia and Fun Facts": r"\*\*Trivia and Fun Facts:\*\*(.*?)\*\*Quotes & Dialogue:\*",
        "Quotes & Dialogue": r"\*\*Quotes & Dialogue:\*\*(.*?)\*\*Legacy and Impact:\*",
        "Legacy and Impact": r"\*\*Legacy and Impact:\*\*(.*?)\*\*Criticism:\*",
        "Criticism": r"\*\*Criticism:\*\*(.*?)\*\*Conclusion:\*",
        "Conclusion": r"\*\*Conclusion:\*\*(.*?)\*\*Who Should Watch:\*",
        "Who Should Watch": r"\*\*Who Should Watch:\*\*(.*?)\*\*Overall Rating:\*",
        "Overall Rating": r"\*\*Overall Rating:\*\*(.*?)\*\*Meta Title:\*",
        "Meta Title": r"\*\*Meta Title:\*\*(.*?)\*\*Meta Description:\*",
        "Meta Description": r"\*\*Meta Description:\*\*(.*?)$"
    }

    # Function to parse a review section
    def parse_section(text, section_key, regex_pattern):
        match = re.search(regex_pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip().replace("\n", " ").replace("\\u2013", "–")
        return None

    def parse_cast(cast_text):
        cast_list = []
        for line in cast_text.split('\n'):
            line = line.strip()
            if ' as ' in line:
                try:
                    actor_name, role_name = line.split(' as ', 1)  # Limit to 2 splits only
                    cast_list.append({
                        'actor_name': actor_name.strip(),
                        'role_name': role_name.strip()
                    })
                except ValueError:
                    continue  # Skip lines that don't follow the expected format
        return cast_list

    # Parse the review
    review_data = {}
    for key, pattern in sections.items():
        parsed_value = parse_section(review_text, key, pattern)
        
        if key == 'Main Cast' and parsed_value:
            # Main Cast section has nested lead and supporting actors
            lead_actors_text = re.search(r"Lead Actors:(.*?)Supporting Cast:", parsed_value, re.DOTALL)
            supporting_cast_text = re.search(r"Supporting Cast:(.*)", parsed_value, re.DOTALL)
            
            review_data['Main Cast'] = {
                "Lead Actors": parse_cast(lead_actors_text.group(1)) if lead_actors_text else [],
                "Supporting Cast": parse_cast(supporting_cast_text.group(1)) if supporting_cast_text else []
            }
        else:
            review_data[key] = parsed_value
    
    return review_data

# Example movie review text (JSON format input)
movie_review_text = '''{
    "movie_name": "The Last of Us",
    "review": "**Title:**\\n\"The Last of Us (2023) \u2013 A Gripping Post-Apocalyptic Drama with Stellar Performances\"\\n\\n**General Information:**\\n- Release Year: 2023\\n- Genre: Drama, Thriller\\n- Runtime: 2 hours 15 minutes\\n- IMDb Rating: 8.5/10\\n- MPAA Rating: R\\n- Language: English\\n- Country of Origin: USA\\n- Filming Locations: Abandoned urban landscapes, rural settings\\n- Box Office Information: Budget $80 million, Opening Weekend $30 million, Gross Earnings $250 million (worldwide)\\n\\n**Director and Crew:**\\n- Director: Emily Wells (Known for \"The Ruins of Hope,\" \"Broken Souls\")\\n- Writer: Mark Johnson (Notable for \"Silent Echoes,\" \"Echoes of Tomorrow\")\\n- Producers: Sarah Parker, Michael Adams\\n\\n**Main Cast:**\\n- Lead Actors: \\n  - Sarah Williams as Ellie: A young survivor with a tough exterior and a vulnerable core.\\n  - Jack Thompson as Joel: A hardened smuggler grappling with past traumas.\\n- Supporting Cast:\\n  - Emma Stone as Tess: Joel's trusted ally in the post-apocalyptic world.\\n  - Michael B. Jordan as Marlon: A charismatic but morally ambiguous leader.\\n\\n**Plot Summary:**\\nIn a world ravaged by a deadly fungal infection, Ellie, a teenager immune to the disease, teams up with Joel, a smuggler burdened by loss, on a dangerous journey across the desolate landscape. As they navigate treacherous territories and encounter both allies and enemies, their bond is tested in the face of harrowing challenges. The Last of Us delves into themes of survival, sacrifice, and the resilience of the human spirit.\\n\\n**Taglines:**\\n- \"In a world consumed by darkness, their journey begins.\"\\n- \"Survival knows no bounds.\"\\n\\n**Themes & Symbolism:**\\nThe Last of Us explores themes of hope amidst despair, the complexities of human relationships in dire circumstances, and the moral dilemmas that arise in a world stripped of civilization. Symbolically, the overgrown ruins and abandoned cities mirror the decay of society, while acts of compassion and sacrifice serve as beacons of light in the darkness.\\n\\n**Character Development:**\\nEllie's evolution from a spirited yet naive teenager to a hardened survivor mirrors her journey of self-discovery and resilience. Joel's gradual thawing of emotional walls and reconnection with his humanity through Ellie's companionship adds layers to his initially stoic character. Supporting characters like Tess and Marlon offer contrasting perspectives on survival and morality.\\n\\n**Directorial Vision:**\\nEmily Wells' directorial style infuses The Last of Us with gritty realism, capturing the bleak beauty of the post-apocalyptic world through evocative visuals and intimate character moments. The cinematography enhances the sense of isolation and danger, while the use of space conveys the vastness of the ravaged landscape.\\n\\n**Soundtrack & Music:**\\nComposer Lisa Turner provides a hauntingly beautiful score that complements the film's emotional depth. The music reflects both the despair of the environment and the glimmer of hope in the characters' struggles.\\n\\n**Production Design:**\\nThe film's production design immerses viewers in a world where nature has overtaken the remnants of humanity's once-great cities. The meticulous attention to detail in the decaying architecture, overgrown landscapes, and abandoned vehicles adds to the realism and emotional weight of the story.\\n\\n**Pacing and Structure:**\\nThe pacing of The Last of Us is deliberate, allowing the tension to build slowly as the characters navigate dangerous situations. The film strikes a balance between intense action sequences and reflective moments, giving audiences time to connect with the characters.\\n\\n**Cultural, Social, or Historical Context:**\\nThe film's exploration of a world ravaged by a pandemic and the societal collapse that follows resonates with contemporary fears about global crises, making it both a cautionary tale and an exploration of humanity's resilience.\\n\\n**Audience Reception & Critical Acclaim:**\\nThe Last of Us received widespread acclaim for its performances, emotional depth, and faithful adaptation of the original source material. Critics praised the film for its ability to capture the heart of the story while introducing new dimensions to the narrative.\\n\\n**Trivia and Fun Facts:**\\n- The film was shot on location in abandoned urban areas in the Midwest.\\n- Emma Stone underwent extensive physical training for her role as Tess.\\n\\n**Quotes & Dialogue:**\\n- Joel: \"I can't save everyone, Ellie, but I'll die trying to save you.\"\\n- Ellie: \"You don't get to decide who lives and dies anymore.\"\\n\\n**Legacy and Impact:**\\nThe Last of Us has set a new benchmark for post-apocalyptic films, with its emotionally resonant storytelling and complex characters. Its influence can be seen in subsequent adaptations of video games and its profound impact on audiences worldwide.\\n\\n**Criticism:**\\nSome critics noted the film's pacing at times felt uneven, with certain plot points taking longer to resolve than necessary. Additionally, some felt the ending was predictable.\\n\\n**Conclusion:**\\nThe Last of Us is a powerful exploration of love, loss, and survival in a brutal world. With its deeply human story, it resonates on a personal level, leaving a lasting impact on its audience.\\n\\n**Who Should Watch:**\\nFans of post-apocalyptic stories, emotional character-driven narratives, and those who appreciate a thought-provoking examination of humanity's struggle to rebuild after devastation will find much to appreciate in The Last of Us.\\n\\n**Overall Rating:**\\n9/10\\n\\n**Meta Title:**\\nThe Last of Us (2023) Movie Review – A Thrilling, Emotional Post-Apocalyptic Journey\\n\\n**Meta Description:**\\nExplore the world of The Last of Us in this in-depth review of the 2023 adaptation. Discover the plot, characters, direction, and much more in this must-read article.\\n}"
}'''

# Running the function on the review text
parsed_review = convert_review_to_dict(movie_review_text)

# Output parsed review as a formatted JSON
print(json.dumps(parsed_review, indent=4))
