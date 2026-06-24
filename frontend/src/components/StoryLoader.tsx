import { useNavigate, useParams } from "react-router";
import LoadingStatus from "./LoadingStatus";
import { useQuery } from "@tanstack/react-query";
import StoryGame from "./StoryGame";

function StoryLoader() {
  const { id } = useParams();
  const navigate = useNavigate();

  const { isPending, error, data } = useQuery({
    queryKey: ["story"],
    queryFn: () =>
      fetch(`http://localhost:8000/api/stories/${id}/complete`).then((res) => res.json()),
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
          <h2>Story Not Found</h2>
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
      </div>
    );
  }
}

export default StoryLoader;
