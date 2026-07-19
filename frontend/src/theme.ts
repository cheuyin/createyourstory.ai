import { createTheme } from "flowbite-react";

/**
 * Central design system for CreateYourStory.ai.
 *
 * The brand color itself is defined once in `src/index.css` by mapping
 * Tailwind's `primary-*` scale onto amber — every Flowbite component
 * (buttons, focus rings, spinners, links…) picks it up automatically.
 *
 * Keep this file for *structural* component overrides only (shape, borders,
 * layout), not for re-declaring the brand color. Add new component overrides
 * here instead of scattering inline className color/gradient hacks.
 */
export const appTheme = createTheme({
  card: {
    root: {
      base: "flex rounded-lg border border-primary-200/60 bg-white shadow-lg dark:border-gray-700 dark:bg-gray-800",
    },
  },
  button: {
    color: {
      // flowbite-react 0.12 renamed the Button's brand color from "primary"
      // to "default". Alias it so existing color="primary" call sites keep
      // working. Styles mirror the default theme's "default" entry.
      primary:
        "bg-primary-700 text-white hover:bg-primary-800 focus:ring-primary-300 dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800",
    },
  },
});
