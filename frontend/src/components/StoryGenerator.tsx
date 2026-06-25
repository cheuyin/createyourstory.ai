import { useState } from "react";
import { useNavigate } from "react-router";
import type { StoryJobCreate, StoryJobPublic } from "../types";
import { useQuery, useMutation } from "@tanstack/react-query";
import ThemeInput from "./ThemeInput";
import LoadingStatus from "./LoadingStatus";

// Creates a request for a new story
// After sending the request, polls until status of story job is resolved
// If story is finished, navigate to story page

export default function StoryGenerator() {
  const navigate = useNavigate();
  const [job, setJob] = useState<StoryJobPublic | null>(null);
  const [theme, setTheme] = useState<string>("");

  const mutation = useMutation({
    mutationFn: (newStory: StoryJobCreate) => {
      return fetch("http://localhost:8000/api/stories/create", {
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
    },
  });

  const generateStory = (theme: string) => {
    setTheme(theme);
    mutation.mutate({
      theme,
    });
  };

  return (
    <div className="story-generator">
      {mutation.error && (
        <div className="error-message">
          <p>{mutation.error.message}</p>
          <button onClick={() => console.log("RESET")}>Try Again</button>
        </div>
      )}
      {!mutation.error && !job && !mutation.isPending && (
        <ThemeInput onSubmit={generateStory} />
      )}
      {mutation.isPending && <LoadingStatus theme={theme} />}
      {job && <p>{job.job_id}</p>}
    </div>
  );
}
