import { Card, Spinner } from "flowbite-react";

interface LoadingStatusProps {
  theme: string;
}

function LoadingStatus({ theme }: LoadingStatusProps) {
  return (
    <Card className="flex flex-col items-center py-12">
      <h2 className="mb-4 text-xl font-semibold text-gray-900 dark:text-white">
        Generating Your {theme} Story
      </h2>
      <Spinner size="xl" aria-label="Generating story" />
      <p className="mt-4 text-gray-500 dark:text-gray-400">
        Please wait while we generate your story...
      </p>
    </Card>
  );
}

export default LoadingStatus;
