import { useQuery } from "@tanstack/react-query";
import { BASE_URL } from "../api";
import StoryListItem from "./StoryListItem";
import type { CompleteStoryPublic } from "../types";

export default function StoryList() {
  const { isPending, isError, data, error } = useQuery({
    queryKey: ["story_list"],
    queryFn: async () => {
      const response = await fetch(`${BASE_URL}/api/stories`);
      const data = await response.json();
      console.log(data);
      if (!response.ok) {
        throw new Error(`${data.error}: ${data.message}`);
      }
      return data;
    },
  });

  if (isPending) {
    return <p>Waiting...</p>;
  }

  if (isError) {
    return <p>{error.message}</p>;
  }

  console.log(data);

  return (
    <div className="shadow-xl p-4 rounded-lg mt-6">
      <h2 className="text-3xl text-center">Saved Stories</h2>
      <ul className="h-100 overflow-scroll overflow-x-hidden">
        {data.map((story: CompleteStoryPublic) => (
          <StoryListItem key={story.id} story={story} />
        ))}
      </ul>
    </div>
  );
}
