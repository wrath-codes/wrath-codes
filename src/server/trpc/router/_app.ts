import { router } from "../trpc";
import { authRouter } from "./auth";
import { devToRouter } from "./devto";
import { exampleRouter } from "./example";

export const appRouter = router({
  example: exampleRouter,
  auth: authRouter,
  devto: devToRouter
});

// export type definition of API
export type AppRouter = typeof appRouter;
