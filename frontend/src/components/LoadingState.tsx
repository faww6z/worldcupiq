type LoadingStateProps = {
  label?: string;
};

export default function LoadingState({ label = "Loading fixtures" }: LoadingStateProps) {
  return (
    <div className="grid gap-3" aria-label={label}>
      {[0, 1, 2].map((item) => (
        <div key={item} className="h-28 animate-pulse rounded border border-black/10 bg-white" />
      ))}
    </div>
  );
}

