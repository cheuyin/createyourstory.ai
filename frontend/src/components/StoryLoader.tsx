import { useNavigate, useParams } from "react-router";
import LoadingStatus from "./LoadingStatus";
import { useQuery } from "@tanstack/react-query";
import StoryGame from "./StoryGame";
import { BASE_URL } from "../api";
import ImageLoader from "./ImageLoader";
import { Alert, Badge, Button } from "flowbite-react";

function StoryLoader() {
  const { id } = useParams();
  const navigate = useNavigate();

  const { isPending, error, data } = useQuery({
    queryKey: ["story", id],
    queryFn: async () => {
      const response = await fetch(`${BASE_URL}/api/stories/${id}`);
      const data = await response.json();
      if (!response.ok) {
        throw new Error(`${data.error}: ${data.message}`);
      }
      return data;
    },
    retry: false,
  });

  const createNewStory = () => {
    navigate("/");
  };

  if (isPending) {
    return <LoadingStatus theme={"story"} />;
  }

  if (error) {
    return (
      <Alert color="failure">
        <p className="mb-3">{error.message}</p>
        <Button size="sm" color="failure" onClick={createNewStory}>
          Go to story generator
        </Button>
      </Alert>
    );
  }

  if (data) {
    return (
      <div className="mx-auto max-w-6xl">
        <div className="grid items-start gap-8 lg:grid-cols-[2fr_3fr]">
          <div className="lg:sticky lg:top-8">
            <div className="text-center lg:text-left">
              <h2 className="font-serif text-3xl font-bold text-gray-900 dark:text-white">
                {data.title}
              </h2>
              <div className="mt-3 flex flex-wrap justify-center gap-2 lg:justify-start">
                <Badge color="gray">{data.ai_model}</Badge>
                <Badge color="success">{data.num_words} words</Badge>
                <Badge color="indigo">{data.num_endings} endings</Badge>
                <Badge color="yellow">
                  {data.num_winning_endings} winning endings
                </Badge>
              </div>
            </div>
            <ImageLoader story={data} />
          </div>
          <StoryGame story={data} onNewStory={createNewStory} />
        </div>
      </div>
    );
  }
}

export default StoryLoader;
