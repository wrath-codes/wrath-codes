import { z } from "zod";

export const createTodoSchema = z.object({
  title: z
    .string({
      required_error: "Todo title must be between 1 and 50 characters",
    })
    .min(1)
    .max(50),
});

export const updateTodoSchema = z.object({
  id: z.string().cuid(),
  title: z
    .string({
      required_error: "Todo title must be between 1 and 50 characters",
    })
    .min(1)
    .max(50),
});

export const modifyTodoSchema = z.object({
  id: z.string().cuid(),
});
