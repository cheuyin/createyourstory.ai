import { useQuery } from "@tanstack/react-query";
import type { CompleteStoryPublic, ImageJobPublic } from "../types";
import { BASE_URL } from "../api";
import { Spinner } from "flowbite-react";
import ErrorAlert from "./ErrorAlert";

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
      <div className="mt-5 flex aspect-[2/3] w-full flex-col items-center justify-center rounded-xl border-2 border-dashed border-amber-200 bg-amber-50/40 px-6 dark:border-gray-600 dark:bg-gray-800/40">
        <Spinner size="lg" color="warning" aria-label="Generating image" />
        <p className="mt-4 font-medium text-gray-700 dark:text-gray-200">
          Illustrating your story…
        </p>
        <p className="mt-1 text-center text-sm text-gray-500 dark:text-gray-400">
          The image usually takes a few seconds to paint.
        </p>
      </div>
    );
  }

  if (imagePoll.error) {
    return (
      <ErrorAlert
        className="mt-5"
        title="Couldn’t generate the illustration"
        message={imagePoll.error.message}
      />
    );
  }

  if (imageQuery.isPending) {
    return (
      <div className="mt-5 flex aspect-[2/3] w-full flex-col items-center justify-center rounded-xl border-2 border-dashed border-amber-200 bg-amber-50/40 px-6 dark:border-gray-600 dark:bg-gray-800/40">
        <Spinner size="lg" color="warning" aria-label="Loading image" />
        <p className="mt-4 font-medium text-gray-700 dark:text-gray-200">
          Loading illustration…
        </p>
      </div>
    );
  }

  if (imageQuery.error) {
    return (
      <ErrorAlert
        className="mt-5"
        title="Couldn’t load the illustration"
        message={imageQuery.error.message}
      />
    );
  }

  return (
    <img
      src={`data:image/jpeg;base64,${imageQuery.data.image_base_64}`}
      alt="Story cover illustration"
      className="mt-5 aspect-[2/3] w-full rounded-xl object-cover shadow-lg"
    />
  );
}

export default ImageLoader;
