import { Alert, Button } from "flowbite-react";

interface ErrorAlertProps {
  message: string;
  title?: string;
  onRetry?: () => void;
  retryLabel?: string;
  className?: string;
}

function ErrorAlert({
  message,
  title = "Something went wrong",
  onRetry,
  retryLabel = "Try Again",
  className,
}: ErrorAlertProps) {
  return (
    <Alert
      color="failure"
      role="alert"
      aria-live="assertive"
      className={className}
    >
      <div className="flex flex-col items-start gap-3">
        <div>
          <h2 className="font-semibold">{title}</h2>
          <p className="mt-1">{message}</p>
        </div>
        {onRetry && (
          <Button
            size="sm"
            color="light"
            onClick={onRetry}
            className="self-start"
          >
            {retryLabel}
          </Button>
        )}
      </div>
    </Alert>
  );
}

export default ErrorAlert;