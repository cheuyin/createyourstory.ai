import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import type { StoryJobCreate, StoryJobPublic } from "../types";
import { useQuery, useMutation } from "@tanstack/react-query";
import CreateStoryForm from "./CreateStoryForm";
import LoadingStatus from "./LoadingStatus";
import { apiFetch, BASE_URL } from "../api";
import { Spinner } from "flowbite-react";
import ErrorAlert from "./ErrorAlert";

export default function StoryGenerator() {
  const navigate = useNavigate();
  const [job, setJob] = useState<StoryJobPublic | null>(null);
  const isJobFetchingCompleted = job && job.status === "completed";
  const [theme, setTheme] = useState<string>("");
  const job_poll = useQuery({
    queryKey: ["story_job", job ? job.job_id : null],
    queryFn: async () => {
      if (!job) {
        return null;
      }
      const data = await apiFetch<StoryJobPublic>(
        `${BASE_URL}/api/jobs/stories/${job.job_id}`,
      );
      setJob(data);
      return data;
    },
    refetchInterval: (query) => {
      if (isJobFetchingCompleted) return false;
      if (query.state.error) return false;
      return 3000;
    },
    enabled: Boolean(job),
  });

  const mutation = useMutation({
    mutationFn: async (newStory: StoryJobCreate) => {
      return apiFetch<StoryJobPublic>(`${BASE_URL}/api/stories/create`, {
        method: "POST",
        body: JSON.stringify(newStory),
        headers: {
          "Content-Type": "application/json",
        },
      });
    },
    onSuccess: async (data) => {
      const job = await data;
      setJob(job);
      job_poll.refetch();
    },
  });

  const generateStory = (story: StoryJobCreate) => {
    setTheme(theme);
    mutation.mutate(story);
  };

  const handleTryAgain = () => {
    navigate(0);
  };

  useEffect(() => {
    if (isJobFetchingCompleted) {
      navigate("/story/" + job.story_id, {
        state: {
          storyId: job.story_id,
          imageJobId: job.image_job_id,
        },
      });
    }
  }, [isJobFetchingCompleted, job, navigate]);

  if (mutation.isPending) {
    return <LoadingStatus theme={theme} />;
  }

  if (mutation.isError) {
    return (
      <ErrorAlert message={mutation.error.message} onRetry={handleTryAgain} />
    );
  }

  if (job && !isJobFetchingCompleted && !job_poll.isError) {
    return (
      <div className="flex flex-col items-center py-12">
        <Spinner size="xl" aria-label="Creating story" />
        <p className="mt-4 text-gray-500 dark:text-gray-400">
          Please wait while your story is being created...
        </p>
      </div>
    );
  }

  if (job_poll.isError) {
    return (
      <ErrorAlert message={job_poll.error.message} onRetry={handleTryAgain} />
    );
  }

  return (
    <CreateStoryForm
      onSubmit={(values: StoryJobCreate) => generateStory(values)}
    />
  );
}
