type ErrorStateProps = {
  title?: string;
  message: string;
};

export default function ErrorState({ title = "Could not load data", message }: ErrorStateProps) {
  return (
    <div className="rounded border border-red-200 bg-red-50 px-4 py-3 text-red-900">
      <p className="font-bold">{title}</p>
      <p className="mt-1 text-sm">{message}</p>
    </div>
  );
}

