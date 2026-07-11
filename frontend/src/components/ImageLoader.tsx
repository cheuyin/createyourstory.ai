import LoadingStatus from "./LoadingStatus";
import { useQuery } from "@tanstack/react-query";
import StoryGame from "./StoryGame";
import { BASE_URL } from "../api";

interface ImageLoaderProps {
  storyId: number;
  imageJobId: string;
}

function ImageLoader({ storyId, imageJobId }: ImageLoaderProps) {
  console.log({
    storyId,
    imageJobId,
  });

  return <p>Image</p>;
}

export default ImageLoader;
