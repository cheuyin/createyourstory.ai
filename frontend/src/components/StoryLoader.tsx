import { useNavigate, useParams } from "react-router";
import LoadingStatus from "./LoadingStatus";
import { useQuery } from "@tanstack/react-query";
import StoryGame from "./StoryGame";
import { BASE_URL } from "../api";
import ImageLoader from "./ImageLoader";
import { Alert, Button } from "flowbite-react";

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
      <>
        <StoryGame story={data} onNewStory={createNewStory} />
        <ImageLoader story={data} />
      </>
    );
  }
}

export default StoryLoader;
