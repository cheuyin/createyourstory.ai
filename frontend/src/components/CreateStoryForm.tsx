import { useRef, useState } from "react";
import type { StoryJobCreate } from "../types";
import { Button, Card, Select, TextInput } from "flowbite-react";

interface CreateStoryFormProps {
  onSubmit: (story: StoryJobCreate) => void;
}

const EXAMPLE_THEMES = [
  { emoji: "🏴‍☠️", label: "Pirates" },
  { emoji: "🚀", label: "Space Odyssey" },
  { emoji: "🏰", label: "Medieval Quest" },
  { emoji: "🌊", label: "Deep Sea Mystery" },
  { emoji: "🧙", label: "Wizard's Journey" },
  { emoji: "🤖", label: "Robot Uprising" },
];

function CreateStoryForm({ onSubmit }: CreateStoryFormProps) {
  const [error] = useState("");
  const [showAdvanced, setShowAdvanced] = useState(false);
  const themeRef = useRef<HTMLInputElement>(null);

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

  const fillTheme = (label: string) => {
    if (themeRef.current) {
      themeRef.current.value = label;
      themeRef.current.focus();
    }
  };

  return (
    <Card>
      <form onSubmit={handleSubmit} className="flex flex-col gap-5">
        <div>
          <TextInput
            ref={themeRef}
            type="text"
            name="theme"
            autoComplete="off"
            placeholder="A haunted lighthouse on a distant shore..."
            color={error ? "failure" : undefined}
            sizing="lg"
            required
          />
          {error && (
            <p className="mt-1 text-sm text-red-600 dark:text-red-500">
              {error}
            </p>
          )}
        </div>

        <div className="flex flex-wrap justify-center gap-2">
          {EXAMPLE_THEMES.map(({ emoji, label }) => (
            <button
              key={label}
              type="button"
              onClick={() => fillTheme(label)}
              className="rounded-full border border-amber-200 bg-amber-50 px-3 py-1.5 text-sm text-amber-800 transition-colors hover:bg-amber-100 dark:border-gray-600 dark:bg-gray-700 dark:text-gray-300 dark:hover:bg-gray-600"
            >
              {emoji} {label}
            </button>
          ))}
        </div>

        <div>
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-sm text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300"
          >
            {showAdvanced
              ? "▾ Hide model settings"
              : "▸ Advanced: choose model"}
          </button>
          {showAdvanced && (
            <div className="mt-2">
              <Select
                id="ai_model"
                name="ai_model"
                defaultValue="google/gemini-3.1-flash-lite"
              >
                <option value="google/gemini-3.1-pro-preview">
                  gemini-3.1-pro-preview
                </option>
                <option value="google/gemini-3.5-flash">
                  gemini-3.5-flash
                </option>
                <option value="google/gemini-3.1-flash-lite">
                  gemini-3.1-flash-lite
                </option>
                <option value="google/gemini-2.5-pro">gemini-2.5-pro</option>
                <option value="google/gemini-2.5-flash">
                  gemini-2.5-flash
                </option>
                <option value="x-ai/grok-4.5">grok-4.5</option>
              </Select>
            </div>
          )}
          {!showAdvanced && (
            <input
              type="hidden"
              name="ai_model"
              value="google/gemini-3.1-flash-lite"
            />
          )}
        </div>

        <Button type="submit" size="xl" color="primary" className="w-full">
          ✨ Generate Story
        </Button>
      </form>
    </Card>
  );
}

export default CreateStoryForm;
