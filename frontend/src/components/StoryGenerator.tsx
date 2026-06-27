import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import type { StoryJobCreate, StoryJobPublic } from "../types";
import { useQuery, useMutation } from "@tanstack/react-query";
import ThemeInput from "./ThemeInput";
import LoadingStatus from "./LoadingStatus";
import { BASE_URL } from "../api";

export default function StoryGenerator() {
  const navigate = useNavigate();
  const [job, setJob] = useState<StoryJobPublic | null>(null);
  const [theme, setTheme] = useState<string>("");
  const job_poll = useQuery({
    queryKey: ["story_job", job ? job.job_id : null],
    queryFn: async () => {
      if (!job) {
        return null;
      }
      const response = await fetch(`${BASE_URL}/api/jobs/${job.job_id}`);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      const data = await response.json();
      setJob(data);
      return data;
    },
    refetchInterval: () => {
      if (job && job.status === "completed") return false;
      return 3000;
    },
    enabled: Boolean(job),
  });

  const mutation = useMutation({
    mutationFn: (newStory: StoryJobCreate) => {
      return fetch(`${BASE_URL}/api/stories/create`, {
        method: "POST",
        body: JSON.stringify(newStory),
        headers: {
          "Content-Type": "application/json",
        },
      });
    },
    onSuccess: async (data) => {
      const job = await data.json();
      setJob(job);
      job_poll.refetch();
    },
  });

  const generateStory = (theme: string) => {
    setTheme(theme);
    mutation.mutate({
      theme,
    });
  };

  useEffect(() => {
    if (job && job.status === "completed") {
      navigate("/story/" + job.story_id);
    }
  }, [job, navigate]);

  return (
    <div className="story-generator">
      {mutation.isPending && <LoadingStatus theme={theme} />}

      {job?.status === "processing" && (
        <p>Please wait while your story is being created...</p>
      )}

      {mutation.isError && (
        <div className="error-message">
          <p>{mutation.error.message}</p>
          <button onClick={() => console.log("RESET")}>Try Again</button>
        </div>
      )}

      {job_poll.isError && (
        <div className="error-message">
          <p>{job_poll.error.message}</p>
          <button onClick={() => console.log("RESET")}>Try Again</button>
        </div>
      )}

      {!mutation.error && !mutation.isPending && !job && (
        <ThemeInput onSubmit={generateStory} />
      )}
    </div>
  );
}
