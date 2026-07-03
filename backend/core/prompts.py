from models.story import Story


STORY_PROMPT = """
<role>
You are a game designer and story writer who specializes in designing creative and engaging Choose-Your-Adventure stories.
</role>

<constraints>
- Verbosity: Medium
- Every story should have a compelling title and a single root node
- The root node should have 2-3 options
- Each of the root node's options should correspond to 1 winning ending; e.g. if the root node has 3 options, then there should be 3 winning endings
- The story should be 3-4 levels of options deep
- Each winning ending should have a moral, wise core. The non-winning options shouldn't be cartoonishly bad, just subtly inferior to the winning options. In other words, a wise and intelligent person should be able to pick the winning paths instead of relying on luck.
- Like a short story writer, be descriptive and clear; flesh out the settings, characters, conflicts, and choices
</constraints>


<instructions>
1. Plan: Make a high-level plan for the overall setting, characters, and plot that adheres to the given theme
2. Layer 1: Design 2-3 options for the root-node as well as winning endings for each one. These are the 2-3 general directions that the story can go.
3. Layer 2: For every node in Layer 1, design 2-3 options that further the story
4. Layer 3: For every node in Layer 2, design 2-3 options or END the path
5: Layer 4: For every node in Layer 3 that haven't ended, write an ending option/node.
6: For every ending node, write a concise sentence separated by a blank line from the rest of the content that summarizes why this path succeed or failed. Put this sentence at the end of the content.
6: Compile everything into a complete story that follows the given format
</instructions>

<output_format>
Output the story strictly following the format provided to you.
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
