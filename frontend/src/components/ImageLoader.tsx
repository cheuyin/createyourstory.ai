import { useQuery } from "@tanstack/react-query";
import type { ImageJobPublic } from "../types";
import { BASE_URL } from "../api";

interface ImageLoaderProps {
  storyId: number;
  imageJobId: string;
}

function ImageLoader({ storyId, imageJobId }: ImageLoaderProps) {
  const imagePoll = useQuery({
    queryKey: ["image_poll", imageJobId],
    queryFn: async () => {
      const response = await fetch(`${BASE_URL}/api/jobs/images/${imageJobId}`);
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
    queryKey: ["story_image", storyId],
    queryFn: async () => {
      const response = await fetch(`${BASE_URL}/api/stories/${storyId}`);
      const data = await response.json();
      if (!response.ok) {
        throw Error(`${data.error}: ${data.message}`);
      }
      return data;
    },
    enabled: isImageJobCompleted,
  });

  if (!isImageJobCompleted) {
    return <p>Image is being created...</p>;
  }

  if (imagePoll.error) {
    return <p>Couldn't create image: {imagePoll.error.message}</p>;
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
