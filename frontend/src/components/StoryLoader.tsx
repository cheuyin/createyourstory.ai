import { useLocation, useNavigate, useParams } from "react-router";
import LoadingStatus from "./LoadingStatus";
import { useQuery } from "@tanstack/react-query";
import StoryGame from "./StoryGame";
import { BASE_URL } from "../api";
import ImageLoader from "./ImageLoader";

function StoryLoader() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { state } = useLocation();

  const { isPending, error, data } = useQuery({
    queryKey: ["story", id],
    queryFn: async () => {
      const response = await fetch(`${BASE_URL}/api/stories/${id}`);
      const data = await response.json();
      if (!response.ok) {
        throw new Error(`${data.error}: ${data.message}`);
      }
      return data;
    },
    retry: false,
  });

  const createNewStory = () => {
    navigate("/");
  };

  if (isPending) {
    return <LoadingStatus theme={"story"} />;
  }

  if (error) {
    return (
      <div className="story-loader">
        <div className="error-message">
          <p>{error.message}</p>
          <button onClick={createNewStory}>Go to story generator</button>
        </div>
      </div>
    );
  }

  if (data) {
    return (
      <div className="story-loader">
        <StoryGame story={data} onNewStory={createNewStory} />
        {/* <img src={`data:image/jpeg;base64,${data.image_base_64}`} /> */}
        <ImageLoader storyId={state.storyId} imageJobId={state.imageJobId} />
      </div>
    );
  }
}

export default StoryLoader;
