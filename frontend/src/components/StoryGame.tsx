import { useState } from "react";
import type { CompleteStoryNodePublic, CompleteStoryPublic } from "../types";
import { Alert, Badge, Button, Card } from "flowbite-react";

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
    <Card>
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
          {story.title}
        </h2>
        <div className="mt-2 flex flex-wrap justify-center gap-2">
          <Badge>{story.ai_model}</Badge>
          <Badge color="success">{story.num_words} words</Badge>
          <Badge color="indigo">{story.num_endings} endings</Badge>
          <Badge color="yellow">
            {story.num_winning_endings} winning endings
          </Badge>
        </div>
      </div>

      {currentNode && (
        <div>
          <p className="text-lg leading-relaxed text-gray-700 dark:text-gray-300">
            {currentNode.content}
          </p>

          {currentNode.is_ending ? (
            <Alert
              color={currentNode.is_winning_ending ? "success" : "gray"}
              className="mt-6"
            >
              <span className="font-semibold">
                {currentNode.is_winning_ending ? "Congratulations!" : "The End"}
              </span>
              <br />
              {currentNode.is_winning_ending
                ? "You reached a winning ending."
                : "Your adventure has ended."}
            </Alert>
          ) : (
            <div className="mt-6">
              <h3 className="mb-3 text-lg font-semibold text-gray-900 dark:text-white">
                What will you do?
              </h3>
              <div className="flex flex-col gap-3">
                {currentNode.options.map((option, index) => (
                  <Button
                    key={index}
                    color="light"
                    className="justify-start text-left"
                    onClick={() => chooseOption(option.node_id)}
                  >
                    {option.text}
                  </Button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      <div className="mt-6 flex justify-center gap-3 border-t border-gray-200 pt-4 dark:border-gray-700">
        <Button color="gray" onClick={restartStory}>
          Restart Story
        </Button>
        {onNewStory && <Button onClick={onNewStory}>New Story</Button>}
      </div>
    </Card>
  );
}

export default StoryGame;
