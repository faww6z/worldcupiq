import { NavLink, Route, Routes } from "react-router-dom";

import Fixtures from "./pages/Fixtures";
import Home from "./pages/Home";
import MatchCenter from "./pages/MatchCenter";

function App() {
  return (
    <div className="min-h-screen bg-[#f6f3eb] text-ink">
      <header className="border-b border-black/10 bg-white/85 backdrop-blur">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between lg:px-8">
          <NavLink to="/" className="flex items-center gap-3">
            <span className="grid h-10 w-10 place-items-center rounded bg-pitch text-sm font-black text-white">WIQ</span>
            <span>
              <span className="block text-lg font-black tracking-normal">WorldCupIQ</span>
              <span className="block text-xs font-semibold uppercase text-clay">2026 fixtures</span>
            </span>
          </NavLink>
          <nav className="flex gap-2 text-sm font-semibold">
            <NavLink
              to="/"
              className={({ isActive }) =>
                `rounded px-3 py-2 ${isActive ? "bg-pitch text-white" : "text-ink hover:bg-black/5"}`
              }
            >
              Home
            </NavLink>
            <NavLink
              to="/fixtures"
              className={({ isActive }) =>
                `rounded px-3 py-2 ${isActive ? "bg-pitch text-white" : "text-ink hover:bg-black/5"}`
              }
            >
              Fixtures
            </NavLink>
          </nav>
        </div>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/fixtures" element={<Fixtures />} />
          <Route path="/matches/:matchId" element={<MatchCenter />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
