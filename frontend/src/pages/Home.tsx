import { Link } from "react-router-dom";

import ErrorState from "../components/ErrorState";
import LoadingState from "../components/LoadingState";
import MatchCard from "../components/MatchCard";
import { useMatches } from "../hooks/useMatches";

export default function Home() {
  const { matches, isLoading, error } = useMatches({ upcomingOnly: true });
  const previewMatches = matches.slice(0, 6);

  return (
    <div className="mx-auto grid max-w-7xl gap-8 px-4 py-8 lg:px-8">
      <section className="grid gap-5">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm font-black uppercase text-clay">World Cup 2026</p>
            <h1 className="mt-2 max-w-3xl text-4xl font-black tracking-normal text-ink sm:text-5xl">
              WorldCupIQ
            </h1>
          </div>
          <Link
            to="/fixtures"
            className="inline-flex w-fit items-center justify-center rounded bg-pitch px-4 py-2.5 text-sm font-black text-white shadow-sm hover:bg-[#14523d]"
          >
            View all fixtures
          </Link>
        </div>
      </section>

      <section className="grid gap-4">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-black tracking-normal">Upcoming Matches</h2>
          <span className="rounded bg-gold px-3 py-1 text-xs font-black uppercase text-black/70">
            MVP seed
          </span>
        </div>
        {isLoading && <LoadingState />}
        {error && <ErrorState message={error} />}
        {!isLoading && !error && (
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {previewMatches.map((match) => (
              <MatchCard key={match.id} match={match} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

