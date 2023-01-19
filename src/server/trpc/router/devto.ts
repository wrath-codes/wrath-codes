import { publicProcedure, router } from "../trpc";

export const devToRouter = router({
  getWrathArticles: publicProcedure.query(async () => {
    const response = await fetch("https://dev.to/api/articles?username=wrathcodes");
    const data = await response.json();
    return data;
  }),
});
