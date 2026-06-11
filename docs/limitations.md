# WorldCupIQ MVP Limitations

WorldCupIQ currently prioritizes a working product loop over advanced modelling depth: fixtures load from the database, match pages render predictions, and group tables update from finished scores.

## Current Data Limits

- The fixture seed covers the 72 group-stage matches only.
- Fixture data is manually maintained from FIFA schedule references.
- Match statuses and scores are not updated from a live feed yet.
- Historical international results have not been imported or cleaned yet.
- Team aliases and country-name normalization are deferred to the historical-data milestone.

## Current Model Limits

- Team ratings are seeded constants, not generated from historical results.
- Attack and defence strengths are seeded constants, not learned from match data.
- The Poisson model assumes independent team scoring.
- Dixon-Coles low-score correction is not implemented yet.
- Predictions have not been backtested for log loss, Brier score, calibration, or accuracy.
- Player availability, squad strength, injuries, rest days, and qualification form are not included yet.

## Current Product Limits

- The app is local-first and not deployed yet.
- Group table sorting uses points, goal difference, goals scored, then team name. Full FIFA tiebreakers are deferred.
- Group impact is a simple projection for the selected match, not a full tournament simulation.
- Knockout-stage brackets and best-third-place ranking are not implemented yet.
- There is no caching, async job queue, monitoring, or error tracking yet.

## Planned Upgrades

1. Import and clean historical international results.
2. Build generated Elo, attack, defence, and recent-form ratings.
3. Add backtesting and a model-performance view.
4. Implement official group tiebreakers and best-third-place ranking.
5. Add tournament simulation and cached stage probabilities.
6. Add player intelligence after the core model is trustworthy.
