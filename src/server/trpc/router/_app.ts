import { router } from "../trpc";
import { authRouter } from "./auth";
import { devToRouter } from "./devto";
import { todoRouter } from "./todo";

export const appRouter = router({
  auth: authRouter,
  devto: devToRouter,
  todo: todoRouter
});

// export type definition of API
export type AppRouter = typeof appRouter;
