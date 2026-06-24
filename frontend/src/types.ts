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
