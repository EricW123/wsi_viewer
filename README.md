# wsi_viewer

The backend is ran by `uvicorn main:app --reload --port 5000`.

The frontend is ran by `cd frontend && npm run dev`.

I didn't have time to finish the work, since the original code uses react-style routing, and it's mostly hardcoded, so I need more time to figure out best way to implement it in Next.js.

The backend is finished and workable. The frontend is compilable but not fully runnable.

The electron part mostly doesn't need to change, so the project is still runnable by using the new backend with port 5000 and ask the electron to link to it.

Also due to the routing issue, electron part of code is copied to this repo but cannot work properly, since it tries to fetch a weird path that needs to be changed via Next.js.
