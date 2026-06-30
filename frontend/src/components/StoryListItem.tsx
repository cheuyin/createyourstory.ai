import type { CompleteStoryPublic } from "../types";
import { useNavigate } from "react-router";

interface StoryListItemProps {
  story: CompleteStoryPublic;
}

export default function StoryListItem(story: StoryListItemProps) {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/story/" + story.story.id);
  };

  return (
    <div
      className="shadow-md p-4 flex justify-between rounded-md cursor-pointer hover:bg-gray-50"
      onClick={handleClick}
    >
      <p>{story.story.id}</p>
      <p>{story.story.title}</p>
      <p>{new Date(story.story.created_at).toLocaleString()}</p>
    </div>
  );
}
