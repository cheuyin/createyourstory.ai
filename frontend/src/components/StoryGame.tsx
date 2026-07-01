import { useState } from "react";
import type { CompleteStoryNodePublic, CompleteStoryPublic } from "../types";
import { Badge } from "flowbite-react";

interface StoryGameProps {
  story: CompleteStoryPublic;
  onNewStory: () => void;
}

function StoryGame({ story, onNewStory }: StoryGameProps) {
  const [currentNode, setCurrentNode] =
    useState<CompleteStoryNodePublic | null>(story.root_node);

  const chooseOption = (optionId: number) => {
    const option = currentNode?.options.find(
      (option) => option.node_id == optionId,
    );
    if (!option) {
      throw new Error(`Option ${option} not found`);
    }
    setCurrentNode(story.all_nodes[option.node_id]);
  };

  const restartStory = () => {
    setCurrentNode(story.root_node);
  };

  return (
    <div className="story-game">
      <header className="story-header">
        <h2>{story.title}</h2>
        <Badge className="w-fit rounded-lg">{story.ai_model}</Badge>
        <Badge className="w-fit rounded-lg" color="success">{story.num_words} words</Badge>
        <Badge className="w-fit rounded-lg" color="indigo">{story.num_endings} endings</Badge>
        <Badge className="w-fit rounded-lg" color="yellow">
          {story.num_winning_endings} winning endings
        </Badge>
      </header>

      <div className="story-content">
        {currentNode && (
          <div className="story-node">
            <p>{currentNode.content}</p>
            {currentNode.is_ending ? (
              <div className="story-ending">
                <h3>
                  {currentNode.is_winning_ending ? "Congratuations" : "End"}
                </h3>
                {currentNode.is_winning_ending
                  ? "You reached a winning ending"
                  : "Your adventure has ended"}
              </div>
            ) : (
              <div className="story-options">
                <h3>What will you do?</h3>
                <div className="options-list">
                  {currentNode.options.map((option, index) => {
                    return (
                      <button
                        key={index}
                        onClick={() => chooseOption(option.node_id)}
                        className="option-btn"
                      >
                        {option.text}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        )}

        <div className="story-controls">
          <button onClick={restartStory} className="reset-btn">
            Restart Story
          </button>
        </div>

        {onNewStory && (
          <button onClick={onNewStory} className="new-story-btn">
            New Story
          </button>
        )}
      </div>
    </div>
  );
}

export default StoryGame;
