import { protectedProcedure, publicProcedure, router } from "../trpc";
import { createTodoSchema, modifyTodoSchema, updateTodoSchema } from "./../../../common/todo";

export const todoRouter = router({
  getAll: publicProcedure.query(async ({ ctx }) => {
    const todos = await ctx.prisma.todo.findMany({
      select: {
        author: { select: { name: true } },
      },
    });
    return todos;
  }),
  getUsers: protectedProcedure.query(async ({ ctx }) => {
    const todos = await ctx.prisma.todo.findMany({
      where: { authorId: ctx.session?.user?.id },
    });
    return todos;
  }),
  create: protectedProcedure.input(createTodoSchema).mutation(async ({ ctx, input }) => {
    const { prisma, session } = ctx;
    const todo = await prisma.todo.create({
      data: {
        title: input.title,
        authorId: session?.user?.id,
      },
    });
    return todo;
  }),
  toggleCompleted: protectedProcedure.input(modifyTodoSchema).mutation(async ({ ctx, input }) => {
    const { prisma } = ctx;
    const todo = await prisma.todo.update({
      where: { id: input.id },
      data: {
        completed: true,
      },
    });
    return todo;
  }),
  toggleUncompleted: protectedProcedure.input(modifyTodoSchema).mutation(async ({ ctx, input }) => {
    const { prisma } = ctx;
    const todo = await prisma.todo.update({
      where: { id: input.id },
      data: {
        completed: false,
      },
    });
    return todo;
  }),
  delete: protectedProcedure.input(modifyTodoSchema).mutation(async ({ ctx, input }) => {
    const { prisma } = ctx;
    const todo = await prisma.todo.delete({
      where: { id: input.id },
    });
    return todo;
  }),
  updateTitle: protectedProcedure.input(updateTodoSchema).mutation(async ({ ctx, input }) => {
    const { prisma } = ctx;
    const todo = await prisma.todo.update({
      where: { id: input.id },
      data: {
        title: input.title,
      },
    });
    return todo;
  }),
});
