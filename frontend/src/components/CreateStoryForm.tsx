import { useState } from "react";
import type { StoryJobCreate } from "../types";
import { Button, Card, Label, Select, TextInput } from "flowbite-react";

interface CreateStoryFormProps {
  onSubmit: (story: StoryJobCreate) => void;
}

function CreateStoryForm({ onSubmit }: CreateStoryFormProps) {
  const [error] = useState("");

  const handleSubmit = (e: React.SubmitEvent) => {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const theme = formData.get("theme");
    const ai_model = formData.get("ai_model");
    if (typeof theme !== "string" || typeof ai_model !== "string") {
      throw Error("Submitted form values are invalid");
    }
    onSubmit({
      theme,
      ai_model,
    });
  };

  return (
    <Card>
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
          Generate Your Adventure
        </h2>
        <p className="mt-1 text-gray-500 dark:text-gray-400">
          Enter a theme for your interactive story
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div>
          <TextInput
            type="text"
            name="theme"
            autoComplete="off"
            placeholder="Enter a theme (e.g. pirates, space, medieval...)"
            color={error ? "failure" : undefined}
            required
          />
          {error && (
            <p className="mt-1 text-sm text-red-600 dark:text-red-500">
              {error}
            </p>
          )}
        </div>

        <div>
          <div className="mb-2 block">
            <Label htmlFor="ai_model">Model</Label>
          </div>
          <Select
            id="ai_model"
            name="ai_model"
            defaultValue="google/gemini-3.1-flash-lite"
          >
            <option value="google/gemini-3.1-pro-preview">
              gemini-3.1-pro-preview
            </option>
            <option value="google/gemini-3.5-flash">gemini-3.5-flash</option>
            <option value="google/gemini-3.1-flash-lite">
              gemini-3.1-flash-lite
            </option>
            <option value="google/gemini-2.5-pro">gemini-2.5-pro</option>
            <option value="google/gemini-2.5-flash">gemini-2.5-flash</option>
            <option value="x-ai/grok-4.5">grok-4.5</option>
          </Select>
        </div>

        <Button type="submit" size="lg">
          Generate Story
        </Button>
      </form>
    </Card>
  );
}

export default CreateStoryForm;
