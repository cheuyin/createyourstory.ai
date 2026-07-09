import { useState } from "react";
import type { StoryJobCreate } from "../types";

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
    <div className="theme-input-container">
      <h2>Generate Your Adventure</h2>
      <p>Enter a theme for your interactive story</p>

      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <input
            type="text"
            name="theme"
            autoComplete="off"
            placeholder="Enter a theme (e.g. pirates, space, medieval...)"
            className={error ? "error" : ""}
          />
          <label
            htmlFor="ai_model"
            className="block mb-2.5 text-sm font-medium text-heading"
          >
            Select a model
          </label>
          <select
            id="ai_model"
            name="ai_model"
            className="block w-full px-3 py-2.5 bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand shadow-xs placeholder:text-body"
            defaultValue={"gemini-3.1-flash-lite"}
          >
            <option value="gemini-3.1-pro-preview">
              gemini-3.1-pro-preview
            </option>
            <option value="gemini-3.5-flash">gemini-3.5-flash</option>
            <option value="gemini-3.1-flash-lite">gemini-3.1-flash-lite</option>
            <option value="gemini-2.5-pro">gemini-2.5-pro</option>
            <option value="gemini-2.5-flash">gemini-2.5-flash</option>
          </select>
          {error && <p className="error-text">{error}</p>}
          <button type="submit" className="generate-btn">
            Generate Story
          </button>
        </div>
      </form>
    </div>
  );
}

export default CreateStoryForm;
