import { useQuery } from "@tanstack/react-query";
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
  const { isPending, isError, data, error } = useQuery({
    queryKey: ["story_list"],
    queryFn: async () => {
      const response = await fetch(`${BASE_URL}/api/stories`);
      const data = await response.json();
      console.log(data);
      if (!response.ok) {
        throw new Error(`${data.error}: ${data.message}`);
      }
      return data;
    },
  });

  if (isPending) {
    return <p>Waiting...</p>;
  }

  if (isError) {
    return <p>{error.message}</p>;
  }

  const handleClick = (story: CompleteStoryPublic) => {
    navigate("/story/" + story.id);
  };

  return (
    <div className="shadow-xl p-4 rounded-lg mt-6">
      <h2 className="text-3xl text-center">Saved Stories</h2>
      <Table hoverable>
        <TableHead>
          <TableRow>
            <TableHeadCell>ID</TableHeadCell>
            <TableHeadCell>Title</TableHeadCell>
            <TableHeadCell>Model</TableHeadCell>
            <TableHeadCell>Date Created</TableHeadCell>
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
              <TableCell>{story.ai_model}</TableCell>
              <TableCell>
                {new Date(story.created_at).toLocaleString()}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
