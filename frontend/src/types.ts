export interface StoryOptionPublic {
  text: string;
  node_id: number;
}

export interface CompleteStoryNodePublic {
  id: number;
  content: string;
  is_ending: boolean;
  is_winning_ending: boolean;
  options: StoryOptionPublic[];
}

export interface CompleteStoryPublic {
  id: number;
  title: string;
  ai_model: string;
  username: string;
  session_id: string | null;
  created_at: Date;
  root_node: CompleteStoryNodePublic;
  all_nodes: Record<number, CompleteStoryNodePublic>;
  num_endings: number;
  num_winning_endings: number;
  num_words: number;
  image_job_id: string | null;
  image_base_64: string | null;
}

export interface StoryJobPublic {
  job_id: string;
  username: string;
  status: string;
  ai_model: string;
  created_at: Date;
  story_id: number | null;
  image_job_id: string | null;
  completed_at: Date | null;
  error: string | null;
}

export interface StoryJobCreate {
  theme: string;
  ai_model: string;
}

export interface APIError {
  error: string;
  message: string;
}

export interface UserPublic {
  username: string;
  fullName: string;
}

export interface ImageJobPublic {
  job_id: string;
  theme: string;
  status: string;
  image_model: string;
  story_id: number | null;
  error: string | null;
  username: string | null;
  created_at: Date;
  completed_at: Date | null;
}
