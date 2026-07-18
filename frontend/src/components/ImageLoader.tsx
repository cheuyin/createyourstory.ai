import { useQuery } from "@tanstack/react-query";
import type { CompleteStoryPublic, ImageJobPublic } from "../types";
import { BASE_URL } from "../api";
import { Alert, Card, Spinner } from "flowbite-react";

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
    return (
      <Card className="mt-6 flex flex-col items-center py-8">
        <Spinner size="lg" aria-label="Generating image" />
        <p className="mt-3 text-gray-500 dark:text-gray-400">
          Image is being created...
        </p>
      </Card>
    );
  }

  if (imagePoll.error) {
    return (
      <Alert color="failure" className="mt-6">
        {imagePoll.error.name}: {imagePoll.error.message}
      </Alert>
    );
  }

  if (imageQuery.isPending) {
    return (
      <Card className="mt-6 flex flex-col items-center py-8">
        <Spinner size="lg" aria-label="Loading image" />
        <p className="mt-3 text-gray-500 dark:text-gray-400">
          Loading image...
        </p>
      </Card>
    );
  }

  if (imageQuery.error) {
    return (
      <Alert color="failure" className="mt-6">
        Couldn&apos;t load image: {imageQuery.error.message}
      </Alert>
    );
  }

  return (
    <Card className="mt-6">
      <img
        src={`data:image/jpeg;base64,${imageQuery.data.image_base_64}`}
        alt="Story illustration"
        className="h-auto w-full rounded-lg"
      />
    </Card>
  );
}

export default ImageLoader;
