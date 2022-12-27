import { protectedProcedure, publicProcedure, router } from '../trpc';

export const authRouter = router({
  getSession: publicProcedure.query(({ ctx }) => {
    return ctx.session;
  }),
  getSecretMessage: protectedProcedure.query(({ ctx }) => {
    return `Your name is: ${ ctx.session?.user?.name }`;
  }),
});
