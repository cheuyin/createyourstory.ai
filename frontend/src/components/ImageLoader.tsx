import { useQuery } from "@tanstack/react-query";
import type { CompleteStoryPublic, ImageJobPublic } from "../types";
import { BASE_URL } from "../api";

interface ImageLoaderProps {
  story: CompleteStoryPublic;
}

function ImageLoader({ story }: ImageLoaderProps) {
  const imagePoll = useQuery({
    queryKey: ["image_poll", story.image_job_id],
    queryFn: async () => {
      const response = await fetch(
        `${BASE_URL}/api/jobs/images/${story.image_job_id}`,
      );
      const data = await response.json();
      if (!response.ok) {
        throw Error(`${data.error}: ${data.message}`);
      }
      return data;
    },
    refetchInterval: (query) => {
      if (query.state.error) return false;
      const imageJob: ImageJobPublic | undefined = query.state.data;
      if (imageJob && imageJob.status == "completed") {
        return false;
      }
      return 3000;
    },
    enabled: true,
  });

  const isImageJobCompleted =
    imagePoll.data && imagePoll.data.status == "completed";

  const imageQuery = useQuery({
    queryKey: ["story_image", story.id],
    queryFn: async () => {
      const response = await fetch(`${BASE_URL}/api/stories/${story.id}`);
      const data = await response.json();
      if (!response.ok) {
        throw Error(`${data.error}: ${data.message}`);
      }
      return data;
    },
    enabled: isImageJobCompleted,
  });

  if (!imagePoll.error && !isImageJobCompleted) {
    return <p>Image is being created...</p>;
  }

  if (imagePoll.error) {
    return (
      <p>
        {imagePoll.error.name} {imagePoll.error.message}
      </p>
    );
  }

  if (imageQuery.isPending) {
    return <p>Loading image...</p>;
  }

  if (imageQuery.error) {
    return <p>Couldn't load image: {imageQuery.error.message}</p>;
  }

  return (
    <img src={`data:image/jpeg;base64,${imageQuery.data.image_base_64}`} />
  );
}

export default ImageLoader;
