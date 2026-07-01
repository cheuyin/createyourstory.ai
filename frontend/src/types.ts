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
  session_id: string | null;
  ai_model: string;
  created_at: Date;
  root_node: CompleteStoryNodePublic;
  all_nodes: Record<number, CompleteStoryNodePublic>;
  num_endings: number;
  num_winning_endings: number;
  num_words: number;
}

export interface StoryJobPublic {
  job_id: string;
  status: string;
  created_at: Date;
  story_id: number | null;
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
