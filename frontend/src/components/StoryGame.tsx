import { useState } from "react";
import type { CompleteStoryNodePublic, CompleteStoryPublic } from "../types";
import { Button } from "flowbite-react";

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
    <div>
      {currentNode && (
        <div>
          <p className="font-serif text-lg leading-loose text-gray-800 dark:text-gray-200">
            {currentNode.content}
          </p>

          {currentNode.is_ending ? (
            <div
              className={`mt-8 rounded-lg border-2 p-6 text-center ${
                currentNode.is_winning_ending
                  ? "border-emerald-300 bg-emerald-50 dark:border-emerald-700 dark:bg-emerald-900/20"
                  : "border-gray-300 bg-gray-50 dark:border-gray-600 dark:bg-gray-800/50"
              }`}
            >
              <span className="text-4xl">
                {currentNode.is_winning_ending ? "🎉" : "💀"}
              </span>
              <h3
                className={`mt-2 text-xl font-bold ${
                  currentNode.is_winning_ending
                    ? "text-emerald-700 dark:text-emerald-400"
                    : "text-gray-700 dark:text-gray-300"
                }`}
              >
                {currentNode.is_winning_ending ? "Congratulations!" : "The End"}
              </h3>
              <p
                className={`mt-1 ${
                  currentNode.is_winning_ending
                    ? "text-emerald-600 dark:text-emerald-400"
                    : "text-gray-500 dark:text-gray-400"
                }`}
              >
                {currentNode.is_winning_ending
                  ? "You reached a winning ending."
                  : "Your adventure has ended."}
              </p>
            </div>
          ) : (
            <div className="mt-8">
              <h3 className="mb-4 text-lg font-semibold text-gray-900 dark:text-white">
                What will you do?
              </h3>
              <div className="flex flex-col gap-3">
                {currentNode.options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => chooseOption(option.node_id)}
                    className="rounded-lg border-l-4 border-amber-400 bg-amber-50/50 px-4 py-3 text-left text-gray-800 transition-all hover:border-amber-500 hover:bg-amber-100/60 hover:shadow-sm dark:border-amber-500 dark:bg-gray-800 dark:text-gray-200 dark:hover:border-amber-400 dark:hover:bg-gray-700"
                  >
                    {option.text}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      <div className="mt-8 flex justify-center gap-3 border-t border-gray-200 pt-5 dark:border-gray-700">
        <Button color="gray" onClick={restartStory}>
          ↩ Restart Story
        </Button>
        {onNewStory && (
          <Button color="primary" onClick={onNewStory}>
            ✨ New Story
          </Button>
        )}
      </div>
    </div>
  );
}

export default StoryGame;
