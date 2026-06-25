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
  created_at: Date;
  root_node: CompleteStoryNodePublic;
  all_nodes: Record<number, CompleteStoryNodePublic>;
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
}
