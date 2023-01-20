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

export const todoSchema = z.object({
  id: z.string().cuid(),
  title: z
    .string()
    .min(1, { message: "Todo title must be between 1 and 50 characters" })
    .max(50, { message: "Todo title must be between 1 and 50 characters" }),
  completed: z.boolean(),
  createdAt: z.date(),
  updatedAt: z.date(),
});

export type Todo = z.infer<typeof todoSchema>;
