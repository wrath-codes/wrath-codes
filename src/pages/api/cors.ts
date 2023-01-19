import sgMail from "@sendgrid/mail";
import Cors from "cors";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";

import type { NextApiRequest, NextApiResponse } from 'next';



// Initializing the cors middleware
// You can read more about the available options here: https://github.com/expressjs/cors#configuration-options
const cors = Cors({
  methods: ['POST', 'GET', 'HEAD'],
})

// Helper method to wait for a middleware to execute before continuing
// And to throw an error when an error happens in a middleware
function runMiddleware(
  req: NextApiRequest,
  res: NextApiResponse,
  fn: Function
) {
  return new Promise((resolve, reject) => {
    fn(req, res, (result: any) => {
      if (result instanceof Error) {
        return reject(result)
      }

      return resolve(result)
    })
  })
}

type NextApiRequestWithEmail = NextApiRequest & {
  body: {
    firstName: string;
    lastName: string;
    email: string;
    phone: string;
    subject: string;
    message: string;
  };
};


interface EmailInput {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  subject: string;
  body: string;
  timestamp: string;
}

export default async function sendEmail(
  req: NextApiRequestWithEmail,
  res: NextApiResponse
) {
  // Run the middleware
  await runMiddleware(req, res, cors)

  sgMail.setApiKey(process.env.SG_API_KEY as string)
  // Rest of the API logic
  const { firstName, lastName, email, phone, subject, message } = req.body;

  await sgMail.send({
    to: process.env.SG_TO_EMAIL as string,
    from: process.env.SG_FROM_EMAIL as string,
    subject: `New message from ${ firstName } ${ lastName }`,
    templateId: process.env.SG_TEMPLATE_ID as string,
    dynamicTemplateData: {
      sender_name: `${ firstName } ${ lastName }`,
      sender_email: email,
      sender_phone: phone,
      subject: `New message from ${ firstName } ${ lastName }` || subject,
      body: message,
      timestamp: format(new Date(), "dd/MM/yyyy 'às' HH:mm", { locale: ptBR }),
    },
  });



  res.status(200).json({ status: "success", message: "Email sent successfully" });

}