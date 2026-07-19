import { createTheme } from "flowbite-react";

/**
 * Central design system for CreateYourStory.ai.
 *
 * All Flowbite-React components automatically pick up these overrides
 * via the <ThemeProvider> in main.tsx. Add new component overrides here
 * instead of scattering inline className color/gradient hacks.
 */
export const appTheme = createTheme({
  button: {
    color: {
      // Primary CTA — warm amber gradient
      primary:
        "bg-gradient-to-r from-amber-500 to-orange-500 text-white hover:from-amber-600 hover:to-orange-600 focus:ring-amber-300 dark:focus:ring-amber-800",
      // Secondary — neutral
      gray: "bg-gray-700 text-white hover:bg-gray-800 focus:ring-gray-300 dark:bg-gray-600 dark:hover:bg-gray-700 dark:focus:ring-gray-800",
      // Danger
      failure:
        "bg-red-700 text-white hover:bg-red-800 focus:ring-red-300 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-800",
      red: "bg-red-700 text-white hover:bg-red-800 focus:ring-red-300 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-800",
    },
  },
  spinner: {
    color: {
      default: "fill-amber-500",
    },
  },
  card: {
    root: {
      base: "flex rounded-lg border border-amber-200/60 bg-white shadow-lg dark:border-gray-700 dark:bg-gray-800",
    },
  },
});
