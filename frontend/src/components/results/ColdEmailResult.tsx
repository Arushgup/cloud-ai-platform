import { Copy } from "lucide-react";

type Props = {
  result: any;
};

export default function ColdEmailResult({ result }: Props) {
  const emails = result.emails || result;

  const variants =
    emails.variants ??
    emails.email_variants ??
    [];

  const followUp =
    emails.follow_up ??
    emails.followup ??
    "";

  function copy(text: string) {
    navigator.clipboard.writeText(text);
    alert("Copied!");
  }

  return (
    <div className="mt-10 space-y-8">

      {variants.map((email: any, index: number) => (

        <div
          key={index}
          className="rounded-2xl bg-white p-8 shadow-lg"
        >

          <div className="mb-5 flex items-center justify-between">

            <h2 className="text-2xl font-bold">
              Email Variant {index + 1}
            </h2>

            <button
              onClick={() =>
                copy(
                  `${email.subject}\n\n${email.body}`
                )
              }
              className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-white"
            >
              <Copy size={18} />
              Copy
            </button>

          </div>

          <div className="mb-5">

            <p className="font-semibold">
              Subject
            </p>

            <div className="mt-2 rounded-lg border bg-gray-50 p-4">
              {email.subject}
            </div>

          </div>

          <div>

            <p className="font-semibold">
              Email
            </p>

            <div className="mt-2 whitespace-pre-wrap rounded-lg border bg-gray-50 p-4">
              {email.body}
            </div>

          </div>

        </div>

      ))}

      {followUp && (

        <div className="rounded-2xl bg-white p-8 shadow-lg">

          <div className="mb-5 flex items-center justify-between">

            <h2 className="text-2xl font-bold">
              Follow Up Email
            </h2>

            <button
              onClick={() => copy(followUp)}
              className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-white"
            >
              <Copy size={18} />
              Copy
            </button>

          </div>

          <div className="whitespace-pre-wrap rounded-lg border bg-gray-50 p-4">
            {followUp}
          </div>

        </div>

      )}

    </div>
  );
}