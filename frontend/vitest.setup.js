import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

// Vitest has no globals here, so React Testing Library cannot register its own cleanup.
afterEach(cleanup);
