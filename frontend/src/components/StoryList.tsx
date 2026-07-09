import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { BASE_URL } from "../api";
import type { CompleteStoryPublic } from "../types";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeadCell,
  TableRow,
} from "flowbite-react";
import { useNavigate } from "react-router";

export default function StoryList() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { isPending, isError, data, error } = useQuery({
    queryKey: ["story_list"],
    queryFn: async () => {
      const response = await fetch(`${BASE_URL}/api/stories`);
      const data = await response.json();
      if (!response.ok) {
        throw new Error(`${data.error}: ${data.message}`);
      }
      return data;
    },
    retry: 1,
  });

  const mutation = useMutation({
    mutationFn: async (story_id: number) => {
      const response = await fetch(`${BASE_URL}/api/stories/${story_id}`, {
        method: "DELETE",
      });
      const data = await response.json();
      if (!response.ok) {
        throw Error(`${data.error}: ${data.message}`);
      }
      return null;
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["story_list"] });
    },
  });

  if (isPending) {
    return <p>Loading...</p>;
  }

  if (isError) {
    return <p>{error.message}</p>;
  }

  if (mutation.isError) {
    alert(mutation.error.message);
  }

  const handleClick = (story: CompleteStoryPublic) => {
    navigate("/story/" + story.id);
  };

  const handleDelete = (event: React.SyntheticEvent, story_id: number) => {
    event.stopPropagation();
    mutation.mutate(story_id);
  };

  return (
    <div className="shadow-xl p-4 rounded-lg mt-6">
      <h2 className="text-3xl text-center">Saved Stories</h2>
      <Table hoverable>
        <TableHead>
          <TableRow>
            <TableHeadCell>ID</TableHeadCell>
            <TableHeadCell>Title</TableHeadCell>
            <TableHeadCell>Word Count</TableHeadCell>
            <TableHeadCell>Model</TableHeadCell>
            <TableHeadCell>Date Created</TableHeadCell>
            <TableHeadCell>
              <span className="sr-only">Delete</span>
            </TableHeadCell>
          </TableRow>
        </TableHead>
        <TableBody className="divide-y">
          {data.map((story: CompleteStoryPublic) => (
            <TableRow
              key={story.id}
              className="bg-white dark:border-gray-700 dark:bg-gray-800 hover:cursor-pointer"
              onClick={() => handleClick(story)}
            >
              <TableCell className="whitespace-nowrap font-medium text-gray-900 dark:text-white">
                {story.id}
              </TableCell>
              <TableCell>{story.title}</TableCell>
              <TableCell>{story.num_words} words</TableCell>
              <TableCell>{story.ai_model}</TableCell>
              <TableCell>
                {new Date(story.created_at).toLocaleString()}
              </TableCell>
              <TableCell
                onClick={(ev) => handleDelete(ev, story.id)}
                className="font-medium text-primary-600 hover:underline dark:text-red-200"
              >
                Delete
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
