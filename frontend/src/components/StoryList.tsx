import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiFetch, BASE_URL } from "../api";
import type { CompleteStoryPublic } from "../types";
import { Card, Spinner } from "flowbite-react";
import { useNavigate } from "react-router";
import ErrorAlert from "./ErrorAlert";

function formatRelativeDate(value: string | Date): string {
  const date = new Date(value);
  const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
  if (seconds < 60) return "just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 30) return `${days}d ago`;
  return date.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function shortModelName(model: string): string {
  return model.split("/").pop() ?? model;
}

export default function StoryList() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { isPending, isError, data, error } = useQuery({
    queryKey: ["story_list"],
    queryFn: async () => {
      return apiFetch<CompleteStoryPublic[]>(`${BASE_URL}/api/stories`);
    },
    retry: 1,
  });

  const mutation = useMutation({
    mutationFn: async (story_id: number) => {
      await apiFetch<null>(`${BASE_URL}/api/stories/${story_id}`, {
        method: "DELETE",
      });
      return null;
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["story_list"] });
    },
  });

  if (isPending) {
    return (
      <div className="mt-6 flex justify-center">
        <Spinner size="lg" aria-label="Loading saved stories" />
      </div>
    );
  }

  if (isError) {
    return (
      <Card className="mt-6">
        <ErrorAlert
          title="Couldn’t load saved stories"
          message={error.message}
        />
      </Card>
    );
  }

  const handleClick = (story: CompleteStoryPublic) => {
    navigate("/story/" + story.id);
  };

  const handleDelete = (event: React.SyntheticEvent, story_id: number) => {
    event.stopPropagation();
    mutation.mutate(story_id);
  };

  return (
    <Card className="mt-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
        Saved Stories
      </h2>
      {data.length === 0 ? (
        <p className="py-8 text-center text-gray-500 dark:text-gray-400">
          No stories yet — create your first one above ✨
        </p>
      ) : (
        <ul className="divide-y divide-gray-100 dark:divide-gray-700">
          {data.map((story: CompleteStoryPublic) => (
            <li key={story.id}>
              <div
                role="button"
                tabIndex={0}
                onClick={() => handleClick(story)}
                onKeyDown={(e) => e.key === "Enter" && handleClick(story)}
                className="-mx-4 flex cursor-pointer items-center justify-between gap-4 rounded-lg px-4 py-3 transition-colors hover:bg-amber-50/60 dark:hover:bg-gray-700/50"
              >
                <div className="min-w-0">
                  <p className="truncate font-semibold text-gray-900 dark:text-white">
                    {story.title}
                  </p>
                  <p className="mt-0.5 text-sm text-gray-500 dark:text-gray-400">
                    {story.num_words.toLocaleString()} words ·{" "}
                    {shortModelName(story.ai_model)} ·{" "}
                    {formatRelativeDate(story.created_at)}
                  </p>
                </div>
                <button
                  type="button"
                  aria-label={`Delete "${story.title}"`}
                  onClick={(ev) => handleDelete(ev, story.id)}
                  className="shrink-0 rounded-lg p-2 text-gray-400 transition-colors hover:bg-red-50 hover:text-red-500 focus:outline-none focus:ring-2 focus:ring-red-300 dark:hover:bg-red-900/20 dark:hover:text-red-400"
                >
                  <svg
                    className="h-4 w-4"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth={2}
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M9 7V4a1 1 0 011-1h4a1 1 0 011 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
      {mutation.isError && (
        <ErrorAlert
          className="mt-4"
          title="Couldn’t delete the story"
          message={mutation.error.message}
          onRetry={() => {
            if (mutation.variables !== undefined) {
              mutation.mutate(mutation.variables);
            }
          }}
        />
      )}
    </Card>
  );
}
