from models.story import Story


STORY_PROMPT = """
<role>
You are an expert game designer and short story writer specializing in engaging, meaningful Choose-Your-Adventure stories.
</role>

<narrative_goals>
Create a story that is imaginative, emotionally engaging, and satisfying to explore. Every choice should feel meaningful, and every path should teach something about human nature, judgment, or character.

Write with medium verbosity. Like a skilled short story writer, vividly describe the setting, characters, atmosphere, and conflict while keeping the pacing brisk.

Every story should have:
- A compelling, memorable title.
- A single protagonist.
- Clear stakes that escalate as the story progresses.
</narrative_goals>

<story_structure>
The story is a decision tree.

- The story has exactly one root node.
- The root node contains 2–3 choices.
- Every non-ending node contains 2–3 choices.
- The maximum depth is 4 decision levels.
- Every path ends in exactly one ending.
- Each root choice must ultimately contain exactly one winning ending. E.g. If the root has 3 choices then there are 3 winning endings.
</story_structure>

<choice_design>
Every choice should present a genuine trade-off.

Avoid choices where one option is obviously correct or obviously foolish.

Readers should be able to reason toward the best decisions using the information available rather than relying on luck.

Each decision should:
- Reveal new information,
- Increase the stakes,
- Develop the characters,
- Or meaningfully change the situation.

Avoid cosmetic choices that lead to nearly identical outcomes.
</choice_design>

<ending_design>
Winning endings should result from wisdom, courage, compassion, honesty, discipline, creativity, or good judgment—not luck.

Losing endings should arise from believable human mistakes such as impatience, pride, fear, greed, overconfidence, distraction, or shortsightedness. They should feel understandable rather than cartoonishly bad.

Every ending should conclude with a sentence summarizing why the path succeeded or failed.
- E.g. Winning: "You trusted in hard work and consistency over quick results, enabling you to build the foundation needed to land the job."
- E.g. Losing: "You forgot about the Dark Lord's powerful close combat abilities allowing him to defeat anyone 1 on 1"

</ending_design>

<planning>
Before writing the story, internally develop a complete outline of the narrative, branching structure, and endings. Do not output the outline.
</planning>

<output_format>
Output only the completed story, strictly following the required story format.
</output_format>
"""


def generate_story_image_prompt(story: Story) -> str:
    story_transcript = ""
    for node in story.nodes:
        story_transcript += node.content + "\n"
    PROMPT = f"""
You are given the complete transcript of a choose-your-own-adventure story.

<transcript>
{story_transcript}
</transcript>

Your task is to generate ONE image depicting a single moment that actually occurs within the story.

Choose the moment that:
- has the greatest dramatic tension or emotional impact,
- makes the viewer curious about what happens next,
- does not reveal or spoil the ending,
- could plausibly have been captured by a camera if someone had been present.

By default, the image should be a highly realistic cinematic photograph—not concept art, not a movie poster, not a book cover, not a collage, and not multiple scenes combined.

The image should feel like a frame from a high-budget live-action film:
- natural lighting
- believable environments
- authentic facial expressions
- cinematic composition
- rich detail
- grounded realism

If the story is clearly set in a stylized fictional universe (for example, anime, western animation, comics, or another recognizable artistic style), faithfully match that world's visual style instead of converting it into live action.

Depict only a single moment. Do not include text, logos, borders, captions, or titles.
"""
    return PROMPT
