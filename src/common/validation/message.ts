import { z } from "zod";

export const createMessageSchema = z.object({
  firstName: z.string().min(1).max(50),
  lastName: z.string().min(1).max(50),
  email: z.string().email(),
  subject: z.string().min(1).max(200),
  message: z.string().min(1).max(500),
  phone: z.string().min(1).max(20),
});

export type ICreateMessage = z.infer<typeof createMessageSchema>;